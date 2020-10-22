from mainPackage import db

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

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

    def __init__(self, email, firstName, lastName, job, username, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.job = job
        self.username = username
        self.password = password
