from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from db import Database
from psycopg import errors
import base64

blueprint = Blueprint("avaliacao", __name__)


@blueprint.route("/")
def index():
    db = Database()

    avaliacoes = db.execute_fetchall_query(
        """
        SELECT * FROM turma_avaliacoes_view
    """
    )

    return render_template("listar_avaliacoes.html", avaliacoes=avaliacoes)


@blueprint.route(
    "/criar_avaliacao/disciplina/<disciplina_codigo>/professor/<professor_matricula>/periodo/<periodo>",
    methods=["GET", "POST"],
)
def create(disciplina_codigo: str, professor_matricula: str, periodo: str):
    current_matricula = request.cookies.get("userID")
    default_information = {
        "disciplina_codigo": disciplina_codigo,
        "professor_matricula": professor_matricula,
        "periodo": periodo,
        "estudante_matricula": current_matricula,
    }
    form_url = url_for(
        "avaliacao.create",
        disciplina_codigo=disciplina_codigo,
        professor_matricula=professor_matricula,
        periodo=periodo,
    )

    if request.method == "POST":
        db = Database()
        try:
            db.execute_query(
                """
                INSERT INTO avaliacao (estrelas, comentario, turma_periodo, turma_matricula_professor, turma_codigo_disciplina, estudante_matricula)
                VALUES(%s, %s, %s, %s, %s, %s);
            """,
                (
                    request.form.get("estrelas"),
                    request.form.get("comentario"),
                    periodo,
                    professor_matricula,
                    disciplina_codigo,
                    current_matricula,
                ),
            )
        except errors.UniqueViolation:
            flash("Você já avaliou essa turma.", "warning")
            return redirect(form_url)

        flash("Avaliação criada com sucesso!", "success")

        return redirect(url_for("avaliacao.index"))

    db = Database()
    turma = db.execute_fetchone_query(
        """
        select p.nome as professor_nome, d.nome as disciplina_nome, t.periodo from turma t
        left join disciplina d on d.codigo = t.codigo_disciplina
        left join professor p on p.matricula = t.matricula_professor
        where t.periodo = %s and t.matricula_professor = %s and t.codigo_disciplina = %s
    """,
        (periodo, professor_matricula, disciplina_codigo),
    )
    turma = {**dict(turma or {}), **default_information}
    form_url = url_for(
        "avaliacao.create",
        disciplina_codigo=disciplina_codigo,
        professor_matricula=professor_matricula,
        periodo=periodo,
    )

    return render_template("criar_avaliacao.html", turma=turma, form_url=form_url)
