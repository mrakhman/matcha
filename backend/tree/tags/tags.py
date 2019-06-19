import http
import os
import uuid

from flask import blueprints, jsonify, abort, g, request, current_app, send_from_directory, url_for

from models.tag import Tag
from utils.security import authorised_only


tags = blueprints.Blueprint("tags", __name__)

@tags.route('/create', methods=['POST'])
@authorised_only
def create_tags():
    pass
