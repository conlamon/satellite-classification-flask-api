
import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import ImageTile

def add_tile(z_coord, x_coord, y_coord, path):
    """
    Helper function to add a image tile info to the database
    Input:
        - z_coord: (int) Zoom value of image
        - x_coord: (int) X coordinate of image in MB Tiles format
        - y_coord: (int) Y coordinate of image in MB Tiles format
        - path: (string) Location of image tile
    """

    tile = ImageTile(z_coord=z_coord, x_coord=x_coord, y_coord=y_coord, path=path)
    db.session.add(tile)
    db.session.commit()


class TestInferenceService(BaseTestCase):
    """
    Unit tests for the API
    """
    def test_ping(self):
        """Simple verification of server status"""
        response = self.client.get('/inference/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_predict(self):
        """Test that the /predict endpoint is working correctly"""
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

if __name__ == '__main__':
    unittest.main()