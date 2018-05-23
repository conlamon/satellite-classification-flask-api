from services.inference_service import predict
from flask_restful import Resource, request
from sqlalchemy import exc
from models.tiles import TileModel
from utils import deg_to_num
import os


class ClassificationApi(Resource):
    ''' REST API interface for classification model'''
    def post(self):
        '''
        Runs classification model on image based on received lat/lng coordinates

        produces:
          - application/json
        parameters:
            - lat: float
              lng: float
              description: JSON object containing center lat/lon coordinate of location to classify
              schema:
                  properties:
                      id: type - character varying
                      lat: type - numeric
                      lon: type - numeric
                      geom: type - polygon
                      z: type - numeric
                      x: type - numeric
                      y: type - numeric
                      path: type - string

        responses:
            201:
                description: Prediction generated correctly
            500:
                description: Internal Server Error
        '''
        zoom = int(os.environ.get('PREDICTION_ZOOM', 10))

        # Retrieve the sent payload
        long_lat_json = request.get_json()

        # Retrieve the center Lat, Lng coordinate
        lat_1, lng_1 = long_lat_json['lat1'], long_lat_json['lng1']

        # Convert the coordinate to x,y values
        xtile, ytile = deg_to_num(lat_1, lng_1, zoom)

        # Lookup the image path in the database
        #image_path = 'static/tiles/{}/{}/{}.png'.format(zoom, xtile, ytile)
        try:
            image_path = TileModel.find_path_by_coords(z_coord=zoom, x_coord=xtile, y_coord=ytile)
        except exc.SQLAlchemyError:
            return {'Message': 'An error occurred while searching for image in the database'}

        # Make a prediction
        json_result = predict(image_path)

        return json_result
