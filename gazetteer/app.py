from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY, CONFIG

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)
# On configure le secret
app.config['SECRET_KEY'] = SECRET_KEY
# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://gazetteer_user:password@localhost/gazetteer'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# On initie l'extension
db = SQLAlchemy(app)

# On met en place la gestion d'utilisateur-rice-s
login = LoginManager(app)


from .routes import generic
from .routes import api

#configuration pour les tests.
def config_app(config_name="test"):
    """ Create the application """
    app.config.from_object(CONFIG[config_name])

    # Set up extensions
    db.init_app(app)
    # assets_env = Environment(app)
    login.init_app(app)

    # Register Jinja template functions

    return app


"""
# configuration pour la performance du sql via la fonction get_debug_queries de SQLALCHEMY_DATABASE_URI
SQLALCHEMY_RECORD_QUERIES = True
#configuration de la limite au dela de laquelle la durée de query est trop longue, en seconde:
DATABASE_QUERY_TIMEOUT = 1
A debugger si le temps.
"""
