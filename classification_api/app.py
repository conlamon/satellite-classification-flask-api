from flask import Flask
from flask_restful import Api
from resources.classification_api import ClassificationApi
from services.inference_service import load_model
import os


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(ClassificationApi, '/predict')


if __name__ == '__main__':

    print(("* Loading Keras model and starting Flask server..."
           "Please wait until server has fully started"))

    # Load in the model first, before starting the flask server when testing locally
    load_model()

    # Load in the database
    from db import db
    db.init_app(app)

    # Start the flask server
    app.run()
