"""
Starting point of the application.

The application is called without any options.
"""

from app import create_app
from config import DevelopmentConfig

if __name__ == "__main__":
    app = create_app(DevelopmentConfig).run()
