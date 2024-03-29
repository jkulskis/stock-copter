# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddStock.sizePolicy().hasHeightForWidth())
        self.pushButtonAddStock.setSizePolicy(sizePolicy)
        self.pushButtonAddStock.setObjectName("pushButtonAddStock")
        self.horizontalLayout.addWidget(self.pushButtonAddStock)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Garuda")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.treeWidget.setFont(font)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.setAutoFillBackground(False)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
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
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
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
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionAdd_Stock)
        self.menuFile.addAction(self.actionEdit_Headers)
        self.menuFile.addAction(self.actionCreate_Expression)
        self.menuHelp.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Copter"))
        self.labelTitle.setText(_translate("MainWindow", "Stock Copter"))
        self.pushButtonHeaderEditor.setText(_translate("MainWindow", "Edit Headers + Conditionals"))
        self.pushButtonExpressionCreator.setText(_translate("MainWindow", "Create Expression"))
        self.pushButtonAddStock.setText(_translate("MainWindow", "Add Stock"))
        self.treeWidget.setSortingEnabled(False)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAdd_Stock.setText(_translate("MainWindow", "Add Stock"))
        self.actionEdit_Headers.setText(_translate("MainWindow", "Edit Headers + Conditionals"))
        self.actionEdit_Headers.setIconText(_translate("MainWindow", "Edit Headers + Conditionals"))
        self.actionEdit_Headers.setToolTip(_translate("MainWindow", "Edit Headers + Conditionals"))
        self.actionCreate_Expression.setText(_translate("MainWindow", "Create Expression"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

