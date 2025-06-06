from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '../database/pedidos.db')

    from . import routes
    app.register_blueprint(routes.main)

    from . import models
    app.teardown_appcontext(models.close_db)

    return app
