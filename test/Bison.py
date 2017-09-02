import bson
import json
from random import randint
from random import uniform
import pickle
import math


class Bison:

    def create_lidar_message(self):
        randint(0, 3)
        # message = {"Segments": [None,
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         None,
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30),
        #                         randint(0, 30)],
        #            "Timestamp": 0}
        message = {"Segments": [1000,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                2000],
                   "Timestamp": 0}
        message_json = json.dumps(message)

        return message_json

    def create_sorted_message(self):
        pass

        message ={
                "MapLeftLimits": {"x": [0, 0, 5, 5, 10, 15, 15, 20],
                                  "y": [5, 10, 15, 20, 20, 25, 25, 30]},  # [x1, y1, x2, y2, ...]
                "MapRightLimits": {"x": [5, 5, 10, 10, 15, 20, 20, 25],
                                   "y": [5, 10, 15, 20, 20, 25, 25, 30]}
                 }


        message_json = json.dumps(message)

        return message_json

    def create_ldc_message(self):
        pass
        # message = {"CurrentLap": 0,
        #            "Trajectory":
        #                [
        #                    {"v": 5,
        #                     "x": 1,
        #                     "y": 1
        #                     },
        #                    {"v": 15,
        #                     "x": 2.0,
        #                     "y": 2.0
        #                     },
        #                    {"v": 25,
        #                     "x": 3.0,
        #                     "y": 3.0
        #                     },
        #                    {"v": 35,
        #                     "x": 4.0,
        #                     "y": 3.0
        #                     },
        #                    {"v": 45,
        #                     "x": 5.0,
        #                     "y": 3.0
        #                     },
        #                    {"v": 55,
        #                     "x": 6.0,
        #                     "y": 3.0
        #                     },
        #                    {"v": 65,
        #                     "x": 6.0,
        #                     "y": 4.0
        #                     },
        #                    {"v": 75,
        #                     "x": 6.0,
        #                     "y": 5.0
        #                     },
        #                    {"v": 85,
        #                     "x": 6.0,
        #                     "y": 6.0
        #                     },
        #                    {"v": 95,
        #                     "x": 6.0,
        #                     "y": 7.0
        #                     },
        #                    {"v": 105,
        #                     "x": 7.0,
        #                     "y": 7.0
        #                     },
        #                 ]
        #            }
        x = []
        y = []
        v = []
        trajectories = []
        for i in range(0, 10000):
            x = randint(-200,200)
            y = randint(-200,200)
            v = randint(0,120)
            trajectories.append({
                                "v": v,
                                "x": x,
                                "y": y
                                })
        message = {"CurrentLap": 0,
                   "Trajectory": trajectories
                   }

        message_json = json.dumps(message)

        return message_json

    def create_sdcparameter_position_orientation_message(self):

        # Create dict for transformation to JSON/BSON
        message = {
            "LatProp": randint(-20, 20),
            "LatDeri": randint(-20, 20),
            "LatLp": randint(-20, 20),
            "LongProp": randint(-20, 20),
            "LongDeri": randint(-20, 20),
            "RateLimSteering": randint(-20, 20)
        }

        message_json = json.dumps(message)

        return message_json

    def create_slam_position_orientation_message(self):
        x_car = randint(-20, 20)
        y_car = randint(-20, 20)
        theta_car = uniform(0, 2 * math.pi)

        # Create dict for transformation to JSON/BSON
        message = {
            "car_pos": [x_car, y_car, theta_car],
        }

        message_json = json.dumps(message)

        return message_json

    def create_slam_message(self):
        """
        Creates dummy SLAM data with
        :return: (json)
        """
        # Create 500 cones
        cones = []

        for index in range(1, 30):
            x = randint(-20, 20)
            y = randint(-20, 20)
            color = randint(0, 5)
            cid = randint(0, 500)

            cones.append(x)
            cones.append(y)
            cones.append(color)
            cones.append(cid)

        x_car = randint(-20, 20)
        y_car = randint(-20, 20)
        theta_car = uniform(0, 2*math.pi)

        # Create dict for transformation to JSON/BSON
        slam_message = {
            "car_pos": [x_car, y_car, theta_car],
            "cones_pos": cones
        }

        # slam_message = {
        #     "car_pos": [0, 0, math.pi/4],
        #     "cones_pos": [0, 10, 1, 1000,
        #                   10, 0, 2, 1000,
        #                   0, 200, 3, 1000,
        #                   200, 0, 4, 1000]
        # }

        # Convert dict to JSON
        slam_message_json = json.dumps(slam_message)

        return slam_message_json


    def create_cv_message(self):
        """
        Creates random dummy computer vision data
        :return: (json)
        """
        # Create 20 cones
        cones = []
        cones_dict = {}
        # Create dict for transformation to JSON/BSON
        # cv_message = {
        #     "Cones": [
        #         {"Type": ctype,
        #          "Angle": theta,
        #          "CameraId": cid,
        #          "Distance": distance1
        #          }
        #     ]
        # }
        cv_message = {
            "Cones": []
        }

        # for index in range(0, 20):
        #     theta = uniform(0, math.pi/4)
        #     distance1 = randint(0, 20)
        #     ctype = randint(0, 5)
        #     cid = randint(0, 6)
        #
        #     cones_dict = {"Type": ctype,
        #                  "Angle": theta,
        #                  "CameraId": cid,
        #                  "Distance": distance1
        #                  }
        #     cv_message["Cones"].append(cones_dict)

        cone1_dict = {"Type": 0,
                          "Angle": 0,
                          "CameraId": 1,
                          "Distance": 5}
        cv_message["Cones"].append(cone1_dict)
        cone2_dict = {"Type": 1,
                      "Angle": -math.pi/4,
                      "CameraId": 1,
                      "Distance": 10}
        cv_message["Cones"].append(cone2_dict)
        cone3_dict = {"Type": 2,
                      "Angle": math.pi/4,
                      "CameraId": 1,
                      "Distance": 15}
        cv_message["Cones"].append(cone3_dict)
        cone4_dict = {"Type": 3,
                      "Angle": math.pi / 2,
                      "CameraId": 1,
                      "Distance": 20}
        cv_message["Cones"].append(cone4_dict)
        cone5_dict = {"Type": 4,
                      "Angle": math.pi,
                      "CameraId": 1,
                      "Distance": 25}
        cv_message["Cones"].append(cone5_dict)


        # Convert dict to JSON
        cv_message_json = json.dumps(cv_message)

        return cv_message_json

    def read_json(self, filename):
        """
        Reads in json file and returns dict object.
        :param filename: Filename of input json file
        :return:
        """
        f = open(filename, "r")
        json_data = f.read()
        json_dict = json.loads(json_data)
        return json_dict

    def read_bson(self, filename):
        f = open(filename, "rb")
        bson_data = f.read()
        message_dict = bson.loads(bson_data)
        print(message_dict)

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)



