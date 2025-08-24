import sys
from pathlib import Path

from PySide6.QtGui import QAction, QCursor, QCloseEvent, QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QSystemTrayIcon, QApplication, QStackedWidget, QMenu, QMessageBox

from EZTyping import RuleMixin
from EZMainPage import MainPage
from EZCfgWidget import SettingDlg
from EZStartupManager import MacStartupOnBoot, setup_logging

class EZApp(RuleMixin, QStackedWidget):
    def __init__(self, bind : QApplication, **kwargs):
        super().__init__(**kwargs)

        self.mainPage = MainPage()
        self.setting = SettingDlg()
        self.trayIcon = QSystemTrayIcon(
            QIcon(str(Path(__file__).parent / "assets/logo.ico")),
            bind
        )

        self.bind = bind

        self.__setUI()
        self.__link()
    def __setUI(self) -> None:
        self.setMaximumSize(QSize(400, 800))
        self.setMinimumSize(QSize(300, 300))
        self.resize(QSize(300, 300))

        self.setWindowTitle('EZ')
        self.setWindowIcon(QIcon(str(Path(__file__).parent / "assets/logo.ico")))

        self.addWidget(self.mainPage)
        self.addWidget(self.setting)
        self.setCurrentIndex(0)

        self.__setTray()
    def __setTray(self) -> None:
        menu = QMenu()

        showEZ = QAction('显示剪切板', menu)
        # 检查当前是否已启用开机启动
        if MacStartupOnBoot.is_enabled():
            needStartupEZ = QAction('已设置开机启动', menu)
        else:
            needStartupEZ = QAction('已关闭开机启动', menu)
        setEZ = QAction('设置', menu)
        exitEZ = QAction('退出', menu)

        menu.addActions([showEZ, needStartupEZ, setEZ, exitEZ])

        showEZ.triggered.connect(lambda : (self.setCurrentIndex(0), self.show()))
        needStartupEZ.triggered.connect(lambda : self.toggle_startup(needStartupEZ))
        setEZ.triggered.connect(lambda : (self.setCurrentIndex(1), self.show()))
        exitEZ.triggered.connect(self.bind.quit)

        self.trayIcon.setContextMenu(menu)
        self.trayIcon.show()
        self.trayIcon.setToolTip('EZ📋')

    def __link(self) -> None:
        self.mainPage.toolkit.clearBtn.clicked.connect(self.mainPage.core.clearAll)
        self.mainPage.toolkit.settingsBtn.clicked.connect(lambda : self.setCurrentIndex(1))
        self.setting.backBtn.clicked.connect(lambda : self.setCurrentIndex(0))
        self.trayIcon.activated.connect(lambda r: self.onTrayActivated(self.trayIcon.contextMenu(), r))

    @staticmethod
    def onTrayActivated(menu : QMenu, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            menu.exec(QCursor.pos())

    def closeEvent(self, event : QCloseEvent, /) -> None:
        event.ignore()
        self.hide()
        self.trayIcon.show()

    # 开机启动检查
    def toggle_startup(self, action : QAction):
        if action.text() == '已关闭开机启动':
            ok = MacStartupOnBoot.on_()
            if ok:
                action.setText('已设置开机启动')
            else:
                QMessageBox.warning(self, "失败", "EZ开启失败，请检查日志")
        else:
            ok = MacStartupOnBoot.off_()
            if ok:
                action.setText('已关闭开机启动')
            else:
                QMessageBox.warning(self, "失败", "EZ开启失败，请检查日志")

if __name__ == '__main__':
    setup_logging()
    app = QApplication(sys.argv)
    ui = EZApp(app)
    ui.show()
    sys.exit(app.exec())
