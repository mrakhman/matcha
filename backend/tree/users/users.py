from flask import blueprints, jsonify, abort

from models.user import User

users = blueprints.Blueprint("users", __name__)


@users.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.from_db(user_id)
    if user:
        return jsonify(user.get_view("public"))

    abort(404)

