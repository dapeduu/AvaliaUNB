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
    db = Database()
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

    return render_template("criar_denuncia.html", avaliacao=avaliacao)
