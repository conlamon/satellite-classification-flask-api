
from sqlalchemy.sql import func
from project import db



class ImageTile(db.Model):
    """Describes the image tile database table and allows querying for image tile information"""
    __tablename__ = 'tiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    z_coord = db.Column(db.Integer, nullable=False)
    x_coord = db.Column(db.Integer, nullable=False)
    y_coord = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(128), nullable=False)

    def __init__(self, z_coord, x_coord, y_coord, path):
        self.z_coord = z_coord
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.path = path

    @staticmethod
    def find_path_by_coords(z_coord, x_coord, y_coord):
        """
        Query the database for the image path (str) and return it

        Input:  z_coord -- int; WMS tile layer z coordinate value (zoom level)
                x_coord -- int; WMS tile layer x coordinate value (see deg_to_num in utils.py for conversion)
                y_coord -- int; WMS tile layer y coordinate value (see deg_to_num in utils.py for conversion)

        Output: string; Path to the image
        """
        return db.session.query(ImageTile.path).filter_by(z_coord=z_coord,
                                                          x_coord=x_coord,
                                                          y_coord=y_coord).scalar()

    def to_json(self):
        return {
            'z_coord': self.z_coord,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'path': self.path
        }
