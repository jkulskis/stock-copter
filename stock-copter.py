from forms.MainWindow import MainWindow
from util.config import Config
from PySide2.QtWidgets import QApplication, QDialog, QTreeView
import sys

if __name__ == '__main__':
    app = QApplication()
    master = MainWindow(config=Config())
    master.show()
    sys.exit(app.exec_())