class Filter(object):
    def __init__(self):
        self.name = None
        self.transformation = None

    def __str__(self):
        return self.name

    def set_transformation(self, transformation):
        self.transformation = transformation

    def get_transformation(self):
        return self.transformation

    def get_name(self):
        """
        Function returns filter's name
        :return:
        """
        return self.name

    def get_info(self):
        pass

    def get_configuration_info(self):
        info = "Filter - {} \n".format(self.name)
        return info

class MinMaxFilter(Filter):
    def __init__(self):
        super(MinMaxFilter, self).__init__()
        self.name = "MinMaxFilter"
        self.feature_range = None       # Normalize all values to self.norm

    def get_configuration_info(self):
        info = "Filter - {} \n".format(self.name)
        info += "Range = {}".format(self.feature_range)
        return info

    def set_feature_range(self, feature_range):
        self.feature_range = feature_range

class MeanFilter(Filter):
    def __init__(self):
        super(MeanFilter, self).__init__()



