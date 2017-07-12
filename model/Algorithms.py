from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from matplotlib import pyplot as plt
import numpy as np


class Cluster:
    pass


class SimleKMeans(Cluster):
    """
    This class implements a SimpleKMeans Cluster Analasys
    """
    def __init__(self, max_iterations=10, number_clusters=2, seed=12):
        # User definable parameters
        self.distance_measure = None
        self.algo_k_means_max_iterations = max_iterations
        self.algo_k_means_number_clusters = number_clusters
        self.algo_k_means_seed = seed
        self.cross_validation = True

        # Attributes
        self.X = None
        self.Y = None
        self.accuracy = None

        # Filter DEBUG: Erstelle Filter Klasse
        self.filter_type = "MinMax Filter"
        self.filter_norm = 1
        self.filter_std = 2

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
        estimator = KNeighborsClassifier()
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
            estimator = KNeighborsClassifier(n_neighbors=n_neighbors)
            scores = cross_val_score(estimator, self.X, self.Y, scoring='accuracy')
            avg_scores.append(np.mean(scores))
            all_scores.append(scores)

        # Plot num_neighbours vs. model_quality
        plt.plot(parameter_values, avg_scores, '-o')

        # Filter/
        X_broken = np.array(self.X)
        X_broken[:, ::2] /= 10
        X_transformed = MinMaxScaler().fit_transform(X_broken)
        estimator = KNeighborsClassifier()
        transformed_scores = cross_val_score(estimator, X_transformed, self.Y, scoring='accuracy')
        print("The average accuracy for is {0: .1f} % ".format(np.mean(transformed_scores) * 100))

        # Create a pipeline
        scaling_pipeline = Pipeline([('scale', MinMaxScaler()), ('predict', KNeighborsClassifier())])
        scores = cross_val_score(scaling_pipeline, X_broken, self.Y, scoring='accuracy')
        print("The pipeline scored an average accuracy for is {0:.1f}%".format(np.mean(transformed_scores) * 100))

    def get_accuracy(self):
        """
        This Function returns the accuracy of the model
        :return: (int) Accuracy of model
        """
        return self.accuracy

    def get_algorithm_parameters(self):
        """
        This function returns information about selected algorithm and selected parameters
        :return: (str) Returns selected algorithm and selected parameters as string
        """
        pass
        algo_info = "Angewandter Algorithmus: {}\n".format("Simple K Means")
        algo_info += "\n"
        algo_info += "Parameter\n"
        algo_info += "{}{}\n".format("Max Anzahl an Iterationen = ", self.algo_k_means_max_iterations)
        algo_info += "{}{}\n".format("Max Anzahl an Clustern = ", self.algo_k_means_number_clusters)
        algo_info += "{}{}\n".format("Seed = ", self.algo_k_means_seed)
        algo_info += "{}{}\n".format("Cross Validation = ", self.cross_validation)
        return algo_info

    def get_filter_parameters(self):
        """
        This function returns information about selected filter and selected parameters
        :return: (str) Returns selected filter and selected parameters as string
        """
        filter_info = "Angewandter Filter: {}\n".format(self.filter_type)
        filter_info += "\n"
        filter_info += "Parameter"
        filter_info += "{}{}\n".format("Normalisierung = ", self.filter_norm)
        filter_info += "{}{}\n".format("Standardabweichung = ", self.filter_std)
        return filter_info

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



