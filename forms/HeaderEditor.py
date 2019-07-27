from forms.HeaderEditorUI import Ui_HeaderEditorDialog
from forms.ExpressionCreatorDialog import ExpressionCreatorDialog
from PySide2 import QtCore, QtGui, QtWidgets

class HeaderEditorDialog(QtWidgets.QDialog):

    def __init__(self, headers):
        super(HeaderEditorDialog, self).__init__()
        self.ui = Ui_HeaderEditorDialog()
        self.ui.setupUi(self)
        self.headers = headers
        self.populate_tree_widget()
        if len(self.headers): # select the first item on startup if there is one
            self.selected_item = {'item' : self.get_item(0), 'index' : 0, 'parent_index' : None}
            self.ui.treeWidgetHeaders.setItemSelected(self.selected_item['item'], True)
        else:
            self.selected_item = {'item' : None, 'index' : None, 'parent_index' : None}
        self.update_actions()

    def update_actions(self):
        self.ui.treeWidgetHeaders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.ui.treeWidgetHeaders.currentItemChanged.connect(self.item_changed) # itemSelectionChanged is buggy when mouse is dragged, so use currentItemChanged
        self.ui.treeWidgetHeaders.itemActivated.connect(self.edit)
        self.ui.pushButtonUp.pressed.connect(self.up)
        self.ui.pushButtonDown.pressed.connect(self.down)
        self.ui.pushButtonAddConditional.pressed.connect(self.add_conditional)
        self.ui.pushButtonAddHeader.pressed.connect(self.add_header)
        self.ui.pushButtonEdit.pressed.connect(self.edit)
        self.ui.pushButtonRemove.pressed.connect(self.remove)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            pass
        if event.key() == QtCore.Qt.Key_Escape:
            self.accept()

    def populate_tree_widget(self):
        self.ui.treeWidgetHeaders.clear()
        for header in self.headers:
            header_widget = QtWidgets.QTreeWidgetItem(self.ui.treeWidgetHeaders)
            header_widget.setText(0, header['text'])
            if 'conditionals' in header:
                for conditional in header['conditionals']:
                    conditional_widget = QtWidgets.QTreeWidgetItem(header_widget)
                    conditional_widget.setText(0, conditional['eq'])
        self.ui.treeWidgetHeaders.expandAll()

    def item_changed(self):
        if self.ui.treeWidgetHeaders.currentItem():
            self.selected_item['item'] = self.ui.treeWidgetHeaders.currentItem()
            self.selected_item['index'] = self.ui.treeWidgetHeaders.currentIndex().row()
            if self.ui.treeWidgetHeaders.currentItem().parent(): # check if conditional by seeing if parent is not None
                parent_text = self.ui.treeWidgetHeaders.currentItem().parent().text(0)
                for ii in range(len(self.headers)):
                    if self.headers[ii]['text'] == parent_text:
                        self.selected_item['parent_index'] = ii
                        break 
            else:
                self.selected_item['parent_index'] = None

    def get_item(self, root_index, child_index=None):
        root = self.ui.treeWidgetHeaders.invisibleRootItem()
        item = root.child(root_index)
        if child_index is not None:
            item = item.child(child_index)
        return item
    
    def top_level_item_count(self):
        root = self.ui.treeWidgetHeaders.invisibleRootItem()
        return root.childCount()

    def add_header(self):
        if self.selected_item['parent_index'] is not None:
            index = self.selected_item['parent_index'] + 1
        elif self.selected_item['index'] is not None:
            index = self.selected_item['index'] + 1
        else:
            index = len(self.headers)
        expression_creator_dialog = ExpressionCreatorDialog(policy='add_header')
        accepted = expression_creator_dialog.exec_()
        if accepted:
            new_header = dict.fromkeys(('text', 'eq', 'parsed_eq'))
            new_header['text'] = expression_creator_dialog.header_name
            new_header['eq'] = expression_creator_dialog.expression
            new_header['parsed_eq'] = expression_creator_dialog.parsed_expression
            self.headers.insert(index, new_header)
        self.populate_tree_widget()
        self.selected_item = {'item' : None, 'index' : None, 'parent_index' : None}

    def add_conditional(self):
        expression_creator_dialog = ExpressionCreatorDialog(policy='conditional')
        accepted = expression_creator_dialog.exec_()
        if accepted:
            new_conditional = dict.fromkeys(('eq', 'parsed_eq'))
            new_conditional['eq'] = expression_creator_dialog.conditional
            new_conditional['parsed_eq'] = expression_creator_dialog.parsed_conditional
            if self.selected_item['parent_index']:
                if 'conditionals' in self.headers[self.selected_item['parent_index']]:
                    self.headers[self.selected_item['parent_index']]['conditionals'].append(new_conditional)
                else:
                    self.headers[self.selected_item['parent_index']]['conditionals'] = [new_conditional]
            else:
                if 'conditionals' in self.headers[self.selected_item['index']]:
                    self.headers[self.selected_item['index']]['conditionals'].append(new_conditional)
                else:
                    self.headers[self.selected_item['index']]['conditionals'] = [new_conditional]
            self.populate_tree_widget()
            self.selected_item = {'item' : None, 'index' : None, 'parent_index' : None}

    def edit(self):
        if self.selected_item['parent_index']:
            expression_creator_dialog = ExpressionCreatorDialog(policy='conditional', 
                old_conditional=self.headers[self.selected_item['parent_index']]['conditionals'][self.selected_item['index']]['eq'])
            accepted = expression_creator_dialog.exec_()
            if accepted:
                new_conditional = dict.fromkeys(('eq', 'parsed_eq'))
                new_conditional['eq'] = expression_creator_dialog.conditional
                new_conditional['parsed_eq'] = expression_creator_dialog.parsed_conditional
                self.headers[self.selected_item['parent_index']]['conditionals'][self.selected_item['index']] = new_conditional
                self.populate_tree_widget()
                self.selected_item['item'] = self.get_item(self.selected_item['parent_index'], self.selected_item['index'])
                self.ui.treeWidgetHeaders.setItemSelected(self.selected_item['item'], True)
        else:
            expression_creator_dialog = ExpressionCreatorDialog(policy='edit_header', old_header_name=self.headers[self.selected_item['index']]['text'], 
                old_expression=self.headers[self.selected_item['index']]['eq'])
            accepted = expression_creator_dialog.exec_()
            if accepted:
                new_header = dict.fromkeys(('text', 'eq', 'parsed_eq'))
                new_header['text'] = expression_creator_dialog.header_name
                new_header['eq'] = expression_creator_dialog.expression
                new_header['parsed_eq'] = expression_creator_dialog.parsed_expression
                self.headers[self.selected_item['index']] = new_header
                self.populate_tree_widget()
                self.selected_item['item'] = self.get_item(self.selected_item['index'])
                self.ui.treeWidgetHeaders.setItemSelected(self.selected_item['item'], True)

    def remove(self):
        if self.selected_item['parent_index'] is not None:
            del self.headers[self.selected_item['parent_index']]['conditionals'][self.selected_item['index']]
        else:
            del self.headers[self.selected_item['index']]
        self.populate_tree_widget()
    
    def up(self):
        ii = self.selected_item['index']
        conditional = False
        if ii == 0:
            return # can't move up if index is 0
        if self.selected_item['parent_index'] is not None:
            conditional = True
            self.headers[self.selected_item['parent_index']]['conditionals'][ii], self.headers[self.selected_item['parent_index']]['conditionals'][ii - 1] = \
                self.headers[self.selected_item['parent_index']]['conditionals'][ii - 1], self.headers[self.selected_item['parent_index']]['conditionals'][ii]
        else:
            self.headers[ii], self.headers[ii - 1] = self.headers[ii - 1], self.headers[ii]
        self.populate_tree_widget()
        if conditional:
            self.selected_item['item'] = self.get_item(self.selected_item['parent_index'], ii - 1)
        else:
            self.selected_item['item'] = self.get_item(ii - 1)
        self.selected_item['index'] = ii - 1
        self.ui.treeWidgetHeaders.setItemSelected(self.selected_item['item'], True)
    
    def down(self):
        ii = self.selected_item['index']
        conditional = False
        if self.selected_item['parent_index'] is not None:
            conditional = True
            if ii == self.get_item(self.selected_item['parent_index']).childCount() - 1:
                return # can't move down if index is the greatest
        elif ii == self.top_level_item_count() - 1:
            return # can't move down if index is the greatest
        if conditional:
            self.headers[self.selected_item['parent_index']]['conditionals'][ii], self.headers[self.selected_item['parent_index']]['conditionals'][ii + 1] = \
                self.headers[self.selected_item['parent_index']]['conditionals'][ii + 1], self.headers[self.selected_item['parent_index']]['conditionals'][ii]
        else:
            self.headers[ii], self.headers[ii + 1] = self.headers[ii + 1], self.headers[ii]
        self.populate_tree_widget()
        if conditional:
            self.selected_item['item'] = self.get_item(self.selected_item['parent_index'], ii + 1)
        else:
            self.selected_item['item'] = self.get_item(ii + 1)
        self.selected_item['index'] = ii + 1
        self.ui.treeWidgetHeaders.setItemSelected(self.selected_item['item'], True)
    
    

