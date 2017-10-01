# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/ConfigureFilterDialog.ui'
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
        ConfigureFilterDialog.resize(350, 350)
        ConfigureFilterDialog.setMinimumSize(QtCore.QSize(350, 350))
        ConfigureFilterDialog.setMaximumSize(QtCore.QSize(350, 350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConfigureFilterDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ConfigureFilterDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.maxIterationsLineEdit = QtGui.QLineEdit(ConfigureFilterDialog)
        self.maxIterationsLineEdit.setObjectName(_fromUtf8("maxIterationsLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.maxIterationsLineEdit)
        self.label_3 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.numClustersLineEdit = QtGui.QLineEdit(ConfigureFilterDialog)
        self.numClustersLineEdit.setObjectName(_fromUtf8("numClustersLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.numClustersLineEdit)
        self.numClustersLineEdit_2 = QtGui.QLineEdit(ConfigureFilterDialog)
        self.numClustersLineEdit_2.setObjectName(_fromUtf8("numClustersLineEdit_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.numClustersLineEdit_2)
        self.label_4 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(ConfigureFilterDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.numClustersLineEdit_3 = QtGui.QLineEdit(ConfigureFilterDialog)
        self.numClustersLineEdit_3.setObjectName(_fromUtf8("numClustersLineEdit_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.numClustersLineEdit_3)
        self.numClustersLineEdit_4 = QtGui.QLineEdit(ConfigureFilterDialog)
        self.numClustersLineEdit_4.setObjectName(_fromUtf8("numClustersLineEdit_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.numClustersLineEdit_4)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigureFilterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_2.setBuddy(self.maxIterationsLineEdit)
        self.label_3.setBuddy(self.numClustersLineEdit)
        self.label_4.setBuddy(self.numClustersLineEdit)
        self.label_5.setBuddy(self.numClustersLineEdit)
        self.label_6.setBuddy(self.numClustersLineEdit)

        self.retranslateUi(ConfigureFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ConfigureFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ConfigureFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureFilterDialog)

    def retranslateUi(self, ConfigureFilterDialog):
        ConfigureFilterDialog.setWindowTitle(_translate("ConfigureFilterDialog", "MinMaxScaler - Parametrisierung", None))
        self.label_2.setText(_translate("ConfigureFilterDialog", "Min", None))
        self.label_3.setText(_translate("ConfigureFilterDialog", "Scale", None))
        self.label_4.setText(_translate("ConfigureFilterDialog", "Range", None))
        self.label_5.setText(_translate("ConfigureFilterDialog", "Data_Min", None))
        self.label_6.setText(_translate("ConfigureFilterDialog", "Data_Max", None))

import resources_rc
