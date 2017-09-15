import Database
from PyQt4.QtGui import *
import sys
import Generator
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':

    app = QApplication(sys.argv)

    database_connection = Database.DatabaseConnection('fa2909', 'fa2909', 'localhost', '0000')

    generator = Generator.Generator()

    generator.plot_generated_data()

    database_connection.start_logging_simulation(1)



