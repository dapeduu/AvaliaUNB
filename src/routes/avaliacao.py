from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    flash,
    redirect,
    url_for,
    jsonify,
)
from db import Database
from psycopg import errors
import base64

blueprint = Blueprint("avaliacao", __name__)


@blueprint.route("/")
def index():
    make_avaliar_url = lambda x: {
        **x,
        "avaliar_url": url_for(
            "avaliacao.create",
            disciplina_codigo=x["codigo_disciplina"],
            professor_matricula=x["matricula_professor"],
            periodo=x["turma_periodo"],
        ),
    }
    make_comentarios_url = lambda x: {
        **x,
        "comentarios_url": url_for(
            "avaliacao.list_comentarios",
            turma_codigo_disciplina=x["codigo_disciplina"],
            turma_matricula_professor=x["matricula_professor"],
            turma_periodo=x["turma_periodo"],
        ),
    }

    db = Database()

    avaliacoes = db.execute_fetchall_query(
        """
        SELECT * FROM turma_avaliacoes_view
    """
    )
    avaliacoes = map(make_avaliar_url, avaliacoes)
    avaliacoes = map(make_comentarios_url, avaliacoes)

    return render_template(
        "listar_avaliacoes.html",
        avaliacoes=avaliacoes,
        current_user=request.cookies.get("userID"),
    )


@blueprint.route(
    "/listar_comentarios/turma/<turma_periodo>/<turma_matricula_professor>/<turma_codigo_disciplina>"
)
def list_comentarios(
    turma_periodo: str, turma_matricula_professor: int, turma_codigo_disciplina: str
):
    db = Database()

    turma = db.execute_fetchone_query(
        """
        SELECT p.nome AS nome_professor, t.periodo FROM turma t
        LEFT JOIN professor p ON p.matricula = t.matricula_professor
        WHERE t.periodo = %s AND t.matricula_professor = %s AND t.codigo_disciplina = %s
    """,
        (turma_periodo, turma_matricula_professor, turma_codigo_disciplina),
    )

    avaliacoes = db.execute_fetchall_query(
        """
            SELECT * FROM avaliacao
            WHERE avaliacao.turma_matricula_professor = %s
                  AND avaliacao.turma_periodo = %s
                  AND turma_codigo_disciplina = %s
        """,
        (
            turma_matricula_professor,
            turma_periodo,
            turma_codigo_disciplina,
        ),
    )

    avaliacoes = generate_avaliacoes_with_denuncia(avaliacoes)

    return render_template(
        "listar_comentarios.html", comentarios=avaliacoes, turma=turma
    )


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


def generate_avaliacoes_with_denuncia(avaliacoes: list):
    for avaliacao in avaliacoes:
        denuncia_url = generate_denuncia_url(
            avaliacao["turma_periodo"],
            avaliacao["turma_matricula_professor"],
            avaliacao["turma_codigo_disciplina"],
            avaliacao["estudante_matricula"],
        )

        avaliacao["denuncia_url"] = denuncia_url

    return avaliacoes


def generate_denuncia_url(
    turma_periodo: str,
    turma_matricula_professor: int,
    turma_codigo_disciplina: str,
    estudante_matricula: int,
):
    return url_for(
        "denuncia.create",
        turma_periodo=turma_periodo,
        turma_matricula_professor=turma_matricula_professor,
        turma_codigo_disciplina=turma_codigo_disciplina,
        estudante_matricula=estudante_matricula,
    )
