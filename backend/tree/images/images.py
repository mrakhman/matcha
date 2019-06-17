import http
import os
import uuid

from flask import blueprints, jsonify, abort, g, request, current_app, send_from_directory, url_for

from models.image import Image
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
        file = request.files.get('user_image')
        source = 'user_image'
        if not file:
            abort(http.HTTPStatus.BAD_REQUEST)

    # print('Hey, source is: ', source)

    if allowed_file(file.filename):
        filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        current_user = g.current_user

        if source == 'profile_image':
            current_user.profile_image = url_for('images.get_image', filename=filename, _external=True)
            current_user.update()
            return jsonify({"ok": True})

        if source == 'user_image':
            new_image = Image.from_dict({
                'user_id': current_user.id,
                'image_src': url_for('images.get_image', filename=filename, _external=True)
            })
            new_image.create()
            return jsonify(ok=True)

    return jsonify({"ok": False})


@images.route('/my', methods=['GET'])
@authorised_only
def get_user_images():
    current_user = g.current_user
    user_images = Image.get_user_images(current_user.id)
    return jsonify(user_images=user_images)
    # return jsonify({"images": user_images.get_view('public')})


@images.route('/delete', methods=['POST'])
@authorised_only
def delete_image():
    req_data = request.get_json()
    current_app.logger.info(f"Here we are, the request is: {req_data}")
    print(req_data)
    del_img = req_data['id']
    current_user = g.current_user

    if del_img and current_user:
        Image.delete(current_user.id, del_img)
        return jsonify(ok=True)
    abort(http.HTTPStatus.BAD_REQUEST)
    # If image id doesn't exist in db - no response is returned - same success ok=True



