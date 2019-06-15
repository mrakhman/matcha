import datetime

from flask.json import JSONEncoder

from models.model import Model


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat('T')
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Model):
            return obj.get_view()
        return JSONEncoder.default(self, obj)
