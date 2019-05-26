from flask.json import JSONEncoder
import datetime
from models.user import User


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat('T')
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, User):
            return obj.get_view()
        return JSONEncoder.default(self, obj)
