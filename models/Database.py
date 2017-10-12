from PyQt4.QtSql import *
import psycopg2
import ast
import psycopg2 as p


class DatabaseConnection(object):
    def __init__(self):
        super(DatabaseConnection, self).__init__()
        self.seqnr_slam = 0
        self.run = 1
        self.car = 7000
        self.connected = False
        self.db_name = None
        self.db_user = None
        self.db_host = None
        self.db_password = None
        self.connection = None
        self.cursor = None

    def is_connected(self):
        """
        Function returns database connection status.
        :return: (bool) Returns True if database connection is active and False otherwise.
        """
        return self.connected

    def open(self, host_name, user_name, database_name, password):
        try:
            self.db_name = database_name
            self.db_user = user_name
            self.db_host = host_name
            self.db_password = password
            self.connection = p.connect("dbname ='{}' user='{}' host='{}' password='{}'".format(database_name,
                                                                                                user_name,
                                                                                                host_name,
                                                                                                password))
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

    def get_data(self):
        """
        Returns data stored in database as dict instead of JSON
        :return: (dict): data as JSON. Returns 'None' in case of error
        """
        query = "SELECT * FROM data"
        self.cursor.execute(query)
        # result = self.cursor.fetchall()
        # Transform list of tuples of dicts into list of dicts
        data = []
        for index, record in enumerate(self.cursor):
            column = list()
            column.append(record[0])
            column.append(record[1])
            column.append(record[2])
            column.append(record[3])
            column.append(record[4])
            column.append(record[5])
            column.append(record[6])
            data.append(column)
        return data

    def get_unprocessed_data(self):
        """
        Function returns list with all unprocessed database entries
        :return: (list)
        """
        query = "SELECT * FROM data WHERE processed = 'False'"
        self.cursor.execute(query)
        # result = self.cursor.fetchall()
        # Transform list of tuples of dicts into list of dicts
        data = []
        for record in self.cursor:

            id = record[0]  # id (uuid)
            time = record[1]  # time
            part_id = record[2]  # part_id
            component_id = record[3]  # component_id
            processed = record[4]  # processed
            classified = record[5]  # classified
            data_record = record[6]  # data

            data_json = data_record
            data_json.update({"PartId": part_id})
            data.append(data_json)

        # Flag all data as processd
        query = "UPDATE data SET processed = 'True' WHERE processed = 'False'"
        self.cursor.execute(query)

        return data

    def get_training_data(self):
        """
        Get all Database entries where classified = True
        :return: (dict) All data entries and PartId
        """
        query = "SELECT * FROM data WHERE classified = 'True'"
        self.cursor.execute(query)
        # result = self.cursor.fetchall()
        # Transform list of tuples of dicts into list of dicts
        data = []
        for record in self.cursor:
            id = record[0]  # id (uuid)
            time = record[1]  # time
            part_id = record[2]  # part_id
            component_id = record[3]  # component_id
            processed = record[4]  # processed
            classified = record[5]  # classified
            data_record = record[6]  # data

            data_json = data_record
            data_json.update({"PartId": part_id})
            data.append(data_json)
        return data

    def get_column_names(self):
        """
        Function returns list of column names
        :return:
        """
        query = "SELECT * FROM data"
        self.cursor.execute(query)
        # result = self.cursor.fetchall()
        # Transform list of tuples of dicts into list of dicts
        header = []
        for description in self.cursor.description:
            header.append(description[0])
        return header

    def delete_entry(self, uuid):
        """
        Function deletes a database entry with given uuid
        :param uuid: uuid of entry which should be deleted
        :return:
        """
        query = "DELETE FROM data WHERE id = '{}'".format(uuid)
        self.cursor.execute(query)

    def delete_table_entries(self):
        query = "DELETE FROM data"
        self.cursor.execute(query)

    def get_host_name(self):
        return self.db_host

    def get_db_name(self):
        return self.db_name

    def count_db_entries(self):
        query = "SELECT COUNT(*) FROM data"
        self.cursor.execute(query)
        nr_db_entries = self.cursor.fetchone()
        nr_db_entries = nr_db_entries[0]
        return nr_db_entries

    def count_training_data(self):
        query = "SELECT COUNT(*) FROM data WHERE classified = 'True'"
        self.cursor.execute(query)
        nr_training_data = self.cursor.fetchone()
        nr_training_data = nr_training_data[0]
        return nr_training_data

    def count_processed_data(self):
        query = "SELECT COUNT(*) FROM data WHERE processed = 'True'"
        self.cursor.execute(query)
        nr_processed_data = self.cursor.fetchone()
        nr_processed_data = nr_processed_data[0]
        return nr_processed_data





