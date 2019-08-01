from blueprints import db
from flask_restful import fields

# CLIENT CLASS
class Clients(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)

    response_fields = {
        'id': fields.Integer,
        'client_key': fields.String,
        'client_secret': fields.String,
        'birth_date': fields.String
    }

    def __init__(self, client_key, client_secret, birth_date):
        self.client_key = client_key
        self.client_secret = client_secret
        self.birth_date = birth_date

    def __repr__(self):
        return '<Client %r>' % self.id
