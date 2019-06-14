import datetime
import http
import os

from flask import blueprints, jsonify, abort, current_app, session, request

from models.user import User
from models.image import Image
from utils.form_validator import check_fields
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

images = blueprints.Blueprint("images", __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@images.route('/upload', methods=['POST'])
def upload_image():
	# file = (request.form, request.files)
	current_app.logger.debug(f"Req_data is {request.files}")
	print(request.files['image'])
	file = request.files.get('image')
	if not file:
		abort(http.HTTPStatus.BAD_REQUEST)
	# current_app.logger.debug(f"Type of file is {type(file)}")
	if allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))
	 	# TODO: save to database
		return jsonify({"ok": True})
	return jsonify({"ok": False})


@images.route('/profile_image', methods=['GET'])
def profile_image():
	current_user_id = session.get('user_id')
	if current_user_id:
		get_profile_imageimage = Image.get_profile_image(int(current_user_id))
		if profile_image:
			return jsonify({"user": current_user.get_view('personal')})
	abort(401)