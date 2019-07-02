# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddStockDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(262, 149)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditTicker = QtWidgets.QLineEdit(Dialog)
        self.lineEditTicker.setObjectName("lineEditTicker")
        self.verticalLayout.addWidget(self.lineEditTicker)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButtonWatchList = QtWidgets.QRadioButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButtonWatchList.sizePolicy().hasHeightForWidth())
        self.radioButtonWatchList.setSizePolicy(sizePolicy)
        self.radioButtonWatchList.setChecked(True)
        self.radioButtonWatchList.setObjectName("radioButtonWatchList")
        self.horizontalLayout_2.addWidget(self.radioButtonWatchList)
        self.radioButtonPortfolio = QtWidgets.QRadioButton(Dialog)
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
        self.lineEditShares = QtWidgets.QLineEdit(Dialog)
        self.lineEditShares.setReadOnly(True)
        self.lineEditShares.setObjectName("lineEditShares")
        self.horizontalLayout.addWidget(self.lineEditShares)
        self.lineEditPrice = QtWidgets.QLineEdit(Dialog)
        self.lineEditPrice.setReadOnly(True)
        self.lineEditPrice.setObjectName("lineEditPrice")
        self.horizontalLayout.addWidget(self.lineEditPrice)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelError = QtWidgets.QLabel(Dialog)
        self.labelError.setObjectName("labelError")
        self.verticalLayout.addWidget(self.labelError)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEditTicker, self.radioButtonWatchList)
        Dialog.setTabOrder(self.radioButtonWatchList, self.radioButtonPortfolio)
        Dialog.setTabOrder(self.radioButtonPortfolio, self.lineEditShares)
        Dialog.setTabOrder(self.lineEditShares, self.lineEditPrice)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Stock"))
        self.lineEditTicker.setPlaceholderText(_translate("Dialog", "TICKER"))
        self.radioButtonWatchList.setText(_translate("Dialog", "Watch List"))
        self.radioButtonPortfolio.setText(_translate("Dialog", "Portfolio"))
        self.lineEditShares.setPlaceholderText(_translate("Dialog", "Shares"))
        self.lineEditPrice.setPlaceholderText(_translate("Dialog", "Price"))
        self.labelError.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ff0000;\">Error: Invalid Ticker</span></p></body></html>"))

