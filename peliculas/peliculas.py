
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('peliculas', __name__)

@bp.route('/')
def index():
    db = get_db()
    peliculas = db.execute(
        'SELECT f film_id, films'
        ' FROM film'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('peliculas/hola.html', peliculas=peliculas)

def get_pelicula(id):
    return None

@bp.route('/<int:id>/detalle', methods=['GET'])
def mostrarpelicula(id):
    pelicula = get_pelicula(id)


    return render_template('templates/base.html', peliculas=pelicula)

