from PyQt4.QtSql import *
import ast


class DatabaseConnection(QSqlDatabase):
    def __init__(self):
        super(QSqlDatabase, self).__init__()
        self.connection = self.addDatabase("QPSQL")
        pass

    def is_connected(self):
        """
        Function returns database connection status.
        :return: (bool) Returns True if database connection is active and False otherwise.
        """
        return self.connection.isOpen()

    def print_hello(self):
        print("Hallo")

    def open(self, host_name, user_name, database_name, password):
        self.connection.setHostName(host_name)
        self.connection.setDatabaseName(database_name)
        self.connection.setPassword(password)
        self.connection.setUserName(user_name)
        if self.connection.open():
            return True
        else:
            return False

    def get_num_rows(self, selected_table_name):
        pass
        # Update number of Rows and Columns. Safe DB Content to memory
        query = QSqlQuery()
        query.setForwardOnly(True)
        query.prepare("SELECT * FROM {}".format(selected_table_name))
        query.exec_()
        num_rows = query.size()

        return num_rows

    def get_num_columns(self, selected_table_name):
        pass
        # Update number of Rows and Columns. Safe DB Content to memory
        query = QSqlQuery()
        query.setForwardOnly(True)
        query.prepare("SELECT * FROM {}".format(selected_table_name))
        query.exec_()
        num_columns = query.record().count()

        return num_columns

    def get_tables(self):
        tables = self.connection.tables()
        return tables

    def get_unprocessed_data(self):
        """
        Function returns list with all unprocessed database entries
        :return: (list)
        """

        query = QSqlQuery()
        query.setForwardOnly(True)
        query.prepare("SELECT data FROM data WHERE processed = 'False'")
        query.exec_()
        data = []
        while query.next():  # query successfully executed
            data_str = str(query.value(0).toString())
            # data_json = ast.literal_eval(data_str)
            data.append(data_str)
        return data


    def get_data(self, uuid):
        """
        Returns data stored in database as dict instead of JSON
        :return: (dict): data as JSON. Returns 'None' in case of error
        """
        # Update number of Rows and Columns. Safe DB Content to memory
        query = QSqlQuery()
        query.setForwardOnly(True)
        query.prepare("SELECT data FROM data WHERE id = '{}'".format(uuid))
        query.exec_()
        data = None
        if query.isActive():        # query successfully executed
            query.next()
            data_str = str(query.value(0).toString())
            data_json = ast.literal_eval(data_str)
        return data_json


    def get_unprocessed_data2(self):
        """
        Function returns list with all unprocessed database entries
        :return: (list)
        """

        query = QSqlQuery()
        query.setForwardOnly(True)
        query.prepare("SELECT data FROM data WHERE processed = 'False'")
        query.exec_()
        data = []
        data = None
        if query.isActive():        # query successfully executed
            query.next()
            data_str = str(query.value(0).toString())
            data_json = ast.literal_eval(data_str)
        return data_json





