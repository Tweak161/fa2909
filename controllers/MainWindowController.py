import sys  # Access command line
import os

# Data Analysis
import numpy as np
# PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ast

from threading import Thread


from models.MatplotLibWidget import MplCanvas
from models.MatplotLibWidget import DynamicMplCanvas

# Views
from views import MainWindow, ConfigureFilterDialog
from views import OpenDatabaseDialog

# Controller
from controllers import KNeighborsClassifierDialogController

# Models
from models.Pipeline import MyPipeline
from models import Filter
from models.Database import DatabaseConnection

# Spalten Indices
# SEPAL_LENGTH = 0                              #   Umbenennen in   sepal_length
# SEPAL_WIDTH = ASSETID = 1                   #                   sepal_width
# PETAL_LENGTH = DATE = DESCRIPTION = 2       #                   petal_length
# PETAL_WIDTH = ACTIONID = 3                 #                   petal_width
# SPECIES = 4


class MainWindowClass(QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self):
        super(MainWindowClass, self).__init__()
        self.setupUi(self)

        self.db = DatabaseConnection()
        self.irisDataModel = QSqlTableModel(self)
        self.databaseTableView.setModel(self.irisDataModel)
        self.selected_table_name = None
        self.selected_distance_measure = None
        self.num_rows = None
        self.num_columns = None
        self.db_data = None
        self.attributes = None
        self.columns = None
        self.simpleKMeans = None
        self.applied_algorithms = []            # Replace with self.pipelines
        self.selected_filter_list = []
        self.selected_filter = None
        self.selected_algorithm_object = None
        self.pipelines = []
        self.selected_pipeline_nr = None
        self.selected_pipeline_object = None
        self.selected_algorithm_name = None
        self.selected_filter_name = None
        self.selected_workpiece = None
        self.selected_data = None
        self.selected_id = None
        self.online_analysis_active = False

        # #############################################################################################################
        # Initialize Timers
        # #############################################################################################################
        self.process_data_timer = QTimer(self)
        self.process_data_timer.timeout.connect(self.process_data_timer_cb)
        self.process_data_timer.start(500)              # 500ms

        self.update_gui_timer = QTimer(self)
        self.process_data_timer.timeout.connect(self.update_ui)
        self.process_data_timer.start(500)

        # #############################################################################################################
        # Initialize Plots
        # #############################################################################################################
        l1 = QVBoxLayout(self.plotLabel1)
        self.plot1 = DynamicMplCanvas(self.plotLabel1, width=5, height=4, dpi=100)
        l1.addWidget(self.plot1)

        # #############################################################################################################
        # Initialize Dialogs
        # #############################################################################################################
        self.simpleKMeansDialog = KNeighborsClassifierDialogController.Controller()
        # self.simpleKMeansDialog.setupUi(self.simpleKMeansDialog)

        self.openDatabaseDialog = QDialog()
        self.openDatabaseDialog.ui = OpenDatabaseDialog.Ui_Dialog()
        self.openDatabaseDialog.ui.setupUi(self.openDatabaseDialog)

        self.configureFilterDialog = QDialog()
        self.configureFilterDialog.ui = ConfigureFilterDialog.Ui_ConfigureFilterDialog()
        self.configureFilterDialog.ui.setupUi(self.configureFilterDialog)

        # ###################################################################################################################
        # Signals
        # ###################################################################################################################
        # QAction
        self.connect(self.actionOpenNewDatabase, SIGNAL("triggered()"), self.action_open_new_database_callback)
        self.connect(self.actionQuit, SIGNAL("triggered()"), self.close)
        self.connect(self.actionOnlineAnalysis, SIGNAL("triggered()"), self.action_online_analysis_callback)

        # QButton
        self.connect(self.addEntryButton, SIGNAL("clicked()"), self.add_entry)
        self.connect(self.deleteEntryButton, SIGNAL("clicked()"), self.delete_entry)
        self.connect(self.algoConfigButton, SIGNAL("clicked()"), self.configure_algo)
        self.connect(self.applyAlgoButton, SIGNAL("clicked()"), self.apply_pipeline)
        self.connect(self.configureFilterButton, SIGNAL("clicked()"), self.configure_filter)
        self.connect(self.connectToDatabasePushButton, SIGNAL("clicked()"), self.action_open_new_database_callback)
        self.connect(self.addFilterButton, SIGNAL("clicked()"), self.add_filter)
        self.connect(self.deletePipelineButton, SIGNAL("clicked()"), self.delete_pipeline)
        self.connect(self.startRestPushButton, SIGNAL("clicked()"), self.start_rest)
        self.connect(self.refreshTableButton, SIGNAL("clicked()"), self.refresh_table)

        # QTableWidget
        self.connect(self.appliedFilterTableWidget, SIGNAL("itemSelectionChanged()"),
                     self.filter_selection_cb)
        self.connect(self.pipelinesTableWidget, SIGNAL("itemSelectionChanged()"),
                     self.pipeline_selection_cb)
        self.connect(self.databaseTableView.selectionModel(), SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.id_selection_cb)

        # QComboBox
        # self.connect(self.workpieceSelectionComboBox, SIGNAL("currentIndexChanged(int)"), self.populate_table_view)
        self.connect(self.chooseAlgoComboBox, SIGNAL("currentIndexChanged(int)"), self.set_algo)
        self.connect(self.choseFilterComboBox, SIGNAL("currentIndexChanged(int)"), self.select_filter)


        # #############################################################################################################
        # Toolbar setup
        # #############################################################################################################
        # self.toolBar.addAction(newDatabaseAction)
        # self.menuFile.addAction(newDatabaseAction)

    # #################################################################################################################
    # Static/Internal Functions
    # #################################################################################################################
    def print_filter_selection(self, index):
        """
        Function prints parameters for the filter selected in the "appliedFilterTableWidget" in the "Analyse" Tab
        :param index:
        :return:
        """
        pass
        # algorithm = self.applied_algorithms[index]
        # algorithm_result = algorithm.get_algorithm_parameters()
        # algorithm_result += '\n'
        # algorithm_result += algorithm.get_filter_parameters()
        # algorithm_result += '\n'
        # algorithm_result += algorithm.get_result()
        # self.algoResultsTextEdit.setPlainText(algorithm_result)
    def _update_pipeline_info(self):
        if self.selected_pipeline_nr:
            index = self.selected_pipeline_nr
            selected_pipeline = self.pipelines[index]
            pipeline_info_str = selected_pipeline.get_configuration_info()
            pipeline_info_str += '\n'
            pipeline_info_str += selected_pipeline.get_result_info()
            self.pipelineInfoTextEdit.setPlainText(pipeline_info_str)        # Set pipelineInfoTextEdit

    def _update_algo_table(self):
        if self.applied_algorithms:
            for index, algorithm in enumerate(self.pipelines):
                self.pipelinesTableWidget.setColumnCount(1)
                self.pipelinesTableWidget.setRowCount(len(self.pipelines))

                item = QTableWidgetItem()
                item.setText(algorithm.get_name())
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.pipelinesTableWidget.setItem(index, 0, item)
                self.pipelinesTableWidget.resizeColumnsToContents()
                self.pipelinesTableWidget.setHorizontalHeaderLabels(QStringList('Pipeline'))
                self.pipelinesTableWidget.horizontalHeader().setStretchLastSection(True)

    def _update_filter_table(self):
        self.appliedFilterTableWidget.clear()
        filter_list = self.selected_pipeline_object.get_filter_list()
        self.appliedFilterTableWidget.setColumnCount(1)
        self.appliedFilterTableWidget.setRowCount(len(filter_list))

        for index, filter in enumerate(filter_list):
            item = QTableWidgetItem()
            item.setText(filter.get_name())
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.appliedFilterTableWidget.setItem(index, 0, item)
            self.appliedFilterTableWidget.resizeColumnsToContents()
            self.appliedFilterTableWidget.setHorizontalHeaderLabels(QStringList('Filter'))
            self.appliedFilterTableWidget.horizontalHeader().setStretchLastSection(True)

    # #################################################################################################################
    # Callbacks
    # #################################################################################################################
    def refresh_table(self):
        self.populate_table_view()

    def start_rest(self):
        self.restServerActiveLabel.setStyleSheet("QLabel { background-color : green}")
        thread = Thread(target=rest_thread, args=(10,))
        try:
            thread.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        # os.system("python ../REST/mysite/manage.py runserver")

    def update_ui(self):
        """
        Updates gui cyclically
        :return:
        """
        # Display Pipeline Results
        if self.selected_pipeline_object:
            # Set "Auswertung" > "Genauigkeit [%]"
            prediction_accuracy = self.selected_pipeline_object.get_accuracy()
            prediction_accuracy = prediction_accuracy[0:5]
            self.predictionAccuracyLineEdit.setText(prediction_accuracy)

            # Set "Auswertung" > "Ausschuss [%]"
            junk_percentage = self.selected_pipeline_object.get_junk()
            self.junkPercentageLineEdit.setText(junk_percentage)

            # Plot Classification "Auswertung" > "Plot"
            pipeline_results = self.selected_pipeline_object.get_results()
            print("rest_response = {}".format(pipeline_results))
            self.plot1.set_data(pipeline_results)

            # Print Report
            report = self.selected_pipeline_object.get_report()
            self.reportTextEdit.setPlainText(report)

    def process_data_timer_cb(self):
        """
        Callback Function. Executes each 500ms.
        Queries new database entrys and sends data to pipelines for processing.
        :return:
        """
        if self.db.is_connected() and self.online_analysis_active:
            pass
            # Train Model
            training_data = self.db.get_training_data()
            for pipeline in self.pipelines:
                pipeline.train_model(training_data)

            # Classify
            # Query new data from database and pass it to pipeline for processing
            data_list = self.db.get_unprocessed_data2()

            for pipeline in self.pipelines:
                for data in data_list:
                    pipeline.set_data(data, self.online_analysis_active)

    def select_filter(self):
        pass
        self.selected_filter_name = self.choseFilterComboBox.currentText()

    def add_filter(self):
        """

        :return:
        """
        pass
        self._update_filter_table()
        if self.selected_filter_name and self.selected_pipeline_object:
            if self.selected_filter_name == "MinMaxFilter":
                new_filter = Filter.MinMaxFilter()
                self.selected_filter = new_filter
                self.selected_pipeline_object.add_filter(new_filter)

                self._update_filter_table()

        self._update_pipeline_info()

    def delete_pipeline(self):
        pass
        # Get selected Row
        selected_row = self.pipelinesTableWidget.currentRow()
        if selected_row:
            pass
            selected_item = self.pipelinesTableWidget.currentItem()
            self.pipelinesTableWidget.removeRow(selected_row)
            del self.pipelines[selected_row]

    def id_selection_cb(self, index1, index2):
        q_model_index_list = index1.indexes()       # list with QModelIndex Instances of each column for selected row
        q_model_index_uuid = q_model_index_list[0]      # column uuid
        self.selected_id = self.irisDataModel.data(q_model_index_uuid).toString()

        ##############################################################################################################
        # Update pipelines calculations
        ##############################################################################################################
        # Get data
        q_model_index_data= q_model_index_list[4]
        data = self.irisDataModel.data(q_model_index_data).toString()

        data = self.db.get_data(self.selected_id)

        # Set new data for all pipelines
        for pipeline in self.pipelines:
            pipeline.set_data(data, False)

        # Pipline calculations changed > Update pipeline info
        self._update_pipeline_info()

    def filter_selection_cb(self):
        """
        Callback function is triggered, when user selects an entry in the "appliedFilterTableWidget"
        :return:
        """
        qmodel_index = self.pipelinesTableWidget.currentIndex()        # currentIndex() returns QModelIndex
        if not qmodel_index.isValid():
            return
        index = qmodel_index.row()
        self.print_filter_selection(index)

    def pipeline_selection_cb(self):
        """
        Callback function is triggered, when user selects an entry in the "Angewandte Analyseverfahren" table
        under the "Analyse" Tab.
        :return:
        """
        # self.algoResultsListTableWidget.select
        qmodel_index = self.pipelinesTableWidget.currentIndex()        # currentIndex() returns QModelIndex
        if not qmodel_index.isValid():
            return
        index = qmodel_index.row()
        self.selected_pipeline_nr = self.pipelinesTableWidget.currentIndex().row()
        self.selected_pipeline_object = self.pipelines[self.selected_pipeline_nr]

        # Update GUI elements
        self._update_filter_table()
        self._update_pipeline_info

        selected_pipeline = self.pipelines[index]
        pipeline_info_str = selected_pipeline.get_configuration_info()
        pipeline_info_str += '\n'
        pipeline_info_str += selected_pipeline.get_result_info()
        self.pipelineInfoTextEdit.setPlainText(pipeline_info_str)        # Set pipelineInfoTextEdit

    def configure_filter(self):
        """
        This Callback function gets triggered when user clicks the "Konfiguration" button for the filter configuration
        in the Analysis Tab.
        :return:
        """
        if self.configureFilterDialog.exec_():
            pass

    def apply_pipeline(self):
        """
        This Callback function gets triggered when user clicks the "Hinzufuegen" Button in the "Analyse" Tab
        :return:
        """
        # Create new pipeline
        new_pipeline = MyPipeline(self.selected_algorithm_object)
        self.pipelines.append(new_pipeline)


        # Output to console
        # output = self.simpleKMeans.get_algorithm_parameters()
        # output += "\n"
        # output += self.simpleKMeans.get_result()
        #
        # self.algoResultsTextEdit.clear()
        # self.algoResultsTextEdit.appendPlainText(output)

        self.applied_algorithms.append(self.simpleKMeans)

        self._update_algo_table()

        if self.selected_pipeline_nr is None:
            self.selected_pipeline_nr = 0
        else:
            self.selected_pipeline_nr = len(self.pipelines)-1
        self.pipelinesTableWidget.selectRow(self.selected_pipeline_nr)
        self._update_pipeline_info()

    def action_online_analysis_callback(self):
        self.online_analysis_active = not self.online_analysis_active

    def action_open_new_database_callback(self):
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

        if not self.db.open(host_name, user_name, database_name, password):
            self.dbConnectionActiveLabel.setStyleSheet("QLabel { background-color : red}")
            QMessageBox.warning(None, "Asset Manager",
                                QString("Database Error: %1").arg(self.db.lastError().text()))
            sys.exit(1)

        else:
            # Display Connection status in textEdit
            output = "Datenbank Verbindung erfolgreich hergestellt: Hostname = {}, Datenbank = {}" \
                     "".format(host_name, database_name)
            self.textEdit.setText(output)
            self.dbConnectionActiveLabel.setStyleSheet("QLabel { background-color : green}")

            self.currentDatabaseConnectionLabel.setText("Host = {}, Database = {}".format(host_name, database_name))
            # Populate tableSelectionComboBox with available Tables
            # self.tableSelectionComboBox.clear()
            # for tableEntry in self.db.get_tables():
            #     self.tableSelectionComboBox.addItem(tableEntry)

        self.populate_table_view()

    def populate_table_view(self):
        """
        This function populates the tabeleView in the the Datenintegration Window with the database data.
        :return:
        """
        # ###################################################################################################################
        # Database Integration
        # ###################################################################################################################
        self.selected_table_name = 'data' #self.tableSelectionComboBox.itemText(index)

        # self.selected_workpiece = ...

        self.irisDataModel.setTable(self.selected_table_name)             # Load "iris" table from currently open database

        self.irisDataModel.select()

        self.databaseTableView.setModel(self.irisDataModel)
        # self.connect(self.databaseTableView.selectionModel(), SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.id_selection_cb)

        # # Set custom Delegate
        # self.databaseTableView.setItemDelegate()
        self.databaseTableView.setSelectionMode(QTableView.SingleSelection)
        self.databaseTableView.hideColumn(6)
        self.databaseTableView.setSelectionBehavior(QTableView.SelectRows)
        self.databaseTableView.resizeColumnsToContents()

        self.extract_data()
        self.setup_dialoges()

    def extract_data(self):
        """
        Get data from selected data entry and save it to memory
        :return:
        """
        # Update number of Rows and Columns. Safe DB Content to memory
        # self.selected_data = self.db.get_data(self.selected_id)

    def add_entry(self):
        """
        This Function is a callback to addButton.
        It adds an Entry to the database
        :return:
        """
        row = self.databaseTableView.currentIndex().row() \
            if self.databaseTableView.currentIndex().isValid() else 0

        QSqlDatabase.database().transaction()
        self.irisDataModel.insertRow(row)
        index = self.irisDataModel.index(row, 0)
        self.databaseTableView.setCurrentIndex(index)

        query = QSqlQuery()
        query.exec_("SELECT MAX(id) FROM {}".format(self.selected_table_name))
        QSqlDatabase.database().commit()
        self.databaseTableView.edit(index)

    def delete_entry(self):
        """
        Callback Function
        This callback is triggered by clicking "Delete Entry" Button
        It deletes the selected entry from the database
        :return:
        """
        # FIX: Funktion loescht immer alle Eintraege mit gleichem Inhalt
        index = self.databaseTableView.currentIndex()
        if not index.isValid():
            return

        self.irisDataModel.removeRow(index.row())
        self.irisDataModel.submitAll()

    def configure_algo(self):
        """
        Callback Function.
        This Function is executed, when the "Konfiguration" Button is clicked.
        It opens a dialog where the user can configure the selected Algorithm.
        :return:
        """
        pass
        # Create Dialog
        self.selected_algorithm_name = str(self.chooseAlgoComboBox.currentText())
        if self.selected_algorithm_name == 'KNeighborsClassifier':

            if self.simpleKMeansDialog.exec_():
                self.simpleKMeans = self.simpleKMeansDialog.get_algorithm()
            if self.simpleKMeans:
                # for row in range(0, self.num_rows):
                # self.simpleKMeans.set_attributes(X)
                # self.simpleKMeans.set_class(Y)
                # self.simpleKMeans.train_model()
                # TODO: Execute Algorithm

                self.selected_algorithm_object = self.simpleKMeans

        elif self.selected_algorithm_name == 'FilteredClusterer':
            pass

        elif self.selected_algorithm_name == 'Cobweb':
            pass

    ###################################################################################################################
    # Set Functions
    ###################################################################################################################

    def set_algo(self, index):
        """
        Callback Function.
        This Function is executed, when the Algorithms Combobox is changed
        :return:
        """
        self.selected_algorithm_name = self.chooseAlgoComboBox.itemText(index)

    def setup_dialoges(self):
        """
        Function is executed after a database connection is established.
        Function populates Dialoges with data depending on the database connection
        :return:
        """
        pass


def rest_thread(arg):
    print("Start Rest Server...")
    rest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'REST', 'mysite', 'manage.py')
    run_rest_cmd = 'python ' + rest_path + ' runserver'
    os.system(run_rest_cmd)
    while True:
        pass







