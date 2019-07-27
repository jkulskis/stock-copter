from util.config import conf
from forms.MainWindow import MainWindow
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QTextStream, QCoreApplication, Qt
import sys
import os
import qdarkstyle

if __name__ == '__main__':

    exit_code = conf.REBOOT_CODE

    while exit_code == conf.REBOOT_CODE:
        try:
            os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
            app = QApplication()
            app.setAttribute(Qt.AA_EnableHighDpiScaling)
            master = MainWindow()
            master.show()
        except RuntimeError:
            app = QCoreApplication.instance() 
        if conf['preferences']['theme'] == 'dark':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        elif conf['preferences']['theme'] == 'light':
            app.setStyleSheet("") # if the theme is light, then just use the default qt theme
        exit_code = app.exec_()
        QCoreApplication.instance().quit()
    sys.exit(exit_code)