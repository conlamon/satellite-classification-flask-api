
import unittest
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import ImageTile
from project.api.inference_helper import load_model
import coverage


# ------- Setup code coverage reporting
# Configure the code coverage report
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()

# ------- Start Flask App
app = create_app()
cli = FlaskGroup(create_app=create_app)

# Load the TensorFlow model before finishing app load
print("Loading the model")
load_model()


# Handle CORS
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

# ------- Setup CLI commands for docker deployment

# Command to recreate the database
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Command to run unit tests
@cli.command()
def test():
    """Runs tests without code coverage report"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# Command to seed the database with information provided in a .csv file
# Note: Use psycopg2 copy_from command to perform this operation efficiently
@cli.command()
def seed_db():
    """Seeds the database with provided csv data of tile location"""
    cursor = db.session.connection().connection.cursor()
    with open("project/static/dbload/tiles-db-init.csv", 'r') as data_file:
        # Skip the header row
        next(data_file)
        cursor.copy_from(data_file, 'tiles', sep=',')
    db.session.commit()

# Run code coverage report
@cli.command()
def cov():
    """Runs the unt tests with coverage"""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()