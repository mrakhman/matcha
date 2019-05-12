from flask import blueprints, jsonify, abort, current_app, session

from models.user import User

users = blueprints.Blueprint("users", __name__)


@users.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f"Getting user #{user_id}")
    user = User.from_db(user_id)
    if user:
        return jsonify(user.get_view("public"))

    abort(404)


@users.route('/me', methods=['GET'])
def get_me():
    if 'username' in session and session['username']:
        return jsonify({'my_username': session['username']})
    abort(401)