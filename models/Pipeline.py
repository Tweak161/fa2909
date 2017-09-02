from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import numpy as np
import requests
import random


class MyPipeline:
    def __init__(self, algorithm):
        pass
        self.algorithm = algorithm
        self.filter_list = []
        self.name = self.algorithm.get_name()
        self.data = None
        self.pipeline = Pipeline([
            ('filter', MinMaxScaler()),
            ('algorithm', KNeighborsClassifier())
        ])
        self.auto_configuration = False
        self.cross_val_score = None

    def print_results(self):
        pass

    def get_result_text(self):
        pass

    def get_result_plots(self):
        pass

    def get_name(self):
        return self.name

    def get_filter(self):
        return self.filter_list

    def get_filter_list(self):
        return self.filter_list

    def add_filter(self, filter):
        self.filter_list.append(filter)

    def remove_filter(self, index):
        """

        :param filter: (int) Index of Object
        :return:
        """
        del self.filter_list[index]

    def set_data(self, data, online_analysis_active):
        self.data = data
        if online_analysis_active:
            self.calculate()
            self.save_to_rest()
        else:
            self.calculate()

    def calculate(self):
        sepal_length = self.data['sepal_length']
        sepal_width = self.data['sepal_width']
        petal_length = self.data['petal_length']
        petal_width = self.data['petal_width']
        species = self.data['species']


        num_attributes = 4
        num_samples = len(sepal_length)

        X = np.zeros((num_samples, num_attributes), dtype='float64')          # Attributes
        y = np.zeros(num_samples, dtype='float64')          # Class

        X[:, 0] = sepal_length
        X[:, 1] = sepal_width
        X[:, 2] = petal_length
        X[:, 3] = petal_width

        for index, spe in enumerate(species):
            if spe == "setosa":
                y[index] = 1
            elif spe == "versicolor":
                y[index] = 2
            elif spe == "virginica":
                y[index] = 3

        # Create train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 14)

        if self.algorithm.auto_config_on():
            pass
            # Determine parameter: n_neighbors
            parameter_values = list(range(1, 50))  # Include 20
            opt_parameter = parameter_values[0]
            opt_parameter_score = 0
            for n_neighbors in parameter_values:
                estimator = KNeighborsClassifier(n_neighbors=n_neighbors)
                score = cross_val_score(estimator, X, y, scoring='accuracy')
                if score > opt_parameter_score:
                    opt_parameter = n_neighbors
                    opt_parameter_score = score
            n_neighbors = opt_parameter
        else:
            parameters= self.algorithm.get_parameters()
            n_neighbors = parameters["n_neighbors"]
            metric = parameters["metric"]
            algorithm = parameters["algorithm"]

        estimator = KNeighborsClassifier(n_neighbors=n_neighbors, metric=metric, algorithm=algorithm)

        self.cross_val_score = cross_val_score(estimator, X, y, scoring='accuracy')

        print("RMSE calculate = {}".format(self.cross_val_score))

        result_string = "TODO: Result String"

    def get_configuration_info(self):
        pass
        info = "######################################################################\n"
        info += "Algorithmus \n"
        info += "######################################################################\n"
        info += self.algorithm.get_configuration_info()
        info += "\n"
        for filter_nr, filter in enumerate(self.filter_list):
            info += "######################################################################\n"
            info += "Filter {} \n".format(filter_nr)
            info += "######################################################################\n"
            info += filter.get_configuration_info()
            info += "\n"
        return info

    def get_result_info(self):
        results = "######################################################################\n"
        results += "Results \n"
        results += "######################################################################\n"
        results += "Cross validation score: {}".format(self.cross_val_score)
        return results

    def save_to_rest(self):
        pass

        url = 'http://localhost:8000/result/'
        # response = requests.get(url)
        # print("response = {}".format(response))
        # print("response.json() = {}".format(response.json()))

        cross_val_score = self.cross_val_score *100
        print("RMSE save_to_rest = {}".format(self.cross_val_score))
        print("POST Results")
        data = {'Time': 100,
                'PartId': 1,
                'ComponentId': 1,
                'Algorithm': "KNeighborsClassifier",
                "Pipeline": "2",
                "Filter": "MinMax",
                "Rmse": random.uniform(80, 95)}    # random.uniform(80, 95)

        response = requests.post(url, json=data)





