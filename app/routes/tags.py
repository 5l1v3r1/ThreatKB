from app import app, db, admin_only, auto
from app.models import tags
from flask import abort, jsonify, request
from flask.ext.login import login_required
import json


@app.route('/ThreatKB/tags', methods=['GET'])
@auto.doc()
@login_required
def get_all_tags():
    """Return all tags
    Return: list of tag dictionaries"""
    entities = tags.Tags.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/ThreatKB/tags/<int:id>', methods=['GET'])
@auto.doc()
@login_required
def get_tags(id):
    """Return tag associated with given id
    Return: tag dictionary"""
    entity = tags.Tags.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/ThreatKB/tags', methods=['POST'])
@auto.doc()
@login_required
def create_tags():
    """Create new tag
    From Data: text"""
    created_tag = create_tag(request.json['text'])
    return jsonify(created_tag.to_dict()), 201


def create_tag(tag_text):
    entity = tags.Tags(
        text=tag_text
    )
    db.session.add(entity)
    db.session.commit()
    return entity


@app.route('/ThreatKB/tags/<int:id>', methods=['PUT'])
@auto.doc()
@login_required
@admin_only()
def update_tags(id):
    """Update tag associatd with given id
    From Data: text
    Return: tag dictionary"""
    entity = tags.Tags.query.get(id)
    if not entity:
        abort(404)
    entity = tags.Tags(
        text=request.json['text'],
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/ThreatKB/tags/<int:id>', methods=['DELETE'])
@auto.doc()
@login_required
@admin_only()
def delete_tags(id):
    """Delete tag associated with given id
    Return: None"""
    entity = tags.Tags.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204
