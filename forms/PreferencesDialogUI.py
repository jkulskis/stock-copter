# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreferencesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(365, 173)
        self.verticalLayout = QtWidgets.QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelRefreshRate = QtWidgets.QLabel(PreferencesDialog)
        self.labelRefreshRate.setObjectName("labelRefreshRate")
        self.horizontalLayout_2.addWidget(self.labelRefreshRate)
        self.spinBoxRefreshRate = QtWidgets.QSpinBox(PreferencesDialog)
        self.spinBoxRefreshRate.setObjectName("spinBoxRefreshRate")
        self.horizontalLayout_2.addWidget(self.spinBoxRefreshRate)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelGraphColor = QtWidgets.QLabel(PreferencesDialog)
        self.labelGraphColor.setObjectName("labelGraphColor")
        self.horizontalLayout_3.addWidget(self.labelGraphColor)
        delegate = QtWidgets.QStyledItemDelegate()
        self.comboBoxGraphColor = QtWidgets.QComboBox(PreferencesDialog)
        self.comboBoxGraphColor.setItemDelegate(delegate)
        self.comboBoxGraphColor.setObjectName("comboBoxGraphColor")
        self.horizontalLayout_3.addWidget(self.comboBoxGraphColor)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelFont = QtWidgets.QLabel(PreferencesDialog)
        self.labelFont.setObjectName("labelFont")
        self.horizontalLayout.addWidget(self.labelFont)
        self.fontComboBox = QtWidgets.QFontComboBox(PreferencesDialog)
        self.fontComboBox.setObjectName("fontComboBox")
        self.horizontalLayout.addWidget(self.fontComboBox)
        self.label = QtWidgets.QLabel(PreferencesDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBoxFontSize = QtWidgets.QSpinBox(PreferencesDialog)
        self.spinBoxFontSize.setObjectName("spinBoxFontSize")
        self.horizontalLayout.addWidget(self.spinBoxFontSize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelError = QtWidgets.QLabel(PreferencesDialog)
        self.labelError.setObjectName("labelError")
        self.verticalLayout.addWidget(self.labelError)
        self.buttonBox = QtWidgets.QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PreferencesDialog)
        self.buttonBox.accepted.connect(PreferencesDialog.accept)
        self.buttonBox.rejected.connect(PreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)

    def retranslateUi(self, PreferencesDialog):
        _translate = QtCore.QCoreApplication.translate
        PreferencesDialog.setWindowTitle(_translate("PreferencesDialog", "Preferences"))
        self.labelRefreshRate.setText(_translate("PreferencesDialog", "Price Refresh Rate:"))
        self.labelGraphColor.setText(_translate("PreferencesDialog", "Graph Color:"))
        self.labelFont.setText(_translate("PreferencesDialog", "Font:"))
        self.label.setText(_translate("PreferencesDialog", "Size:"))
        self.labelError.setText(_translate("PreferencesDialog", "Error Label"))

