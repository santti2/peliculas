from flask import (
    Blueprint, flash, g, redirect, jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from peliculas.db import get_db

bp = Blueprint('category', __name__, url_prefix="/category/")

@bp.route('/')
def index():
    db = get_db()
    category = db.execute(
        """SELECT name
            FROM category
            ORDER BY name ASC """
    ).fetchall()
    return jsonify('category/index.html', category=category)

def get_category(id):
    categoria = get_db().execute(
        """SELECT *
            FROM category
            WHERE category_id = ? """,
            (id,)
    ).fetchone()
    if categoria is None:
        abort(404, f"Post id {id} doesn't exist.")


@bp.route('/<int:id>/detalle', methods=['GET'])
def mostrarcategoria(id):
    category = get_category(id)


    return jsonify('category/index.html', category=category)