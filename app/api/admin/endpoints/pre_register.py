from flask_restx import Namespace, Resource # type: ignore

ns = Namespace("pre-register", description="pre-register a user who is allowed to register himself")

@ns.route("/")
class Myclass(Resource):
    def get(self):
        return {'high': 'hello'}
    