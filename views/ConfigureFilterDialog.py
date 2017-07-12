# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConfigureFilterDialog.ui'
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

class Ui_ConfigureFilterDialog(object):
    def setupUi(self, ConfigureFilterDialog):
        ConfigureFilterDialog.setObjectName(_fromUtf8("ConfigureFilterDialog"))
        ConfigureFilterDialog.resize(300, 350)
        ConfigureFilterDialog.setMinimumSize(QtCore.QSize(300, 350))
        ConfigureFilterDialog.setMaximumSize(QtCore.QSize(300, 350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConfigureFilterDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ConfigureFilterDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.maxIterationsLineEdit = QtGui.QLineEdit(ConfigureFilterDialog)
        self.maxIterationsLineEdit.setObjectName(_fromUtf8("maxIterationsLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.maxIterationsLineEdit)
        self.label_3 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.numClustersLineEdit = QtGui.QLineEdit(ConfigureFilterDialog)
        self.numClustersLineEdit.setObjectName(_fromUtf8("numClustersLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.numClustersLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigureFilterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_2.setBuddy(self.maxIterationsLineEdit)
        self.label_3.setBuddy(self.numClustersLineEdit)

        self.retranslateUi(ConfigureFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ConfigureFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ConfigureFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureFilterDialog)

    def retranslateUi(self, ConfigureFilterDialog):
        ConfigureFilterDialog.setWindowTitle(_translate("ConfigureFilterDialog", "Dialog", None))
        self.label_2.setText(_translate("ConfigureFilterDialog", "Standard Abweichung", None))
        self.label_3.setText(_translate("ConfigureFilterDialog", "Normalisierung", None))

import resources_rc
