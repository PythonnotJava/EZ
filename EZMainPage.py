from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from qtawesome import icon as qtIcon

from EZTyping import RuleMixin
from EZCore import EZView
class ToolkitLayout(RuleMixin, QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.settingsBtn = QPushButton()
        self.clearBtn = QPushButton()

        self.__setUI()
    def __setUI(self) -> None:
        self.settingsBtn.setIcon(qtIcon('ri.settings-3-line'))
        self.clearBtn.setIcon(qtIcon('msc.clear-all'))
        self.settingsBtn.setMaximumWidth(50)
        self.clearBtn.setMaximumWidth(50)
        self.clearBtn.setToolTip('清空剪切板')
        self.settingsBtn.setToolTip('设置预览与编辑')
        _blank = QWidget()
        _blank.setFixedWidth(10)

        self.addWidget(self.clearBtn)
        self.addWidget(self.settingsBtn)
        self.addWidget(_blank)

        self.setAlignment(Qt.AlignmentFlag.AlignRight)

class MainPage(RuleMixin, QWidget):
    def __init__(self):
        super().__init__()

        self.toolkit = ToolkitLayout()
        self.core = EZView()

        self.__setUI()
    def __setUI(self) -> None:
        lay = QVBoxLayout()
        lay.addWidget(self.core, 8)
        lay.addLayout(self.toolkit, 1)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)