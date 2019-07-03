import http

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.history import History
from utils.security import authorised_only


history = blueprints.Blueprint("history", __name__)


# @history.route("/add/<int:profile_id>", methods=["GET"])
# @authorised_only
# def add_history(profile_id):
#     History.add_to_history(g.current_user.id, profile_id)
#     return jsonify({"ok": True})


@history.route("/get", methods=["GET"])
@authorised_only
def get_my_history():
    my_history = History.get_user_history(g.current_user.id)
    return jsonify(history=my_history)


@history.route("/delete", methods=["DELETE"])
@authorised_only
def delete_history():
    if History.delete_history(g.current_user.id):
        return jsonify({"ok": True})
    return jsonify({"ok": False})
