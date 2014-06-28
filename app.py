from bottle import Bottle, route, run, abort,
static_file, error, response, request, post, redirect
from mako.template import Template
from utils.io import get_files
from utils.db import db
from services.manager import *
import datetime
import time


@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie("account", username, secret='organizer-project')
        redirect("/notes")
    else:
        redirect("/")


@post('/register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if db.users.find_one({"username": username}):
        abort(500, "User already exists")
    else:
        db.users.save({
            "_id": str(ObjectId()),
            "username": username,
            "password": password
        })


# Define routes
@route('/')
def hello():
    print("/")
    template = Template(filename='views/index.html')
    return template.render()


@route('/index')
def index():
    print("/index")
    template = Template(filename='views/index.html')
    return template.render()


@route('/manager')
def manager():
    print("/manager")
    abort_if_not_authorized()
    template = Template(filename='views/manager.html')
    now = datetime.datetime.now()
    daily_report = list(db.reports.find({"day": now.day}))
    monthly_report = list(db.reports.find({"month": now.month}))

    total = db.reports.aggregate([
        {"$match": {"day": now.day}},
        {"$group": {"_id": "$day", "total": {"$sum": "$amount"}}}])

    today = {
        'total': total['result'][0]['total'],
        'entries': daily_report
    }

    total = db.reports.aggregate([
        {"$match": {"month": now.month}},
        {"$group": {"_id": "$month", "total": {"$sum": "$amount"}}}])

    this_month = {
        'total': total['result'][0]['total'],
        'entries': monthly_report
    }

    categories = eval(get_categories())
    return template.render(
        daily_report=today,
        monthly_report=this_month,
        categories=categories
    )


@route('/notes')
def notes():
    print("/notes")
    abort_if_not_authorized()
    template = Template(filename='views/notes.html')
    notes = list(db.notes.find())
    return template.render(notes=notes)


@route('/todo')
def todo():
    print("/todo")
    abort_if_not_authorized()
    todos = list(db.todos.find())
    template = Template(filename='views/todo.html')
    return template.render(todos=todos)


@route('/files')
def file_list():
    print("/files")
    abort_if_not_authorized()
    template = Template(filename='views/files.html')
    return template.render(files=get_files())


@route('/test')
def file_list():
    template = Template(filename='views/testing.html')
    return template.render()


# Security - restrict view templates
@route('/views/<template>')
def restricted(template):
    print("Unauthorized attempt to accesss template " + template)
    abort(401, "Sorry, access denied.")


def check_login(username, password):
    users = list(db.users.find({"username": username, "password": password}))
    return len(users) > 0


# Define modules/routes
import services.files
import services.notes
import services.todos
import services.manager


# Serve static content
@route('/<static_file_type>/<filename>')
def server_static(static_file_type, filename):
    return static_file(filename, root=str(static_file_type))


run(host='0.0.0.0', port=8080, debug=True)
