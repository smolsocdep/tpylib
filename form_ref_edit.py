# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_ref_edit.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_qRefItemEditDialog(object):
    def setupUi(self, qRefItemEditDialog):
        qRefItemEditDialog.setObjectName("qRefItemEditDialog")
        qRefItemEditDialog.setWindowModality(QtCore.Qt.WindowModal)
        qRefItemEditDialog.resize(504, 134)
        qRefItemEditDialog.setWindowTitle("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(qRefItemEditDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(qRefItemEditDialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.qRefItemLineEdit = QtWidgets.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.qRefItemLineEdit.setFont(font)
        self.qRefItemLineEdit.setObjectName("qRefItemLineEdit")
        self.verticalLayout.addWidget(self.qRefItemLineEdit)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.qCancelToolButton_2 = QtWidgets.QToolButton(qRefItemEditDialog)
        self.qCancelToolButton_2.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.qCancelToolButton_2.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/gtk_apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qCancelToolButton_2.setIcon(icon)
        self.qCancelToolButton_2.setIconSize(QtCore.QSize(22, 22))
        self.qCancelToolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.qCancelToolButton_2.setObjectName("qCancelToolButton_2")
        self.horizontalLayout.addWidget(self.qCancelToolButton_2)
        self.qCancelToolButton = QtWidgets.QToolButton(qRefItemEditDialog)
        self.qCancelToolButton.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.qCancelToolButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pixmaps/icons/gtk_cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qCancelToolButton.setIcon(icon1)
        self.qCancelToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qCancelToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.qCancelToolButton.setObjectName("qCancelToolButton")
        self.horizontalLayout.addWidget(self.qCancelToolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(qRefItemEditDialog)
        self.qCancelToolButton.clicked.connect(qRefItemEditDialog.reject)
        self.qCancelToolButton_2.clicked.connect(qRefItemEditDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(qRefItemEditDialog)

    def retranslateUi(self, qRefItemEditDialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("qRefItemEditDialog", "Наименование"))
        self.qCancelToolButton_2.setText(_translate("qRefItemEditDialog", "   Принять"))
        self.qCancelToolButton.setText(_translate("qRefItemEditDialog", "   Отмена"))


from tpylib import tpylib_rc
