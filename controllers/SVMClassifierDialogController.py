from PyQt4 import QtCore, QtGui, Qt

from views import SVMClassifierDialog
from models.Algorithms import SVMAlgorithm

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Controller(Qt.QDialog, SVMClassifierDialog.Ui_SVMClassifierDialog):
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)
        self.algorithm = None
        self.decision_function_shape = 'ovo'
        self.kernel = 'rbf'

        # ###################################################################################################################
        # Populate GUI
        # ###################################################################################################################
        self.kernelComboBox.addItem('linear')
        self.kernelComboBox.addItem('poly')
        self.kernelComboBox.addItem('rbf')
        self.kernelComboBox.addItem('sigmoid')
        self.kernelComboBox.addItem('precomputed')
        self.kernelComboBox.addItem('callable')

        self.decisionFunctionShapeComboBox.addItem('ovo')
        self.decisionFunctionShapeComboBox.addItem('ovr')

        # ###################################################################################################################
        # Signals
        # ###################################################################################################################
        self.connect(self.decisionFunctionShapeComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.set_decision_function_shape)
        self.connect(self.kernelComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.set_kernel)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.apply)

    def apply(self):
        # Following Code is executed after closing KNeighborsClassifierDialog Window
        if self.degreeLineEdit.text() != '':
            degree = int(self.degreeLineEdit.text())
        else:
            degree = 3          # Default
        if self.penaltyLineEdit.text() != '':
            penalty = int(self.penaltyLineEdit.text())
        else:
            penalty = 1.0       # Default
        self.algorithm = SVMAlgorithm(penalty, degree, self.kernel, self.decision_function_shape)

    def get_algorithm(self):
        """
        Returns parameterized algorithm instance
        :return:parameterized (Algorithm.SVM) Instance of class Algorithm.SVM with selected parameter
        """
        return self.algorithm

    def set_decision_function_shape(self, index):
        self.decision_function_shape = str(self.decisionFunctionShapeComboBox.itemText(index))

    def set_kernel(self, index):
        self.kernel = str(self.kernelComboBox.itemText(index))


