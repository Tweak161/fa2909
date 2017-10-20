from PyQt4 import QtCore, QtGui, Qt

from views import ScalerDialog

from sklearn.preprocessing import StandardScaler
from models import Filter

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Controller(Qt.QDialog,ScalerDialog.Ui_ScalerDialog):
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)
        self.transformation = None
        self.filter = None
        self.with_mean = True
        self.with_variance = True

        # QButtons
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.apply)

        # QComboBox
        self.connect(self.meanComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.set_mean)
        self.connect(self.varianceComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.set_variance)

    def apply(self):
        # Create Transformation object
        self.transformation = StandardScaler(copy=True, with_mean=self.with_mean, with_std=self.with_variance)
        # Create Filter object
        self.filter = Filter.Scaler()
        self.filter.set_transformation(self.transformation)
        info = "Filter - {} \n".format("StandardScaler")
        info += "Zentrieren auf Mittel = {}\n".format(self.with_mean)
        info += "Skalierung um Einheits Varianz = {}\n".format(self.with_variance)
        self.filter.set_configuration_info(info)

    def get_filter(self):
        """
        Returns parameterized filter object
        :return:parameterized (MinMaxScaler) Instance of class Filter.SimpleKMeans with selected parameter
        """
        return self.filter

    def set_variance(self, index):
        text = str(self.varianceComboBox.itemText(index))
        if text == 'Ja':
            self.with_variance = True
        else:
            self.with_variance = False

    def set_mean(self, index):
        text = str(self.meanComboBox.itemText(index))
        if text == 'Ja':
            self.with_mean = True
        else:
            self.with_mean = False


