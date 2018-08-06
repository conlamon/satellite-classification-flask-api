
import unittest
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import ImageTile
from project.api.inference_helper import load_model
import coverage


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

# Create the flask app

app = create_app()
cli = FlaskGroup(create_app=create_app)

# Load the TensorFlow model before finishing app load
print("Loading the model")
load_model()


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()



@cli.command()
def test():
    """Runs tests without code coverage report"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database with provided csv data of tile location"""
    cursor = db.session.connection().connection.cursor()
    with open("project/static/dbload/tiles-db-init.csv", 'r') as data_file:
        # Skip the header row
        next(data_file)
        cursor.copy_from(data_file, 'tiles', sep=',')
    db.session.commit()


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