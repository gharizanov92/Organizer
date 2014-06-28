from bottle import *
from utils.io import *
from bson.objectid import ObjectId
from utils.db import *
from utils.auth import abort_if_not_authorized


@post("/todos/add")
def add_todo():
    abort_if_not_authorized()
    text = request.forms.get('text')
    _id = str(ObjectId())
    db.todos.save(locals())


@post("/todos/delete/<_id>")
def remove_todo(_id):
    abort_if_not_authorized()
    db.todos.remove(locals())
