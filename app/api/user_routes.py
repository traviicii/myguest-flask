from . import api
from flask import request
from flask_httpauth import HTTPTokenAuth
from .auth_helper import token_auth_required
from ..models import Client

token_auth = HTTPTokenAuth()

@api.post('/addclient')
@token_auth_required
def addClientAPI(user):
    try:
        data = request.json
        print(data)
        
        user_id = data["user_id"]
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data["phone"]
        birthday = data["birthday"]
        type = data["type"]
        notes = data["notes"]

        newclient = Client(user_id, first_name, last_name, email, phone, birthday, type, notes)

        newclient.saveToDB()

                
        return {
            'status': 'ok',
            'message': 'Successfully added new client.',
        }, 201
    except:
        return {
            'status': 'not ok',
            'message': 'Not enough info provided to add client.'
        }, 400
    

@api.get('/userclients')
@token_auth_required
def getClientsAPI(user):
    # user = token_auth.current_user()
    # print(user)
    clients = Client.query.filter_by(user_id= user.id).all()

    if clients:
        return {
            'status': 'ok',
            'results': len(clients),
            'clients': [client.to_dict() for client in clients]
        }, 200
