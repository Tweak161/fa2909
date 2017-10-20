# Script creates .py files from .ui (Qt Designer file format) files and .rcc (Resource XML file) files
pyuic4 views/MainWindow.ui -o views/MainWindow.py
pyuic4 views/KNeighborsClassifierDialog.ui -o views/KNeighborsClassifierDialog.py
pyuic4 views/OpenDatabaseDialog.ui -o views/OpenDatabaseDialog.py
pyuic4 views/MinMaxScalerDialog.ui -o views/MinMaxScalerDialog.py
pyuic4 views/ScalerDialog.ui -o views/ScalerDialog.py
pyuic4 views/TestAppMainWindow.ui -o views/TestAppMainWindow.py
pyuic4 views/SVMClassifierDialog.ui -o views/SVMClassifierDialog.py
pyrcc4 content/resources.qrc -o views/resources_rc.py
