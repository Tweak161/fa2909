import sys

from PyQt4.QtGui import *

from controllers import TestMainWindowController

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = TestMainWindowController.MainWindowClass()
    form.show()
    app.exec_()
