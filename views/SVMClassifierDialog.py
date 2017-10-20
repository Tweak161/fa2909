# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/SVMClassifierDialog.ui'
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

class Ui_SVMClassifierDialog(object):
    def setupUi(self, SVMClassifierDialog):
        SVMClassifierDialog.setObjectName(_fromUtf8("SVMClassifierDialog"))
        SVMClassifierDialog.resize(308, 250)
        SVMClassifierDialog.setMinimumSize(QtCore.QSize(308, 250))
        SVMClassifierDialog.setMaximumSize(QtCore.QSize(308, 250))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SVMClassifierDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SVMClassifierDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(SVMClassifierDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.kernelComboBox = QtGui.QComboBox(SVMClassifierDialog)
        self.kernelComboBox.setObjectName(_fromUtf8("kernelComboBox"))
        self.gridLayout.addWidget(self.kernelComboBox, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(SVMClassifierDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.decisionFunctionShapeComboBox = QtGui.QComboBox(SVMClassifierDialog)
        self.decisionFunctionShapeComboBox.setObjectName(_fromUtf8("decisionFunctionShapeComboBox"))
        self.gridLayout.addWidget(self.decisionFunctionShapeComboBox, 1, 1, 1, 1)
        self.label = QtGui.QLabel(SVMClassifierDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.degreeLineEdit = QtGui.QLineEdit(SVMClassifierDialog)
        self.degreeLineEdit.setObjectName(_fromUtf8("degreeLineEdit"))
        self.gridLayout.addWidget(self.degreeLineEdit, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(SVMClassifierDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.penaltyLineEdit = QtGui.QLineEdit(SVMClassifierDialog)
        self.penaltyLineEdit.setObjectName(_fromUtf8("penaltyLineEdit"))
        self.gridLayout.addWidget(self.penaltyLineEdit, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(SVMClassifierDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SVMClassifierDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SVMClassifierDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SVMClassifierDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SVMClassifierDialog)

    def retranslateUi(self, SVMClassifierDialog):
        SVMClassifierDialog.setWindowTitle(_translate("SVMClassifierDialog", "SVM Classifier - Parametrisierung", None))
        self.label_4.setText(_translate("SVMClassifierDialog", "Kernel", None))
        self.label_5.setText(_translate("SVMClassifierDialog", "Decision Function", None))
        self.label.setText(_translate("SVMClassifierDialog", "Degree", None))
        self.label_2.setText(_translate("SVMClassifierDialog", "Penalty Parameter", None))

import resources_rc
