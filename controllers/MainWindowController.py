import sys  # Access command line
import os
import platform

# PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from threading import Thread

from models.MatplotLibWidget import DynamicMplCanvas

# Views
from views import MainWindow, ConfigureFilterDialog
from views import OpenDatabaseDialog

# Controller
from controllers import KNeighborsClassifierDialogController
from controllers import MinMaxScalerDialogController
from controllers import SVMClassifierDialogController
from controllers import ScalerDialogCongroller

# Models
from models.Pipeline import MyPipeline
from models.Database import DatabaseConnection

__version__ = "1.0"


class MainWindowClass(QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self):
        super(MainWindowClass, self).__init__()
        self.setupUi(self)

        self.db = DatabaseConnection()
        self.selected_table_name = None
        # Algorithms
        self.kNeighborAlgorithm = None
        self.SVMAlgorithm = None
        # Filter
        self.minMaxFilter = None
        self.scalerFilter = None
        self.selected_algorithm_object = None
        self.pipelines = []
        self.selected_pipeline_nr = None
        self.selected_algorithm_name = None
        self.selected_pipeline_object = None
        self.selected_filter_nr = None
        self.selected_filter_name = None
        self.selected_filter_object = None
        self.selected_id = None
        self.online_analysis_active = False
        self.applied_algorithms = []
        self.selected_db_entry_uuid = None
        self.filename = None

        # #############################################################################################################
        # Initialize Timers
        # #############################################################################################################
        self.process_data_timer = QTimer(self)
        self.process_data_timer.timeout.connect(self.process_data_timer_cb)
        self.process_data_timer.start(1500)              # 500ms

        self.update_gui_timer = QTimer(self)
        self.process_data_timer.timeout.connect(self.update_ui_timer_cb)
        self.process_data_timer.start(1500)

        # #############################################################################################################
        # Initialize Plots
        # #############################################################################################################
        l1 = QVBoxLayout(self.plotLabel1)
        self.plot1 = DynamicMplCanvas(self.plotLabel1, width=5, height=4, dpi=100)
        l1.addWidget(self.plot1)

        # #############################################################################################################
        # Initialize Dialogs
        # #############################################################################################################
        self.kNeighborClassifierDialogController = KNeighborsClassifierDialogController.Controller()
        self.minMaxScalerDialogController = MinMaxScalerDialogController.Controller()
        self.SVMClassifierDialogController = SVMClassifierDialogController.Controller()
        self.scalerDialogController = ScalerDialogCongroller.Controller()

        self.configureFilterDialog = QDialog()
        self.configureFilterDialog.ui = ConfigureFilterDialog.Ui_ConfigureFilterDialog()
        self.configureFilterDialog.ui.setupUi(self.configureFilterDialog)

        self.openDatabaseDialog = QDialog()
        self.openDatabaseDialog.ui = OpenDatabaseDialog.Ui_Dialog()
        self.openDatabaseDialog.ui.setupUi(self.openDatabaseDialog)

        # #############################################################################################################
        # Signals
        # #############################################################################################################
        # QAction
        self.connect(self.actionOpenNewDatabase, SIGNAL("triggered()"), self.action_open_new_database_cb)
        self.connect(self.actionQuit, SIGNAL("triggered()"), self.close)
        self.connect(self.actionOnlineAnalysis, SIGNAL("triggered()"), self.action_online_analysis_cb)
        self.connect(self.actionHelpAbout, SIGNAL("triggered()"), self.action_help_about_cb)
        self.connect(self.actionSaveFile, SIGNAL("triggered()"), self.action_save_cb)
        self.connect(self.actionSaveFileAs, SIGNAL("triggered()"), self.action_save_as_cb)
        self.connect(self.actionPrint, SIGNAL("triggered()"), self.action_print_cb)

        # QButton
        self.connect(self.connectToDatabasePushButton, SIGNAL("clicked()"), self.action_open_new_database_cb)
        self.connect(self.deleteEntryButton, SIGNAL("clicked()"), self.delete_entry_cb)
        self.connect(self.deleteFilterButton, SIGNAL("clicked()"), self.delete_filter_cb)
        self.connect(self.algoConfigButton, SIGNAL("clicked()"), self.configure_algo_cb)
        self.connect(self.applyAlgoButton, SIGNAL("clicked()"), self.apply_pipeline_cb)
        self.connect(self.configureFilterButton, SIGNAL("clicked()"), self.configure_filter_cb)
        self.connect(self.addFilterButton, SIGNAL("clicked()"), self.add_filter_cb)
        self.connect(self.deletePipelineButton, SIGNAL("clicked()"), self.delete_pipeline_cb)
        self.connect(self.startRestPushButton, SIGNAL("clicked()"), self.start_rest_cb)
        self.connect(self.refreshTableButton, SIGNAL("clicked()"), self.populate_table_view_cb)
        self.connect(self.deleteTableButton, SIGNAL("clicked()"), self.delete_table_cb)
        self.connect(self.startStopAnalysisPushButton, SIGNAL("clicked()"), self.start_stop_analysis_cb)

        # QTableWidget
        self.connect(self.appliedFilterTableWidget, SIGNAL("itemSelectionChanged()"),
                     self.filter_selection_cb)
        self.connect(self.pipelinesTableWidget, SIGNAL("itemSelectionChanged()"),
                     self.pipeline_selection_cb)
        self.connect(self.databaseTableWidget, SIGNAL("itemSelectionChanged()"),
                     self.database_selection_cb)

        # QComboBox
        self.connect(self.chooseAlgoComboBox, SIGNAL("currentIndexChanged(int)"), self.set_algo)
        self.connect(self.chooseFilterComboBox, SIGNAL("currentIndexChanged(int)"), self.select_filter_cb)

    # #################################################################################################################
    # Static/Internal Functions
    # #################################################################################################################
    def _update_pipeline_info(self):
        if self.selected_pipeline_nr is not None:
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
    def start_rest_cb(self):
        self.restServerActiveLabel.setStyleSheet("QLabel { background-color : green}")
        thread = Thread(target=rest_thread, args=(10,))
        try:
            thread.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    def update_ui_timer_cb(self):
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
            self.plot1.set_data(pipeline_results)

            # Print Report
            report = self.selected_pipeline_object.get_report()
            self.reportTextEdit.setPlainText(report)

            # Update Database Info Field
            self.update_database_info()

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
            data_list = self.db.get_unprocessed_data()

            for pipeline in self.pipelines:
                for data in data_list:
                    pipeline.set_data(data, self.online_analysis_active)

    def select_filter_cb(self):
        self.selected_filter_name = self.chooseFilterComboBox.currentText()

    def add_filter_cb(self):
        """
        Adds configured Filter to the selected pipeline
        :return:
        """
        self._update_filter_table()
        if self.selected_filter_name and self.selected_pipeline_object:
            if self.selected_filter_name == "MinMaxScaler":
                new_filter = self.minMaxFilter
            if self.selected_filter_name == "StandardScaler":
                new_filter = self.scalerFilter
            self.selected_filter_object = new_filter

            self.selected_pipeline_object.add_filter(new_filter)

            self._update_filter_table()

            self._update_pipeline_info()

    def delete_pipeline_cb(self):
        # Get selected Row
        # selected_row = self.pipelinesTableWidget.currentRow()
        selected_row = self.pipelinesTableWidget.currentIndex().row()
        print("selected_row = {}".format(selected_row))
        if selected_row is not None and self.pipelines is not None:
            if selected_row >= 0:
                self.pipelinesTableWidget.removeRow(selected_row)
                del self.pipelines[selected_row]

    def filter_selection_cb(self):
        """
        Callback function is triggered, when user selects an entry in the "appliedFilterTableWidget"
        :return:
        """
        qmodel_index = self.pipelinesTableWidget.currentIndex()        # currentIndex() returns QModelIndex
        if not qmodel_index.isValid():
            return
        index = qmodel_index.row()
        self.selected_filter_nr = index

    def database_selection_cb(self):
        """
        Callback function is triggered, when user selects an entry "Angewandte Analyseverfahren" table under the
        "Analyse" Tab
        :return:
        """
        # self.algoResultsListTableWidget.select
        qmodel_index = self.databaseTableWidget.currentIndex()        # currentIndex() returns QModelIndex
        if not qmodel_index.isValid():
            return
        row = qmodel_index.row()
        self.selected_db_entry_uuid = self.databaseTableWidget.item(row, 0).text()      # uuid

    def pipeline_selection_cb(self):
        """
        Callback function is triggered, when user selects an entry in the "Pipeline" table
        under the "Analyse" Tab.
        :return:
        """
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

    def configure_filter_cb(self):
        """
        This Callback function gets triggered when user clicks the "Konfiguration" button for the filter configuration
        in the Analysis Tab.
        :return:
        """
        # Create Dialog
        self.selected_filter_name = self.chooseFilterComboBox.currentText()
        if self.selected_filter_name == "MinMaxScaler":
            print("MinMaxScaler Config")
            if self.minMaxScalerDialogController.exec_():
                self.minMaxFilter = self.minMaxScalerDialogController.get_filter()
            if self.minMaxFilter:
                self.selected_filter_object = self.minMaxFilter
        if self.selected_filter_name == "StandardScaler":
            if self.scalerDialogController.exec_():
                self.scalerFilter = self.scalerDialogController.get_filter()
            if self.scalerFilter:
                self.selected_filter_object = self.scalerFilter

    def apply_pipeline_cb(self):
        """
        This Callback function gets triggered when user clicks the "Hinzufuegen" Button in the "Analyse" Tab
        :return:
        """       
        # Create new pipeline
        if self.selected_algorithm_object:      # Only add, if user configured algorithm
            new_pipeline = MyPipeline(self.selected_algorithm_object)
            self.pipelines.append(new_pipeline)

            self.applied_algorithms.append(self.selected_algorithm_object)

            self._update_algo_table()

            if self.selected_pipeline_nr is None:
                self.selected_pipeline_nr = 0
                print("if self.selected_pipeline_nr is None")
            else:
                self.selected_pipeline_nr = len(self.pipelines) - 1
            self.pipelinesTableWidget.selectRow(self.selected_pipeline_nr)

            self._update_pipeline_info()

    def action_online_analysis_cb(self):
        self.online_analysis_active = not self.online_analysis_active
        if self.online_analysis_active:
            self.startStopAnalysisPushButton.setText("Stoppe Analyse")
        else:
            self.startStopAnalysisPushButton.setText("Starte Analyse")

    def action_open_new_database_cb(self):
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
        if self.db.open(host_name, user_name, database_name, password) is True:
            # Display Connection status in textEdit
            self.db.get_data()
            self.update_database_info()

            self.dbConnectionActiveLabel.setStyleSheet("QLabel { background-color : green}")

            self.currentDatabaseConnectionLabel.setText("Host = {}, Database = {}".format(host_name, database_name))
            # Populate tableSelectionComboBox with available Tables
            # self.tableSelectionComboBox.clear()
            # for tableEntry in self.db.get_tables():
            #     self.tableSelectionComboBox.addItem(tableEntry)
        else:
            self.dbConnectionActiveLabel.setStyleSheet("QLabel { background-color : red}")
            print("No Database Connection possible")

        self.populate_table_view_cb()

    def delete_table_cb(self):
        """
        Callback Function. Called when QButton Delete Table is pressed. Deletes all entries in data
        :return:
        """
        self.db.delete_table_entries()
        self.populate_table_view_cb()

    def start_stop_analysis_cb(self):
        """
        Function starts or stops Online data analysis, when the "Start Analyse" PushButton in the "Analyse" Tab
        is pressed
        :return:
        """
        button_text = self.startStopAnalysisPushButton.text()
        if button_text == "Starte Analyse":
            self.startStopAnalysisPushButton.setText("Stoppe Analyse")
            self.online_analysis_active = True
            self.actionOnlineAnalysis.setChecked(True)
        if button_text == "Stoppe Analyse":
            self.startStopAnalysisPushButton.setText("Starte Analyse")
            self.online_analysis_active = False
            self.actionOnlineAnalysis.setChecked(False)

    def update_database_info(self):
        output = ""
        if self.db.is_connected():
            db_name = self.db.get_db_name()
            db_host = self.db.get_host_name()
            output += "Datenbank Verbindung erfolgreich hergestellt: Hostname = {}, Datenbank = {}\n" \
                     "".format(db_host, db_name)
            output += "Anzahl an Datenbankeintraegen: {} \n".format(self.db.count_db_entries())
            output += "... davon Trainingsdaten: {} \n".format(self.db.count_training_data())
            output += "... davon analysiert: {} \n".format(self.db.count_processed_data())
        else:
            output += "Keine aktive Datenbankverbindung"
        self.textEdit.setText(output)

    def populate_table_view_cb(self):
        """
        This function populates the tabeleView in the the Datenintegration Window with the database data.
        :return:
        """
        #############
        header_names = self.db.get_column_names()
        header_names = header_names[:-1]        # header_names[:-1] means don't regard last column > data
        entries = self.db.get_data()
        if len(entries) > 149:
            # Only display 149 elements to save memory
            entries = entries[-149:]
        self.databaseTableWidget.setColumnCount(len(header_names))
        self.databaseTableWidget.setRowCount(len(entries))
        self.databaseTableWidget.verticalHeader().setVisible(True)

        # Header
        self.databaseTableWidget.setHorizontalHeaderLabels(QStringList(header_names))
        self.databaseTableWidget.horizontalHeader().setStretchLastSection(True)
        # Loop through all entries/cells
        for row_nr, row in enumerate(entries):
            for col_nr, col in enumerate(row[:-1]):      # row[:-1] means don't regard last column > data
                item = QTableWidgetItem()
                item.setText(str(col))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.databaseTableWidget.setItem(row_nr, col_nr, item)
                self.databaseTableWidget.resizeColumnsToContents()

    def delete_entry_cb(self):
        """
        Callback Function
        This callback is triggered by clicking "Delete Entry" Button
        It deletes the selected entry from the database
        :return:
        """
        if self.selected_db_entry_uuid:
            self.db.delete_entry(self.selected_db_entry_uuid)
            self.populate_table_view_cb()

    def delete_filter_cb(self):
        """

        :return:
        """
        selected_filter_nr = self.selected_filter_nr
        if self.selected_pipeline_object is not None:
            self.selected_pipeline_object.delete_filter(selected_filter_nr)
            selected_row = self.pipelinesTableWidget.currentRow()
            self.appliedFilterTableWidget.removeRow(selected_row)
            self._update_pipeline_info()

    def configure_algo_cb(self):
        """
        Callback Function.
        This Function is executed, when the "Konfiguration" Button is clicked.
        It opens a dialog where the user can configure the selected Algorithm.
        :return:
        """
        # Create Dialog
        self.selected_algorithm_name = str(self.chooseAlgoComboBox.currentText())
        if self.selected_algorithm_name == 'KNeighborsClassifier':

            if self.kNeighborClassifierDialogController.exec_():
                self.kNeighborAlgorithm = self.kNeighborClassifierDialogController.get_algorithm()
            if self.kNeighborAlgorithm:
                self.selected_algorithm_object = self.kNeighborAlgorithm

        elif self.selected_algorithm_name == 'SVM':
            if self.SVMClassifierDialogController.exec_():
                self.SVMAlgorithm = self.SVMClassifierDialogController.get_algorithm()
            if self.SVMAlgorithm:
                self.selected_algorithm_object = self.SVMAlgorithm

    def action_help_about_cb(self):
        QMessageBox.about(self, "Ueber Data Analyzer",
                          """<b>Data Analyzer</b> v %s
                          <p>Copyright &copy; 2017 IAS Universitaet Stuttgart
                          <p>Diese Software soll die Umsetzung eines automatisierten
                          Daten Analyse Prozesses zur industriellen Qualitaetssicherung exemplarisch darstellen.
                          <p style="color:#0000FF";>Support: hessat@yahoo.de
                          <p>Python %s - Qt %s - PyQt %s on %s""" % (
                              __version__, platform.python_version(),
                              QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def action_save_as_cb(self):
        pass
        dialog = QFileDialog()
        dialog.setDefaultSuffix(QString(".png"))
        file_name = ""
        file_name = unicode(dialog.getSaveFileName(self,
                                                       "Analysis - Save Result", file_name,
                                                       "Dateiendungen (*.png, *.jpeg, *.jpg, *.bmp"))

        if file_name == "":         # Dialog canceled by user
            self.filename = None
            return
        # Default suffix
        if file_name.find(".") == -1:         # -1 means character not found
            file_name += ".png"
        self.filename = file_name
        self.action_save_cb()

    def action_save_cb(self):
        pass
        if self.filename is None:
            self.action_save_as_cb()
        else:
            figure = self.plot1.get_figure()
            figure.savefig(self.filename)
            QMessageBox.information(None, "Analyseergebniss erfolgreich gespeichert",
                                QString("Analyseergebniss erfolgreich gespeichert: \n "
                                        "Pfad: {}".format(self.filename)))

    def action_print_cb(self):
        pass
        self.printer = QPrinter(QPrinter.HighResolution)
        # self.printer.setPageSize(QPrinter.Letter)
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            image = QPixmap.grabWidget(self.plotLabel1)
            size = image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x()*10, rect.y()*10, size.width()*10,
            size.height()*10)
            qimage = image.toImage()
            qpoint = QPoint(0, 0)
            painter.drawImage(qpoint, qimage)

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

def rest_thread(arg):
    rest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'REST', 'mysite', 'manage.py')
    run_rest_cmd = 'python ' + rest_path + ' runserver'
    os.system(run_rest_cmd)
    while True:
        pass







