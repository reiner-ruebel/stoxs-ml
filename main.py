from app.web import WebApp

web_app = WebApp()  # create the web app
app = web_app.create_app()  # create the flask app
app.run()
