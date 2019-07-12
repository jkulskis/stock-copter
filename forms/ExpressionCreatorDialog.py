from PySide2 import QtCore, QtGui, QtWidgets
from forms.ExpressionCreatorDialogUI import Ui_ExpressionCreatorDialog
from util.stock import Stock
from util.format import Formatter
from util.config import conf
import qdarkstyle

class ExpressionCreatorDialog(QtWidgets.QDialog):

    def __init__(self, policy='all_fields', old_expression='', old_conditional='', old_header_name='', old_custom_variable_name='', old_custom_description=''):
        super(ExpressionCreatorDialog, self).__init__()
        self.ui = Ui_ExpressionCreatorDialog()
        self.ui.setupUi(self)
        self.policy = policy
        if self.policy == 'conditional':
            self.last_line_edit_changed = self.ui.lineEditConditional
        else:
            self.last_line_edit_changed = self.ui.lineEditExpression
        self.hide_initial()
        self.ui.checkBoxAddToHeaders.setChecked(True)
        self.update_actions()
        self.custom_variables_casing = [conf['custom_variables'][variable]['true_casing'] for variable in conf['custom_variables']]
        self.update_boxes()
        self.expression = old_expression
        self.parsed_expression = []
        self.conditional = old_conditional
        self.old_conditional = old_conditional
        self.parsed_conditional = []
        self.header_name = old_header_name
        self.old_header_name = old_header_name
        self.custom_variable_name = old_custom_variable_name
        self.old_custom_variable_name = old_custom_variable_name
        self.custom_variable_description = old_custom_description
        self.update_line_edits()

    def accept(self):
        self.expression = self.ui.lineEditExpression.text().rstrip()
        self.header_name = self.ui.lineEditHeaderName.text().rstrip()
        self.conditional = self.ui.lineEditConditional.text().rstrip()
        self.custom_variable_name = self.ui.lineEditCustomVariableName.text().rstrip()
        self.custom_variable_description = self.ui.lineEditVariableDescription.text().rstrip()
        error = False
        if self.policy == 'all_fields':
            error = self.check_full_expression()
        elif self.policy == 'add_header':
            error = self.check_header(same_name_allowed=False)
            if self.ui.checkBoxAddConditional.isChecked():
                error = self.check_conditional()
        elif self.policy == 'edit_header':
            error = self.check_header(same_name_allowed=True)
        elif self.policy == 'conditional':
            error = self.check_conditional()
        elif self.policy == 'custom':
            error = self.check_custom()
        if self.policy != 'conditional': # expression is editable for every policy except for conditionals
            check_expression = Formatter.check_eq(self.expression) 
            if not check_expression[0]:
                self.ui.labelErrorExpression.show()
                self.ui.labelErrorExpression.setText(Formatter.get_error_text(check_expression[1]))
                error = True
            else:
                self.parsed_expression = check_expression[2]
        if not error:
            super().accept()

    def check_full_expression(self):
        error = False
        if self.ui.checkBoxAddConditional.isChecked():
            check_conditional = Formatter.check_eq(self.conditional, conditional=True)
            if not check_conditional[0]:
                self.ui.labelErrorConditional.show()
                self.ui.labelErrorConditional.setText(Formatter.get_error_text(check_conditional[1]))
                error = True
            else:
                self.parsed_conditional = check_conditional[2]
        if self.ui.checkBoxAddToHeaders.isChecked():
            if not self.validate_header():
                self.ui.labelErrorHeader.show()
                error = True
        if self.ui.checkBoxSaveVariable.isChecked():
            if not self.validate_custom_variable():
                self.ui.labelErrorVariableName.show()
                error = True
        if not self.ui.checkBoxAddToHeaders.isChecked() and not self.ui.checkBoxSaveVariable.isChecked():
            self.ui.labelErrorExpression.show()
            self.ui.labelErrorExpression.setText(Formatter.get_error_text('If you do not save as a header or custom variable, \
                                                                            this expression will be lost'))
            error = True
        return error
    
    def check_header(self, same_name_allowed=False):
        error = False
        if not self.validate_header(same_name_allowed=same_name_allowed): # editing a header, so it's okay if they enter the same header name
            self.ui.labelErrorHeader.show()
            error = True
        return error
    
    def check_conditional(self):
        error = False
        check_conditional = Formatter.check_eq(self.conditional, conditional=True)
        if not check_conditional[0]:
            self.ui.labelErrorConditional.show()
            self.ui.labelErrorConditional.setText(Formatter.get_error_text(check_conditional[1]))
            error = True
        else:
            self.parsed_conditional = check_conditional[2]
        return error
    
    def check_custom(self):
        error = False
        if not self.validate_custom_variable():
            self.ui.labelErrorVariableName.show()
            error = True
        return error

    def get_error_text(self, text):
        return '<html><head/><body><p><span style=" color:#ff0000;">Error: {0}</span></p></body></html>'.format(text)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            return # don't close the window on enter key pressed
        QtWidgets.QDialog.keyPressEvent(self, event)

    def update_actions(self):
        self.ui.checkBoxSaveVariable.stateChanged.connect(lambda : self.checkBox_changed(self.ui.checkBoxSaveVariable, self.ui.layoutCustomVariables))
        self.ui.checkBoxAddToHeaders.stateChanged.connect(lambda : self.checkBox_changed(self.ui.checkBoxAddToHeaders, self.ui.layoutHeader))
        self.ui.checkBoxAddConditional.stateChanged.connect((lambda : self.checkBox_changed(self.ui.checkBoxAddConditional, self.ui.layoutConditional)))
        self.ui.listViewVariableBox.itemActivated.connect((lambda : self.insert_variable(self.ui.listViewVariableBox)))
        self.ui.listViewOperatorBox.itemActivated.connect((lambda : self.insert_variable(self.ui.listViewOperatorBox)))
        self.ui.listViewConditionalBox.itemActivated.connect((lambda : self.insert_variable(self.ui.listViewConditionalBox)))
        self.ui.lineEditExpression.textChanged.connect((lambda : self.validate_expression(self.ui.lineEditExpression)))
        self.ui.lineEditConditional.textChanged.connect((lambda : self.validate_expression(self.ui.lineEditConditional)))
        if self.policy == 'edit_header':
            self.ui.lineEditHeaderName.textChanged.connect((lambda : self.validate_header(same_name_allowed=True)))
        else:
            self.ui.lineEditHeaderName.textChanged.connect((lambda : self.validate_header(same_name_allowed=False)))
        self.ui.lineEditCustomVariableName.textChanged.connect((lambda : self.validate_custom_variable()))

    def update_line_edits(self):
        self.ui.lineEditExpression.setText(self.expression)
        self.ui.lineEditHeaderName.setText(self.header_name)
        self.ui.lineEditConditional.setText(self.conditional)
        self.ui.lineEditCustomVariableName.setText(self.custom_variable_name)
        self.ui.lineEditVariableDescription.setText(self.custom_variable_description)

    def color_on_validation(self, lineEdit, valid=None):
        self.last_line_edit_changed = lineEdit
        if valid:
            lineEdit.setStyleSheet('background-color: green')
        elif valid == False:
            lineEdit.setStyleSheet('background-color: red')
        else:
            #lineEdit.setStyleSheet("""QLineEdit { background-color: white}""")
            #default_background = 'QLineEdit { background-color: {}}'.format(QtGui.QTextLine.palette().color(QtGui.QPalette.Background).name())
            lineEdit.setStyleSheet('background-color: {}'.format(qdarkstyle.DarkPalette().COLOR_BACKGROUND_DARK))
            pass

    def validate_expression(self, lineEdit):
        self.last_line_edit_changed = lineEdit
        conditional = 'Conditional' in lineEdit.objectName()
        if conditional:
            self.ui.labelErrorConditional.hide()
        else:
            self.ui.labelErrorExpression.hide()
        check = Formatter.check_eq(lineEdit.text(), conditional=conditional)
        if not lineEdit.text().rstrip():
            valid = None
        elif check[0]:
            valid = True
        else:
            valid = False
        self.color_on_validation(lineEdit, valid=valid)
        if conditional:
            self.ui.labelErrorConditional.setText(Formatter.get_error_text(check[1]))
        else:
            self.ui.labelErrorExpression.setText(Formatter.get_error_text(check[1]))
        return valid

    def validate_custom_variable(self):
        variable_name = self.ui.lineEditCustomVariableName.text().upper().rstrip()
        self.ui.labelErrorVariableName.hide()
        valid = False
        if not variable_name:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name cannot be empty'))
            valid = None
        elif ' ' in variable_name:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name cannot contain spaces'))
        elif [conditional for conditional in Formatter.CONDITIONALS_NO_SPACING if conditional in variable_name]:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name cannot contain conditional symbols'))
        elif [op for op in Formatter.OPERATORS if op in variable_name]:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name cannot contain an operator'))
        elif [result for result in Formatter.CONDITIONAL_RESULTS if result in variable_name]:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name cannot contain a conditional result'))
        elif variable_name in Formatter.CONDITIONAL_WORDS:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name cannot equal a conditional operator'))
        elif variable_name in conf['custom_variables']:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom Variable Name already exists'))
        elif variable_name in Stock.get_variables()[1]:
            self.ui.labelErrorVariableName.setText(Formatter.get_error_text('Custom variable name cannot be a built in stock variable'))
        else:
            valid = True
        self.color_on_validation(self.ui.lineEditCustomVariableName, valid=valid)
        return valid
    
    def validate_header(self, same_name_allowed=False):
        header_text = self.ui.lineEditHeaderName.text().rstrip()
        self.ui.labelErrorHeader.hide()
        valid = True
        if not header_text:
            self.ui.labelErrorHeader.setText(Formatter.get_error_text('Header Name cannot be empty'))
            valid = None
        else:
            for header in conf['tree_view']['headers']:
                if header_text == header['text']:
                    valid = False
                    self.ui.labelErrorHeader.setText(Formatter.get_error_text('Header Name already exists'))
                    if same_name_allowed and header_text == self.old_header_name:
                        valid = True
        self.color_on_validation(self.ui.lineEditHeaderName, valid=valid)
        return valid         

    def insert_variable(self, box):
        for item in box.selectedItems():
            if self.last_line_edit_changed.text():
                self.last_line_edit_changed.setText('{0} {1}'.format(self.last_line_edit_changed.text().rstrip(), item.text()))
            else:
                self.last_line_edit_changed.setText('{0}'.format(item.text()))
        box.clearSelection()
        self.last_line_edit_changed.setFocus()
        if self.last_line_edit_changed.objectName() == 'lineEditExpression':
            self.validate_expression(self.ui.lineEditExpression)
        elif self.last_line_edit_changed.objectName() == 'lineEditConditional':
            self.validate_expression(self.ui.lineEditConditional)
        elif self.last_line_edit_changed.objectName() == 'lineEditCustomVariableName':
            self.validate_custom_variable()
        elif self.last_line_edit_changed.objectName() == 'lineEditHeaderName':
            self.validate_header()

    def update_boxes(self):
        for variable in Stock.get_variables()[0]:
            self.ui.listViewVariableBox.addItem(variable)
        for variable in self.custom_variables_casing:
            self.ui.listViewVariableBox.addItem(variable)
        for operator in Formatter.OPERATORS:
            self.ui.listViewOperatorBox.addItem(operator)
        for operator in Formatter.CONDITIONALS + Formatter.CONDITIONAL_RESULTS_CASING:
            self.ui.listViewConditionalBox.addItem(operator)

    def hide_initial(self):
        self.ui.labelErrorExpression.hide()
        self.ui.labelErrorConditional.hide()
        self.ui.labelErrorHeader.hide()
        self.ui.labelErrorVariableName.hide()
        self.ui.labelSelectedVariableDescription.hide() # not setup yet
        while True:
            if self.policy == 'all_fields':
                self.ui.checkBoxAddConditional.show()
                self.hide_object(self.ui.layoutConditional)
                self.hide_object(self.ui.layoutCustomVariables)
                break
            self.hide_object(self.ui.checkBoxAddToHeaders)
            if self.policy == 'add_header':
                self.hide_object(self.ui.layoutConditional)
                self.ui.checkBoxAddConditional.show()
                self.hide_object(self.ui.layoutCustomVariables)
                break
            self.hide_object(self.ui.checkBoxAddConditional)
            self.hide_object(self.ui.checkBoxSaveVariable)
            if self.policy == 'edit_header':
                self.hide_object(self.ui.layoutConditional)
                self.hide_object(self.ui.layoutCustomVariables)
            elif self.policy == 'conditional':
                self.hide_object(self.ui.layoutExpression)
                self.hide_object(self.ui.layoutHeader)
                self.hide_object(self.ui.layoutCustomVariables)
            elif self.policy == 'custom':
                self.hide_object(self.ui.layoutConditional)
                self.hide_object(self.ui.layoutHeader)
            break

    def checkBox_changed(self, checkbox, layout):
        if checkbox.isChecked():
            self.show_object(layout)
        else:
            self.hide_object(layout)
        checkbox.show() # if the checkbox is in the layout, still show it

    def hide_object(self, q_object):
        if type(q_object) != QtWidgets.QVBoxLayout:
            q_object.hide()
        else:
            for i in range(q_object.count()):
                if type(q_object.itemAt(i)) == QtWidgets.QVBoxLayout:
                    self.hide_object(q_object.itemAt(i))
                else:
                    q_object.itemAt(i).widget().hide()
                    if type(q_object.itemAt(i).widget()) == QtWidgets.QLineEdit:
                        q_object.itemAt(i).widget().setText('')
    
    def show_object(self, q_object):
        if type(q_object) != QtWidgets.QVBoxLayout:
            q_object.show()
        elif q_object.objectName() != 'layoutDescriptionSubCustomVariables': # not setup yet
            for i in range(q_object.count()):
                if type(q_object.itemAt(i)) == QtWidgets.QVBoxLayout:
                    self.show_object(q_object.itemAt(i))
                elif 'Error' not in q_object.itemAt(i).widget().objectName(): # don't show error labels
                    q_object.itemAt(i).widget().show()