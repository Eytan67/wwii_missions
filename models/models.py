from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Location {self.city}, {self.country}>"

class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Numeric(10, 6), nullable=False)
    longitude = db.Column(db.Numeric(10, 6), nullable=False)

    def __repr__(self):
        return f"<Coordinates ({self.latitude}, {self.longitude})>"

class TargetDetails(db.Model):
    __tablename__ = 'target_details'
    target_id = db.Column(db.Integer, primary_key=True)
    target_type = db.Column(db.String(100), nullable=False)
    target_industry = db.Column(db.String(255), nullable=False)
    target_priority = db.Column(db.String(5), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    coordinates_id = db.Column(db.Integer, db.ForeignKey('coordinates.id'))

    location = db.relationship('Location', backref='targets')
    coordinates = db.relationship('Coordinates', backref='targets')

    def __repr__(self):
        return f"<TargetDetails {self.target_type}>"

class Mission(db.Model):
    __tablename__ = 'mission'
    mission_id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('target_details.target_id'))

    target = db.relationship('TargetDetails', backref='missions')

    def __repr__(self):
        return f"<Mission {self.mission_id}>"







