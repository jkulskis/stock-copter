from PySide2 import QtCore, QtGui, QtWidgets

class TreeWidget(QtWidgets.QTreeWidget):

    def __init__(self, central_widget):
        super().__init__(central_widget)
        font = QtGui.QFont()
        font.setFamily("Garuda")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setAutoFillBackground(False)
        self.setDragEnabled(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAnimated(True)
        self.setExpandsOnDoubleClick(True)
        self.setObjectName("treeWidget")
        self.header().setCascadingSectionResizes(False)
        self.setSortingEnabled(True)
    
    def dropEvent(self, event):
        print('here')


    # def mouseReleaseEvent(self, event):
    #     if event.button() == QtCore.Qt.RightButton:
    #         self.clearSelection()