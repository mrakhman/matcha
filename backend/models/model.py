class Model:
    _fields = {}
    _views = {}

    def __init__(self):
        # Init all attributes:
        for f, props in self._fields.items():
            setattr(self, f, props['default'])

        self.id = None

    def create(self):
        pass

    def update(self):
        pass

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
        return cls()

    def check_attributes(self):
        for f, props in self._fields.items():
            if props['required'] and not getattr(self, f, None):
                raise ValueError(f"{f} is required for {self.__class__.__name__}")

            if props['required'] and props['validator'] and not props['validator'](getattr(self, f, None)):
                raise ValueError(f"{f}({getattr(self, f)}) did not pass validator for {self.__class__.__name__}")

    def is_valid(self):
        try:
            self.check_attributes()
        except ValueError:
            return False
        return True

    def get_view(self, view="public"):
        dict_obj = {}
        if view not in self._views:
            return dict_obj

        for f in self._views[view]['fields']:
            dict_obj[f] = getattr(self, f)
        return dict_obj
