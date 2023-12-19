from flask import current_app
from flask_security import roles_required
from flask_restx import Namespace, Resource # type: ignore
from flask_jwt_extended import jwt_required

from app.shared.http_status_codes import HttpStatusCodes
from app.core.application.config import config
from app.core.application.database import db
from app.core.database.seed_db import DbSeeder
from app.core.security.permissions import Permissions
from app.api.shared.utils import Api_Response, create_api_response, create_namespace, validate_request

from ..models.reset import ResetInput


ns: Namespace = create_namespace(__file__)

@ns.route('/')
class reset_db(Resource):
    @jwt_required(refresh=True)
    @roles_required(Permissions.APP_ADMIN)
    @validate_request(ResetInput)
    def post(self, model: ResetInput) -> Api_Response:
        """ Reset the database. """

        if model.password is None or model.password != config.CUSTOM_RESET_CODE:
            return create_api_response("Unauthorized", HttpStatusCodes.HTTP_401_UNAUTHORIZED)

        with current_app.app_context():
            db_seeder = DbSeeder(db)
            db_seeder.reset()

        return create_api_response('Database reset.')
