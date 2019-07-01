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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.add_stock_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_stock_button.sizePolicy().hasHeightForWidth())
        self.add_stock_button.setSizePolicy(sizePolicy)
        self.add_stock_button.setObjectName("add_stock_button")
        self.horizontalLayout.addWidget(self.add_stock_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Garuda")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.treeWidget.setFont(font)
        self.treeWidget.setAutoFillBackground(False)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setExpandsOnDoubleClick(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setCascadingSectionResizes(False)
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
        self.menuFile.addAction(self.actionAdd_Stock)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Copter"))
        self.labelTitle.setText(_translate("MainWindow", "Stock Copter"))
        self.pushButton.setText(_translate("MainWindow", "-"))
        self.add_stock_button.setText(_translate("MainWindow", "+"))
        self.treeWidget.setSortingEnabled(True)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAdd_Stock.setText(_translate("MainWindow", "Add Stock"))

