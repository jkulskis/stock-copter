# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HeaderEditor.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_HeaderEditorDialog(object):
    def setupUi(self, HeaderEditorDialog):
        HeaderEditorDialog.setObjectName("HeaderEditorDialog")
        HeaderEditorDialog.resize(748, 360)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(HeaderEditorDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeWidgetHeaders = QtWidgets.QTreeWidget(HeaderEditorDialog)
        self.treeWidgetHeaders.setAnimated(True)
        self.treeWidgetHeaders.setHeaderHidden(False)
        self.treeWidgetHeaders.setColumnCount(1)
        self.treeWidgetHeaders.setObjectName("treeWidgetHeaders")
        self.horizontalLayout_2.addWidget(self.treeWidgetHeaders)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonAddHeader = QtWidgets.QPushButton(HeaderEditorDialog)
        self.pushButtonAddHeader.setObjectName("pushButtonAddHeader")
        self.verticalLayout.addWidget(self.pushButtonAddHeader)
        self.pushButtonAddConditional = QtWidgets.QPushButton(HeaderEditorDialog)
        self.pushButtonAddConditional.setObjectName("pushButtonAddConditional")
        self.verticalLayout.addWidget(self.pushButtonAddConditional)
        self.pushButtonRemove = QtWidgets.QPushButton(HeaderEditorDialog)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.verticalLayout.addWidget(self.pushButtonRemove)
        self.pushButtonEdit = QtWidgets.QPushButton(HeaderEditorDialog)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.verticalLayout.addWidget(self.pushButtonEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonUp = QtWidgets.QPushButton(HeaderEditorDialog)
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.horizontalLayout.addWidget(self.pushButtonUp)
        self.pushButtonDown = QtWidgets.QPushButton(HeaderEditorDialog)
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.horizontalLayout.addWidget(self.pushButtonDown)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(HeaderEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(HeaderEditorDialog)
        self.buttonBox.accepted.connect(HeaderEditorDialog.accept)
        self.buttonBox.rejected.connect(HeaderEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HeaderEditorDialog)

    def retranslateUi(self, HeaderEditorDialog):
        _translate = QtCore.QCoreApplication.translate
        HeaderEditorDialog.setWindowTitle(_translate("HeaderEditorDialog", "Dialog"))
        self.treeWidgetHeaders.headerItem().setText(0, _translate("HeaderEditorDialog", "Headers"))
        self.pushButtonAddHeader.setText(_translate("HeaderEditorDialog", "Add Header"))
        self.pushButtonAddConditional.setText(_translate("HeaderEditorDialog", "Add Conditional"))
        self.pushButtonRemove.setText(_translate("HeaderEditorDialog", "Remove"))
        self.pushButtonEdit.setText(_translate("HeaderEditorDialog", "Edit"))
        self.pushButtonUp.setText(_translate("HeaderEditorDialog", "∧"))
        self.pushButtonDown.setText(_translate("HeaderEditorDialog", "∨"))

