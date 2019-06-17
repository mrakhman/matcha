import http

from flask import blueprints, jsonify, abort, g

from models.notification import Notification
from utils.security import authorised_only

notifications = blueprints.Blueprint("notifications", __name__)


@notifications.route("/", methods=["GET"])
@authorised_only
def get_my_notifications():
    my_notifications = Notification.get_user_notifications(g.current_user.id)
    return jsonify(notifications=my_notifications)


@notifications.route("/<int:notification_id>/read", methods=['POST'])
@authorised_only
def mark_as_read(notification_id):
    notification = Notification.get_by_id(notification_id)
    if not notification or notification.user_id != g.current_user.id:
        abort(http.HTTPStatus.NOT_FOUND)
    notification.read = True
    notification.update()
    return jsonify(ok=True)