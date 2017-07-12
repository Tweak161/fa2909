# Script creates .py files from .ui (Qt Designer file format) files and .rcc (Resource XML file) files
pyuic4 MainWindow.ui -o MainWindow.py
pyuic4 SimpleKMeansDialog.ui -o SimpleKMeansDialog.py
pyuic4 OpenDatabaseDialog.ui -o OpenDatabaseDialog.py
pyuic4 ConfigureFilterDialog.ui -o ConfigureFilterDialog.py
pyrcc4 resources.qrc -o resources_rc.py
