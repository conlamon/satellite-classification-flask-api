import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the db
db = SQLAlchemy()


# Setup the flask application
# Note: the create_app function is based on the Flask Application Factory structure to make testing and config easier

def create_app(script_info=None):

    # Initialize the app
    app = Flask(__name__)

    # Set the config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Setup extensions
    print("Loading the database")
    db.init_app(app)

    # Register the blueprints
    from project.api.inference import inference_blueprint
    app.register_blueprint(inference_blueprint)

    # Shell context for the flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
