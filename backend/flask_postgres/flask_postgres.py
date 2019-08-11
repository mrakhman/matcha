import glob

import postgresql
from flask import current_app, _app_ctx_stack, Flask


class Postgres(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def _initialize_tables(self, sql_folder: str):
        sql_files = glob.glob(f'{sql_folder}/*.sql')
        sql_files.sort()
        print("Initializing DB:")
        with self.connect() as connection:
            with connection.xact():
                for filename in sql_files:
                    print(f"\t{filename[:-4].split('/')[-1]}")
                    try:
                        with open(filename, 'r') as file:
                            sql = file.read()
                            connection.execute(sql)
                    except FileNotFoundError:
                        pass
        print("====== done ======")

    def init_app(self, app: Flask):
        app.config.setdefault('PSQL_DATABASE_URI', None)
        app.config.setdefault('PSQL_DATABASE_INIT_FOLDER', './database')
        app.teardown_appcontext(self.teardown)
        with app.app_context():
            self._initialize_tables(app.config.get('PSQL_DATABASE_INIT_FOLDER'))

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
