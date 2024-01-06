# from app.web.startup import Program

# if __name__ != '__main__':
#     program = Program()
#     program.run()

from importlib import import_module

from flask import Flask
#from flask_restx import Resource, Api
from dependency_injector.wiring import inject, Provide

from app.web.resources import WsgiServices


@inject
def get_app(app: Flask = Provide[WsgiServices.app]) -> Flask:
    return app

WsgiServices().wire(modules=[__name__])


#from flask_restx import Resource, Api

#app = Flask(__name__)

# api = Api(app)

# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

app = get_app()

@app.route('/show')
def _show_routes():
    """Quick overview of the routes of the application (dev mode only)"""

    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        line = f"{rule.endpoint}: {methods} {rule.rule}"
        output.append(line)

    return '<br>'.join(output)


with app.app_context():
    import_module('app.web.controllers.test')

app.run(debug=True)
