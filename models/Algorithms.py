from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.svm.libsvm import decision_function


class Algorithm(object):
    def __init__(self):
        super(Algorithm, self).__init__()
        self.name = "DefaultAlgorithmName"
        self.data_component1 = None
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

    def get_parameters(self):
        return self.parameters

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


class SVMAlgorithm(Cluster):
    """
    This class implements a KNeighborsClassifier Classifier
    """
    def __init__(self, penalty=1.0, degree=3, kernel='rbf', decision_function_shape='ovo'):
        super(SVMAlgorithm, self).__init__()
        # User definable parameters
        self.name = "SVMClassifier"

        self.parameters = {"C (Penalty Parameter des Error Terms)": penalty,
                           "degree": degree,
                           "kernel": kernel,
                           "decision_function_shape": decision_function_shape
                           }

        self.estimator = SVC(C=penalty, degree=degree, kernel=kernel, decision_function_shape=decision_function_shape)

    #     # Attributes
    #     self.X = None
    #     self.Y = None
    #     self.accuracy = None
    #
    def get_parameters(self):
        return self.parameters

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