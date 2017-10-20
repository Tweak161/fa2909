from PyQt4 import QtCore, QtGui, Qt

from views import KNeighborsClassifierDialog
from models.Algorithms import KNeighborsAlgorithm

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Controller(Qt.QDialog, KNeighborsClassifierDialog.Ui_KNeighborsClassifierDialog):
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)
        self.algorithm = None
        self.distance_measure = None

        # ###################################################################################################################
        # Populate GUI
        # ###################################################################################################################
        self.distanceMeassureComboBox.addItem('cityblock')
        self.distanceMeassureComboBox.addItem('cosine')
        self.distanceMeassureComboBox.addItem('euclidean')
        self.distanceMeassureComboBox.addItem('l1')
        self.distanceMeassureComboBox.addItem('l2')
        self.distanceMeassureComboBox.addItem('manhatten')

        self.chooseAlgorithmComboBox.addItem('auto')
        self.chooseAlgorithmComboBox.addItem('ball_tree')
        self.chooseAlgorithmComboBox.addItem('kd_tree')
        self.chooseAlgorithmComboBox.addItem('brute')

        # ###################################################################################################################
        # Signals
        # ###################################################################################################################
        self.connect(self.distanceMeassureComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.set_distance_measure)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.apply)

    def apply(self):
        # Following Code is executed after closing KNeighborsClassifierDialog Window
        if self.numNeighborsLineEdit.text() == "":
            n_neighbors = 3       # Default Value
        else:
            n_neighbors = int(self.numNeighborsLineEdit.text())
        metric = str(self.distanceMeassureComboBox.currentText())
        if self.leafSizeLineEdit.text() == "":
            leaf_size = 30          # Default value
        else:
            leaf_size = int(self.leafSizeLineEdit.text())
        algorithm = str(self.chooseAlgorithmComboBox.currentText())
        self.algorithm = KNeighborsAlgorithm(n_neighbors, metric, algorithm, leaf_size)

    def get_algorithm(self):
        """
        Returns parameterized algorithm instance
        :return:parameterized (Algorithm.SimpleKMeans) Instance of class Algorithm.SimpleKMeans with selected parameter
        """
        return self.algorithm

    def set_distance_measure(self, index):
        """
        Callback Function. SimpleKMeansDialog
        This Function is exectued when the "Distanzmass" ComboBox is changed.
        It sets the value for the Distanzmass
        :return:
        """
        self.distance_measure = self.distanceMeassureComboBox.itemText(index)


