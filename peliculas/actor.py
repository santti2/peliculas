from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from peliculas.db import get_db

bp = Blueprint('actor', __name__)

@bp.route('/')
def index():
    db = get_db()
    actor = db.execute(
        """SELECT *
            FROM actor
            ORDER BY first_name, last_name """
    ).fetchall()
    return render_template('actor/index.html', actor=actor)

def get_actor(id):
    actor = get_db().execute(
        """SELECT *
            FROM actor
            WHERE actor_id = ? """,
            (id,)
    ).fetchone()
    if actor is None:
     abort(404, f"Post id {id} doesn't exist.")


@bp.route('/<int:id>/detalle', methods=['GET'])
def mostraractores(id):
    actor = get_actor(id)


    return render_template('actor/detalle.html', actor=actor)