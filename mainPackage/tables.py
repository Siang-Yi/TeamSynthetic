from mainPackage import db

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    coordinate = db.relationship('Coordinate', backref='visitor')

    def __init__(self, email, firstName, lastName, username, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    job = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    taskPercentage = db.relationship('Coordinate', backref='staff')

    def __init__(self, email, firstName, lastName, job, username, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.job = job
        self.username = username
        self.password = password


class Coordinate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

    def __init__(self, lat, lng, visitor=None, staff=None):
        self.lat = lat
        self.lng = lng
        self.visitor = visitor
        self.staff = staff
