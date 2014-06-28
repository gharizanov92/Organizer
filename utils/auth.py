from bottle import request, abort

def abort_if_not_authorized():
    username = request.get_cookie("account", secret='organizer-project')
    print(username)
    if not username:
        abort(401, "Sorry, access denied.")