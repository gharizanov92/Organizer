from bottle import *
from utils.io import *
from utils.auth import abort_if_not_authorized


@post("/upload")
def upload():
    abort_if_not_authorized()
    url = request.forms.get('url')
    download_from_url(url)


@get("/download/<file>")
def download(file):
    abort_if_not_authorized()
    return static_file(file, root='files')


@route("/files/all")
def list_files():
    abort_if_not_authorized()
    return str(get_files())
