from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

if __name__ == '__main__' : 
    app.run(debug=True)

basedir =os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), unique=False)
    lastName = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30), unique=False)
    address = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(30), unique=False)
    state = db.Column(db.String(30), unique=False)
    phone = db.Column(db.number(10), unique=False)

    def __init__(self, firstName, lastName, email, password, streetAddress, city, state, phone):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.streetAddress = streetAddress
        self.city = city
        self.state = state
        self.phone = phone

class UserSchema(ma.Schema) :
    class Meta:
        fields = ('firstName', 'lastName', 'email', 'password', 'streetAddress', 'city', 'state', 'phone')

user_schema = UserSchema()
users_schema = UserSchema(many=True)