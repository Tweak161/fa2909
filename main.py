import sys

from PyQt4.QtGui import *

from controllers import MainWindowController

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = MainWindowController.MainWindowClass()
    form.show()
    app.exec_()
