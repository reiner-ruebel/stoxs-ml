from flask_restx import Resource, Namespace, Model, fields

from dependency_injector.wiring import inject, Provide
 
from app.services import IAccountService, RegisterPayload, RegisterResult, Services
from app.web import WebUtils, NamespaceFactory, NamespaceDocu

class AccountController:
    @inject
    def __init__(self,
                 account_service: IAccountService = Provide[Services.account_service]
                 namespace_manager: NamespaceFactory = Provide[WebUtils.namespace_manager]
                 ) -> None:
        self._account_service = account_service


@inject
def get_service(account_service: IAccountService = Provide[Services.account_service]) -> IAccountService:
    return account_service
    
Services().wire(modules=[__name__])

docu: NamespaceDocu = NamespaceFactory._create_namespace_docu(__name__, RegisterPayload, [201])


responses = {'201': ('Account successfully created.', model)}
ns_doc_kwargs = {'description':"d", 'body': model, 'responses': responses}

ns = Namespace('Account', description="Account Management")
ns.model('account.register', model)
ns_route = '/register'

ns, ns_route, ns_doc_kwargs = NamespaceFactory.create_namespace(__name__, RegisterPayload)



@ns.route(docu.route)
class Register(Resource):
    @ns.doc(**ns_doc_kwargs)
    @WebUtils.validate_request(RegisterPayload)
    def post(self, payload: RegisterPayload):
        """Register a new account"""
        result: RegisterResult = get_service().register(payload)

        return result, 200
