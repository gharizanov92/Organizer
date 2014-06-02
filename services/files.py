from bottle import Bottle, route, run, abort, static_file, error, post, get, request
from utils.io import download_from_url

@post("/upload")
def upload():
    url = request.forms.get('url')
    print("url is: " + url)
    download_from_url(url)

@get("/download/<file>")
def download(file):
    return static_file(file, root='files')
