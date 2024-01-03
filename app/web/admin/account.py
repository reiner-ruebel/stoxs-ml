from flask_restx import Resource, Namespace, Model, fields, Api

from dependency_injector.wiring import inject, Provide
 
from app.services import IAccountService, RegisterPayload, RegisterResult, Services
from app.web.shared import WebUtils


@inject
def get_service(account_service: IAccountService = Provide[Services.account_service]) -> IAccountService:
    return account_service
    
Services().wire(modules=[__name__])


model = Model('account.register', {
    'task': fields.String,
    'uri': fields.Url('todo_ep')
})

ns = Namespace('Account', description="Account Management")
ns.model('account.register', model)

@ns.route('/register')
class Register(Resource):
    @ns.doc(**{'description':"resting is so toog", 'body': model})
    @ns.response(201, 'Account successfully created.', model)
    @WebUtils.validate_request(RegisterPayload)
    def post(self, payload: RegisterPayload):
        """Register a new account"""
        result: RegisterResult = get_service().register(payload)

        return result, 200

ns.add_resource(Register, '/register')
