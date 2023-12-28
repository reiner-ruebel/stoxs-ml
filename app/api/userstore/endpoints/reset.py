from flask import current_app
from flask_security import roles_required
from flask_restx import Namespace, Resource # type: ignore
from flask_jwt_extended import jwt_required
from app.core.application.apis import Apis
from app.shared.AppTypes import Api_Response

from app.shared.http_status_codes import HttpStatusCodes
from app.core.application.config import config_object
from app.core.database.db_seeder import DbSeeder
from app.core.security.permissions import Permissions
from app.api.shared.utils import ApiUtils

from ..models.reset import ResetInput

class PayloadModel:
    pass

ns, swagger_model = Apis.endpoint_package(__name__, PayloadModel)

@ns.route('/')
class ResetDb(Resource):
    # @jwt_required(refresh=True)
    # @roles_required(Permissions.APP_ADMIN)
    @ApiUtils.validate_request(ResetInput)
    def post(self, model: ResetInput) -> Api_Response:
        """ Reset the database. """

        if model.password is None or model.password != config_object.CUSTOM_RESET_CODE:
            return ApiUtils.create_api_response("Unauthorized", HttpStatusCodes.HTTP_401_UNAUTHORIZED)

        DbSeeder.reset()

        return ApiUtils.create_api_response('Database reset.')
