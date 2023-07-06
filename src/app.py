from flask import Flask
from db import Database

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/dbtest')
    def db_test():
        db = Database()
        db.execute_query("""CREATE TABLE IF NOT EXISTS test (
                id serial PRIMARY KEY,
                num integer,
                data text)""")

        db.execute_query("INSERT INTO test (num, data) VALUES (1, 'Data 1'), (2, 'Data 2'), (3, 'Data 3')")

        result = db.execute_fetchone_query("SELECT * FROM test")

        # Return the fetched data as a response
        return str(result)

    return app

if __name__ == "__main__":
    create_app().run()
