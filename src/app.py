from flask import Flask, render_template, request, redirect, url_for, flash
from database.db import Database
import base64

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = '/uploads'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    @app.route('/')
    def home():
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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            matricula = request.form['matricula']
            senha = request.form['senha']

            db = Database()
            user = db.execute_fetchone_query("""
                SELECT matricula, senha FROM estudante
                WHERE matricula = %s AND senha = %s
            """, (matricula, senha))

            if user:
                return redirect(url_for('home'))
            else:
                return render_template('login.html', message="Usuário não encontrado!")

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':

            student = dict(request.form)
            student['email'] = f'{student["matricula"]}@aluno.unb.br'

            avatar = request.form['avatar']
            avatar_file = request.files.get(avatar)

            if avatar_file:
                encoded_image = base64.b64encode(avatar_file)
                student['avatar'] = encoded_image

            # Stores on database

            breakpoint()

            db = Database()
            db.execute_query("""
                INSERT INTO estudante (matricula, avatar, senha, email)
                VALUES (%s, %s, %s, %s)
            """, tuple(student.values()))

            return redirect(url_for('home'))

        return render_template('register.html')

    return app

if __name__ == "__main__":
    create_app().run()
