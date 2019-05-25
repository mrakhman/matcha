class Row(object):
    """
        A row Class dynamically implemented for each table
    """

    def __init__(self, fields, table_name):
        """
            fields: A list of [column_name : value of column]

            table_name: the name of the table
        """
        # Assign the name of the current table to the class
        self.__class__.__name__ = table_name + "_Row"

        for name, value in fields:
            setattr(self, name, value)
