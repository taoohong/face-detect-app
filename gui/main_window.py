import logging
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF

from gui.view.check_in_interface import CheckInInterface
from gui.view.dashboard_interface import DashboardInterface
from gui.view.random_pick_interface import RandomPickInterface
from gui.view.register_interface import RegisterInterface
from gui.view.settings_interface import SettingsInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # Must set a globally unique object name for the sub-interface
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):
    """ Main Interface """

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s-%(levelname)s-%(message)s')

        # Create sub-interfaces, when actually using, replace Widget with your own sub-interface
        self.checkInInterface = CheckInInterface(self)
        self.dashboardInterface = DashboardInterface(self)
        self.registerFaceInterface = RegisterInterface(self)

        self.toolsInterface = Widget('Tools Interface', self)
        self.randomPickInterface = RandomPickInterface(self)

        self.settingInterface = SettingsInterface(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.checkInInterface, FIF.CAMERA, '签到')
        self.addSubInterface(self.dashboardInterface, FIF.PEOPLE, '签到表')
        self.addSubInterface(self.registerFaceInterface, FIF.ADD_TO, '登记')

        self.addSubInterface(self.toolsInterface, FIF.LEAF, '课堂助手', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.randomPickInterface, FIF.LEAF, '随机点名', parent=self.toolsInterface)

        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('assets/fcb_logo.jpg'))
        self.setWindowTitle('考勤签到平台')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
