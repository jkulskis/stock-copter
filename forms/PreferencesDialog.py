from PySide2 import QtCore, QtGui, QtWidgets
from forms.PreferencesDialogUI import Ui_PreferencesDialog
from util.format import Formatter
from util.config import conf
import os, sys
import qdarkstyle

'''
line 32 dark theme fix for graph color combobox in ui code
delegate = QtWidgets.QStyledItemDelegate()
self.comboBoxGraphColor = QtWidgets.QComboBox(PreferencesDialog)
self.comboBoxGraphColor.setItemDelegate(delegate)

line 69 dark theme fix for theme combobox in ui code
delegate = QtWidgets.QStyledItemDelegate()
self.comboBoxTheme = QtWidgets.QComboBox(PreferencesDialog)
self.comboBoxTheme.setItemDelegate(delegate)
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
        self.ui.comboBoxTheme.addItem("Light")
        self.ui.comboBoxTheme.addItem("Dark")

    def fill_old_settings(self):
        self.ui.spinBoxRefreshRate.setValue(self.preferences['refresh_time'])
        self.ui.spinBoxRefreshRate.setSuffix("s")
        self.ui.fontComboBox.setCurrentFont(QtGui.QFont(self.preferences['font']['family']))
        self.ui.spinBoxFontSize.setValue(self.preferences['font']['size'])
        self.ui.spinBoxGraphLineWidth.setValue(self.preferences['graph_settings']['line_width'])
        self.set_color_index()
        self.set_theme_index()
    
    def set_color_index(self):
        if self.preferences['graph_settings']['color'] == 'g':
            self.ui.comboBoxGraphColor.setCurrentIndex(0)
        elif self.preferences['graph_settings']['color'] == 'r':
            self.ui.comboBoxGraphColor.setCurrentIndex(1)
        elif self.preferences['graph_settings']['color'] == 'b':
            self.ui.comboBoxGraphColor.setCurrentIndex(2)
        elif self.preferences['graph_settings']['color'] == 'c':
            self.ui.comboBoxGraphColor.setCurrentIndex(3)
        elif self.preferences['graph_settings']['color'] == 'y':
            self.ui.comboBoxGraphColor.setCurrentIndex(4)
    
    def set_theme_index(self):
        if self.preferences['theme'] == 'light':
            self.ui.comboBoxTheme.setCurrentIndex(0)
        elif self.preferences['theme'] == 'dark':
            self.ui.comboBoxTheme.setCurrentIndex(1)
    
    def open_restart_msgbox(self, setting):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText('To change the {} setting you must restart to see changes. \n Restart Now?')
        msg_box.setWindowTitle('Preferences Changed')
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg_box.exec_() == QtWidgets.QMessageBox.Yes:
            QtCore.QCoreApplication.exit(conf.REBOOT_CODE)

    def accept(self):
        if self.ui.spinBoxRefreshRate.value() < 10:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Refresh rate must be >= 10 seconds'))
            self.ui.labelError.show()
            return
        elif self.ui.spinBoxFontSize.value() < 7:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Font size must be >= 7'))
            self.ui.labelError.show()
            return
        self.preferences['graph_settings']['color'] = self.ui.comboBoxGraphColor.currentText()[0].lower()
        self.preferences['graph_settings']['line_width'] = self.ui.spinBoxGraphLineWidth.value()
        self.preferences['refresh_time'] = self.ui.spinBoxRefreshRate.value()
        self.preferences['font']['family'] = self.ui.fontComboBox.currentFont().family()
        self.preferences['font']['size'] = self.ui.spinBoxFontSize.value()
        chosen_theme = self.ui.comboBoxTheme.currentText().lower()
        if chosen_theme != self.preferences['theme']:
            self.preferences['theme'] = chosen_theme
            if chosen_theme == 'light':
                QtGui.qApp.setStyleSheet("")
            elif chosen_theme == 'dark':
                QtGui.qApp.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        super().accept()