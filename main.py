from importlib import import_module
from app.web import create_app, Config


if __name__ == '__main__':
    app = create_app()
    debug = Config().is_development()
    import_module('app.web.namespaces.account')

    @app.route('/')
    def _show_routes():
        """Quick overview of the routes of the application (dev mode only)"""

        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            line = f"{rule.endpoint}: {methods} {rule.rule}"
            output.append(line)

        return '<br>'.join(output)

    app.run(debug = debug)
    