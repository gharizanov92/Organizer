from bottle import Bottle, route, run, abort, static_file, error, post, get, request
from utils.io import *

@post("/upload")
def upload():
    url = request.forms.get('url')
    download_from_url(url)

@get("/download/<file>")
def download(file):
    return static_file(file, root='files')

@route("/files/all")
def list_files():
    return str(get_files())
