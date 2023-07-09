from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import Database
import base64

blueprint = Blueprint('auth', __name__)

@blueprint.route('/login', methods=['GET', 'POST'])
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

@blueprint.route('/register', methods=['GET', 'POST'])
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
