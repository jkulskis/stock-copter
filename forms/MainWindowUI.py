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
        MainWindow.resize(950, 521)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.add_stock_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_stock_button.sizePolicy().hasHeightForWidth())
        self.add_stock_button.setSizePolicy(sizePolicy)
        self.add_stock_button.setObjectName("add_stock_button")
        self.gridLayout.addWidget(self.add_stock_button, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
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
        self.treeWidget.headerItem().setText(0, "Stock")
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Copter"))
        self.add_stock_button.setText(_translate("MainWindow", "+"))
        self.pushButton.setText(_translate("MainWindow", "-"))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Price"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

