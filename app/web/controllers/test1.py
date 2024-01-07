from flask import current_app

from app.web.resources import WsgiServices

WsgiServices().wire(modules=[__name__])

app = current_app
@app.route('/hello')
def hello():
    return {'hello': 'world'}
