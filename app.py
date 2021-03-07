from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

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
    phone = db.Column(db.Integer, unique=False)

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

@app.route('/user', methods=["POST"])
def add_user():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    streetAddress = request.json['streetAddress']
    city = request.json['city']
    state = request.json['state']
    phone = request.json['phone']

    new_user = User(firstName, lastName, email, password, streetAddress, city, state, phone)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<id>', methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    streetAddress = request.json['streetAddress']
    city = request.json['city']
    state = request.json['state']
    phone = request.json['phone']

    user.firstName = firstName
    user.lastName = lastName
    user.email = email
    user.password = password
    user.streetAddress = streetAddress
    user.city = city
    user.state = state
    user.phone = phone

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['DELETE'])    
def user_delete(id):
    user = User.query.get(id)
        
    db.session.delete(user)
    db.session.commit()

    return f'successfully deleted {user}' 

if __name__ == '__main__':
    app.run(debug=True)