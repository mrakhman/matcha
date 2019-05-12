from flask import blueprints, jsonify, session

auth = blueprints.Blueprint("auth", __name__)


@auth.route('/login', methods=['GET'])  # TODO
def pseudo_login():
    session['username'] = "su"
    return jsonify({'status': 'ok'})


@auth.route('/logout', methods=['GET'])
def pseudo_logout():
    del session['username']
    return jsonify({'status': 'ok'})


@auth.route('/whoami', methods=['GET'])
def whoami():
    return jsonify({'my_username': session.get('username')})
