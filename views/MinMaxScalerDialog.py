# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/MinMaxScalerDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MinMaxScalerDialog(object):
    def setupUi(self, MinMaxScalerDialog):
        MinMaxScalerDialog.setObjectName(_fromUtf8("MinMaxScalerDialog"))
        MinMaxScalerDialog.resize(250, 250)
        MinMaxScalerDialog.setMinimumSize(QtCore.QSize(250, 250))
        MinMaxScalerDialog.setMaximumSize(QtCore.QSize(250, 250))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MinMaxScalerDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MinMaxScalerDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(MinMaxScalerDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_5 = QtGui.QLabel(MinMaxScalerDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        spacerItem = QtGui.QSpacerItem(17, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dataMinLineEdit = QtGui.QLineEdit(MinMaxScalerDialog)
        self.dataMinLineEdit.setMinimumSize(QtCore.QSize(90, 0))
        self.dataMinLineEdit.setMaximumSize(QtCore.QSize(90, 16777215))
        self.dataMinLineEdit.setObjectName(_fromUtf8("dataMinLineEdit"))
        self.horizontalLayout.addWidget(self.dataMinLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_6 = QtGui.QLabel(MinMaxScalerDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        spacerItem1 = QtGui.QSpacerItem(17, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.dataMaxLineEdit = QtGui.QLineEdit(MinMaxScalerDialog)
        self.dataMaxLineEdit.setMinimumSize(QtCore.QSize(90, 0))
        self.dataMaxLineEdit.setMaximumSize(QtCore.QSize(90, 16777215))
        self.dataMaxLineEdit.setObjectName(_fromUtf8("dataMaxLineEdit"))
        self.horizontalLayout_2.addWidget(self.dataMaxLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(MinMaxScalerDialog)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(MinMaxScalerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(MinMaxScalerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MinMaxScalerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MinMaxScalerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MinMaxScalerDialog)
        MinMaxScalerDialog.setTabOrder(self.dataMinLineEdit, self.dataMaxLineEdit)
        MinMaxScalerDialog.setTabOrder(self.dataMaxLineEdit, self.buttonBox)

    def retranslateUi(self, MinMaxScalerDialog):
        MinMaxScalerDialog.setWindowTitle(_translate("MinMaxScalerDialog", "MinMaxScaler - Parametrisierung", None))
        self.label.setText(_translate("MinMaxScalerDialog", "Range", None))
        self.label_5.setText(_translate("MinMaxScalerDialog", "Min", None))
        self.label_6.setText(_translate("MinMaxScalerDialog", "Max", None))
        self.label_2.setText(_translate("MinMaxScalerDialog", "Alle Features werden auf den Wertebereich, welcher durch die Parameter Min und Max gegeben ist skaliert.", None))

import resources_rc
