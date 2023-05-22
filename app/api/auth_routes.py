from . import api
from ..models import User
from flask import request
from .auth_helper import token_auth_required, basic_auth, google_auth_required

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
    return {
            'status': 'ok',
            'message': "You have successfully logged in.",
            'data': basic_auth.current_user().to_dict()
        }, 200

@api.post('/google/login')
@google_auth_required
def googleLoginAPI(user):
    return {
            'status': 'ok',
            'message': "You have successfully logged in.",
            'data': user.to_dict()
        }, 200