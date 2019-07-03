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
        qRefItemEditDialog.resize(504, 177)
        qRefItemEditDialog.setWindowTitle("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(qRefItemEditDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.qModeCheckBox = QtWidgets.QCheckBox(qRefItemEditDialog)
        self.qModeCheckBox.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.qModeCheckBox.setFont(font)
        self.qModeCheckBox.setObjectName("qModeCheckBox")
        self.verticalLayout_2.addWidget(self.qModeCheckBox)
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.qOkToolButton = QtWidgets.QToolButton(qRefItemEditDialog)
        self.qOkToolButton.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.qOkToolButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/gtk_apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qOkToolButton.setIcon(icon)
        self.qOkToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qOkToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.qOkToolButton.setObjectName("qOkToolButton")
        self.horizontalLayout_2.addWidget(self.qOkToolButton)
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
        self.horizontalLayout_2.addWidget(self.qCancelToolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(qRefItemEditDialog)
        self.qCancelToolButton.clicked.connect(qRefItemEditDialog.reject)
        self.qOkToolButton.clicked.connect(qRefItemEditDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(qRefItemEditDialog)

    def retranslateUi(self, qRefItemEditDialog):
        _translate = QtCore.QCoreApplication.translate
        self.qModeCheckBox.setText(_translate("qRefItemEditDialog", "Режим изменения"))
        self.label.setText(_translate("qRefItemEditDialog", "Наименование"))
        self.qOkToolButton.setText(_translate("qRefItemEditDialog", "   Принять"))
        self.qCancelToolButton.setText(_translate("qRefItemEditDialog", "   Отмена"))


from tpylib import tpylib_rc
