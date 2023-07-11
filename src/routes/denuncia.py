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
