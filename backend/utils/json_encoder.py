import datetime
from decimal import Decimal

from flask.json import JSONEncoder

from models.model import Model


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat('T') + 'Z'
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Model):
            return obj.get_view()
        if isinstance(obj, Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)
