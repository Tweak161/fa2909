import sys  # Access command line

from views import TestAppMainWindow
from views import OpenDatabaseDialog

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from models.DatabaseTest import DatabaseConnection
import os
from models import Generator

class MainWindowClass(QMainWindow, TestAppMainWindow.Ui_TestAppMainWindow):

    def __init__(self):
        super(MainWindowClass, self).__init__()
        self.setupUi(self)
        self.db = DatabaseConnection()
        self.generator = Generator.Generator()

        # #############################################################################################################
        # Initialize Timers
        # #############################################################################################################
        self.logging_timer = QTimer(self)
        self.logging_timer.timeout.connect(self.logging_timer_cb)

        self.data_generation_timer = QTimer(self)
        self.data_generation_timer.timeout.connect(self.data_generation_cb)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_timer_cb)
        self.refresh_timer.start(500)

        # #############################################################################################################
        # Initialize Dialogs
        # #############################################################################################################
        self.openDatabaseDialog = QDialog()
        self.openDatabaseDialog.ui = OpenDatabaseDialog.Ui_Dialog()
        self.openDatabaseDialog.ui.setupUi(self.openDatabaseDialog)

        # ###################################################################################################################
        # Signals
        # ###################################################################################################################
        # QButton
        self.connect(self.connectToDatabasePushButton, SIGNAL("clicked()"), self.action_open_new_database)
        self.connect(self.startLoggingPushButton, SIGNAL("clicked()"), self.start_stop_logging)
        self.connect(self.startTrainingDataGenerationPushButton, SIGNAL("clicked()"),
                     self.start_training_data_generation)
        self.connect(self.deleteDatabasePushButton, SIGNAL("clicked()"), self.delete_database)
        self.connect(self.clearRestPushButton, SIGNAL("clicked()"), self.clear_rest)
        self.connect(self.plotPushButton, SIGNAL("clicked()"), self.plot_trainings_data)
        self.connect(self.createTablePushButton, SIGNAL("clicked()"), self.create_table)

    def start_stop_logging(self):
        if self.logging_timer.isActive():
            self.logging_timer.stop()
            self.loggingActiveLabel.setStyleSheet("QLabel { background-color : red}")
            self.startLoggingPushButton.setText('Starte Logging Simulation')
        else:
            self.logging_timer.start()
            self.loggingActiveLabel.setStyleSheet("QLabel { background-color : green}")
            self.startLoggingPushButton.setText('Stoppe Logging Simulation')

    def logging_timer_cb(self):
        logging_info = self.db.simulate_logging()
        self.plainTextEdit.setPlainText(logging_info)

    def data_generation_cb(self):
        info = self.db.generate_training_data()
        self.plainTextEdit.setPlainText(info)

    def refresh_timer_cb(self):
        """
        Refresh the GUI.
        :return:
        """
        if self.db:
            if self.db.is_connected():
                self.connectionActiveLabel.setStyleSheet("QLabel { background-color : green}")
            else:
                self.connectionActiveLabel.setStyleSheet("QLabel { background-color : red}")

    def start_training_data_generation(self):
        if self.data_generation_timer.isActive():
            self.data_generation_timer.stop()
            self.trainingDataGenerationActiveLabel.setStyleSheet("QLabel { background-color : red}")
            self.startTrainingDataGenerationPushButton.setText('Starte Trainingsdaten Generierung')
        else:
            self.data_generation_timer.start()
            self.trainingDataGenerationActiveLabel.setStyleSheet("QLabel { background-color : green}")
            self.startTrainingDataGenerationPushButton.setText('Stoppe Trainingsdaten Generierung')

    def delete_database(self):
        info = self.db.clear_table('data')
        self.plainTextEdit.setPlainText(info)

    def clear_rest(self):
        rest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'REST', 'mysite', 'manage.py')
        run_rest_cmd = 'python ' + rest_path + ' flush --no-input'
        os.system(run_rest_cmd)

    def action_open_new_database(self):
        """
        This Callback function gets triggered when user executes the newDatabase-Action.
        This can happen either through the Menu, the Toolbar or the Hotkey "Strg + N".
        A Dialog is opened where a new Database-Connection can be established
        :return:
        """
        # dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # Set default dialog Values
        self.openDatabaseDialog.ui.hostLineEdit.setText('localhost')
        self.openDatabaseDialog.ui.userLineEdit.setText('fa2909')
        self.openDatabaseDialog.ui.databaseLineEdit.setText('fa2909')
        self.openDatabaseDialog.ui.passwordLineEdit.setText('0000')
        if self.openDatabaseDialog.exec_():
            host_name = self.openDatabaseDialog.ui.hostLineEdit.text()
            user_name = self.openDatabaseDialog.ui.userLineEdit.text()
            database_name = self.openDatabaseDialog.ui.databaseLineEdit.text()
            password = self.openDatabaseDialog.ui.passwordLineEdit.text()

            self.db.connect(database_name, user_name, host_name, password)
        if not self.db.is_connected():
            string = ("Datenbankverbindung konnte nicht hergestellt werden"
                      ": Host = {}, Database = {}".format(host_name, database_name))
            self.plainTextEdit.setPlainText(string)
            # sys.exit(1)

        else:
            string = ("Datenbankverbindung hergestellt: Host = {}, Database = {}".format(host_name, database_name))
            self.plainTextEdit.setPlainText(string)
            self.connectionActiveLabel.setStyleSheet("QLabel { background-color : green}")

    def plot_trainings_data(self):
        """
        aa
        :return:
        """
        self.generator.plot_generated_data()

    def create_table(self):
        """
        Creates a new database table with the required format
        :return:
        """
        success = self.db.load_dump()
        if success:
            self.plainTextEdit.setPlainText("Neue Tabelle erfolgreich erstellt: data")
        else:
            self.plainTextEdit.setPlainText("Neue Tabelle konnte nicht erstellt werden."
                                            " Vielleicht existiert sie bereits")