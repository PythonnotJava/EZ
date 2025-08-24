import sys
from os.path import getsize
from typing import Optional
from collections import deque

from PySide6.QtCore import QTimer, QIODevice, QSize, QBuffer, QMimeData, QUrl, Qt
from PySide6.QtGui import QImage, QTextDocument
from PySide6.QtWidgets import QApplication, QScrollArea, QWidget, QVBoxLayout

from EZTyping import RuleMixin, DataItem
from EZCfg import MAXITEMCOUNTS, CARDFIXHEIGHT, TOTALFILESMAXSUPPORT
from EZItemCard import ItemCard

# UI本身
class EZView(RuleMixin, QScrollArea):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 历史队列
        self.history_deque: deque[DataItem] = deque(maxlen=MAXITEMCOUNTS)

        self.last_signature = None

        # 核心部件
        self.mainLay = QVBoxLayout()
        self.coreWidget = QWidget()

        # 每0.5秒检查一次
        self.timer = QTimer(self)
        self.timer.start(1000)

        # 剪贴板
        self.clip = QApplication.clipboard()

        self.__setUI()
        self.__link()

    def __setUI(self) -> None:
        self.setWidgetResizable(True)

        self.mainLay.setSpacing(5)
        self.mainLay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.coreWidget.setLayout(self.mainLay)
        self.setWidget(self.coreWidget)

    def __link(self) -> None:
        self.timer.timeout.connect(self.on_clipboard_changed)

    # 在已确定支持情况，添加一个Item到Card
    # 同时检查是不是超出了最大卡片数
    def addItem(self, item : DataItem):
        card = ItemCard(item)
        card.clicked.connect(lambda : self.on_item_clicked(card))
        self.mainLay.insertWidget(0, card)

        # 如果超过最大数量，删除最后一个
        if self.mainLay.count() > MAXITEMCOUNTS:
            last_item = self.mainLay.itemAt(MAXITEMCOUNTS - 1)
            if last_item:
                widget = last_item.widget()
                if widget:
                    self.mainLay.removeWidget(widget)
                    widget.deleteLater()

    # 签名验证
    @staticmethod
    def signature_of_mime(item: DataItem) -> str:
        """生成一个签名，避免重复记录（文本内容/文件列表/图片尺寸+哈希）"""
        if item.id == 0 or item.id == 3:
            return f"text:{item.content}"
        if item.id == 2:
            imageData : QImage = item.content[1]
            imgNew: QImage = imageData.scaled(
                QSize(CARDFIXHEIGHT - 10, CARDFIXHEIGHT - 10),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
            buf = QBuffer()
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            imgNew.save(buf, "PNG")
            data = buf.data()
            return f"image:{imgNew.width()}x{imgNew.height()}:{hash(bytes(data)[:256])}"
        if item.id == 1:
            paths : list[str] = item.content
            return "files:" + "|".join(paths)

    # ---- 剪贴板监控 ----
    def on_clipboard_changed(self):
        md : QMimeData = self.clip.mimeData()
        if not (md.hasText() or md.hasHtml() or md.hasUrls() or md.hasImage()):
            return
        item : Optional[DataItem] = None
        # 多文本情况
        if md.hasUrls():
            print('id == 1')
            urls : list[QUrl] = md.urls()
            paths = [u.toLocalFile() for u in urls if u.isLocalFile()]
            if not paths:
                return
            total_size = sum(getsize(p) for p in paths)
            if total_size > TOTALFILESMAXSUPPORT:
                return
            item = DataItem(content=paths, id=1)

        # 像素图情况
        elif md.hasImage():
            print('id == 2')
            pix : QImage = self.clip.image()
            if pix.isNull():
                return
            item = DataItem(content=('图片效果预览', pix), id=2)

        # 纯文本但是优先 HTML（Word 粘贴富文本）
        elif md.hasFormat("text/html"):
            print('id == 3')
            item = DataItem(content=md.html(), id=3)

        # 退回纯文本
        elif md.hasFormat("text/plain"):
            print('id == 0')
            item = DataItem(content=md.text(), id=0)

        if not item:
            return

        # 签名验证部分
        # 查重，只和上一次做对比
        sig = self.signature_of_mime(item)
        if sig == self.last_signature:
            return
        self.last_signature = sig

        self.addItem(item)
        self.history_deque.appendleft(item)

    # ---- 点击卡片回贴到剪贴板（双击）----
    def on_item_clicked(self, card : ItemCard):
        getId = card.item.id
        md = QMimeData()
        if getId == 0:
            md.setText(card.item.content)
        elif getId == 1:
            paths : list[str] = card.item.content
            md.setUrls([QUrl.fromLocalFile(p) for p in paths])
        elif getId == 2:
            imageData : QImage = card.item.content[1]
            md.setImageData(imageData)
        elif getId == 3:
            html : str = card.item.content
            md.setHtml(html)
            d = QTextDocument()
            d.setHtml(html)
            md.setText(d.toPlainText())
        self.clip.setMimeData(md)

    # 清空
    def clearAll(self) -> None:
        QApplication.clipboard().clear()
        self.last_signature = None
        for _ in range(self.mainLay.count()):
            w = self.mainLay.itemAt(0).widget()
            self.mainLay.removeWidget(w)
            w.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = EZView()
    ui.show()
    sys.exit(app.exec())