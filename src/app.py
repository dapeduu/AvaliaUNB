from flask import Flask, render_template, request, redirect, url_for, flash
from database.db import Database
import base64
from werkzeug.utils import secure_filename


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = '/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Precisa dessa chave pra mostrar flash messages

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
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Usuário ou senha incorretos!', 'warning')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            student = dict(request.form)

            student['email'] = f'{student["matricula"]}@aluno.unb.br'

            avatar = request.files.get('avatar', False)

            if avatar:
                encoded_image = base64.b64encode(avatar.read())
                student['avatar'] = encoded_image
            else:
                flash('Não foi possível carregar sua foto de perfil.', 'info')

            # Stores on database

            db = Database()
            db.execute_query("""
                INSERT INTO estudante (matricula, avatar, senha, email)
                VALUES (%s, %s, %s, %s)
            """, (student.get('matricula'), student.get('avatar'), student.get('senha'), student.get('email')))

            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('home'))

        return render_template('register.html')

    return app

if __name__ == "__main__":
    create_app().run()
