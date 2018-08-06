
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app

# Need to setup the app for testing
# use the create_app() function to follow flask-testing library convention
app = create_app()

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
            self.assertTrue(app.config['SECRET_KEY'] == 'w-=a*dw')
            self.assertFalse(current_app is None)
            self.assertTrue(
                    app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')
                )

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'w-=a*dw')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'w-=a*dw')
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
