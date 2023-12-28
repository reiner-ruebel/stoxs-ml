from flask import current_app
from flask_security import roles_required
from flask_restx import Namespace, Resource # type: ignore
from flask_jwt_extended import jwt_required

from app.shared.http_status_codes import HttpStatusCodes
from app.core.application.app_components import AppComponents as C
from app.core.database.db_seeder import DbSeeder
from app.core.security.permissions import Permissions
from app.api.shared.utils import ApiUtils

from ..models.reset import ResetInput


ns: Namespace = ApiUtils.create_namespace(__name__)

@ns.route('/')
class ResetDb(Resource):
    # @jwt_required(refresh=True)
    # @roles_required(Permissions.APP_ADMIN)
    @ApiUtils.validate_request(ResetInput)
    def post(self, model: ResetInput) -> ApiUtils.Api_Response:
        """ Reset the database. """

        if model.password is None or model.password != C.config_object.CUSTOM_RESET_CODE:
            return ApiUtils.create_api_response("Unauthorized", HttpStatusCodes.HTTP_401_UNAUTHORIZED)

        DbSeeder.reset()

        return ApiUtils.create_api_response('Database reset.')
