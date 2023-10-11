from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from peliculas.db import get_db

bp = Blueprint('lenguage', __name__)

@bp.route('/')
def index():
    db = get_db()
    lenguage = db.execute(
        """SELECT name
            FROM language
            ORDER BY name ASC """
    ).fetchall()
    return render_template('lenguage/index.html', lenguage=lenguage)

def get_language(id):
     lenguage = get_db().execute(
        """SELECT *
            FROM language
            WHERE lenguage_id """
    ).fetchone()
     if lenguage is None:
      abort(404, f"Post id {id} doesn't exist.")

@bp.route('/<int:id>/detalle', methods=['GET'])
def mostrarlenguage(id):
    lenguage = get_language(id)


    return render_template('lenguage/index.html', lenguage=lenguage)