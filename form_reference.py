# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_reference.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_qReferenceMainWindow(object):
    def setupUi(self, qReferenceMainWindow):
        qReferenceMainWindow.setObjectName("qReferenceMainWindow")
        qReferenceMainWindow.resize(648, 490)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(qReferenceMainWindow.sizePolicy().hasHeightForWidth())
        qReferenceMainWindow.setSizePolicy(sizePolicy)
        qReferenceMainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(qReferenceMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.qAddToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qAddToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qAddToolButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qAddToolButton.setIcon(icon)
        self.qAddToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qAddToolButton.setObjectName("qAddToolButton")
        self.horizontalLayout.addWidget(self.qAddToolButton)
        self.qEditToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qEditToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qEditToolButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pixmaps/icons/accessories-text-editor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qEditToolButton.setIcon(icon1)
        self.qEditToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qEditToolButton.setObjectName("qEditToolButton")
        self.horizontalLayout.addWidget(self.qEditToolButton)
        self.qDeleteToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qDeleteToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qDeleteToolButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pixmaps/icons/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qDeleteToolButton.setIcon(icon2)
        self.qDeleteToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qDeleteToolButton.setObjectName("qDeleteToolButton")
        self.horizontalLayout.addWidget(self.qDeleteToolButton)
        self.line = QtWidgets.QFrame(self.frame_2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.qTrashToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qTrashToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qTrashToolButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pixmaps/icons/user-trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qTrashToolButton.setIcon(icon3)
        self.qTrashToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qTrashToolButton.setObjectName("qTrashToolButton")
        self.horizontalLayout.addWidget(self.qTrashToolButton)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.qFilterLineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.qFilterLineEdit.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        self.qFilterLineEdit.setFont(font)
        self.qFilterLineEdit.setText("")
        self.qFilterLineEdit.setObjectName("qFilterLineEdit")
        self.horizontalLayout.addWidget(self.qFilterLineEdit)
        self.qFilterToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qFilterToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qFilterToolButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pixmaps/icons/view-filter_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qFilterToolButton.setIcon(icon4)
        self.qFilterToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qFilterToolButton.setObjectName("qFilterToolButton")
        self.horizontalLayout.addWidget(self.qFilterToolButton)
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.qAcceptToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qAcceptToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qAcceptToolButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/pixmaps/icons/gtk_apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qAcceptToolButton.setIcon(icon5)
        self.qAcceptToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qAcceptToolButton.setObjectName("qAcceptToolButton")
        self.horizontalLayout.addWidget(self.qAcceptToolButton)
        self.qRejectToolButton = QtWidgets.QToolButton(self.frame_2)
        self.qRejectToolButton.setMinimumSize(QtCore.QSize(26, 26))
        self.qRejectToolButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/pixmaps/icons/gtk_cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qRejectToolButton.setIcon(icon6)
        self.qRejectToolButton.setIconSize(QtCore.QSize(22, 22))
        self.qRejectToolButton.setObjectName("qRejectToolButton")
        self.horizontalLayout.addWidget(self.qRejectToolButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame_2)
        self.qReferenceTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.qReferenceTableWidget.setObjectName("qReferenceTableWidget")
        self.qReferenceTableWidget.setColumnCount(0)
        self.qReferenceTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.qReferenceTableWidget)
        qReferenceMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(qReferenceMainWindow)
        self.statusbar.setObjectName("statusbar")
        qReferenceMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(qReferenceMainWindow)
        QtCore.QMetaObject.connectSlotsByName(qReferenceMainWindow)

    def retranslateUi(self, qReferenceMainWindow):
        _translate = QtCore.QCoreApplication.translate
        qReferenceMainWindow.setWindowTitle(_translate("qReferenceMainWindow", "MainWindow"))
        self.qAddToolButton.setToolTip(_translate("qReferenceMainWindow", "Добавить элемент справочника"))
        self.qAddToolButton.setStatusTip(_translate("qReferenceMainWindow", "Добавить элемент справочника"))
        self.qEditToolButton.setToolTip(_translate("qReferenceMainWindow", "Изменить элемент справочника"))
        self.qEditToolButton.setStatusTip(_translate("qReferenceMainWindow", "Изменить элемент справочника"))
        self.qDeleteToolButton.setToolTip(_translate("qReferenceMainWindow", "Удалить элемент справочника"))
        self.qDeleteToolButton.setStatusTip(_translate("qReferenceMainWindow", "Удалить элемент справочника"))
        self.qTrashToolButton.setToolTip(_translate("qReferenceMainWindow", "Корзина"))
        self.qTrashToolButton.setStatusTip(_translate("qReferenceMainWindow", "Корзина"))
        self.qFilterLineEdit.setPlaceholderText(_translate("qReferenceMainWindow", "Наименование"))
        self.qFilterToolButton.setToolTip(_translate("qReferenceMainWindow", "Фильтр"))
        self.qFilterToolButton.setStatusTip(_translate("qReferenceMainWindow", "Фильтр"))
        self.qAcceptToolButton.setToolTip(_translate("qReferenceMainWindow", "Принять"))
        self.qAcceptToolButton.setStatusTip(_translate("qReferenceMainWindow", "Принять"))
        self.qRejectToolButton.setToolTip(_translate("qReferenceMainWindow", "Отмена"))
        self.qRejectToolButton.setStatusTip(_translate("qReferenceMainWindow", "Отмена"))


import tpylint_rc
