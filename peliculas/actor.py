from flask import (
    Blueprint, flash, g, redirect, jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from peliculas.db import get_db
from flaskr.auth import login_required

bp = Blueprint('actor', __name__,url_prefix="/actor/")
bpapi = Blueprint('Actor', __name__,url_prefix="/actor/")

@bp.route('/')
def index():
    db = get_db()
    actor = db.execute(
        """SELECT first_name as nombre , last_name as apellido
            FROM actor
            ORDER BY nombre, apellido """
    ).fetchall()
    return jsonify('actor/index.html', actor=actor)

def get_actor(id):
    actor = get_db().execute(
    """ SELECT a.actor_id,a.first_name,a.last_name,c.name as categoria FROM film f 
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id  
    WHERE f.film_id = ?""",(id,)
    ).fetchone()
    if actor is None:
     abort(404, f"Post id {id} doesn't exist.")

    return actor
@bp.route('/<int:id>/detalle', methods=['GET'])
def detalle(id):
   info_del_actor = get_actor(id)
   apariciones = get_actor_de_peliculas(id)
   return render_template    ('actor/detalle.html', info_del_actor = info_del_actor, apariciones=apariciones)

def get_actor_de_peliculas(id):
    actor_pelis = get_db().execute(
    """ SELECT f.film_id, a.actor_id,f.title as peli,a.first_name,a.last_name FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a on fa.actor_id = a.actor_id
    WHERE a.actor_id = ?""",(id,)).fetchall()    
    return actor_pelis

def detalle_api(id):
    info_del_actor = get_actor(id)
    apariciones = get_actor_de_peliculas(id)

    
    return jsonify(info_del_actor = info_del_actor, apariciones=apariciones)