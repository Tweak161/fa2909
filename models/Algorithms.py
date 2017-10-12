from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from matplotlib import pyplot as plt
import numpy as np
# from django.db import models

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets


class Algorithm(object):
    def __init__(self):
        super(Algorithm, self).__init__()
        self.name = "DefaultAlgorithmName"
        self.data_component1 = None
        self.auto_config = False
        self.estimator = None

    def get_estimator(self):
        """
        Returns estimator
        :return: (sklearn.Estimator)
        """
        return self.estimator

    def get_name(self):
        """
        Function returns the name of the algorithm/class as a string
        :return: (str) name of algorithm
        """
        return self.name

    def auto_config_on(self):
        if self.auto_config is True:
            return True
        else:
            return False

    def set_auto_config(self, autoconfig):
        self.auto_config = autoconfig

    def set_data(self, data):
        self.data_component1 = data
        self.calculate()

    def calculate(self):
        """
        Calculate
        Must be reimplemented for every subclass
        :return:
        """
        pass

    def return_parameters(self):
        pass

class Cluster(Algorithm):
    def __init__(self):
        super(Cluster, self).__init__()


class KNeighborsAlgorithm(Cluster):
    """
    This class implements a KNeighborsClassifier Classifier
    """
    def __init__(self, n_neighbors=3, metric='euclidean', algorithm='auto', leaf_size=30):
        super(KNeighborsAlgorithm, self).__init__()
        # User definable parameters
        self.name = "KNeighborsClassifier"
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.cross_validation = True

        self.parameters = {"n_neighbors": self.n_neighbors,
                           "metric": self.metric,
                           "algorithm": self.algorithm,
                           "leaf_size": self.leaf_size,
                           "cross_validation": self.cross_validation
                           }
        self.estimator = KNeighborsClassifier(n_neighbors=self.n_neighbors, metric=self.metric,
                                              algorithm=self.algorithm, leaf_size=self.leaf_size, )

        # Attributes
        self.X = None
        self.Y = None
        self.accuracy = None

        # Filter DEBUG: Erstelle Filter Klasse
        self.filter_list = []
        # self.filter_type = "MinMax Filter"
        # self.filter_norm = 1
        # self.filter_std = 2

    def get_parameters(self):
        return self.parameters

    def set_attributes(self, x):
        """
        Set Attributes. Attributes are saved as class attributes
        :param X: (numpy array) Attributes as numpy array. Rows are samples. Columns are attributes
        :return:
        """
        self.X = x

    def set_class(self, y):
        """
        Set Class attributes. Class attributes
        :param Y: (numpy array) Class Attribute as numpy array. Rows are samples. Columns are class attributes
        :return:
        """
        self.Y = y

    def train_model(self):
        """
        Local Function. Splits attributes and class samples into training and test datasets
        :return:
        """
        self.X = np.zeros((351, 34), dtype='float')
        self.Y = np.zeros((351,), dtype='bool')

        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, random_state=14)
        estimator = KNeighborsAlgorithm()
        estimator.fit(X_train, Y_train)

        if self.cross_validation is False:
            Y_predicted = estimator.predict(X_test)
            accuracy = np.mean(Y_test == Y_predicted) * 100

            self.accuracy = accuracy
        else:
            scores = cross_val_score(estimator, self.X, self.Y, scoring='accuracy')
            self.accuracy = np.mean(scores) * 100

        # Test number of nearest neighbours
        avg_scores = []
        all_scores = []
        parameter_values = list(range(1, 21))  # Include 20
        for n_neighbors in parameter_values:
            estimator = KNeighborsAlgorithm(n_neighbors=n_neighbors)
            scores = cross_val_score(estimator, self.X, self.Y, scoring='accuracy')
            avg_scores.append(np.mean(scores))
            all_scores.append(scores)

        # Plot num_neighbours vs. model_quality
        plt.plot(parameter_values, avg_scores, '-o')

        # Filter/
        X_broken = np.array(self.X)
        X_broken[:, ::2] /= 10
        X_transformed = MinMaxScaler().fit_transform(X_broken)
        estimator = KNeighborsAlgorithm()
        transformed_scores = cross_val_score(estimator, X_transformed, self.Y, scoring='accuracy')

        # Create a pipeline
        scaling_pipeline = Pipeline([('scale', MinMaxScaler()), ('predict', KNeighborsAlgorithm())])
        scores = cross_val_score(scaling_pipeline, X_broken, self.Y, scoring='accuracy')

    def get_configuration_info(self):
        """
        This function returns information about selected algorithm and selected parameters
        :return: (str) Returns selected algorithm and selected parameters as string
        """
        pass
        algo_info = "Algorithmus - {}\n".format(self.name)
        algo_info += "\n"
        algo_info += "Parameter\n"
        for parameter_key in self.parameters:
            algo_info += "{}: {} \n".format(parameter_key, self.parameters[parameter_key])
        return algo_info

    # def get_filter_parameters(self):
    #     """
    #     This function returns information about selected filter and selected parameters
    #     :return: (str) Returns selected filter and selected parameters as string
    #     """
    #     for filter in self.filter_list:
    #         filter_info = filter.get_info()
    #         filter_info += "\n"
    #     return filter_info

    def get_result(self):
        """
        This function returns the result of the Algorithm
        :return: (str) Returns result of algorithm
        """

        algo_results = "Ergebnisse\n"
        algo_results += "Number of iterations: 7"
        algo_results += "Within cluster sum of squared errors: 62.1436882815797"
        algo_results += "\n"
        algo_results += "Attribute                Full Data               0               1"
        algo_results += "                             (150)           (100)            (50)"
        algo_results += "==================================================================\n"
        algo_results += "sepallength                 5.8433           6.262           5.006\n"
        algo_results += "sepalwidth                   3.054           2.872           3.418\n"
        algo_results += "petallength                 3.7587           4.906           1.464\n"
        algo_results += "petalwidth                  1.1987           1.676           0.244\n"
        algo_results += "class                  Iris-setosa Iris-versicolor     Iris-setosa\n"
        return algo_results

    def plot_result(self):
        """
        Function plots result. It returns a instance of MatplotLibCanvas
        :return:
        """
        np.random.seed(5)

        centers = [[1, 1], [-1, -1], [1, -1]]
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target

        estimators = {'k_means_iris_3': KMeans(n_clusters=3),
                      'k_means_iris_8': KMeans(n_clusters=8),
                      'k_means_iris_bad_init': KMeans(n_clusters=3, n_init=1,
                                                      init='random')}

        fignum = 1
        for name, est in estimators.items():
            fig = plt.figure(fignum, figsize=(4, 3))
            plt.clf()
            ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

            plt.cla()
            est.fit(X)
            labels = est.labels_

            ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=labels.astype(np.float))

            ax.w_xaxis.set_ticklabels([])
            ax.w_yaxis.set_ticklabels([])
            ax.w_zaxis.set_ticklabels([])
            ax.set_xlabel('Petal width')
            ax.set_ylabel('Sepal length')
            ax.set_zlabel('Petal length')
            fignum = fignum + 1

        # Plot the ground truth
        fig = plt.figure(fignum, figsize=(4, 3))
        plt.clf()
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

        plt.cla()

        for name, label in [('Setosa', 0),
                            ('Versicolour', 1),
                            ('Virginica', 2)]:
            ax.text3D(X[y == label, 3].mean(),
                      X[y == label, 0].mean() + 1.5,
                      X[y == label, 2].mean(), name,
                      horizontalalignment='center',
                      bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
        # Reorder the labels to have colors matching the cluster results
        y = np.choose(y, [1, 2, 0]).astype(np.float)
        ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y)

        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        ax.set_xlabel('Petal width')
        ax.set_ylabel('Sepal length')
        ax.set_zlabel('Petal length')
        plt.show()

