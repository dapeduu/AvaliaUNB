from flask import url_for


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


def generate_comentarios_url(
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
