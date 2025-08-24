from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from qtawesome import icon as qtIcon

from EZTyping import RuleMixin
from EZCfg import writeBack, cfgReaderPretty, judgeIsDict

class SettingDlg(RuleMixin, QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.textEdit = QPlainTextEdit()
        self.saveBtn = QPushButton()
        self.backBtn = QPushButton()

        self.__setUI()
        self.__link()
    def __setUI(self) -> None:
        self.textEdit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.textEdit.setPlainText(cfgReaderPretty)

        self.saveBtn.setText('保存')
        self.saveBtn.setMaximumWidth(80)
        self.saveBtn.setIcon(qtIcon('fa5s.save'))

        self.backBtn.setIcon(qtIcon('fa6s.arrow-left-long'))
        self.backBtn.setStyleSheet("border:none; background:transparent;")

        self.backBtn.setContentsMargins(10, 0, 0, 0)

        lay = QVBoxLayout()
        row = QHBoxLayout()
        row.addWidget(self.saveBtn)
        row.setAlignment(Qt.AlignmentFlag.AlignRight)

        lay.setContentsMargins(5, 5, 5, 5)
        lay.addWidget(self.backBtn, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        lay.addWidget(self.textEdit, 8)
        lay.addLayout(row, 1)

        self.setLayout(lay)

    def __link(self) -> None:
        self.saveBtn.clicked.connect(self.save)

    def save(self) -> None:
        if not self.textEdit.document().isModified():
            QMessageBox.information(
                self,
                '提示',
                '没做任何修改。',
                QMessageBox.StandardButton.Ok
            )
        else:
            content = self.textEdit.toPlainText()
            can, data = judgeIsDict(content)
            if not can:
                QMessageBox.warning(
                    self,
                    '警告',
                    'Json(5)格式错误，恢复配置。',
                    QMessageBox.StandardButton.Ok
                )
            else:
                writeBack(data)
                QMessageBox.question(
                    self,
                    '请求',
                    '已写入配置，重启生效。',
                    QMessageBox.StandardButton.Ok
                )


