from flask import jsonify
from flask_restx import Resource, Namespace, Model, fields  # type: ignore

from dependency_injector.wiring import inject, Provide
 
from app.services import IAccountService, RegisterPayload, RegisterResult, Services
from app.web.shared import WebUtils


class Controller(Resource):
    @inject
    def __init__(self, account_service: IAccountService = Provide[]) -> None:
        self._account_service: IAccountService = account_service

    def register(self, payload: RegisterPayload) -> RegisterResult:
        return self._account_service.register(payload)

Services().wire(modules=[__name__])


model = Model('register', {
    'task': fields.String,
    'uri': fields.Url('todo_ep')
})

ns = Namespace('Account', description="Account Management")
ns.model('register', model)  # type: ignore

class Register(Controller):
    @ns.expect(model)  # type: ignore
    @WebUtils.validate_request(RegisterPayload)
    def post(self, payload: RegisterPayload):
        result: RegisterResult = self._account_service.register(payload)

        return jsonify(result), 200

ns.add_resource(Register, '/register')  # type: ignore
