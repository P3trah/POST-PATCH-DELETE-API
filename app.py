from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)

class UserSchema(ma.Schema):
    class Meta:
fields = ('id', 'name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)
    name = request.json['name']
    email = request.json['email']

    user.name = name
    user.email = email

    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)