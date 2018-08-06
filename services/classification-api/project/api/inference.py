
from flask import Blueprint, jsonify, request
from sqlalchemy import exc
import os

from project.api.inference_helper import predict
from project.api.models import ImageTile
from project import db
from project.api.utils import deg_to_num

# Setup Flask blueprint
inference_blueprint = Blueprint('inference', __name__)


# Setup test endpoint
@inference_blueprint.route('/inference/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

# Setup the main prediction endpoint
@inference_blueprint.route('/inference/predict', methods=['POST'])
def classify_image():
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
    # Setup the default response object

    response_object = {
        'success': False,
        'predictions': [],
        'message': ''
    }

    zoom = int(os.environ.get('PREDICTION_ZOOM', 11))

    # Retrieve the sent payload, and do a quick error check
    long_lat_json = request.get_json()
    if not long_lat_json or 'lat1' not in long_lat_json or 'lng1' not in long_lat_json:
        # Let the user know the payload was incorrect
        response_object['message'] = 'Invalid payload'
        return jsonify(response_object), 400
    else:
        # Retrieve the center Lat, Lng coordinate
        lat_1, lng_1 = long_lat_json['lat1'], long_lat_json['lng1']

    # Convert the coordinate to x,y values
    xtile, ytile = deg_to_num(lat_1, lng_1, zoom)

    # Lookup the image path in the database
    # image_path = 'project/static/tiles/{}/{}/{}.png'.format(zoom, xtile, ytile)
    try:
        image_path = ImageTile.find_path_by_coords(z_coord=zoom, x_coord=xtile, y_coord=ytile)
    except exc.SQLAlchemyError as err:
        response_object['message'] = 'Issue finding image in database. See error: {}'.format(err)
        return jsonify(response_object), 500

    # Make a prediction
    json_result = predict(image_path)

    return jsonify(json_result), 200