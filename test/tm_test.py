import Database
from PyQt4.QtGui import *
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)

    database_connection = Database.DatabaseConnection('fa2909', 'fa2909', 'localhost', '0000')

    # database_connection.simulate_logging()
    database_connection.start_logging_simulation(1)

    # Infinite loop
    while True:
        pass

