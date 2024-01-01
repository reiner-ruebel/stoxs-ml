from flask import jsonify
from flask_restx import Api, Resource, Namespace  # type: ignore

from dependency_injector.wiring import inject, Provide
 
from app.services import IAccountService, Services, RegisterPayload, RegisterResult
from app.web.container import Container
from app.web.shared import WebUtils


@inject
def _create_namespace(api: Api = Provide[Container.flask_api]) -> Namespace:
    ns = Namespace('account', description='Account related operations.')
    api.add_namespace(ns)
#    return api.namespace('account', description='Account related operations.')  # type: ignore
    return ns

Container().wire(modules=[__name__])
ns = _create_namespace()


@ns.route('/')  # type: ignore
class Register(Resource):
    # @inject
    # def __init__(self, account_service: IAccountService = Provide[Services.account_service]) -> None:
    #     self._account_service: IAccountService = account_service

    @ns.doc('deppschaan')
    @WebUtils.validate_request(RegisterPayload)
    def post(self, payload: RegisterPayload):
        result: RegisterResult = self._account_service.register(payload)

        return jsonify(result), 200
