import os
import uuid

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.like import Like
from utils.form_validator import check_fields
from utils.security import authorised_only

likes = blueprints.Blueprint("likes", __name__)
