
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('peliculas', __name__)

@bp.route('/')
def index():
    db = get_db()
    peliculas = db.execute(
        """SELECT f.title AS titulo, l.name AS lenguaje, release_year
         FROM film f JOIN language l ON f.language_id = l.language_id
         ORDER BY f.film_id """
    ).fetchall()
    return render_template('peliculas/index.html', peliculas=peliculas)

def get_pelicula(id):
    peliculas = get_db().execute(
        """SELECT *
            FROM film
            WHERE film_id = ? """,
            (id,)
    ).fetchone()
    if peliculas is None:
        abort(404, f"Post id {id} doesn't exist.")

##punto5

def get_actors(id):
    actors = get_db().execute(
        """SELECT *
           fROM actor
           order by actor_id ASC""",
            (id,)
    ).fetchall()


@bp.route('/detalle/<int:id>/', methods=['GET'])
def mostrardetalle(id):
    pelicula = get_pelicula(id)
    actors = get_actors(id) 
    return render_template('peliculas/detalle.html', pelicula=pelicula, actors=actors)

