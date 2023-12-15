"""
Starting point for the machine learning part of the Stoxs application: stoxs-ml.

Please see the __init__.py files in the packages for detailed information!
"""

from flask import Flask

from app.core.application import create_app


app: Flask = create_app()

if __name__ == "__main__":
    app.run()
