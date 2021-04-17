from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir =os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), unique=False)
    lastname = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30), unique=False)
    city = db.Column(db.String(30), unique=False)
    state = db.Column(db.String(30), unique=False)
    phone = db.Column(db.Integer, unique=False)
    question = db.Column(db.String(50), unique=False)
    answer =  db.Column(db.String(30), unique=False)

    def __init__(self, firstname, lastname, email, password, city, state, phone, question, answer):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.city = city
        self.state = state
        self.phone = phone
        self.question = question
        self.answer = answer

class UserSchema(ma.Schema) :
    class Meta:
       fields = ('firstname', 'lastname', 'email', 'password', 'city', 'state', 'phone', 'question', 'answer')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=["POST"])
def add_user():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    city = request.json['city']
    state = request.json['state']
    phone = request.json['phone']
    question = request.json['question']
    answer = request.json['answer']

    new_user = User(firstname, lastname, email, password, city, state, phone, question, answer)

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
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    city = request.json['city']
    state = request.json['state']
    phone = request.json['phone']
    question = request.json['question']
    answer = request.json['answer']

    user.firstname = firstname
    user.lastname = lastname
    user.email = email
    user.password = password
    user.city = city
    user.state = state
    user.phone = phone
    user.question = question
    user.answer = answer

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
    cake_flavor = db.Column(db.String(30), unique=False)
    frosting_flavor = db.Column(db.String(30), unique=False)
    toppings = db.Column(db.String(30), unique=False)
    filling = db.Column(db.String(30), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    pickup_date = db.Column(db.String(30), unique=False)
    special_requests = db.Column(db.String(30), unique=False) 

    def __init__(self, cake_flavor, frosting_flavor, toppings, filling, quantity, pickup_date, special_requests):
        self.cake_flavor = cake_flavor
        self.frosting_flavor = frosting_flavor
        self.toppings = toppings
        self.filling = filling
        self.quantity = quantity
        self.pickup_date = pickup_date
        self.special_requests = special_requests

class OrderSchema(ma.Schema) :
    class Meta:
        fields = ('cake_flavor', 'frosting_flavor', 'toppings', 'filling', 'quantity', 'pickup_date', 'special_requests')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route('/order', methods=["POST"])
def add_order():
    cake_flavor = request.json['cake_flavor']
    frosting_flavor = request.json['frosting_flavor']
    toppings = request.json['toppings']
    filling = request.json['filling']
    quantity = request.json['quantity']
    pickup_date = request.json['pickup_date']
    special_requests = request.json['special_requests']
    
    new_order = Order(cake_flavor, frosting_flavor, toppings, filling, quantity, pickup_date, special_requests)

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
    cake_flavor = request.json['cake_flavor']
    frosting_flavor = request.json['frosting_flavor']
    toppings = request.json['toppings']
    filling = request.json['filling']
    quantity = request.json['quantity']
    pickup_date = request.json['pickup_date']
    special_requests = request.json['special_requests']
        
    order.cake_flavor = cake_flavor
    order.frosting_flavor = frosting_flavor
    order.toppings = toppings
    order.filling = filling
    order.quantity = quantity
    order.pickup_date = pickup_date
    order.special_requests = special_requests
    
    db.session.commit()
    
    return order_schema.jsonify(order)

    @app.route('/order/<id>', methods=['DELETE'])
    def order_delete(id):
        order = Order.query.get(id)

        db.sessiondelete(order)
        db.session.commit()

        return f'successfully deleted {order}'

if __name__ == '__main__':
    app.run(debug=True)

