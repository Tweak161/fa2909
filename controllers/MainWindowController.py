import sys  # Access command line

# Data Analysis
import numpy as np
# PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from model.Algorithms import SimleKMeans
# GUIs Import
from views import MainWindow, ConfigureFilterDialog
from views import OpenDatabaseDialog
from views import SimpleKMeansDialog

# Spalten Indices
SEPAL_LENGTH = 0                              #   Umbenennen in   sepal_length
SEPAL_WIDTH = ASSETID = 1                   #                   sepal_width
PETAL_LENGTH = DATE = DESCRIPTION = 2       #                   petal_length
PETAL_WIDTH = ACTIONID = 3                 #                   petal_width
SPECIES = 4


class MainWindowClass(QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self):
        super(MainWindowClass, self).__init__()
        self.setupUi(self)
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.irisDataModel = QSqlRelationalTableModel(self)
        self.selected_table_name = None
        self.selected_algorithm = None
        self.selected_distance_measure = None
        self.num_rows = None
        self.num_columns = None
        self.db_data = None
        self.attributes = None
        self.class_attributes = None
        self.columns = None
        self.simpleKMeans = None
        self.attributes_np = None
        self.class_attributes_np = None
        self.applied_algorithms = []

        # ###################################################################################################################
        # Initialize Dialogs
        # ###################################################################################################################
        self.simpleKMeansDialog = QDialog()
        self.simpleKMeansDialog.ui = SimpleKMeansDialog.Ui_SimpleKMeansDialog()
        self.simpleKMeansDialog.ui.setupUi(self.simpleKMeansDialog)
        self.simpleKMeansDialog.ui.distanceMeassureComboBox.addItem('Manhatten')
        self.simpleKMeansDialog.ui.distanceMeassureComboBox.addItem('Cosinus')
        self.simpleKMeansDialog.ui.distanceMeassureComboBox.addItem('Euklidisch')

        self.openDatabaseDialog = QDialog()
        self.openDatabaseDialog.ui = OpenDatabaseDialog.Ui_Dialog()
        self.openDatabaseDialog.ui.setupUi(self.openDatabaseDialog)

        self.configureFilterDialog = QDialog()
        self.configureFilterDialog.ui = ConfigureFilterDialog.Ui_ConfigureFilterDialog()
        self.configureFilterDialog.ui.setupUi(self.configureFilterDialog)

        # ###################################################################################################################
        # Create Connections
        # ###################################################################################################################
        self.connect(self.tableSelectionComboBox, SIGNAL("currentIndexChanged(int)"), self.populate_table_view)
        self.connect(self.actionOpenNewDatabase, SIGNAL("triggered()"), self.action_open_new_database_callback)
        self.connect(self.actionQuit, SIGNAL("triggered()"), self.close)
        self.connect(self.addEntryButton, SIGNAL("clicked()"), self.add_entry)
        self.connect(self.deleteEntryButton, SIGNAL("clicked()"), self.delete_entry)
        self.connect(self.chooseAlgoComboBox, SIGNAL("currentIndexChanged(int)"), self.set_algo)
        self.connect(self.algoConfigButton, SIGNAL("clicked()"), self.configure_algo)
        self.connect(self.simpleKMeansDialog.ui.distanceMeassureComboBox, SIGNAL("currentIndexChanged(int)"),
                     self.set_distance_measure)
        self.connect(self.applyAlgoButton, SIGNAL("clicked()"), self.apply_algo)
        self.connect(self.configureFilterButton, SIGNAL("clicked()"), self.configure_filter)
        self.connect(self.connectToDatabasePushButton, SIGNAL("clicked()"), self.action_open_new_database_callback)


        # ###################################################################################################################
        # Toolbar setup
        # ###################################################################################################################
        # self.toolBar.addAction(newDatabaseAction)
        # self.menuFile.addAction(newDatabaseAction)



    # ###################################################################################################################
    # Callbacks
    # ###################################################################################################################
    def configure_filter(self):
        """
        This Callback function gets triggered when user clicks the "Konfiguration" button for the filter configuration
        in the Analysis Tab.
        :return:
        """
        if self.configureFilterDialog.exec_():
            pass

    def apply_algo(self):
        """
        This Callback function gets triggered when user clicks the "Hinzufuegen" Button in the "Analyse" Tab
        :return:
        """
        # Output to console
        output = self.simpleKMeans.get_algorithm_parameters()
        output += "\n"
        output += self.simpleKMeans.get_filter_parameters()
        output += self.simpleKMeans.get_result()

        self.algoResultsTextEdit.clear()
        self.algoResultsTextEdit.appendPlainText(output)
        self.applied_algorithms.append(self.selected_algorithm)
        if not self.applied_algorithms:
            pass
        else:
            for algorithm in self.applied_algorithms:
                self.algoResultsListTextEdit.appendPlainText(algorithm)


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
        self.openDatabaseDialog.ui.databaseLineEdit.setText('thomas')
        self.openDatabaseDialog.ui.passwordLineEdit.setText('0000')
        if self.openDatabaseDialog.exec_():
            host_name = self.openDatabaseDialog.ui.hostLineEdit.text()
            database_name = self.openDatabaseDialog.ui.databaseLineEdit.text()
            password = self.openDatabaseDialog.ui.passwordLineEdit.text()

        self.db.setHostName(host_name)
        self.db.setDatabaseName(database_name)
        self.db.setPassword('0000')

        if not self.db.open():
            QMessageBox.warning(None, "Asset Manager",
                                QString("Database Error: %1").arg(self.db.lastError().text()))
            sys.exit(1)

        else:
            # Display Connection status in textEdit
            output = "Datenbank Verbindung erfolgreich hergestellt: Hostname = {}, Datenbank = {}" \
                     "".format(host_name, database_name)
            self.textEdit.setText(output)

            self.currentDatabaseConnectionLabel.setText("Host = {}, Database = {}".format(host_name, database_name))
            # Populate tableSelectionComboBox with available Tables
            self.tableSelectionComboBox.clear()
            for tableEntry in self.db.tables():
                self.tableSelectionComboBox.addItem(tableEntry)

        # self.populate_table_view(0)

    def populate_table_view(self, index):
        """
        This function populates the tabeleView in the the Datenintegration Window with the database data.
        :return:
        """
        # ###################################################################################################################
        # Database Integration
        # ###################################################################################################################
        self.selected_table_name = self.tableSelectionComboBox.itemText(index)

        self.irisDataModel.setTable(self.selected_table_name)             # Load "iris" table from currently open database

        self.irisDataModel.select()

        self.tableView.setModel(self.irisDataModel)
        # # Set custom Delegate
        # self.tableView.setItemDelegate()
        self.tableView.setSelectionMode(QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.resizeColumnsToContents()

        # Update number of Rows and Columns. Safe DB Content to memory
        query = QSqlQuery()
        query.setForwardOnly(True)
        query.prepare("SELECT * FROM {}".format(self.selected_table_name))
        query.exec_()

        self.num_rows = query.size()
        self.num_columns = query.record().count()

        # fieldNo = query.record().indexOf('petal_length')

        self.attributes_np = np.zeros((self.num_rows, self.num_columns - 1), dtype='float')
        self.class_attributes_np = np.zeros((self.num_rows, 1), dtype='str')

        self.attributes = [[0 for x in range(self.num_columns - 1)] for y in range(self.num_rows)]
        self.class_attributes = [[0 for x in range(1)] for y in range(self.num_rows)]
        self.db_data = [[0 for x in range(self.num_columns)] for y in range(self.num_rows)]


        row_counter = 0
        while query.next():             # query contains one table column. query.next() steps one row forward
            for column in range(0, self.num_columns):
                self.db_data[row_counter][column] = str(query.value(column).toString())
                if column < self.num_columns -1:
                    self.attributes[row_counter][column] = int(query.value(column).toString())
                    self.attributes_np[row_counter][column] = float(query.value(column).toString())
                else:
                    pass
                    self.class_attributes[row_counter] = str(query.value(column).toString())
                    self.class_attributes_np = str(query.value(column).toString())

                print(query.value(column).toString())
            row_counter += 1

            #     print("Spalte = {}".format(column))
            # colum_values = query.value(colsumn).toString()
            # print(colum_values)
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #
        # print(self.db_data)
        # query.prepare("SELECT * FROM {} WHERE id = '{}'".format(self.selected_table_name), 0)
        singleCol = query.prepare("SELECT {} FROM {}".format("sepal_width", self.selected_table_name))
        query.exec_()
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # while query.next():
        #     sepal_width = query.record().toString()
        #     print('#################################')
        #     print(sepal_width)
        #     print('#################################')


        wholeTable = query.prepare("SELECT * FROM {}".format(self.selected_table_name))
        query.exec_()

        self.setup_dialoges()

        # print(query.record())
        # while query.next():
        #     sepal_width = query.value(1)
        #     print(sepal_width)


        # self.rows =

        # x=[0,10,100]
        # y=[3,4,5]
        #
        # self.mplwidget = MatplotlibWidgetClass(self.centralwidget)
        # self.mplwidget.setGeometry(QRect(70, 50, 600, 500))
        # self.mplwidget.setObjectName("mplwidget")
        # self.mplwidget.plotDataPoints(x, y)
        #
        #
        # self.mplwidget2 = MyMplCanvas()
        # self.mplwidget2.setGeometry(QRect(70, 50, 600, 500))
        # self.mplwidget2.setObjectName("mplwidget")
        # self.mplwidget2.plotDataPoints(x, y)

        # l = QtGui.QVBoxLayout(self.plotWidget)
        # dc1 = MyDynamicMplCanvas(self.plotWidget, width=5, height=4, dpi=100)
        # dc2 = MyDynamicMplCanvas(self.plotWidget, width=5, height=4, dpi=100)
        # l.addWidget(dc1)
        # l.addWidget(dc2)

    def add_entry(self):
        """
        This Function is a callback to addButton.
        It adds an Entry to the database
        :return:
        """
        row = self.tableView.currentIndex().row() \
            if self.tableView.currentIndex().isValid() else 0

        QSqlDatabase.database().transaction()
        self.irisDataModel.insertRow(row)
        index = self.irisDataModel.index(row, 0)
        self.tableView.setCurrentIndex(index)

        query = QSqlQuery()
        query.exec_("SELECT MAX(id) FROM {}".format(self.selected_table_name))
        QSqlDatabase.database().commit()
        self.tableView.edit(index)

    def delete_entry(self):
        """
        Callback Function
        This callback is triggered by clicking "Delete Entry" Button
        It deletes the selected entry from the database
        :return:
        """
        # FIX: Funktion loescht immer alle Eintraege mit gleichem Inhalt
        index = self.tableView.currentIndex()
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

        if self.selected_algorithm == 'SimpleKMeans':

            if self.simpleKMeansDialog.exec_():
                pass
            # Following Code is executed after closing simpleKMeansDialog Window
            algo_k_means_max_iterations = self.simpleKMeansDialog.ui.maxIterationsLineEdit.text()
            algo_k_means_number_clusters = self.simpleKMeansDialog.ui.numClustersLineEdit.text()
            algo_k_means_seed = self.simpleKMeansDialog.ui.seedLineEdit.text()
            self.simpleKMeans = SimleKMeans(algo_k_means_max_iterations, algo_k_means_number_clusters, algo_k_means_seed)

            X = self.db_data[:][0:self.num_columns-2]
            Y = []
            for row in range(0, self.num_rows):
                Y.append(self.db_data[row][4])
            print("self.db_data[:][0:self.num_columns-2] = {}".format(Y))
            # print("self.db_data[1][4] = {}".format(Y))

            self.simpleKMeans.set_attributes(X)
            self.simpleKMeans.set_class(Y)
            self.simpleKMeans.train_model()

        elif self.selected_algorithm == 'FilteredClusterer':
            pass

        elif self.selected_algorithm == 'Cobweb':
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
        self.selected_algorithm = self.chooseAlgoComboBox.itemText(index)
        print(self.selected_algorithm)

    def set_distance_measure(self, index):
        """
        Callback Function. SimpleKMeansDialog
        This Function is exectued when the "Distanzmass" ComboBox is changed.
        It sets the value for the Distanzmass
        :return:
        """
        pass
        self.selected_distance_measure = self.simpleKMeansDialog.ui.distanceMeassureComboBox.itemText(index)
        print(self.selected_distance_measure)

    def setup_dialoges(self):
        """
        Function is executed after a database connection is established.
        Function populates Dialoges with data depending on the database connection
        :return:
        """
        pass


# if __name__ == '__main__':
#     ###################################################################################################################
#     # Start GUI
#     ###################################################################################################################
#     app = QApplication(sys.argv)
#
#
#     # ###################################################################################################################
#     # # Data Integration
#     # ###################################################################################################################
#     # Establish database connection
#
#
#
#     #
#     # # Connect to database
#     # database_connection = DatabaseConnection('thomas', 'thomas', 'localhost', '0000')
#     #
#     # # Create new table "iris"
#     # database_connection.create_table('iris', ["sepal_length varchar (50) NOT NULL",
#     #                                     "sepal_width varchar (40) NOT NULL",
#     #                                     "petal_length varchar (40) NOT NULL",
#     #                                     "petal_width varchar (40) NOT NULL",
#     #                                     "species varchar (24) check (species in ('setosa', 'versicolor', 'virginica'))"])
#     # # Import values from CSV
#     # database_connection.insert_iris()
#     #
#     # # Insert new record
#     # database_connection.insert_new_record("iris", "sepal_length, sepal_width, petal_length, petal_width, species",
#     #                                       "'1111', '1111', '1111', '1111', 'setosa'")
#     #
#     # print('##########################################################################################################')
#     # print('print_table()')
#     # print('##########################################################################################################')
#     # # Print table "iris"
#     # database_connection.print_table('iris')
#     #
#     # print('##########################################################################################################')
#     # print('print_column_names()')
#     # print('##########################################################################################################')
#     # # Print table columns from table "iris"
#     # database_connection.print_column_names()
#     #
#     # # Delete/Drop table "iris"
#     # # database_connection.drop_table('iris')
#     #
#     # ###################################################################################################################
#     # # Pre Processing
#     # ###################################################################################################################
#     #
#     # ###################################################################################################################
#     # # Analysis
#     # ###################################################################################################################
#     #
#     # ###################################################################################################################
#     # # Visualisation
#     # ###################################################################################################################
#
#     ###################################################################################################################
#     # Show GUI
#     ###################################################################################################################
#     form = MainWindowClass()
#     form.show()
#     app.exec_()
#







