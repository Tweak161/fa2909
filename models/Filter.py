class Filter(object):
    def __init__(self):
        self.name = None
        pass

    def __str__(self):
        return self.name

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
        self.norm = 1       # Normalize all values to self.norm
        self.std = 2        # Filter all values with standard deviation greater than self.std