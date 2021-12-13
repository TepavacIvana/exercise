from datetime import datetime
import uuid

from flask import Flask, request
from my_app.notes import CreateNoteSchema, UpdateNoteSchema

app = Flask(__name__)

storage = {}


def create_uuid():
    unique_id = uuid.uuid1()
    return str(unique_id)


@app.route('/api/note', methods=['POST'])
def create_note():
    errors = CreateNoteSchema().validate(request.json)
    if errors:
        return errors, 400

    key = create_uuid()
    value = dict(**request.json, time_created=datetime.now())
    storage[key] = value

    return storage[key]


@app.route('/api/note', methods=['GET'])
def get_note():
    return storage


@app.route('/api/note/<uuid>', methods=['GET'])
def single_note(uuid):
    if uuid not in storage:
        return {'message': 'Not found'}, 404
    return storage[uuid]


@app.route('/api/note/<uuid>', methods=['PATCH'])
def update_note(uuid):
    if uuid not in storage:
        return {'message': 'Not found'}, 404

    errors = UpdateNoteSchema().validate(request.json)
    if errors:
        return errors, 400
    storage[uuid].update(**request.json, time_updated=datetime.now())

    return storage[uuid]


@app.route('/api/note/<uuid>', methods=['DELETE'])
def delete_note(uuid):
    if uuid not in storage:
        return {'message': 'Not found'}, 404
    del storage[uuid]
    return {'message': 'Note has been deleted'}
