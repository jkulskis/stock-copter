from PySide2 import QtCore, QtGui, QtWidgets
from forms.ExpressionCreatorDialogUI import Ui_ExpressionCreatorDialog
from util.stock import Stock, Formatter
from util.config import conf

class ExpressionCreatorDialog(QtWidgets.QDialog):

    def __init__(self):
        super(ExpressionCreatorDialog, self).__init__()
        self.ui = Ui_ExpressionCreatorDialog()
        self.ui.setupUi(self)
        self.hide_initial()
        self.ui.checkBoxAddToHeaders.setChecked(True)
        self.update_actions()
        self.stock_variables = Stock.get_variables()[0]
        self.custom_variables = conf['custom_variables']
        self.operators = Formatter.OPERATORS
        self.update_boxes()
        self.expression = ''
        self.header_name = ''
        self.conditional = ''
        self.custom_variable_name = ''
        self.description = ''

    def accept(self):
        self.expression = self.ui.lineEditExpression.text()
        self.header_name = self.ui.llineEditHeaderName.text()
        self.conditional = self.ui.lineEditConditional.text()
        self.custom_variable_name = self.ui.lineEditCustomVariableName.text()
        self.description = self.ui.lineEditVariableDescription.text()
        check = Formatter.check_eq(self.expression)
        print(self.expression)
        if not check[0]:
            self.ui.labelError.setText(('<html><head/><body><p><span style=" color:#ff0000;">Error: {0}</span></p></body></html>')
                                    .format(check[1]))
            return
        if self.conditional:
            check = Formatter.check_eq(self.conditional, conditional=True)
            if not check[0]:
                self.ui.labelError.setText(('<html><head/><body><p><span style=" color:#ff0000;">Error: {0}</span></p></body></html>')
                                    .format(check[1]))
                return 
        super().accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            return # don't close the window on enter key pressed
        QtWidgets.QDialog.keyPressEvent(self, event)

    def update_actions(self):
        self.ui.checkBoxSaveVariable.stateChanged.connect(lambda : self.check_changed(self.ui.checkBoxSaveVariable, self.ui.layoutCustomVariables))
        self.ui.checkBoxAddToHeaders.stateChanged.connect(lambda : self.check_changed(self.ui.checkBoxAddToHeaders, self.ui.layoutHeader))
        self.ui.checkBoxAddConditional.stateChanged.connect((lambda : self.check_changed(self.ui.checkBoxAddConditional, self.ui.layoutConditional)))
        self.ui.listViewVariableBox.doubleClicked.connect((lambda : self.insert_variable(self.ui.listViewVariableBox)))
        self.ui.listViewOperatorBox.doubleClicked.connect((lambda : self.insert_variable(self.ui.listViewOperatorBox)))
    
    def insert_variable(self, box):
        for item in box.selectedItems():
            if self.ui.lineEditExpression.text():
                self.ui.lineEditExpression.setText('{0} {1}'.format(self.ui.lineEditExpression.text(), item.text()))
            else:
                self.ui.lineEditExpression.setText('{0}'.format(item.text()))
        box.clearSelection()

    def update_boxes(self):
        for variable in self.stock_variables:
            self.ui.listViewVariableBox.addItem(variable)
        for variable in self.custom_variables:
            self.ui.listViewVariableBox.addItem(variable)
        for operator in self.operators:
            self.ui.listViewOperatorBox.addItem(operator)

    def hide_initial(self):
        #self.hide_layout(self.ui.layoutHeader)
        self.hide_layout(self.ui.layoutConditional)
        self.hide_layout(self.ui.layoutCustomVariables)
    
    def check_changed(self, checkbox, layout):
        if checkbox.isChecked():
            self.show_layout(layout)
        else:
            self.hide_layout(layout)

    def show_layout(self, layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i)
            if type(widget) == QtWidgets.QVBoxLayout:
                self.show_layout(widget)
            else:
                layout.itemAt(i).widget().show()

    def hide_layout(self, layout):
        if layout.objectName() == 'layoutHeader':
            self.hide_layout(self.ui.layoutConditional)
            self.ui.checkBoxAddConditional.setChecked(False)
        for i in range(layout.count()):
            if type(layout.itemAt(i)) == QtWidgets.QVBoxLayout:
                self.hide_layout(layout.itemAt(i))
            else:
                layout.itemAt(i).widget().hide()
                if type(layout.itemAt(i).widget()) == QtWidgets.QLineEdit:
                    layout.itemAt(i).widget().setText('')