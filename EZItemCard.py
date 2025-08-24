import re

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QColor, QPixmap, QImage, QTextDocument, QMouseEvent
from PySide6.QtWidgets import QFrame, QLabel, QGraphicsDropShadowEffect, QSizePolicy, QVBoxLayout, QHBoxLayout

from qtawesome import icon as qtIcon

from EZCfg import (CARDFIXHEIGHT, CARDSTYLE, shadowColor, shadowOpen,
                   PURETEXTFONT, SINGLEFILEPATHFONT, isSupportImageType, MULTEFILEPATHFONT, PIXMAPFONT)
from EZTyping import RuleMixin, DataItem

# 包装Item统一控件
class ItemCard(RuleMixin, QFrame):

    clicked = Signal()

    def __init__(self, item : DataItem, **kwargs):
        super().__init__(**kwargs)

        self.item = item

        self.__setUI()

    def __setUI(self) -> None:
        self.setFixedHeight(CARDFIXHEIGHT)
        self.setStyleSheet(f"ItemCard {{{CARDSTYLE}}}")

        if shadowOpen:
            shadow = QGraphicsDropShadowEffect(self)  # 添加效果类
            shadow.setBlurRadius(18)   # 模糊度
            shadow.setOffset(0, 3)     # 阴影偏移
            shadow.setColor(QColor(*shadowColor))  # 阴影颜色
            self.setGraphicsEffect(shadow)

        label = QLabel()
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        label.setMaximumWidth(400 - CARDFIXHEIGHT - 20)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        # 考虑可能会优化，暂时不把纯文本和文件类分两份简写
        # 纯文本
        if self.item.id == 0:
            label.setText(self.item.content)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setFont(PURETEXTFONT)
            label.setContentsMargins(10, 10, 10, 10)
            vbox.addWidget(label)
        # 文件
        elif self.item.id == 1:
            logo_label = QLabel()
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(10)
            paths : list[str] = self.item.content
            content : str
            if len(paths) == 1:
                label.setFont(SINGLEFILEPATHFONT)
                content = paths[0]
                label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                if isSupportImageType(content):
                    logo_label.setPixmap(
                        QPixmap(content).
                        scaled(
                            QSize(CARDFIXHEIGHT - 10, CARDFIXHEIGHT - 10),
                            Qt.AspectRatioMode.IgnoreAspectRatio,
                            Qt.TransformationMode.FastTransformation
                        )
                    )
                else:
                    logo_label.setPixmap(
                        qtIcon('ei.file-alt', color='orange').
                        pixmap(QSize(CARDFIXHEIGHT - 10, CARDFIXHEIGHT - 10))
                    )
            else:
                label.setFont(MULTEFILEPATHFONT)
                content = f'1. {paths[0]}\n2. {paths[1]}'
                if len(paths) > 2:
                    content += '\n3. More file(s)...'
                logo_label.setPixmap(
                    qtIcon('ei.file-alt', color='orange').
                    pixmap(QSize(CARDFIXHEIGHT - 10, CARDFIXHEIGHT - 10))
                )
            label.setText(content)
            row.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignLeft)
            row.addWidget(label)
            vbox.addLayout(row)
        # 像素图
        elif self.item.id == 2:
            content, imageData = self.item.content
            label.setText(content)
            label.setFont(PIXMAPFONT)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label = QLabel()
            preview_img : QImage = imageData.scaled(
                QSize(CARDFIXHEIGHT - 10, CARDFIXHEIGHT - 10),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
            logo_label.setPixmap(QPixmap.fromImage(preview_img))
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setAlignment(Qt.AlignmentFlag.AlignLeft)
            row.setSpacing(10)
            row.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignTop)
            row.addWidget(label)
            vbox.addLayout(row)

        elif self.item.id == 3:
            # 富文本要去除tags，不然不好看
            richText = QTextDocument()
            richText.setHtml(self.item.content)
            # 过滤掉不可见字符
            text = re.sub(r'[\x00-\x1F]+', '', richText.toPlainText())
            label.setText(text.strip())
            label.setFont(PURETEXTFONT)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setContentsMargins(10, 10, 10, 10)
            vbox.addWidget(label)

        self.setLayout(vbox)

    def mousePressEvent(self, event : QMouseEvent, /) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)