from app.shared.utils import AppUtils
from app.core.application.app_components import AppComponents
from app.core.application.create_app import create_app
from app.core.database.db_seeder import DbSeeder


def main() -> None:
    """Starting point of the flask application."""

    AppUtils.set_application_path(__file__)
    AppComponents.initialize()  # Prepare dependency injection for the Flask application.
    
    app = create_app()
    app.run()

    DbSeeder.seed_db()  # Only available in dev mode and if no migration is taking place.
            

if __name__ == "__main__":
    main()
