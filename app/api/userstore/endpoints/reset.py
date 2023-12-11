from typing import cast, Optional, Any

from flask import Blueprint, request, current_app
from flask_security import roles_required

from app.shared.http_status_codes import HttpStatusCodes
from app.api.shared.utils import Response_c, create_response_c
from app.core.application.config import config
from app.core.application.blueprints import get_blueprint
from app.core.application.database import db
from app.core.database.seed_db import DbSeeder
from app.core.security.permissions import Permissions


_blueprint: Blueprint = get_blueprint(__name__)

@_blueprint.route('/reset', methods=['POST'])
@roles_required(Permissions.APP_ADMIN)
def reset_db() -> Response_c:
    """ Reset the database. """

    json_data = request.json

    if json_data is None:
        return create_response_c("No data provided", ok = False)

    raw_data: dict[str, Any] = cast(dict[str, Any], json_data)

    reset_code: Optional[str] = cast(Optional[str], request.json.get('password'))

    if reset_code is None or reset_code != config.CUSTOM_RESET_CODE:
        return create_response_c("Unauthorized", HttpStatusCodes.HTTP_401_UNAUTHORIZED)

    with current_app.app_context():
        db_seeder = DbSeeder(db)
        if not db_seeder.seed_needed():
            return create_response_c('Database could not be resetted.', HttpStatusCodes.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            db_seeder.reset()
            return create_response_c('Database reset.')
