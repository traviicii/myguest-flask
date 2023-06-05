from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from secrets import token_hex

db = SQLAlchemy()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key= True)
    photoURL = db.Column(db.String(500))
    password = db.Column(db.String(150), nullable = True)
    uid = db.Column(db.String(50))
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    apitoken = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __init__(self, photoURL, password, uid, first_name, last_name, email ):
        self.photoURL = photoURL
        self.password = generate_password_hash(password)
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.apitoken = token_hex(16)

    def to_dict(self):
        return {
            'id': self.id,
            'photoURL': self.photoURL,
            'uid': self.uid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'apitoken': self.apitoken,
            'date_created': self.date_created
        }
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()


class Client(db.Model):

    id = db.Column(db.Integer, primary_key = True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(100), nullable = True, unique = False)
    phone = db.Column(db.String, autoincrement = False)
    birthday = db.Column(db.String)
    type = db.Column(db.String(20))
    notes = db.Column(db.String(800))

    def __init__(self, user_id, first_name, last_name, email, phone, birthday, type, notes):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.type = type
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "birthday": self.birthday,
            "type": self.type,
            "notes": self.notes
        }

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()


class Colorchart(db.Model):

    id = db.Column(db.Integer, primary_key = True, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    client = db.relationship('Client', cascade="all, delete")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    porosity = db.Column(db.String(25))
    hair_texture = db.Column(db.String(25))
    elasticity = db.Column(db.String(25))
    scalp_condition = db.Column(db.String(25))
    natural_level = db.Column(db.String(50))
    desired_level = db.Column(db.String(50))
    contrib_pigment = db.Column(db.String(25))
    gray_front = db.Column(db.String(4), autoincrement = False)
    gray_sides = db.Column(db.String(4), autoincrement = False)
    gray_back = db.Column(db.String(4), autoincrement = False)
    skin_depth = db.Column(db.String(25))
    skin_tone = db.Column(db.String(25))
    eye_color = db.Column(db.String(25))
# , porosity, hair_texture, elasticity, scalp_condition, natural_level, desired_level, contrib_pigment, gray_front, gray_sides, gray_back, skin_depth, skin_tone, eye_color
    def __init__(self, client_id, user_id):
        self.client_id = client_id
        self.user_id = user_id
        # self.porosity = porosity
        # self.hair_texture = hair_texture
        # self.elasticity = elasticity
        # self.scalp_condition = scalp_condition
        # self.natural_level = natural_level 
        # self.desired_level = desired_level 
        # self.contrib_pigment = contrib_pigment 
        # self.gray_front = gray_front
        # self.gray_sides = gray_sides 
        # self.gray_back =  gray_back
        # self.skin_depth = skin_depth
        # self.skin_tone = skin_tone
        # self.eye_color = eye_color

    # will probably need a to_dict() func

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "user_id": self.user_id,
            "porosity": self.porosity,
            "hair_texture": self.hair_texture,
            "elasticity": self.elasticity,
            "scalp_condition": self.scalp_condition,
            "natural_level": self.natural_level,
            "desired_level": self.desired_level,
            "contrib_pigment": self.contrib_pigment,
            "gray_front": self.gray_front,
            "gray_sides": self.gray_sides,
            "gray_back": self.gray_back,
            "skin_depth": self.skin_depth,
            "skin_tone": self.skin_tone,
            "eye_color": self.eye_color
        }


class Formula(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    client = db.relationship('Client', cascade="all, delete")
    notes = db.Column(db.String(750))
    price = db.Column(db.String)
    type = db.Column(db.String(20))
    date = db.Column(db.String, unique = False, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __init__(self, client_id, notes, price, type, date):
        self.client_id = client_id
        self.notes = notes
        self.price = price
        self.type = type
        self.date = date

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "notes": self.notes,
            "price": self.price,
            "type": self.type,
            "date": self.date,
            "date_created": self.date_created
        }

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    formula_id = db.Column(db.Integer, db.ForeignKey('formula.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    imageURL = db.Column(db.String, nullable = False, unique = False)
    image_name = db.Column(db.String, nullable = False)

    def __init__(self, client_id, formula_id, image_url, image_name):
        self.client_id = client_id
        self.formula_id = formula_id
        self.imageURL = image_url
        self.image_name = image_name

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "formula_id": self.formula_id,
            "imageURL": self.imageURL,
            "image_name": self.image_name
        }