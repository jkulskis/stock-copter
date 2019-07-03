# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddStockDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddStockDialog(object):
    def setupUi(self, AddStockDialog):
        AddStockDialog.setObjectName("AddStockDialog")
        AddStockDialog.resize(262, 149)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddStockDialog.sizePolicy().hasHeightForWidth())
        AddStockDialog.setSizePolicy(sizePolicy)
        AddStockDialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddStockDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditTicker = QtWidgets.QLineEdit(AddStockDialog)
        self.lineEditTicker.setObjectName("lineEditTicker")
        self.verticalLayout.addWidget(self.lineEditTicker)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButtonWatchList = QtWidgets.QRadioButton(AddStockDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButtonWatchList.sizePolicy().hasHeightForWidth())
        self.radioButtonWatchList.setSizePolicy(sizePolicy)
        self.radioButtonWatchList.setChecked(True)
        self.radioButtonWatchList.setObjectName("radioButtonWatchList")
        self.horizontalLayout_2.addWidget(self.radioButtonWatchList)
        self.radioButtonPortfolio = QtWidgets.QRadioButton(AddStockDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButtonPortfolio.sizePolicy().hasHeightForWidth())
        self.radioButtonPortfolio.setSizePolicy(sizePolicy)
        self.radioButtonPortfolio.setObjectName("radioButtonPortfolio")
        self.horizontalLayout_2.addWidget(self.radioButtonPortfolio)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditShares = QtWidgets.QLineEdit(AddStockDialog)
        self.lineEditShares.setReadOnly(True)
        self.lineEditShares.setObjectName("lineEditShares")
        self.horizontalLayout.addWidget(self.lineEditShares)
        self.lineEditPrice = QtWidgets.QLineEdit(AddStockDialog)
        self.lineEditPrice.setReadOnly(True)
        self.lineEditPrice.setObjectName("lineEditPrice")
        self.horizontalLayout.addWidget(self.lineEditPrice)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelError = QtWidgets.QLabel(AddStockDialog)
        self.labelError.setObjectName("labelError")
        self.verticalLayout.addWidget(self.labelError)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddStockDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddStockDialog)
        self.buttonBox.accepted.connect(AddStockDialog.accept)
        self.buttonBox.rejected.connect(AddStockDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddStockDialog)
        AddStockDialog.setTabOrder(self.lineEditTicker, self.radioButtonWatchList)
        AddStockDialog.setTabOrder(self.radioButtonWatchList, self.radioButtonPortfolio)
        AddStockDialog.setTabOrder(self.radioButtonPortfolio, self.lineEditShares)
        AddStockDialog.setTabOrder(self.lineEditShares, self.lineEditPrice)

    def retranslateUi(self, AddStockDialog):
        _translate = QtCore.QCoreApplication.translate
        AddStockDialog.setWindowTitle(_translate("AddStockDialog", "Add Stock"))
        self.lineEditTicker.setPlaceholderText(_translate("AddStockDialog", "TICKER"))
        self.radioButtonWatchList.setText(_translate("AddStockDialog", "Watch List"))
        self.radioButtonPortfolio.setText(_translate("AddStockDialog", "Portfolio"))
        self.lineEditShares.setPlaceholderText(_translate("AddStockDialog", "Shares"))
        self.lineEditPrice.setPlaceholderText(_translate("AddStockDialog", "Price"))
        self.labelError.setText(_translate("AddStockDialog", "<html><head/><body><p><span style=\" color:#ff0000;\">Error: Invalid Ticker</span></p></body></html>"))

