from random import seed
from random import random, uniform
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

NUM_FEATURES = 4

class Generator(object):
    """
    Class generates training and test data
    """
    def __init__(self):
        super(Generator, self).__init__()
        pass

    # def random_walk(self):
    #     pass
    #     seed(1)
    #     random_walk = list()
    #     random_walk.append(-1 if random() < 0.5 else 1)
    #     for i in range(1, 1000):
    #         movement = -1 if random() < 0.5 else 1
    #         value = random_walk[i - 1] + movement
    #         random_walk.append(value)
    #     plt.plot(random_walk)
    #     plt.show()

    def _generate_force(self):
        # Ist curve 1 > Random generator
        dev_time = 0  # deviation on time axis
        dev_value = 10  # deviation on values axis

        x_soll = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400]
        y_soll = [5, 20,  30,  40,  45,  20,  10,  7,   4,   0,   0,    0,    0,    0,    0]

        x_val_ist = []
        y_val_ist = []

        for index, value in enumerate(x_soll):
            pass
            if index == 1:
                x_val_ist.append(0)
                y_val_ist.append(0)
            else:
                x_val_ist.append(value + uniform(-dev_time, dev_time))
                y_val_ist.append(y_soll[index] + uniform(-dev_value, dev_value))

        fit_soll = np.poly1d(np.polyfit(x_val_ist, y_val_ist, 4))

        x_ist = list(range(0, 1300, 10))
        y_ist = []
        for x_val in x_ist:
            if fit_soll(x_val) > 0:
                y_ist.append(fit_soll(x_val))
            else:
                y_ist.append(0)

        # Soll curve
        dev_time = 200  # deviation on time axis
        dev_value = 10  # deviation on values axis

        x_val_ist = []
        y_val_ist = []

        for index, value in enumerate(x_soll):
            if index == 1:
                x_val_ist.append(0)
                y_val_ist.append(0)
            else:
                x_val_ist.append(value + uniform(-dev_time, dev_time))
                y_val_ist.append(y_soll[index] + uniform(-dev_value, dev_value))

        fit_ist = np.poly1d(np.polyfit(x_val_ist, y_val_ist, 5))

        x_soll = list(range(0, 1300, 10))
        y_soll = []
        for x_val in x_soll:
            if fit_ist(x_val) > 0:
                y_soll.append(fit_ist(x_val))
            else:
                y_soll.append(0)

        # # Ist curve 2 > Add Random Walk to soll
        # seed(1)
        # y_ist = []
        # walk_steps = 0.5
        # random_walk = list()
        # random_walk.append(-1 if random() < 0.5 else 1)
        # for y_soll_val in y_soll:
        #     movement = -walk_steps if random() < 0.5 else walk_steps
        #     y_ist_val = y_soll_val + movement
        #     y_ist.append(y_ist_val)

        result = {'ForceIst': {
            'X': x_ist,
            'Y': y_ist
             },
            'ForceSoll': {
                'X': x_soll,
                'Y': y_soll
            }
        }

        return result

    def _generate_temperature(self):
        """
        Generates a temperature curve of the warmup process. Temperature roughly behaves as T = xt+c
        :return:
        """
        pass
        x_soll = list(range(0, 100, 5))      # Warmup process lasts 100s, temp meassurements every 5 seconds
        f_soll = uniform(700, 900)          # Finish Temperature
        m = (f_soll-25)/100
        c = 25              # Starting Temperature

        y_soll = []
        for x in x_soll:
            y_soll_val = m*x + c
            y_soll.append(y_soll_val)

        f_ist = f_soll - uniform(-50, 50)
        m = (f_ist - 25) / 100
        x_ist = x_soll

        y_ist = []
        for x in x_ist:
            y_ist_val = m * x + c
            y_ist_val = y_ist_val + np.random.normal(0, 4)      # Add noise
            y_ist.append(y_ist_val)

        result = {'TemperatureSoll': {
            'X': x_soll,
            'Y': y_soll
             },
            'TemperatureIst': {
                'X': x_ist,
                'Y': y_ist
            }
        }

        return result

    def _generate_speed(self):
        """
        Generates speed Soll und Ist curve. Soll curve is given, Ist curve is randomly generated and deviates sligthly
        from Soll curve
        :return:
        """
        pass
        x_soll = list(range(0, 1500, 10))     # Sample Periode 10ms
        y_soll = []
        f = 10.0          # final speed
        rise_time = 500.0
        constant_time = 1000
        m = f/rise_time       # slope

        for x in x_soll:
            if x <= rise_time:                          # rising speed
                y_soll_val = m * x
            elif rise_time < x <= constant_time:         # constant speed
                y_soll_val = m*rise_time
            else:                     # no speed > finished
                y_soll_val = 0
            y_soll.append(y_soll_val)
        x_ist = list(range(0, 1500, 10))     # Sample Periode 10ms
        y_ist = []
        f = uniform(9, 11)  # final speed
        rise_time = uniform(460, 540)
        constant_time = uniform(940, 1060)
        m = f / rise_time  # slope

        for x in x_ist:
            if x <= rise_time:  # rising speed
                y_ist_val = m * x
            elif rise_time < x <= constant_time:  # constant speed
                y_ist_val = m * rise_time
            else:  # no speed > finished
                y_ist_val = 0
            y_ist_val = y_ist_val + np.random.normal(-0.5, 0.5)  # Noise
            y_ist.append(y_ist_val)

        result = {'SpeedSoll': {
            'X': x_soll,
            'Y': y_soll
             },
            'SpeedIst': {
                'X': x_ist,
                'Y': y_ist
            }
        }

        return result

    def generate_data(self):
        """
        Returns randomly generated simulated plant data.
        :return:
        """
        generated_data = {}
        force = self._generate_force()
        speed = self._generate_speed()
        temperature = self._generate_temperature()
        generated_data['Classification'] = "NAN"                 # Only training data has classification
        generated_data.update(force)
        generated_data.update(speed)
        generated_data.update(temperature)

        return generated_data

    def generate_test_data(self):
        """
        Returns randomly generated simulated plant data.
        :return: (dict) {   ForceIst:     (list of floats)
                            ForceSoll:    (list of floats)
                        }
        """
        test_data = self.generate_data()
        return test_data

    def generate_training_data(self):
        """
        Returns randomly generated simulated plant data, similar to the generate_test_data() function.
        However, in comparision to generate_data(), this function also classifies the data in accordance with
        predefined rules
        :return: (dict) {   ForceIst:     (list of floats)
                            ForceSoll:    (list of floats)
                            Classification:     (int)
                        }
        """
        generated_data = self.generate_data()
        classification_score = self._calc_classification_value(generated_data, 'ForceSoll', 'ForceIst')
        classification_score += self._calc_classification_value(generated_data, 'SpeedSoll', 'SpeedIst')
        classification_score += self._calc_classification_value(generated_data, 'TemperatureSoll', 'TemperatureIst')

        if classification_score <= 3:
            classification = 1
        elif classification_score <= 6:
            classification = 2
        else:
            classification = 3

        # Add classification to generated data
        generated_data['Classification'] = classification

        return generated_data

        pass

    def _calc_classification_value(self, generated_data, curve_ist, curve_soll):
        # Calculate Gaussian Distribution of RMSE for 100 generated datasets
        rmse_distribution = []
        for i in range(1, 100):
            rmse_sum = 0
            force_soll = generated_data[curve_ist]['Y']
            force_ist = generated_data[curve_soll]['Y']
            for index, force_s in enumerate(force_soll):
                rmse_sum = rmse_sum + sqrt((force_soll[index] - force_ist[index]) ** 2)
            rmse = rmse_sum / len(force_soll)
            rmse_distribution.append(rmse)
        rmse_distribution_std = np.std(rmse_distribution)
        rmse_distribution_mean = np.mean(rmse_distribution)

        if (rmse_distribution_mean + 0.5 * rmse_distribution_std) < abs(rmse):
            classification = 4  # Bad Quality > quality class 3
        elif (rmse_distribution_mean + 0.25 * rmse_distribution_std) < abs(rmse):
            classification = 2  # Mediocre Quality > quality class 2
        else:
            classification = 1  # Good Quality > quality class 1

        # Add classification to generated data
        generated_data['Classification'] = classification

        return classification

    def plot_generated_data(self):
        """
        This function plots and prints randomly generated plant data.
        :return:
        """

        training_data = self.generate_training_data()
        training_data = self.generate_training_data()
        test_data = self.generate_test_data()

        # Plot1: Force
        fig = plt.figure(1)
        ax1 = fig.add_subplot(311)
        plt1 = ax1.plot(training_data['ForceIst']['X'], training_data['ForceIst']['Y'], '.r',
                        label="Ist Kraft")
        plt1 = ax1.plot(training_data['ForceSoll']['X'], training_data['ForceSoll']['Y'], '.g',
                        label="Soll Kraft")
        plt.xlabel('Time [ms]')
        plt.ylabel('Kraft [kN]')
        # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax1.legend(['Kraft Ist', 'Kraft Soll'])

        # Plot2: Temperature
        # fig = plt.figure()
        ax2 = fig.add_subplot(312)
        plt2 = ax2.plot(training_data['TemperatureIst']['X'], training_data['TemperatureIst']['Y'], '.-r',
                        label="Ist Temperatur")
        plt2 = ax2.plot(training_data['TemperatureSoll']['X'], training_data['TemperatureSoll']['Y'], '.-g',
                        label="Soll Temperatur")
        plt.xlabel('Time [ms]')
        plt.ylabel('Temperatur [Grad C]')
        # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax2.legend(['Temperatur Ist', 'Temperatur Soll'])

        # Plot3: Speed
        # fig = plt.figure()
        ax3 = fig.add_subplot(313)
        plt3 = ax3.plot(training_data['SpeedIst']['X'], training_data['SpeedIst']['Y'], '.-r',
                        label="Ist Geschwindigkeit")
        plt3 = ax3.plot(training_data['SpeedSoll']['X'], training_data['SpeedSoll']['Y'], '.-g',
                        label="Soll Geschwindigkeit")
        plt.xlabel('Time [ms]')
        plt.ylabel('Geschwindigkeit [m/s]')
        # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax3.legend(['Geschwindigkeit Ist', 'Geschwindigkeit Soll'])

        plt.show()


