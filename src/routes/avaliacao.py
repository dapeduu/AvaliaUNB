from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import Database
import base64

blueprint = Blueprint('avaliacao', __name__)

@blueprint.route('/')
def index():
    db = Database()

    avaliacoes = db.execute_fetchall_query("""
        SELECT * FROM turma_avaliacoes_view
    """)

    return render_template('listar_avaliacoes.html', avaliacoes=avaliacoes)

@blueprint.route('/criar_avaliacao')
def create():
    return render_template('criar_avaliacao.html')