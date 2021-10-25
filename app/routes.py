from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.kpop_group import KpopGroup
import json
import jsonschema
from jsonschema import validate

kpop_bp = Blueprint("kpop-groups", __name__, url_prefix="/kpop-groups")

kpop_schema = {
    "key-values":
        {
        "group": {"type", "string"},
        "members": {"type", "string"},
        "label": {"type", "string"}
    },
    "required": ["group", "members", "label"]
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=kpop_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

@kpop_bp.route("", methods=['POST', 'GET'])
def handle_kpop_groups():
    if request.method == "GET":
        kpop_groups = KpopGroup.query.all()
        kpop_response = []
        for group in kpop_groups:
            kpop_response.append({
                "id": group.id,
                "group": group.group,
                "members": group.members,
                "label": group.label
            })
        return jsonify(kpop_response)
    elif request.method == "POST":
        request_body = request.get_json()
        # check that request body has all Kpop Group attributes
        to_check = json.dumps(request_body)
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

@kpop_bp.route("/<group_id>", methods=["GET"])
def handle_kpop_group(group_id):
    group_id = int(group_id)
    kpop_groups = KpopGroup.query.all()
    for group in kpop_groups:
        if group.id == group_id:
            return {
                "id": group.id,
                "group": group.group,
                "members": group.members,
                "label": group.label
            }