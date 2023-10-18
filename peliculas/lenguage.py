from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from peliculas.db import get_db

bp = Blueprint('lenguage', __name__,url_prefix="/lenguaje/")

@bp.route('/')
def index():
    db = get_db()
    lenguaje = db.execute(
        """SELECT *
            FROM language
            ORDER BY name """
    ).fetchall()
    return render_template('lenguage/index.html', lenguaje=lenguaje)


def get_language(id):
     lenguaje = get_db().execute(
        """SELECT *
            FROM language
            WHERE lenguage_id = ? """, (id,)
    ).fetchone()
     if lenguaje is None:
      abort(404, f"Post id {id} doesn't exist.")

@bp.route('/<int:id>/detalle', methods=['GET'])
def mostrarlenguage(id):
    lenguaje = get_language(id)

    return render_template('lenguage/index.html', lenguaje=lenguaje)