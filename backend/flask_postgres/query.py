from postgresql.api import Connection
from .row import Row


class Query(object):
    """
        A query Class which recursive generate the query-string
    """

    def __init__(self, db: Connection, table_name: str, columns: [], sql=None):
        if not sql:
            sql = f'SELECT * FROM {table_name}'
        self.db = db
        self.sql = sql
        self.columns = columns
        self.table_name = table_name

    def filter(self, criteria):
        """
            Implement the "WHERE" statement of the standard sql
        """
        key_word = "AND" if "WHERE" in self.sql else "WHERE"
        sql = self.sql + " %s %s" % (key_word, criteria)
        return Query(self.db, self.table_name, self.columns, sql)

    def order_by(self, criteria):
        """
            Implement the "Order by" statement of the standard sql
        """
        return Query(self.db, self.table_name, self.columns, self.sql + " ORDER BY %s" % criteria)

    def group_by(self, criteria):
        """
            Implement the "Group by" statement of the standard sql
        """
        return Query(self.db, self.table_name, self.columns, self.sql + " GROUP BY %s" % criteria)

    @property
    def rows(self):
        """
            Execute the generated query on the database and return a list of Row Objects
        """
        print(self.sql)
        statement = self.db.prepare(self.sql)
        result = statement()
        return [Row(zip(self.columns, fields), self.table_name) for fields in result]
