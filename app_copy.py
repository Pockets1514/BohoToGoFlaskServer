from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

# class RequestHandler(BaseHTTPRequestHandler):

#     def _send_cors_headers(self):
#         self.send_header("Access-Control-Allow-Origin", "http://localhost:3000")
#         self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE")
#         self.send_header("Access-Control-Allow-Headers", "*")

#     def do_GET(self):
#         self.send_response(200)
#         self._send_cors_headers()
#         self.end_headers()
#     def do_POST(self):
#         self.send_response(200)
#         self._send_cors_headers()
#         self.end_headers()
#     def do_PUT(self):
#         self.send_response(200)
#         self._send_cors_headers()()
#         self.end_headers()
#     def do_DELETE(self):
#         self.send_response(200)
#         self._send_cors_headers()
#         self.end_headers()

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
    city = db.Column(db.String(30), unique=False)
    state = db.Column(db.String(30), unique=False)
    phone = db.Column(db.Integer, unique=False)

    def __init__(self, firstName, lastName, email, password, city, state, phone):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.city = city
        self.state = state
        self.phone = phone

class UserSchema(ma.Schema) :
    class Meta:
        fields = ('firstName', 'lastName', 'email', 'password', 'city', 'state', 'phone')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=["POST"])
def add_user():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    city = request.json['city']
    state = request.json['state']
    phone = request.json['phone']

    new_user = User(firstName, lastName, email, password, city, state, phone)

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
def update_user(id):
    user = User.query.get(id)
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    city = request.json['city']
    state = request.json['state']
    phone = request.json['phone']

    user.firstName = firstName
    user.lastName = lastName
    user.email = email
    user.password = password
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

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cakeFlavor = db.Column(db.String(30), unique=False)
    frostingFlavor = db.Column(db.String(30), unique=False)
    toppings = db.Column(db.String(30), unique=False)
    filling = db.Column(db.String(30), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    pickupDate = db.Column(db.String(30), unique=False)
    specialRequests = db.Column(db.String(30), unique=False)    

    def __init__(self, cakeFlavor, frostingFlavor, toppings, filling, quantity, pickupDate, specialRequests):
        self.cakeFlavor = cakeFlavor
        self.frostingFlavor = frostingFlavor
        self.toppings = toppings
        self.filling = filling
        self.quantity = quantity
        self.pickupDate = pickupDate
        self.specialRequests = specialRequests

class OrderSchema(ma.Schema) :
    class Meta:
        fields = ('cakeFlavor', 'frostingFlavor', 'toppings', 'filling', 'quantity', 'pickupDate', 'specialRequests')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route('/order', methods=["POST"])
@cross_origin(supports_credentials=True)
def add_order():
    cakeFlavor = request.json['cakeFlavor']
    frostingFlavor = request.json['frostingFlavor']
    toppings = request.json['toppings']
    filling = request.json['filling']
    quantity = request.json['quantity']
    pickupDate = request.json['pickupDate']
    specialRequests = request.json['specialRequests']


    new_order = Order(cakeFlavor, frostingFlavor, toppings, filling, quantity, pickupDate, specialRequests)

    db.session.add(new_order)
    db.session.commit()

    order = Order.query.get(new_order.id)

    return order_schema.jsonify(order)

@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result)

@app.route('/order/<id>', methods=["PUT"])
def update_order(id):
    order = Order.query.get(id)
    cakeFlavor = request.json['cakeFlavor']
    frostingFlavor = request.json['frostingFlavor']
    toppings = request.json['toppings']
    filling = request.json['filling']
    quantity = request.json['quantity']
    pickupDate = request.json['pickupDate']
    specialRequests = request.json['specialRequests']
    
    order.cakeFlavor = cakeFlavor
    order.frostingFlavor = frostingFlavor
    order.toppings = toppings
    order.filling = filling
    order.quantity = quantity
    order.pickupDate = pickupDate
    order.specialRequests = specialRequests

    db.session.commit()
    
    return order_schema.jsonify(order)

    @app.route('./order/<id>', methods=['DELETE'])
    def order_delete(id):
        order = Order.query.get(id)

        db.sessiondelete(order)
        db.session.commit()

        return f'successfully deleted {order}'

if __name__ == '__main__':
    app.run(debug=True)