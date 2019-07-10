from forms.HeaderEditorUI import Ui_HeaderEditorDialog
from PySide2 import QtCore, QtGui, QtWidgets

class HeaderEditorDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(HeaderEditorDialog, self).__init__()
        self.parent = parent
        self.ui = Ui_HeaderEditorDialog()
        self.ui.setupUi(self)
        self.headers = self.parent.headers
        self.populate_tree_widget()
        self.ui.treeWidgetHeaders.expandAll()
        self.ui.treeWidgetHeaders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.ui.treeWidgetHeaders.itemSelectionChanged.connect(self.add_header)
    
    def populate_tree_widget(self):
        for header in self.headers:
            header_widget = QtWidgets.QTreeWidgetItem(self.ui.treeWidgetHeaders)
            header_widget.setText(0, header['text'])
            if 'conditionals' in header:
                for conditional in header['conditionals']:
                    conditional_widget = QtWidgets.QTreeWidgetItem(header_widget)
                    conditional_widget.setText(0, conditional['eq'])
    
    def add_header(self):
        print(self.ui.treeWidgetHeaders.currentIndex().row())
        print(self.ui.treeWidgetHeaders.currentItem().parent())

    def add_conditional(self):
        pass

    def edit(self):
        pass
    
    def remove(self):
        pass
    
    def up(self):
        pass
    
    def down(self):
        pass
    
    

