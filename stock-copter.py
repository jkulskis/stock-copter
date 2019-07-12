from util.config import conf
from forms.MainWindow import MainWindow
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QTextStream
import sys
import qdarkstyle

if __name__ == '__main__':
    app = QApplication()
    master = MainWindow()
    master.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    sys.exit(app.exec_())