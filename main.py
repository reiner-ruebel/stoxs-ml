from importlib import import_module
from app.web import create_app, Config

from flask_restx import Api

# from app.web.admin.account import ns


if __name__ == '__main__':
    app = create_app()
    debug = Config().is_development()

    m = import_module('app.web.admin.account')

    api = Api(title="Corvendor stoxs", version="2.3")
    api.add_namespace(m.ns, path='/account')

    api.init_app(app)

    @app.route('/show')
    def _show_routes():
        """Quick overview of the routes of the application (dev mode only)"""

        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            line = f"{rule.endpoint}: {methods} {rule.rule}"
            output.append(line)

        return '<br>'.join(output)

    app.run(debug = debug)
    