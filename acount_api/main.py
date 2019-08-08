
from aiohttp_devtools import runserver
from aiohttp import web

from .models import db
from .views import routes_tables
from .middlewares import middlewares


def make_app(arg=None):
    app = web.Application(middlewares=middlewares)
    for routes_table in routes_tables:
        app.router.add_routes(routes_table)
    return app


if __name__ == "__main__":
    app = make_app()
    web.run_app(app)
