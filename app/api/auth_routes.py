from . import api
from ..models import User
from flask import request
from .auth_helper import token_auth_required, basic_auth, google_auth_required
from werkzeug.security import generate_password_hash

@api.post('/signup')
def signUpAPI():
    data = request.json

    photoURL = data["photoURL"]
    password = data["password"]
    uid = data["uid"]
    first_name =  data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    user = User.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email already exists, please choose a different one.'
        }, 400
    
    user = User(photoURL, password, uid, first_name, last_name, email)
    user.saveToDB()
    return {
        'status': 'ok',
        'message': 'Account successfully created!'
    }, 201


@api.post('/googlesignup')
def googleSignUpAPI():
    data = request.json

    if data["displayName"]:
        temp = data["displayName"].split(" ")
        first = temp[0] 
        last = temp[1]

    photoURL = data["photoURL"]
    password = data["password"]
    uid = data["uid"]
    first_name =  first if data["displayName"] else ''
    last_name = last if data["displayName"] else ''
    email = data["email"]

    user = User.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email already exists, please choose a different one.'
        }, 400
    
    user = User(photoURL, password, uid, first_name, last_name, email)
    user.saveToDB()
    return {
        'status': 'ok',
        'message': 'Account successfully created!'
    }, 201

@api.post('/login')
@basic_auth.login_required
def loginAPI():
    if basic_auth.current_user():
        return {
                'status': 'ok',
                'message': "You have successfully logged in.",
                'data': basic_auth.current_user().to_dict()
            }, 200
    else:
        return {
            'status': 'ok',
            'message': "Incorrect username/password.",
        }, 401

@api.post('/google/login')
@google_auth_required
def googleLoginAPI(user):
    return {
            'status': 'ok',
            'message': "You have successfully logged in.",
            'data': user.to_dict()
        }, 200

@api.post('/user/<int:user_id>/deleteaccount')
@token_auth_required
def deleteUserAPI(user, user_id):
    user = User.query.get(user_id)

    if user:
        user.deleteFromDB()
        return {
            'status': 'ok',
            'message': 'Account successfully deleted. :('
        }, 200
    else:
        return {
            'status': 'not ok',
            'message': "Couldn't complete account deletion"
        }, 404
    
@api.post('/user/updateaccount')
@token_auth_required
def updateUserAccountAPI(user):
    user = User.query.get(user.id)

    data = request.json

    if user:
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        if data['password']:
            user.password = generate_password_hash(data['password'])
        else:
            pass
        user.saveToDB()
        return {
            'status': 'ok',
            'message': 'Successfully updated account info!'
        }