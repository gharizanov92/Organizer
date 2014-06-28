from bottle import Bottle, route, run, abort, static_file, error, post, get, request, Response
from utils.io import *
from bson.objectid import ObjectId
from bson.json_util import dumps
from utils.db import *
from utils.auth import abort_if_not_authorized

@post("/notes/add")
def add_note():
    abort_if_not_authorized()
    caption = request.forms.get('caption')
    body=request.forms.get('body')
    _id = str(ObjectId())
    db.notes.save(locals())

@post("/notes/remove/<_id>")
def remove_note(_id):
    abort_if_not_authorized()
    db.notes.remove(locals())

@post("/notes/update/<_id>")
def update_note(_id):
    abort_if_not_authorized()
    caption = request.forms.get('caption')
    body=request.forms.get('body')
    print(locals())
    db.notes.update({"_id":_id}, locals())
