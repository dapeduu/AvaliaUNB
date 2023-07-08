from flask import Flask, render_template
from database.db import Database

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def hello():
        return render_template('home.html', name="Pedro")

    @app.route('/dbtest')
    def db_test():
        db = Database()

        db.execute_query("""
            INSERT INTO estudante (email, matricula, senha, admin)
            VALUES (%s, %s, %s, %s)
        """, ('teste@teste.com', '2000', '1234', False))

        result = db.execute_fetchall_query("SELECT * FROM estudante")

        # Return the fetched data as a response
        return str(result)

    @app.route('/login')
    def login():
        return render_template('login.html')

    return app

if __name__ == "__main__":
    create_app().run()
