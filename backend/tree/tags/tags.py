import http
import os
import uuid

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.tag import Tag
from utils.form_validator import check_fields
from utils.security import authorised_only

tags = blueprints.Blueprint("tags", __name__)


@tags.route('/create_update', methods=['POST'])
@authorised_only
def create_update_tags():
    req_data = request.get_json()
    form_values = {
        "tags": {
            'required': False,
            'default': None,
            'type': [],
            'validator': None
        }
    }
    current_app.logger.info(f"Here we are, the request is: {req_data}")
    check_fields(req_data, form_values)
    current_user = g.current_user
    # Add tag validation

    # if len(form_values["tags"]) > 0:

    # Update
    if Tag.get_user_tags(current_user.id):
        user_tags = Tag.from_dict(req_data)
        user_tags.update(current_user.id)
        return jsonify({"ok": True})

    # Create
    user_tags = Tag.from_dict(req_data)
    user_tags.create(current_user.id)
    return jsonify({"ok": True})

    # else:
    #     # Delete
    #     if Tag.get_user_tags(current_user.id):
    #         user_tags = Tag.from_dict(req_data)
    #         user_tags.delete(current_user.id)
    #         return jsonify({"ok": True})
    #
    #     else:
    #         # there was no tag and no tag inserted
    #         return jsonify({"ok": False})





