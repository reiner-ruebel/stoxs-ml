"""
Starting point for the machine learning part of the Stoxs application.

The Stoxs class contains the functionality of the application which is embedded in a Flask environment.

Credentials are required to create an instance of the application. These are defined in the Credentials class.

To maintain a dependency injection, the credentials are created independently of the application. The application is then created with the credentials.

Each part can be dynamically replaced by importing it from another module, e.g. for testing purposes.
"""

from flask import Flask

from app.core.application import create_app


app: Flask = create_app()

if __name__ == "__main__":
    app.run()
