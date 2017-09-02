# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/KNeighborsClassifierDialog.ui'
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

class Ui_KNeighborsClassifierDialog(object):
    def setupUi(self, KNeighborsClassifierDialog):
        KNeighborsClassifierDialog.setObjectName(_fromUtf8("KNeighborsClassifierDialog"))
        KNeighborsClassifierDialog.resize(300, 350)
        KNeighborsClassifierDialog.setMinimumSize(QtCore.QSize(300, 350))
        KNeighborsClassifierDialog.setMaximumSize(QtCore.QSize(300, 350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        KNeighborsClassifierDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(KNeighborsClassifierDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_7 = QtGui.QLabel(KNeighborsClassifierDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.autoFitParameterCheckBox = QtGui.QCheckBox(KNeighborsClassifierDialog)
        self.autoFitParameterCheckBox.setText(_fromUtf8(""))
        self.autoFitParameterCheckBox.setObjectName(_fromUtf8("autoFitParameterCheckBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.autoFitParameterCheckBox)
        self.label = QtGui.QLabel(KNeighborsClassifierDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.distanceMeassureComboBox = QtGui.QComboBox(KNeighborsClassifierDialog)
        self.distanceMeassureComboBox.setObjectName(_fromUtf8("distanceMeassureComboBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.distanceMeassureComboBox)
        self.numNeighborsLineEdit = QtGui.QLineEdit(KNeighborsClassifierDialog)
        self.numNeighborsLineEdit.setObjectName(_fromUtf8("numNeighborsLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.numNeighborsLineEdit)
        self.label_5 = QtGui.QLabel(KNeighborsClassifierDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.chooseClassAttributComboBox = QtGui.QComboBox(KNeighborsClassifierDialog)
        self.chooseClassAttributComboBox.setObjectName(_fromUtf8("chooseClassAttributComboBox"))
        self.chooseClassAttributComboBox.addItem(_fromUtf8(""))
        self.chooseClassAttributComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.chooseClassAttributComboBox)
        self.label_6 = QtGui.QLabel(KNeighborsClassifierDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.chooseAlgorithmComboBox = QtGui.QComboBox(KNeighborsClassifierDialog)
        self.chooseAlgorithmComboBox.setObjectName(_fromUtf8("chooseAlgorithmComboBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.chooseAlgorithmComboBox)
        self.label_2 = QtGui.QLabel(KNeighborsClassifierDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(KNeighborsClassifierDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_3)
        self.leafSizeLineEdit = QtGui.QLineEdit(KNeighborsClassifierDialog)
        self.leafSizeLineEdit.setObjectName(_fromUtf8("leafSizeLineEdit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.leafSizeLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(KNeighborsClassifierDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label.setBuddy(self.distanceMeassureComboBox)
        self.label_5.setBuddy(self.chooseClassAttributComboBox)
        self.label_2.setBuddy(self.numNeighborsLineEdit)

        self.retranslateUi(KNeighborsClassifierDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), KNeighborsClassifierDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), KNeighborsClassifierDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(KNeighborsClassifierDialog)

    def retranslateUi(self, KNeighborsClassifierDialog):
        KNeighborsClassifierDialog.setWindowTitle(_translate("KNeighborsClassifierDialog", "Dialog", None))
        self.label_7.setText(_translate("KNeighborsClassifierDialog", "Autofit Parameter", None))
        self.label.setText(_translate("KNeighborsClassifierDialog", "&Distanzmaß", None))
        self.label_5.setText(_translate("KNeighborsClassifierDialog", "&Cross Validation", None))
        self.chooseClassAttributComboBox.setItemText(0, _translate("KNeighborsClassifierDialog", "True", None))
        self.chooseClassAttributComboBox.setItemText(1, _translate("KNeighborsClassifierDialog", "False", None))
        self.label_6.setText(_translate("KNeighborsClassifierDialog", "Algorithmus", None))
        self.label_2.setText(_translate("KNeighborsClassifierDialog", "&Anzahl Nachbarn", None))
        self.label_3.setText(_translate("KNeighborsClassifierDialog", "Leaf Size", None))

import resources_rc
