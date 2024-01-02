from importlib import import_module
from app.web import create_app, Config

from flask import Flask
from flask_restx import Resource, Api, Namespace, Model, fields

app = Flask(__name__)

model = Model('hugo', {
    'task': fields.String,
    'uri': fields.Url('todo_ep')
})

ns = Namespace('Register', description="Register a user")
ns.model('hugo', model)

class HelloWorld(Resource):
    @ns.expect(model)
    def post(self):
        return {'hello': 'world'}

ns.add_resource(HelloWorld, '/register')

#@ns.route('/x/p')
# if __name__ == '__main__':
#     app.run(debug=True)
    

api = Api(title="Corvendor stoxs", version="2.3")
api.add_namespace(ns, path='/users')

api.init_app(app)
app.run(debug=True)

if __name__ != '__main__':
    app = create_app()
    debug = Config().is_development()
    import_module('app.web.namespaces.account')

    @app.route('/')
    def _show_routes():
        """Quick overview of the routes of the application (dev mode only)"""

        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            line = f"{rule.endpoint}: {methods} {rule.rule}"
            output.append(line)

        return '<br>'.join(output)

    app.run(debug = debug)
    