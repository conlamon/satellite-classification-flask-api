from app import app
from db import db
from services.inference_service import load_model

db.init_app(app)

@app.before_first_request
def run_model_load():
    load_model()


