import http
import os
import uuid

from flask import blueprints, jsonify, abort, g, request, current_app, send_from_directory, url_for

from utils.security import authorised_only

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

images = blueprints.Blueprint("images", __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@images.route('/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@images.route('/upload', methods=['POST'])
@authorised_only
def upload_image():
    file = request.files.get('profile_image')
    source = 'profile_image'
    if not file:
        file = request.files.get('user_images')
        source = 'user_images'
        if not file:
            abort(http.HTTPStatus.BAD_REQUEST)

    print('Hey, source is: ', source)

    if allowed_file(file.filename):
        filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if source == 'profile_image':
            current_user = g.current_user
            current_user.profile_image = url_for('images.get_image', filename=filename, _external=True)
            current_user.update()
            return jsonify({"ok": True})

        if source == 'user_images':
            pass
        # new_image = Image.from_hui()
        # add_user_image # Твой ООП меня добьет!
        # TODO: update user images list
    return jsonify({"ok": False})
