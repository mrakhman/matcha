from typing import Union, List

import postgresql.types

from db import db


class Queries:
    @staticmethod
    def query(query: str, one: bool = False):
        def f(*args):
            prepared_query = db.connection.prepare(query)
            if one:
                return prepared_query.first(*args)
            return prepared_query(*args)
        return f


class Model:
    _fields: dict
    _views: dict

    def __init__(self):
        # Init all attributes:
        for f, props in self._fields.items():
            setattr(self, f, props['default'])

        self.id = None

    def create(self):
        raise NotImplemented()

    def update(self):
        raise NotImplemented()

    @classmethod
    def from_dict(cls, d):
        obj = cls()
        for f, props in obj._fields.items():
            if f in d:
                setattr(obj, f, d[f])
        obj.check_attributes()
        return obj

    @classmethod
    def from_db(cls, obj_id):
        raise NotImplemented()

    def check_attributes(self):
        for f, props in self._fields.items():
            if props['required'] and not getattr(self, f, None):
                raise ValueError(f"{f} is required for {self.__class__.__name__}")

            if props['required'] and props['validator'] and not props['validator'](getattr(self, f, None)):
                raise ValueError(f"{f}({getattr(self, f)}) did not pass validator for {self.__class__.__name__}")

    def is_valid(self) -> bool:
        try:
            self.check_attributes()
        except ValueError:
            return False
        return True

    def get_view(self, view="public") -> dict:
        dict_obj = {}
        if view not in self._views:
            return dict_obj

        for f in self._views[view]['fields']:
            dict_obj[f] = getattr(self, f)
        return dict_obj

    @staticmethod
    def dict_from_row(row: postgresql.types.Row) -> dict:
        result = {}
        for key in row.keys():
            result[key] = row[key]
        return result

    @classmethod
    def from_db_row(cls, row: Union[postgresql.types.Row, List[postgresql.types.Row]]):
        if type(row) == list:
            return [cls.from_db_row(r) for r in row]
        data = cls.dict_from_row(row)
        return cls.from_dict(data)
