import http
from datetime import datetime

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.notification import Notification
from utils.security import authorised_only
from utils.form_validator import check_fields


notifications = blueprints.Blueprint("notifications", __name__)


@notifications.route("/", methods=["GET"])
@authorised_only
def get_my_notifications():
    my_notifications = Notification.get_user_notifications(g.current_user.id)
    return jsonify(notifications=my_notifications)


@notifications.route("/<int:notification_id>/is_read", methods=['POST'])
@authorised_only
def mark_as_read(notification_id):
    notification = Notification.get_by_id(notification_id)
    if not notification or notification.user_id != g.current_user.id:
        abort(http.HTTPStatus.NOT_FOUND)
    notification.is_read = True
    notification.update()
    return jsonify(ok=True)


@notifications.route("/all_read", methods=["GET"])
@authorised_only
def all_read():
    if Notification.mark_all_read(g.current_user.id):
        return jsonify({"ok": True})
    return jsonify({"ok": False})


# @notifications.route("/send", methods=["POST"])
# @authorised_only
# def send_notification():
#     req_data = request.get_json()
#     form_values = {
#         'user_id': {
#             'required': True,
#             'default': None,
#             'type': int,
#             'validator': None
#         },
#         'text': {
#             'required': True,
#             'default': None,
#             'type': str,
#             'validator': None
#         },
#         'type': {
#             'required': True,
#             'default': None,
#             'type': str,
#             'validator': None
#         }
#     }
#     check_fields(req_data, form_values)
#     notification = Notification.from_dict(req_data)
#     notification.create()
#     return jsonify({"ok": True})


@notifications.route("/add_history/<int:profile_id>", methods=["GET"])
@authorised_only
def add_history(profile_id):
    Notification.add_to_history(g.current_user.id, profile_id)
    return jsonify({"ok": True})
