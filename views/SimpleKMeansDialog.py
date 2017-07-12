# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SimpleKMeansDialog.ui'
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

class Ui_SimpleKMeansDialog(object):
    def setupUi(self, SimpleKMeansDialog):
        SimpleKMeansDialog.setObjectName(_fromUtf8("SimpleKMeansDialog"))
        SimpleKMeansDialog.resize(300, 350)
        SimpleKMeansDialog.setMinimumSize(QtCore.QSize(300, 350))
        SimpleKMeansDialog.setMaximumSize(QtCore.QSize(300, 350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SimpleKMeansDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SimpleKMeansDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(SimpleKMeansDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.distanceMeassureComboBox = QtGui.QComboBox(SimpleKMeansDialog)
        self.distanceMeassureComboBox.setObjectName(_fromUtf8("distanceMeassureComboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.distanceMeassureComboBox)
        self.label_2 = QtGui.QLabel(SimpleKMeansDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.maxIterationsLineEdit = QtGui.QLineEdit(SimpleKMeansDialog)
        self.maxIterationsLineEdit.setObjectName(_fromUtf8("maxIterationsLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.maxIterationsLineEdit)
        self.label_3 = QtGui.QLabel(SimpleKMeansDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.numClustersLineEdit = QtGui.QLineEdit(SimpleKMeansDialog)
        self.numClustersLineEdit.setObjectName(_fromUtf8("numClustersLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.numClustersLineEdit)
        self.label_4 = QtGui.QLabel(SimpleKMeansDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.seedLineEdit = QtGui.QLineEdit(SimpleKMeansDialog)
        self.seedLineEdit.setObjectName(_fromUtf8("seedLineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.seedLineEdit)
        self.label_5 = QtGui.QLabel(SimpleKMeansDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.chooseClassAttributComboBox = QtGui.QComboBox(SimpleKMeansDialog)
        self.chooseClassAttributComboBox.setObjectName(_fromUtf8("chooseClassAttributComboBox"))
        self.chooseClassAttributComboBox.addItem(_fromUtf8(""))
        self.chooseClassAttributComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.chooseClassAttributComboBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(SimpleKMeansDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label.setBuddy(self.distanceMeassureComboBox)
        self.label_2.setBuddy(self.maxIterationsLineEdit)
        self.label_3.setBuddy(self.numClustersLineEdit)
        self.label_4.setBuddy(self.seedLineEdit)
        self.label_5.setBuddy(self.chooseClassAttributComboBox)

        self.retranslateUi(SimpleKMeansDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SimpleKMeansDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SimpleKMeansDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SimpleKMeansDialog)

    def retranslateUi(self, SimpleKMeansDialog):
        SimpleKMeansDialog.setWindowTitle(_translate("SimpleKMeansDialog", "Dialog", None))
        self.label.setText(_translate("SimpleKMeansDialog", "&Distanzmaß", None))
        self.label_2.setText(_translate("SimpleKMeansDialog", "&Max Iterationen", None))
        self.label_3.setText(_translate("SimpleKMeansDialog", "&Anzahl Cluster", None))
        self.label_4.setText(_translate("SimpleKMeansDialog", "&Seed", None))
        self.label_5.setText(_translate("SimpleKMeansDialog", "&Cross Validation", None))
        self.chooseClassAttributComboBox.setItemText(0, _translate("SimpleKMeansDialog", "True", None))
        self.chooseClassAttributComboBox.setItemText(1, _translate("SimpleKMeansDialog", "False", None))

import resources_rc
