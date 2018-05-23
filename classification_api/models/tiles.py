from db import db
from geoalchemy2 import Geometry


class TileModel(db.Model):
    '''Describes the tiles database table and allows querying for image tile information'''
    __tablename__ = 'tiles'

    # Define the table model
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)
    geom = db.Column(Geometry('POLYGON', srid=4326))
    z = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    path = db.Column(db.String(50))

    def __init__(self, z_coord, x_coord, y_coord):
        self.z = z_coord
        self.x = x_coord
        self.y = y_coord

    @staticmethod
    def find_path_by_coords(z_coord, x_coord, y_coord):
        '''
        Query the database for the image path (str) and return it

        Input:  z_coord -- int; WMS tile layer z coordinate value (zoom level)
                x_coord -- int; WMS tile layer x coordinate value (see deg_to_num in utils.py for conversion)
                y_coord -- int; WMS tile layer y coordinate value (see deg_to_num in utils.py for conversion)

        Output: string; Path to the image
        '''
        return db.session.query(TileModel.path).filter_by(z=z_coord, x=x_coord, y=y_coord).scalar()
