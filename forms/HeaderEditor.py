from forms.HeaderEditor import Ui_HeaderEditorDialog
from PySide2 import QtCore, QtGui, QtWidgets

class HeaderEditorDialog(QtWidgets.QDialog):

    def __init__(self):
        super(HeaderEditorDialog, self).__init__()
        self.ui = Ui_HeaderEditorDialog
        