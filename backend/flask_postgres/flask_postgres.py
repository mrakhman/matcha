import postgresql
from flask import current_app, _app_ctx_stack


class Postgres(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('PSQL_DATABASE_URI', None)
        app.teardown_appcontext(self.teardown)

    @staticmethod
    def connect():
        return postgresql.open(current_app.config['PSQL_DATABASE_URI'])

    @staticmethod
    def teardown(_):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'postgres_db'):
            ctx.postgres_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'postgres_db'):
                ctx.postgres_db = self.connect()
            return ctx.postgres_db
