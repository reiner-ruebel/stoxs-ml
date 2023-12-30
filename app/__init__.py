from .container import Container

container = Container()

app = container.create_app()
app.run()
