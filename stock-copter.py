from util.config import conf
from forms.MainWindow import MainWindow
from PySide2.QtWidgets import QApplication, QDialog, QTreeView
import sys

if __name__ == '__main__':
    app = QApplication()
    master = MainWindow()
    master.show()
    sys.exit(app.exec_())