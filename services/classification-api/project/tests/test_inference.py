
import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import ImageTile

def add_tile(z_coord, x_coord, y_coord, path):
    """

    :param z_coord:
    :param x_coord:
    :param y_coord:
    :param path:
    """

    tile = ImageTile(z_coord=z_coord, x_coord=x_coord, y_coord=y_coord, path=path)
    db.session.add(tile)
    db.session.commit()


class TestInferenceService(BaseTestCase):

    def test_predict(self):
        # Add function to send POST request to /predict endpoint and ensure get response back
        add_tile(z_coord=11, x_coord=332, y_coord=1260, path='project/static/test-tiles/11/332/1260.png')
        with self.client:
            response = self.client.post(
                '/inference/predict',
                data=json.dumps({
                    'lat1': 38.41,
                    'lng1': -121.64
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], True)
            self.assertEqual(response.status_code, 200)


    def test_ping(self):
        response = self.client.get('/inference/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])



if __name__ == '__main__':
    unittest.main()