
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
        """SELECT f.title, l.name AS lenguaje, release_year, f.film_id
         FROM film f JOIN language l ON f.language_id = l.language_id
         ORDER BY f.film_id """
    ).fetchall()
    return render_template('peliculas/index.html', peliculas=peliculas)

def get_pelicula(id):
    pelicula = get_db().execute(
        """SELECT f.title, l.name AS lenguaje, release_year, f.film_id, c.name
         FROM film f JOIN language l ON f.language_id = l.language_id
         JOIN film_category fc on f.film_id = fc.film_id
         JOIN category c on fc.category_id = c.category_id
        WHERE f.film_id = ? """,
            (id,)
    ).fetchone()
    if pelicula is None:
        abort(404, f"Post id {id} doesn't exist.")
    return pelicula

##punto5

def get_actors(id):
    actors = get_db().execute(
            """ SELECT f.film_id, a.actor_id,a.first_name as nombre,a.last_name as apellido FROM film f     
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id  
    WHERE f.film_id = ?""",(id,)
    ).fetchall()
    return actors


@bp.route('/detalle/<int:id>/', methods=['GET'])
def mostrardetalle(id):
    pelicula = get_pelicula(id)
    actors = get_actors(id) 
    print(pelicula)
    return render_template('peliculas/detalle.html', movie_info=pelicula, actor_info=actors)

