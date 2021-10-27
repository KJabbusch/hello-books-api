from flask import Blueprint, jsonify, make_response, request
import sqlalchemy
from app import db
from app.models.kpop_group import KpopGroup
import json
import jsonschema
from jsonschema import validate

kpop_bp = Blueprint("kpop-groups", __name__, url_prefix="/kpop-groups")

kpop_schema = {
    "title": "Kpop Group Data",
    "description": "Contains group name, group members, and their music label.",
    "required": ["group", "members", "label"],
    "type": "object",
    "properties": {
        "group": {
            "type": "string",
        },
        "members": {
            "type": "string",
        },
        "label": {
            "type": "string"
        }
    }
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=kpop_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

@kpop_bp.route("", methods=['POST', 'GET'])
def handle_kpop_groups():
    # get all records
    if request.method == "GET":
        kpop_groups = KpopGroup.query.all()
        kpop_response = []
        for group in kpop_groups:
            kpop_response.append(group.to_dict())
        return jsonify(kpop_response), 200

    # add a new record
    elif request.method == "POST":
        request_body = request.get_json()
        if not validate_json(request_body):
            return make_response("Invalid request", 400)

        new_group = KpopGroup(
            group = request_body["group"],
            members = request_body["members"],
            label = request_body["label"]
        )

        db.session.add(new_group)
        db.session.commit()

        return make_response(f"Kpop Group {new_group.group} successfully created", 201)

@kpop_bp.route("/<group_id>", methods=["GET", "PUT", "DELETE"])
def handle_kpop_group(group_id):
    try:
        int(group_id)
    except:
        return make_response("ID given is not an integer.", 400)

    kpop_group = KpopGroup.query.get_or_404(group_id)
    # if not kpop_group:
    #     return "This group ID does not exist in the database.", 400

    # return the record
    if request.method == "GET":
        return jsonify(kpop_group.to_dict())
    # update the record
    elif request.method == "PUT":
        request_body = request.get_json()
        for key, value in request_body.items():
            if key in KpopGroup.__table__.columns.keys():
                setattr(kpop_group, key, value)

        db.session.commit()
        return jsonify(kpop_group.to_dict())

    # delete the record
    elif request.method == "DELETE":
        db.session.delete(kpop_group)
        db.session.commit()
        return make_response(f"Kpop Group {kpop_group.group} has been deleted from the database.", 200)
