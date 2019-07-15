from PySide2 import QtCore, QtGui, QtWidgets
from forms.PreferencesDialogUI import Ui_PreferencesDialog
from util.format import Formatter
from util.config import conf

'''
line 31 dark theme fix for interval combobox in ui code
delegate = QtWidgets.QStyledItemDelegate()
self.comboBoxGraphColor = QtWidgets.QComboBox(PreferencesDialog)
self.comboBoxGraphColor.setItemDelegate(delegate)
'''

class PreferencesDialog(QtWidgets.QDialog):

    def __init__(self, stock):
        super(PreferencesDialog, self).__init__()
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.preferences = conf['preferences']
        self.ui.labelError.hide()
        self.add_combo_items()
        self.fill_old_settings()
    
    def add_combo_items(self):
        self.ui.comboBoxGraphColor.addItem("Green")
        self.ui.comboBoxGraphColor.addItem("Red")
        self.ui.comboBoxGraphColor.addItem("Blue")
        self.ui.comboBoxGraphColor.addItem("Cyan")
        self.ui.comboBoxGraphColor.addItem("Yellow")

    def fill_old_settings(self):
        self.ui.spinBoxRefreshRate.setValue(self.preferences['refresh_time'])
        self.ui.fontComboBox.setCurrentFont(QtGui.QFont(self.preferences['font']['family']))
        self.ui.spinBoxFontSize.setValue(self.preferences['font']['size'])
        self.set_color_index()
    
    def set_color_index(self):
        if self.preferences['graph_color'] == 'g':
            self.ui.comboBoxGraphColor.setCurrentIndex(0)
        elif self.preferences['graph_color'] == 'r':
            self.ui.comboBoxGraphColor.setCurrentIndex(1)
        elif self.preferences['graph_color'] == 'b':
            self.ui.comboBoxGraphColor.setCurrentIndex(2)
        elif self.preferences['graph_color'] == 'c':
            self.ui.comboBoxGraphColor.setCurrentIndex(3)
        elif self.preferences['graph_color'] == 'y':
            self.ui.comboBoxGraphColor.setCurrentIndex(4)
    
    def accept(self):
        if self.ui.spinBoxRefreshRate.value() < 10:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Refresh rate must be >= 10 seconds'))
            self.ui.labelError.show()
            return
        elif self.ui.spinBoxFontSize.value() < 7:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Font size must be >= 7'))
            self.ui.labelError.show()
            return
        self.preferences['graph_color'] = self.ui.comboBoxGraphColor.currentText()[0].lower()
        self.preferences['refresh_time'] = self.ui.spinBoxRefreshRate.value()
        self.preferences['font']['family'] = self.ui.fontComboBox.currentFont().family()
        self.preferences['font']['size'] = self.ui.spinBoxFontSize.value()
        super().accept()