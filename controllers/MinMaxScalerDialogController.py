from PyQt4 import QtCore, QtGui, Qt

from views import MinMaxScalerDialog

from sklearn.preprocessing import MinMaxScaler
from models import Filter

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Controller(Qt.QDialog,MinMaxScalerDialog.Ui_MinMaxScalerDialog):
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)
        self.transformation = None
        self.filter = None

        # QButtons
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.apply)

    def apply(self):
        pass
        # Following Code is executed after closing KNeighborsClassifierDialog Window
        if self.dataMinLineEdit.text() == '':
            data_min = 0        # default value
        else:
            data_min = int(self.dataMinLineEdit.text())
        if self.dataMaxLineEdit.text() == '':
            data_max = 1        # default value
        else:
            data_max = int(self.dataMaxLineEdit.text())

        feature_range = (data_min, data_max)
        # Create Transformation object
        self.transformation = MinMaxScaler(feature_range=feature_range)
        # Create Filter object
        self.filter = Filter.MinMaxFilter()
        self.filter.set_transformation(self.transformation)
        self.filter.set_feature_range(feature_range)

    def get_filter(self):
        """
        Returns parameterized filter object
        :return:parameterized (MinMaxScaler) Instance of class Filter.SimpleKMeans with selected parameter
        """
        return self.filter
