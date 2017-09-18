import sys

from PyQt4.QtGui import *

from models import DatabaseTest
from models import Generator

if __name__ == '__main__':

    app = QApplication(sys.argv)

    generator = Generator.Generator()

    generator.plot_generated_data()



