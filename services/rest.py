from bottle import Bottle, route, run, abort, static_file, error, post, get, request

@route('/test1')
def test():
    users = {
        "name" : "user",
        "age" : 22,
        "gender" : "male"
    }
    return users