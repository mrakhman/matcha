import http
import os
import uuid

from flask import abort, blueprints, current_app, g, jsonify, redirect, request, url_for
from minio.signer import presign_v4

from models.image import Image
from modules import storage
from utils.security import authorised_only

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

images = blueprints.Blueprint("images", __name__)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@images.route('/<filename>', methods=['GET'])
def get_image(filename):
	bucket_name = current_app.config.get('IMAGES_BUCKET_NAME')
	access_key = current_app.config.get('MINIO_ACCESS_KEY')
	secret_key = current_app.config.get('MINIO_SECRET_KEY')
	storage_endpoint = current_app.config.get('STORAGE_ENDPOINT')

	url = presign_v4('GET', f'{storage_endpoint}/{bucket_name}/{filename}', access_key, secret_key)
	return redirect(url)


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

	if source == 'user_image':
		user_images = Image.get_user_images(g.current_user.id)
		if len(user_images) >= 4:
			abort(http.HTTPStatus.FORBIDDEN)

	if allowed_file(file.filename):
		bucket_name = current_app.config.get('IMAGES_BUCKET_NAME')
		filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
		file.seek(0, os.SEEK_END)
		file_length = file.tell()
		file.seek(0, os.SEEK_SET)
		storage.connection.put_object(bucket_name, filename, file, file_length, file.mimetype)
		current_user = g.current_user

		if source == 'profile_image':
			# Delete old from bucket
			if current_user.profile_image:
				old_filename = current_user.profile_image.split('/')[-1]
				storage.connection.remove_object(bucket_name, old_filename)
			# Update
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


@images.route('/<int:image_id>', methods=['DELETE'])
@authorised_only
def delete_image(image_id):
	img = Image.get_by_id(image_id)
	if img and img.user_id == g.current_user.id:
		img.delete()
		bucket_name = current_app.config.get('IMAGES_BUCKET_NAME')
		filename = img.image_src.split('/')[-1]
		storage.connection.remove_object(bucket_name, filename)
		return jsonify(ok=True)
	abort(http.HTTPStatus.NOT_FOUND)
