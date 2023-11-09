
from flask import (
    Blueprint, flash, g, redirect,jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from peliculas.db import get_db

bp = Blueprint('peliculas', __name__)
bpapi = Blueprint('pelicula_api', __name__, url_prefix="/api/pelicula")



@bp.route('/')
def index():
    peliculas = get_peliculas()
    return render_template('peliculas/index.html', peliculas=peliculas)

def get_language(id):
    language = get_db().execute(
    """ SELECT f.film_id, l.name as idioma FROM film f 
    JOIN language l ON f.language_id = l.language_id
    WHERE f.film_id = ?""",(id,)
    ).fetchone()
    return language


@bpapi.route('/')
def index_api():
    peliculas = get_peliculas()
    for pelicula in peliculas:
        pelicula["url"] = url_for("pelicula_api.detalle_api", id=pelicula["film_id"], _external=True)
    return jsonify(peliculas=peliculas)

def get_peliculas():
    db = get_db()
    res = db.execute(
        """SELECT f.title, l.name AS lenguaje, release_year, f.film_id
         FROM film f JOIN language l ON f.language_id = l.language_id
         ORDER BY f.film_id """
    ).fetchall()    
    return res

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

@bpapi.route ("/<int:id>/")
def detalle_api(id):
    movie_info = get_pelicula(id)
    actor_info = get_actors(id)
    language_info = get_language(id)
    return jsonify(movie_info =movie_info, actor_info = actor_info,language_info = language_info)