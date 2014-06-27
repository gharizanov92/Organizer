from bottle import Bottle, route, run, abort, static_file, error
from mako.template import Template
from utils.io import get_files

# Security - restrict view templates
@route('/views/<template>')
def restricted(template):
    print("Unauthorized attempt to accesss template " + template)
    abort(401, "Sorry, access denied.")

# Define routes
@route('/')
def hello():
    template = Template(filename='views/index.html')
    return template.render()

@route('/index')
def index():
    template = Template(filename='views/index.html')
    return template.render()

@route('/manager')
def manager():
    template = Template(filename='views/manager.html')
    return template.render()

@route('/notes')
def notes():
    template = Template(filename='views/notes.html')
    return template.render()

@route('/todo')
def todo():
    template = Template(filename='views/todo.html')
    return template.render()

@route('/files')
def file_list():
    get_files()
    template = Template(filename='views/files.html')
    return template.render(files = get_files())

# Define modules/routes
import services.rest
import services.files
import services.notes

# Serve static content
@route('/<static_file_type>/<filename>')
def server_static(static_file_type, filename):
    return static_file(filename, root=str(static_file_type))

run(host='0.0.0.0', port=8080, debug=True)