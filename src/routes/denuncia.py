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
import psycopg
from urls import generate_denuncia_url

blueprint = Blueprint("denuncia", __name__)


@blueprint.route(
    "/denunciar_avaliacao/<turma_periodo>/<turma_matricula_professor>/<turma_codigo_disciplina>/<estudante_matricula>",
    methods=["GET", "POST"],
)
def create(
    turma_periodo: str,
    turma_matricula_professor: int,
    turma_codigo_disciplina: str,
    estudante_matricula: int,
):
    form_url = generate_denuncia_url(
        turma_periodo=turma_periodo,
        turma_matricula_professor=turma_matricula_professor,
        turma_codigo_disciplina=turma_codigo_disciplina,
        estudante_matricula=estudante_matricula,
    )
    db = Database()

    if request.method == "POST":
        current_estudante = request.cookies.get("userID")
        comentario = request.form.get("comentario")

        try:
            db.execute_query(
                """
                INSERT INTO denuncia
                (comentario, avaliacao_turma_periodo, avaliacao_turma_matricula_professor, avaliacao_turma_codigo_disciplina, avaliacao_estudante_matricula, estudante_matricula)
                VALUES(%s, %s, %s, %s, %s, %s);
            """,
                (
                    comentario,
                    turma_periodo,
                    turma_matricula_professor,
                    turma_codigo_disciplina,
                    estudante_matricula,
                    current_estudante,
                ),
            )
            flash(
                "Denúncia realizada com sucesso! Um administrador fará a avaliação.",
                "success",
            )
        except psycopg.errors.UniqueViolation:
            flash(
                "Você só pode fazer uma denúncia por comentário.",
                "danger",
            )

        return redirect(
            url_for(
                "avaliacao.list_comentarios",
                turma_periodo=turma_periodo,
                turma_matricula_professor=turma_matricula_professor,
                turma_codigo_disciplina=turma_codigo_disciplina,
            )
        )

    avaliacao = db.execute_fetchone_query(
        """
            SELECT estudante_matricula, comentario, estrelas FROM avaliacao
            WHERE avaliacao.turma_matricula_professor = %s
                  AND avaliacao.turma_periodo = %s
                  AND turma_codigo_disciplina = %s
                  AND estudante_matricula = %s
        """,
        (
            turma_matricula_professor,
            turma_periodo,
            turma_codigo_disciplina,
            estudante_matricula,
        ),
    )

    return render_template(
        "criar_denuncia.html", avaliacao=avaliacao, form_url=form_url
    )


@blueprint.route("/list_denuncias")
def index():
    db = Database()

    denuncias = db.execute_fetchall_query(
        """
                SELECT denuncia.comentario AS comentario_denuncia,
                avaliacao.comentario AS comentario_avaliacao,
                denuncia.avaliacao_turma_periodo,
                denuncia.avaliacao_turma_matricula_professor,
                denuncia.avaliacao_turma_codigo_disciplina,
                denuncia.avaliacao_estudante_matricula,
                denuncia.estudante_matricula,
                avaliacao.estrelas

                FROM denuncia
                JOIN avaliacao ON avaliacao.turma_periodo = denuncia.avaliacao_turma_periodo
                    AND avaliacao.turma_matricula_professor = denuncia.avaliacao_turma_matricula_professor
                    AND avaliacao.turma_codigo_disciplina = denuncia.avaliacao_turma_codigo_disciplina
                    AND avaliacao.estudante_matricula = denuncia.avaliacao_estudante_matricula;
            """
    )

    append_url = lambda x: {
        **x,
        "decline_url": url_for(
            "denuncia.decline",
            avaliacao_turma_periodo=x["avaliacao_turma_periodo"],
            avaliacao_turma_matricula_professor=x[
                "avaliacao_turma_matricula_professor"
            ],
            avaliacao_turma_codigo_disciplina=x["avaliacao_turma_codigo_disciplina"],
            avaliacao_estudante_matricula=x["avaliacao_estudante_matricula"],
            estudante_matricula=x["estudante_matricula"],
        ),
        "accept_url": url_for(
            "denuncia.accept",
            avaliacao_turma_periodo=x["avaliacao_turma_periodo"],
            avaliacao_turma_matricula_professor=x[
                "avaliacao_turma_matricula_professor"
            ],
            avaliacao_turma_codigo_disciplina=x["avaliacao_turma_codigo_disciplina"],
            avaliacao_estudante_matricula=x["avaliacao_estudante_matricula"],
            estudante_matricula=x["estudante_matricula"],
        ),
    }

    denuncias = map(append_url, denuncias)

    return render_template("listar_denuncias.html", denuncias=denuncias)


@blueprint.get(
    "/aceitar_denuncia/<avaliacao_turma_periodo>/<avaliacao_turma_matricula_professor>/<avaliacao_turma_codigo_disciplina>/<avaliacao_estudante_matricula>/<estudante_matricula>"
)
def accept(
    avaliacao_turma_periodo: str,
    avaliacao_turma_matricula_professor: int,
    avaliacao_turma_codigo_disciplina: str,
    avaliacao_estudante_matricula: int,
    estudante_matricula: int,
):
    db = Database()

    db.execute_query(
        """DELETE FROM denuncia
           WHERE avaliacao_turma_periodo=%s AND avaliacao_turma_matricula_professor=%s AND avaliacao_turma_codigo_disciplina=%s AND avaliacao_estudante_matricula=%s AND estudante_matricula=%s;
        """,
        (
            avaliacao_turma_periodo,
            avaliacao_turma_matricula_professor,
            avaliacao_turma_codigo_disciplina,
            avaliacao_estudante_matricula,
            estudante_matricula,
        ),
    )

    db.execute_query(
        """
        DELETE FROM avaliacao
        WHERE estudante_matricula=%s AND turma_codigo_disciplina=%s AND turma_matricula_professor=%s AND turma_periodo=%s;
    """,
        (
            avaliacao_estudante_matricula,
            avaliacao_turma_codigo_disciplina,
            avaliacao_turma_matricula_professor,
            avaliacao_turma_periodo,
        ),
    )

    flash("Denúncia aceita, avaliação removida!", "info")
    return redirect(url_for("denuncia.index"))


@blueprint.get(
    "/rejeitar_denuncia/<avaliacao_turma_periodo>/<avaliacao_turma_matricula_professor>/<avaliacao_turma_codigo_disciplina>/<avaliacao_estudante_matricula>/<estudante_matricula>"
)
def decline(
    avaliacao_turma_periodo: str,
    avaliacao_turma_matricula_professor: int,
    avaliacao_turma_codigo_disciplina: str,
    avaliacao_estudante_matricula: int,
    estudante_matricula: int,
):
    db = Database()
    db.execute_query(
        """DELETE FROM denuncia
           WHERE avaliacao_turma_periodo=%s AND avaliacao_turma_matricula_professor=%s AND avaliacao_turma_codigo_disciplina=%s AND avaliacao_estudante_matricula=%s AND estudante_matricula=%s;
        """,
        (
            avaliacao_turma_periodo,
            avaliacao_turma_matricula_professor,
            avaliacao_turma_codigo_disciplina,
            avaliacao_estudante_matricula,
            estudante_matricula,
        ),
    )

    flash("Denúncia rejeitada!", "info")
    return redirect(url_for("denuncia.index"))
