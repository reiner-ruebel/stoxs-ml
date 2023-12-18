from typing import cast, Optional

from flask import request, current_app
from flask_security import roles_required
from flask_restx import Namespace, Resource # type: ignore

from app.shared.http_status_codes import HttpStatusCodes
from app.api.shared.utils import Api_Response, create_response_c, create_data
from app.core.application.config import config
from app.core.application.database import db
from app.core.database.seed_db import DbSeeder
from app.core.security.permissions import Permissions


ns = Namespace("reset", description="Reset the database to default values.")

@ns.route('/')
#@roles_required(Permissions.APP_ADMIN)
class reset_db(Resource):
    def post(self) -> Api_Response:
        """ Reset the database. """

        request_data = create_data(request)

        if request_data is None:
            return create_response_c("No data provided", ok = False)

        reset_code: Optional[str] = cast(Optional[str], request_data['password'])

        if reset_code is None or reset_code != config.CUSTOM_RESET_CODE:
            return create_response_c("Unauthorized", HttpStatusCodes.HTTP_401_UNAUTHORIZED)

        with current_app.app_context():
            db_seeder = DbSeeder(db)
            db_seeder.reset()
            return create_response_c('Database reset.')
