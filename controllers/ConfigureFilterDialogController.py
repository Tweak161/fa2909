from PyQt4 import QtCore, QtGui, Qt

from views import SimpleKMeansDialog
from models.Algorithms import KNeighborsClassifier

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Controller(Qt.QDialog, SimpleKMeansDialog.Ui_SimpleKMeansDialog):
    def __init__(self, db):
        super(Controller, self).__init__()
        self.setupUi(self)
        # self.db = db
        # self.simpleKMeans = None
        # self.distance_measure = None
        # self.max_iterations = None
        # self.num_clusters = None
        # self.speed = None
        # self.cross_validation = None

        # ###################################################################################################################
        # Populate GUI
        # ###################################################################################################################

        # ###################################################################################################################
        # Signals
        # ###################################################################################################################
        # self.connect(self.distanceMeassureComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
        #              self.set_distance_measure)
        # QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.apply)
        # self.connect(self.buttonBox.button(QDialogButtonBox.Apply), SIGNAL("clicked()"), self.apply)
        # self.connect(self.buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

    def apply(self):
        # Following Code is executed after closing simpleKMeansDialog Window
        algo_k_means_max_iterations = self.maxIterationsLineEdit.text()
        algo_k_means_number_clusters = self.numClustersLineEdit.text()
        algo_k_means_seed = self.seedLineEdit.text()
        self.simpleKMeans = KNeighborsClassifier(algo_k_means_max_iterations, algo_k_means_number_clusters, algo_k_means_seed)
        self._set_training_data()

    def get_algorithm(self):
        """
        Returns parameterized algorithm instance
        :return:parameterized (Algorithm.SimpleKMeans) Instance of class Algorithm.SimpleKMeans with selected parameter
        """
        pass

    def set_distance_measure(self, index):
        """
        Callback Function. SimpleKMeansDialog
        This Function is exectued when the "Distanzmass" ComboBox is changed.
        It sets the value for the Distanzmass
        :return:
        """
        pass


    def _set_training_data(self):
        pass



