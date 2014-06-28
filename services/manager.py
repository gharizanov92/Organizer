from bottle import *
from utils.io import *
from bson.objectid import ObjectId
from bson.json_util import dumps
from utils.db import *
import datetime
from utils.auth import abort_if_not_authorized


@post("/reports/add")
def add_report():
    abort_if_not_authorized()
    _id = str(ObjectId())
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    category = request.forms.get('category')
    amount = float(request.forms.get('amount'))
    db.reports.save(locals())


@get("/categories/all")
def get_categories():
    abort_if_not_authorized()
    reports = db.reports.find()
    categories_candidates = []

    for each in reports:
        categories_candidates.append(each['category'])

    categories = {}

    for each in categories_candidates:
        categories[each] = ""

    categories = list(categories.keys())
    return str(categories)
