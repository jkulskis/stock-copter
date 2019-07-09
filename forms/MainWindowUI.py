# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from forms.tree_widget import TreeWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(934, 502)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Garuda")
        font.setPointSize(12)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName("labelTitle")
        self.horizontalLayout.addWidget(self.labelTitle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonHeaderEditor = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonHeaderEditor.setObjectName("pushButtonHeaderEditor")
        self.horizontalLayout.addWidget(self.pushButtonHeaderEditor)
        self.pushButtonExpressionCreator = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExpressionCreator.setObjectName("pushButtonExpressionCreator")
        self.horizontalLayout.addWidget(self.pushButtonExpressionCreator)
        self.pushButtonAddStock = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAddStock.setObjectName("pushButtonAddStock")
        self.horizontalLayout.addWidget(self.pushButtonAddStock)
        self.pushButtonRemoveStock = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRemoveStock.sizePolicy().hasHeightForWidth())
        self.pushButtonRemoveStock.setSizePolicy(sizePolicy)
        self.pushButtonRemoveStock.setObjectName("pushButtonRemoveStock")
        self.horizontalLayout.addWidget(self.pushButtonRemoveStock)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = TreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Garuda")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.treeWidget.setFont(font)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.setAutoFillBackground(False)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setExpandsOnDoubleClick(True)
        self.treeWidget.setColumnCount(0)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().setDefaultSectionSize(100)
        self.treeWidget.header().setHighlightSections(True)
        self.verticalLayout.addWidget(self.treeWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 934, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Stock = QtWidgets.QAction(MainWindow)
        self.actionAdd_Stock.setObjectName("actionAdd_Stock")
        self.actionEdit_Headers = QtWidgets.QAction(MainWindow)
        self.actionEdit_Headers.setObjectName("actionEdit_Headers")
        self.actionCreate_Expression = QtWidgets.QAction(MainWindow)
        self.actionCreate_Expression.setObjectName("actionCreate_Expression")
        self.menuFile.addAction(self.actionAdd_Stock)
        self.menuFile.addAction(self.actionEdit_Headers)
        self.menuFile.addAction(self.actionCreate_Expression)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Copter"))
        self.labelTitle.setText(_translate("MainWindow", "Stock Copter"))
        self.pushButtonHeaderEditor.setText(_translate("MainWindow", "Edit Headers"))
        self.pushButtonExpressionCreator.setText(_translate("MainWindow", "Create Expression"))
        self.pushButtonAddStock.setText(_translate("MainWindow", "-"))
        self.pushButtonRemoveStock.setText(_translate("MainWindow", "+"))
        self.treeWidget.setSortingEnabled(True)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAdd_Stock.setText(_translate("MainWindow", "Add Stock"))
        self.actionEdit_Headers.setText(_translate("MainWindow", "Edit Headers"))
        self.actionCreate_Expression.setText(_translate("MainWindow", "Create Expression"))

