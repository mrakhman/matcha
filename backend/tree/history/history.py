from flask import blueprints, jsonify, g

from models.history import History
from utils.security import authorised_only

history = blueprints.Blueprint("history", __name__)


@history.route("/", methods=["GET"])
@authorised_only
def get_my_history():
    my_history = History.get_user_history(g.current_user.id)
    return jsonify(history=my_history)


@history.route("/", methods=["DELETE"])
@authorised_only
def delete_history():
    if History.delete_history(g.current_user.id):
        return jsonify({"ok": True})
    return jsonify({"ok": False})
