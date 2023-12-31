from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    make_response,
)
from db import Database
import image

blueprint = Blueprint("auth", __name__)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        matricula = request.form["matricula"]
        senha = request.form["senha"]

        db = Database()
        user = db.execute_fetchone_query(
            """
            SELECT matricula, senha, admin FROM estudante
            WHERE matricula = %s AND senha = %s
        """,
            (matricula, senha),
        )

        if user:
            flash("Login realizado com sucesso!", "success")
            response = make_response(redirect(url_for("avaliacao.index")))
            response.set_cookie("userID", matricula)
            if user["admin"]:
                response.set_cookie("admin", str(user["admin"]))

            return response
        else:
            flash("Usuário ou senha incorretos!", "warning")

    return render_template("login.html")


@blueprint.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for("auth.login")))
    response.delete_cookie("userID")
    response.delete_cookie("admin")
    return response


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student = dict(request.form)

        student["email"] = f'{student["matricula"]}@aluno.unb.br'

        avatar = request.files.get("avatar", False)
        if avatar:
            encoded_image = image.encode_image(avatar)
            student["avatar"] = encoded_image
        else:
            flash("Não foi possível carregar sua foto de perfil.", "info")

        # Stores on database

        db = Database()
        db.execute_query(
            """
            INSERT INTO estudante (matricula, avatar, senha, email)
            VALUES (%s, %s, %s, %s)
        """,
            (
                student.get("matricula"),
                student.get("avatar"),
                student.get("senha"),
                student.get("email"),
            ),
        )

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@blueprint.route("/perfil", methods=["GET", "POST"])
def perfil():
    current_estudante = request.cookies.get("userID")
    if request.method == "POST":
        student = dict(request.form)
        avatar = request.files.get("avatar", False)
        if avatar:
            encoded_image = image.encode_image(avatar)
            student["avatar"] = encoded_image

        db = Database()
        db.execute_query(
            """
            UPDATE estudante
            SET email=%s, senha=%s
            WHERE matricula=%s;
        """,
            (student["email"], student["senha"], current_estudante),
        )

        if avatar:
            db.execute_query(
                """
                UPDATE estudante
                SET avatar=%s
                WHERE matricula=%s;
            """,
                (student["avatar"], current_estudante),
            )

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("auth.perfil"))

    db = Database()

    estudante = db.execute_fetchone_query(
        """
        SELECT matricula, email, avatar, senha FROM estudante
        WHERE estudante.matricula = %s
    """,
        (current_estudante,),
    )

    return render_template("perfil.html", estudante=estudante)
