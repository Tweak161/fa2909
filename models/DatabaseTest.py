import psycopg2 as p
import psycopg2.extras as e     # Neede to access values via column name
import json
from threading import Thread
from threading import Event
import os
import datetime
import pandas as pd
from models import Generator


class SimulationThread(Thread):
    def __init__(self, db_connection, event):
        Thread.__init__(self)
        self.stopped = event
        self.timeout = 1
        self.started = False
        self.db = db_connection

    def set_timeout(self, timeout):
        self.timeout = timeout

    def is_started(self):
        return self.started

    def run(self):
        self.started = True
        while not self.stopped.wait(self.timeout):
            self.db.simulate_logging()


class DatabaseConnection(object):
    def __init__(self):
        super(DatabaseConnection, self).__init__()
        self.seqnr_slam = 0
        self.run = 1
        self.car = 7000
        self.stop_flag = Event()
        self.simulation_thread = SimulationThread(self, self.stop_flag)
        self.connected = False
        self.generator = Generator.Generator()
        self.db_name = None
        self.db_user = None
        self.db_host = None
        self.db_password = None
        self.connection = None
        self.cursor = None

    def connect(self, db_name, db_user, db_host, db_password):
        try:
            self.db_name = db_name
            self.db_user = db_user
            self.db_host = db_host
            self.db_password = db_password
            self.connection = p.connect("dbname ='{}' user='{}' host='{}' password='{}'".format(db_name,
                                                                                                db_user,
                                                                                                db_host,
                                                                                                db_password))
            print("Connection status: {}".format(self.connection))
            print("Connection Status = {}".format(self.connection.status))
            self.connected = True
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            return True

        except:
            print('Cannot connect to database')
            self.connected = False
            return False

    def is_connected(self):
        """
        Function returns connection status. True if connected. False if not connected.
        :return: (bool)
        """
        return self.connected

    def generate_training_data(self):
        """
        This function generates simulated training data and saves it to the postgresql database.
        The function is similar to simulate_logging(), the generated JSON structures are the same.
        However it the simulated plantdata is already classified and isn't generated periodically.
        :return:
        """
        data = self.generator.generate_training_data()
        data_json = json.dumps(data)

        part_id = self.get_highest_id() + 1
        component_id = 1

        # Add new part
        insert_command = "INSERT INTO data (time, part_id, component_id, processed, classified, data)" \
                         " VALUES ('{}', {}, {}, {}, '{}', '{}')".format('now()',
                                                                   part_id,
                                                                   component_id,
                                                                   'False',
                                                                   'True',
                                                                   data_json)

        self.cursor.execute(insert_command)

        string = "Neuer Datenbankeintrag - Training Data: time={}," \
                        " part_id={}, component_id={}, data={}".format(datetime.datetime,
                                                                       part_id,
                                                                       component_id,
                                                                       data_json)
        return string

    # def start_logging_simulation(self, period):
    #     """
    #     Function writes data periodicall to postgresql database. Simulates logging
    #     :param period: (int) Period in s
    #     :return:
    #     """
    #     self.simulation_thread.set_timeout(period)
    #     if self.simulation_thread.is_started():
    #         self.stop_flag.clear()
    #         print('clear stop flag')
    #     else:
    #         self.simulation_thread.start()  # Frequency: 50 Hz

    # def stop_logging_simulation(self):
    #     self.stop_flag.set()

    def get_highest_id(self):
        pass
        command = "SELECT MAX(part_id) FROM data"
        self.cursor.execute(command)
        max_part_id = self.cursor.fetchall()[0][0]
        if max_part_id is None:
            max_part_id = 0

        return max_part_id

    def simulate_logging(self):
        """
        Function writes simulated plant data into postgres database.
        Function is static and is periodically called by the SimulationThread Thread
        :return: (str) Returns info string.
        """
        data = self.generator.generate_data()
        data_json = json.dumps(data)

        part_id = self.get_highest_id() + 1
        component_id = 1

        # Add new part
        insert_command = "INSERT INTO data (time, part_id, component_id, processed, classified, data)" \
                         " VALUES ('{}', {}, {}, {}, '{}', '{}')".format('now()',
                                                                         part_id,
                                                                         component_id,
                                                                         'False',
                                                                         'False',
                                                                         data_json)

        self.cursor.execute(insert_command)

        string = "Neuer Datenbankeintrag: time={}," \
                        " part_id={}, component_id={}, data={}".format(datetime.datetime,
                                                                       part_id,
                                                                       component_id,
                                                                       data_json)

        return string

    def simulate_logging_old(self):
        """
        Function writes to database periodically. This simulates logging
        :return:
        """
        part_id = self.get_highest_id() + 1
        component_id = 1
        # Read in iris dataset
        csv_file = '../SQL/iris.csv'
        df = pd.read_csv(csv_file)
        sepal_length = df['sepal_length'].values.tolist()   # .values to get a numpy.array,  .tolist() to get a list.
        sepal_width = df['sepal_width'].values.tolist()
        petal_length = df['petal_length'].values.tolist()
        petal_width = df['petal_width'].values.tolist()
        species = df['species'].values.tolist()

        data = {'sepal_length': sepal_length,
                'sepal_width': sepal_width,
                'petal_length': petal_length,
                'petal_width': petal_width,
                'species': species
                }

        data_json = json.dumps(data)

        # Add new part
        insert_command = "INSERT INTO data (time, part_id, component_id, processed, data)" \
                         " VALUES ('{}', {}, {}, {}, '{}')".format('now()',
                                                                   part_id,
                                                                   component_id,
                                                                   'False',
                                                                   data_json)

        self.cursor.execute(insert_command)

    def create_gt_database_template(self):
        """
        This function creates the gt logging database structure.
        It basically executes the commands from the gtlog.sql file under /DriverlessApp/Test
        :return:
        """
        pass
        with self.connection as cursor:
            fn = os.path.join(os.path.dirname(__file__), 'gtlog.sql')
            self.cursor.execute(open(fn, "r").read())

    def create_gt_database_template_old(self):
        """
        This function creates the gt logging database structure.
        It basically executes the commands from the gtlog.sql file under /DriverlessApp/Test
        :return:
        """
        pass
        with self.connection as cursor:
            fn = os.path.join(os.path.dirname(__file__), 'gtlogold.sql')
            self.cursor.execute(open(fn, "r").read())

    def print_table(self, table_name):

        try:
            self.cursor.execute('select * from {}'.format(table_name))
            entries = self.cursor.fetchall()

            for entry in entries:
                print(entry)
        except p.Error as exception:
            print(exception.pgerror)

    def print_column(self, column_name):
        current = self.connection.cursor(cursor_factory=e.DictCursor)
        current.execute("select * from playground")
        entries = current.fetchall()
        for entry in entries:
            print(entry[column_name])

    def print_column_names(self):
        """
        Prints all attributes of a table
        """
        counter = 1
        try:
            for col_names in self.cursor.description:
                # print(self.cursor.description[col_names][0])
                print("""Attribut{}: {:<5}, Typ: {:<5}, DisplaySize: {} InternalSize: {:<5}, Precision: {},
                      "Scale: {}, Null_Ok: {}"""
                      .format(counter,
                              col_names[0],
                              col_names[1],
                              col_names[2],
                              col_names[3],
                              col_names[4],
                              col_names[5],
                              col_names[6]))
                counter += 1
        except p.Error as exception:
            print(exception.pgerror)
        except Exception as general_exception:
            print(general_exception)

    def create_table(self, table_name, attribute_list):
        """
        This function creates a new table/relation in the database
        :param table_name: Name of the new table/relation. E.g. iris
        :param attribute_list: List with Attribute Strings. E.g.: ["sepal_length varchar (50) NOT NULL", "sepal_width
         varchar (40) NOT NULL", "species varchar (24) check species in ('setosa', 'versicolor', 'virginica')"]
        :return:
        """
        create_table_command = "CREATE TABLE {}(".format(table_name)

        try:
            for attribute in attribute_list:
                create_table_command = create_table_command + attribute + ","
            create_table_command = create_table_command[:-1]
            create_table_command += ")"
            self.cursor.execute(create_table_command)
        except p.Error as exception:
            print('Exception occured in create_table()')
            print(exception.pgerror)

    def insert_csv(self, file, tablename, sep=','):
        """
        Inserts data from .csv into database
        :param file: (str) Absolute or relative path to .csv file
        :param tablename: (str) Name of table
        :param sep: (str) Seperator
        :return:
        """
        filehandel = open(file, 'r')
        self.cursor.copy_from(filehandel, tablename, sep)
        self.connection.commit()

    def drop_table(self, table_name):
        """
        Drops table > Deletes Table and all values associated with it

        :param table_name: Name of table to be deleted
        :return: (str) Returns status string.
        """
        drop_command = "DROP TABLE {}".format(table_name)
        try:
            self.cursor.execute(drop_command)
            status = 'Table {} dropped'.format(table_name)
        except p.Error as exception:
            status = 'Exception occured in drop_table()'
            print(exception.pgerror)

    def clear_table(self, table_name):
        """
        Deletes all entries in table
        :param table_name: (str) Name of table to be cleared
        :return:
        """
        command = "DELETE FROM {}".format(table_name)
        try:
            self.cursor.execute(command)
            status = 'Alle Inhalte der Tabelle {} wurden erfolgreich geloescht '.format(table_name)
        except p.Error as exception:
            status = 'Fehler: Inhalte der Tabelle {} konnten nicht geloescht werden'.format(table_name)
            print(exception.pgerror)
        return status

    def query_last_entry(self, message_id):
        """
        This Function returns the last database Entry with given message id
        :param message_type: (int) Foreign Key for message_id table
        :return:
        """
        insert_command = "SELECT * FROM data WHERE tlocal=(SELECT MAX(tlocal) FROM data) AND type={}".format(message_id)
        self.cursor.execute(insert_command)
        result = self.cursor.fetchall()
        return result

    def close_connection(self):
        """
        This function closes the database connection
        :return:
        """
        self.cursor.close()
        self.connection.close()

    def commit_changes(self):
        """
        This function commits changes to the database.
        :return:
        """
        self.connection.commit()






























