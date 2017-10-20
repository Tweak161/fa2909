# coding: utf8
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np
import requests
from math import sqrt
import uuid
from time import gmtime, strftime

NUM_FEATURES = 5


class MyPipeline:
    def __init__(self, algorithm):
        pass
        self.algorithm = algorithm
        self.filter_list = []
        self.name = self.algorithm.get_name()
        self.pipeline = None
        self.auto_configuration = False
        self.cross_val_score = None
        self.accuracy = None
        self.pipeline_id = str(uuid.uuid4())
        self.data = None
        self.results = []

        # Initialize pipeline
        self._create_pipeline()

    def get_name(self):
        return self.name

    def get_filter(self):
        return self.filter_list

    def get_filter_list(self):
        return self.filter_list

    def add_filter(self, filter):
        """
        Function adds filter to pipeline's internal list of filters
        :param filter: (Filter) Filter
        :return:
        """
        self.filter_list.append(filter)
        self._create_pipeline()

    def remove_filter(self, index):
        """
        Removes the filter with selected index from the pipeline
        :param filter: (int) Row of Filter to be removed
        :return:
        """
        del self.filter_list[index]

    def set_data(self, data, online_analysis_active):
        """

        :param data: (dict) Dict with database values of one entry
        :param online_analysis_active:
        :return: (dict) Same dict as parm1 with added keys 'Prediction' and 'Features'
        """
        self.data = data
        if online_analysis_active:
            self._calculate()
            self.save_to_rest()
        else:
            self._calculate()
        self.results.append(data)
        return self.data

    def _calculate(self):
        """
        Function calculates Features and classifies.
        :return: (dict) Returns dict with calculated features and classification:
                        "Features": [feature1, feature2, feature3]
                        "Prediction": bald_prediction
        """
        data = self.data
        # temperature_ist = self.data['TemperatureIst']
        # temperature_soll = self.data['TemperatureSoll']
        # speed_ist = self.data['SpeedIst']
        # speed_soll =self.data['SpeedSoll']
        # force_ist = self.data['ForceIst']
        # force_soll = self.data['ForceSoll']
        # classification = self.data['Classification']

        ##############################################################################################################
        # Feature Extraction
        ##############################################################################################################
        # Calculate Feature1: RMSE Temperature
        feature1 = self._calc_rmse(data, 'TemperatureIst', 'TemperatureSoll')
        # Calculate Feature2: RMSE Force
        feature2 = self._calc_rmse(data, 'ForceIst', 'ForceSoll')
        # Calculate Feature3: RMSE Speed
        feature3 = self._calc_rmse(data, 'SpeedIst', 'SpeedSoll')

        Z = np.zeros((1, NUM_FEATURES), dtype='float64')  # Attributes
        Z[0, 0] = feature1
        Z[0, 1] = feature2
        Z[0, 2] = feature3

        prediction = self.pipeline.predict(Z)

        result = {"Features": [feature1, feature2, feature3],
                  "Prediction": prediction[0]}

        self.data.update(result)

    def train_model(self, data_list):
        """
        Trains model
        :param data: (list of dicts) Contains list of classified data entries
        :return:
        """
        num_samples = len(data_list)
        X = np.zeros((num_samples, NUM_FEATURES), dtype='float64')  # Attributes
        y = np.zeros(num_samples, dtype='float64')  # Class
        feature1_list = []
        feature2_list = []
        feature3_list = []
        class_list = []

        ##############################################################################################################
        # Feature Extraction
        ##############################################################################################################
        # Calculate Features
        for data in data_list:
            # Calculate Feature1: RMSE Temperature
            feature1 = self._calc_rmse(data, 'TemperatureIst', 'TemperatureSoll')
            feature1_list.append(feature1)
            # Calculate Feature2: RMSE Force
            feature2 = self._calc_rmse(data, 'ForceIst', 'ForceSoll')
            feature2_list.append(feature2)
            # Calculate Feature3: RMSE Speed
            feature3 = self._calc_rmse(data, 'SpeedIst', 'SpeedSoll')
            feature3_list.append(feature3)
            # Calculate Feature4: Mean Temperature
            class_list.append(int(data["Classification"]))

        X[:, 0] = feature1_list
        X[:, 1] = feature2_list
        X[:, 2] = feature3_list

        y = class_list

        # # Create train and test sets
        # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=14)

        # if self.algorithm.auto_config_on():
        #     ('print > algorithm.auto_config_on()')
        #     # Determine parameter: n_neighbors
        #     parameter_values = list(range(1, 50))  # Include 20
        #     opt_parameter = parameter_values[0]
        #     opt_parameter_score = 0
        #     for n_neighbors in parameter_values:
        #         score = np.mean(cross_val_score(self.pipeline, X, y, scoring='accuracy'))
        #         if score > opt_parameter_score:
        #             opt_parameter = n_neighbors
        #             opt_parameter_score = score
        #     n_neighbors = opt_parameter
        #     print('n_neighbors = {}'.format(n_neighbors))
        # else:
        #     parameters = self.algorithm.get_parameters()
        #     n_neighbors = parameters["n_neighbors"]
        #     metric = parameters["metric"]
        #     algorithm = parameters["algorithm"]

        self.cross_val_score = cross_val_score(self.pipeline, X, y, scoring='accuracy')
        self.pipeline.fit(X, y)
        self.accuracy = self.cross_val_score[0] * 100

        result_string = "TODO: Result String"

    def get_configuration_info(self):
        pass
        info = "######################################################################\n"
        info += "Algorithmus \n"
        info += "######################################################################\n"
        info += self.algorithm.get_configuration_info()
        info += "\n"
        if self.filter_list:
            info += "Anzahl Filter = {}\n".format(len(self.filter_list))
        for filter_nr, filter in enumerate(self.filter_list):
            info += "######################################################################\n"
            info += "Filter {}: \n".format(filter_nr+1)
            info += filter.get_configuration_info()
            info += "\n"
        return info

    def get_result_info(self):
        results = "######################################################################\n"
        results += "Results \n"
        results += "######################################################################\n"
        results += "Cross validation score: {}".format(self.cross_val_score)
        return results

    def _calc_rmse(self, data, curve1, curve2):
        """
        Function calculates the rmse between curve1 and curve2
        :param data: (dict) json of data field
        :param curve1: (str) Value of key in data dict. Must have one of the following values:
                    -"ForceSoll"
                    -"ForceIst"
                    -"TemperatureSoll"
                    -"TemperatureIst"
                    -"SpeedSoll"
                    -"SpeedIst"
        :param curve2: (str) Value of key in data dict. Must have one of the following values:
                    -"ForceSoll"
                    -"ForceIst"
                    -"TemperatureSoll"
                    -"TemperatureIst"
                    -"SpeedSoll"
                    -"SpeedIst"
        :return: (int) RMSE between 2 curves
        """
        rmse_sum = 0
        curve1 = data[curve1]['Y']
        curve2 = data[curve2]['Y']
        for index, curve1_row in enumerate(curve1):
            rmse_sum = rmse_sum + sqrt((curve1[index] - curve2[index]) ** 2)
        rmse = rmse_sum / len(curve1)

        return rmse

    def save_to_rest(self):
        """
        Saves Classification results to REST
        :return: void
        """
        try:
            url = 'http://localhost:8000/result/'
            data = {'Time': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                    'PartId': self.data["PartId"],
                    'Algorithm': "KNeighborsClassifier",
                    "Pipeline": self.pipeline_id,
                    "Filter": "MinMax",
                    "Rmse": self.accuracy,
                    "Prediction": self.data["Prediction"]}
            response = requests.post(url, json=data)
        except:
            pass
            # No Connection to REST

    def get_from_rest(self):
        """
        This function retrieves all Analysis Results saved on the REST Server and returns them as a dictionary
        :return: (dict) Analysis Results from REST
        """
        url = 'http://localhost:8000/result/'
        r = requests.get(url)
        if r.status_code == 200:        # Successfull request
            json_list = r.json()
            json_list_results = []
            for json in json_list:
                if json['Pipeline'] == self.pipeline_id:
                    json_list_results.append(json)
            return json_list_results
        else:
            return False

    ###################################################################################################################
    # Getter/Setter
    ###################################################################################################################
    def get_accuracy(self):
        if self.accuracy is None:
            return "NA"
        else:
            return str(self.accuracy)

    def get_results(self):
        """
        Function returns results of pipeline
        :return: (dict). Dict with results with keys: "Features", "Prediction", "PartId", "ForceIst",
        "ForceSoll", "SpeedIst", "SpeedSoll", "TemperatureIst", TemperatureSoll"
        """
        return self.results

    def get_junk(self):
        """
        Function calculates percentage of samples, classified with quality class 3
        :return: (int) Percentage of samples classified with classification 3
        """
        # Calculate percentage of classification 3
        counter = 0
        if self.results:
            for sample in self.results:
                if sample["Prediction"] == 3:
                    counter += 1
            junk_percentage = (counter/len(self.data))*100

            return str(junk_percentage)
        else:
            return "NA"

    def get_report(self):
        """
        Function returns Analysis Report. This Report is Displayed in the "Auswertung" Tab in the "Bericht" Text Field
        :return: (str) Formatted Analysis Report as String
        """
        pass
        no_action_flag = 1
        result = ""
        for sample in self.results:
            if sample["Prediction"] == 3:
                result += "Ueberpruefe Qualitaet von Werkstueck {} \n".format(sample["PartId"])
                no_action_flag = 0

        if no_action_flag == 1:
            result = "Keine Aktionen notwendig"
        return result

    def _create_pipeline(self):
        pass
        pipeline_list = []
        if self.filter_list:        # check if list is empty

            for index, filter in enumerate(self.filter_list):
                filter_name = 'filter{}'.format(index)
                transformation = filter.get_transformation()
                pipeline_list.append((filter_name, transformation))

        estimator_name = self.algorithm.get_name()
        estimator = self.algorithm.get_estimator()
        estimator_tuple = (estimator_name, estimator)
        pipeline_list.append(estimator_tuple)

        self.pipeline = Pipeline(pipeline_list)
