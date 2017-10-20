# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/ScalerDialog.ui'
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

class Ui_ScalerDialog(object):
    def setupUi(self, ScalerDialog):
        ScalerDialog.setObjectName(_fromUtf8("ScalerDialog"))
        ScalerDialog.resize(250, 250)
        ScalerDialog.setMinimumSize(QtCore.QSize(250, 250))
        ScalerDialog.setMaximumSize(QtCore.QSize(250, 250))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MainWindowIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ScalerDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ScalerDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_5 = QtGui.QLabel(ScalerDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        spacerItem = QtGui.QSpacerItem(17, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.meanComboBox = QtGui.QComboBox(ScalerDialog)
        self.meanComboBox.setMinimumSize(QtCore.QSize(80, 0))
        self.meanComboBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.meanComboBox.setObjectName(_fromUtf8("meanComboBox"))
        self.meanComboBox.addItem(_fromUtf8(""))
        self.meanComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.meanComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_6 = QtGui.QLabel(ScalerDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        spacerItem1 = QtGui.QSpacerItem(17, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.varianceComboBox = QtGui.QComboBox(ScalerDialog)
        self.varianceComboBox.setMinimumSize(QtCore.QSize(80, 0))
        self.varianceComboBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.varianceComboBox.setObjectName(_fromUtf8("varianceComboBox"))
        self.varianceComboBox.addItem(_fromUtf8(""))
        self.varianceComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.varianceComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(ScalerDialog)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(ScalerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ScalerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ScalerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ScalerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ScalerDialog)

    def retranslateUi(self, ScalerDialog):
        ScalerDialog.setWindowTitle(_translate("ScalerDialog", "Scaler - Parametrisierung", None))
        self.label_5.setText(_translate("ScalerDialog", "Zentrieren", None))
        self.meanComboBox.setItemText(0, _translate("ScalerDialog", "Ja", None))
        self.meanComboBox.setItemText(1, _translate("ScalerDialog", "Nein", None))
        self.label_6.setText(_translate("ScalerDialog", "Einheits Varianz", None))
        self.varianceComboBox.setItemText(0, _translate("ScalerDialog", "Ja", None))
        self.varianceComboBox.setItemText(1, _translate("ScalerDialog", "Nein", None))
        self.label_2.setText(_translate("ScalerDialog", "Alle Features werden  um den Mittelwert bereiningt und auf die Varianz skaliert.", None))

import resources_rc
