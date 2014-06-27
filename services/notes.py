from bottle import Bottle, route, run, abort, static_file, error, post, get, request
from utils.io import *
from bson.objectid import ObjectId
from bson.json_util import dumps
from utils.dao import *

@post("/notes/add")
def add_note():
    caption = request.forms.get('caption')
    body=request.forms.get('body')
    _id = str(ObjectId())
    print(locals())
    db.notes.save(locals())