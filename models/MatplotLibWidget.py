from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from PyQt4 import QtGui, QtCore
import random


class MplCanvas(Canvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        Canvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.mouse_init()
        self.axes.autoscale(enable=True, tight=None)

        self.setParent(parent)

        Canvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                             QtGui.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)
        self.data = None
        # self.sca = self.axes.scatter([12000, 12000, 22000], [22000, 33000, 33000])
        self.sca = self.axes.scatter(0, 0 , c='b')
        self.axes.add_artist(self.sca)
        self.sca.set_visible(False)


class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)

    def set_data(self, data):
        """
        Add classified sample to plot
        :return:
        """
        self.data = data
        self._update_figure()

    def get_figure(self):
        pass
        return self.fig

    def get_q_image(self):
        """
        Returns a QImage
        :return: (QImage) Returns QImage of plot.
        """
        size = self.size()
        width, height = size.width(), size.height()
        im = QtGui.QImage(self.buffer_rgba(), width, height, QImage.Format_ARGB32)
        return im

    def _update_figure(self):
        # self.sca.set_visible(False)
        # self.sca = self.axes.scatter([random.randint(0, 10000), random.randint(0, 10000), random.randint(0, 10000)],
        #                              [random.randint(0, 10000), random.randint(0, 10000), random.randint(0, 10000)])
        # self.draw()

        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        f1 = []
        f2 = []
        f3 = []
        prediction = []
        for sample in self.data:
            features = sample["Features"]
            f1.append(features[0])
            f2.append(features[1])
            f3.append(features[2])
            if sample["Prediction"] == 1:
                prediction.append('g')
            if sample["Prediction"] == 2:
                prediction.append('r')
            if sample["Prediction"] == 3:
                prediction.append('b')

        self.sca.set_visible(False)
        self.sca = self.axes.scatter(f1, f2, f3, c=prediction)
        self.draw()

        self.axes.set_xlabel('F1 - RMSE Temperatur')
        self.axes.set_ylabel('F2 - RMSE Kraft')
        self.axes.set_zlabel('F3 - RMSE Geschwindigkeit')



        # self.
        # for sample in self.data:
        #     feature1, feature2, feature3, feature4 = self.data["Features"]
        #     prediction = self.data["Prediction"]
        # # l = [random.randint(0, 10) for i in range(4)]
        # # self.axes.cla()
        # # self.axes.plot([0, 1, 2, 3], l, 'r')
        # # self.draw()
        # # self.axes

