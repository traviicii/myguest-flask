from flask import request
from werkzeug.security import check_password_hash
from ..models import User
import firebase_admin
from firebase_admin import auth, credentials
import os
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            return user

        
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

def token_auth_required(func):
    def decorated(*arg, **kwargs):
        #before
        if "Authorization" in request.headers:
            val = request.headers["Authorization"]

            protocol, token = val.split()
            if protocol == 'Bearer':
                pass

            else:
                return {
                    'status': 'not ok',
                    'message': 'Please use Token Authentication (Bearer Token)'
                }
        else:
            return {
                    'status': 'not ok',
                    'message': 'Please include header Authentication with Token Auth using a Bearer Token'
                }
        user = User.query.filter_by(apitoken = token).first()
        if user:
            return func(user=user, *arg, **kwargs)
        else:
            return {
                    'status': 'not ok',
                    'message': 'Token does not belong to a valid user.'
                }
    decorated.__name__ = func.__name__
    return decorated


def google_auth_required(func):
    def decorated(*arg, **kwargs):
        #before
        if "Authorization" in request.headers:
            val = request.headers["Authorization"]

            protocol, token = val.split()
            if protocol == 'Bearer':
                pass

            else:
                return {
                    'status': 'not ok',
                    'message': 'Please use Token Authentication (Bearer Token)'
                }
        else:
            return {
                    'status': 'not ok',
                    'message': 'Please include header Authentication with Token Auth using a Bearer Token'
                }

        # check if the token is authenticated through Google 
        decoded_token = auth.verify_id_token(token)
        # the user's ID 
        uid = decoded_token['uid']
        # NOW check if that user exists... 
        user = User.query.filter_by(uid=uid).first()
        if user:
            return func(user=user, *arg, **kwargs)

        return {
                'status': 'not ok',
                'message': 'Token does not belong to a valid user.'
            }
    decorated.__name__ = func.__name__
    return decorated