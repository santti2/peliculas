import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/base')
    def Hello():
        return render_template('base.html')


    from . import peliculas
    app.register_blueprint(peliculas.bp)
    app.register_blueprint(peliculas.bpapi)
    app.add_url_rule('/', endpoint='index')
    

    from . import lenguage
    app.register_blueprint(lenguage.bp)

    from . import category  
    app.register_blueprint(category.bp)

    from . import actor
    app.register_blueprint(actor.bpapi)
    app.register_blueprint(actor.bp)    

    from . import db
    db.init_app(app)


    return app