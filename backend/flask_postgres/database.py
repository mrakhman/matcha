import postgresql
from .query import Query


class DataBase(object):

    def __init__(self, uri=""):
        self.uri = uri
        self.db = postgresql.open(uri)
        self._table_columns = {}

    def get_columns(self, table_name):
        """
            Get the columns name information
        """
        columns = self.db.prepare(
            '''SELECT column_name 
            FROM information_schema.columns
            WHERE table_name = $1
            ''')(table_name)
        return [row[0] for row in columns]

    def table(self, table_name):
        """
            A queryable table of the database

            name: the name of the table to query

            return: a Query object
        """
        if table_name in self._table_columns:
            columns = self._table_columns[table_name]
        else:
            columns = self.get_columns(table_name)
            self._table_columns[table_name] = columns

        return Query(self.db, table_name, columns)

    def close(self):
        self.db.close()
