from . import api
from flask import request
from flask_httpauth import HTTPTokenAuth
from .auth_helper import token_auth_required, token_auth
from ..models import Client, Colorchart

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
        birthday = data['birthday']
        type = data["type"]
        notes = data["notes"]

        newclient = Client(user_id, first_name, last_name, email, phone, birthday, type, notes)
        print(newclient.to_dict())
        newclient.saveToDB()
                
        return {
            'status': 'ok',
            'message': 'Successfully added new client.',
        }, 201
    except:
        return {
            'status': 'not ok',
            'message': 'Not enough info provided to add client, or client may already exists.'
        }, 400
    
@api.post('/delete/client/<int:client_id>')
@token_auth_required
def deleteClientAPI(user, client_id):
    client = Client.query.filter_by(id=client_id).first()

    if client:
        client.deleteFromDB()
        return {
            'status': 'ok',
            'message': "Client successfully deleted!"
        }, 200

@api.post('/update/client/<int:client_id>')
@token_auth_required
def updateClientAPI(user, client_id):
    client = Client.query.filter_by(id=client_id).first()
    data = request.json

    client.first_name = data['first_name']
    client.last_name = data['last_name']
    client.email = data['email']
    client.phone = data['phone']
    client.birthday = data['birthday']
    client.type = data['type']
    client.notes = data['notes']

    if client:
        try:
            client.saveToDB()
                    
            return {
                'status': 'ok',
                'message': 'Client information updated!',
            }, 201
        except:
            return {
                'status': 'not ok',
                'message': 'Error saving updated client information.'
            }, 400


@api.get('/userclients')
@token_auth_required
def getClientsAPI(user):
    # user = token_auth.current_user()
    print(user)
    clients = Client.query.filter_by(user_id= user.id).all()

    if clients:
        return {
            'status': 'ok',
            'results': len(clients),
            'clients': sorted([client.to_dict() for client in clients], key=lambda client: client["first_name"].lower())
        }, 200

@api.get('/client/<int:client_id>')
@token_auth_required
def getSingleClientAPI(user, client_id):
    client = Client.query.filter_by(id=client_id).first()

    if client:
        
        return {
            'status': 'ok',
            'client': client.to_dict()
        }, 200

@api.get('/client/<int:client_id>/colorchart')
@token_auth_required
def getColorChartAPI(user, client_id):
    #check is client has a colorchart
    colorchart = Colorchart.query.filter_by(client_id=client_id).first()

    #if colorchart exists:
    if colorchart:
        #return colorchart dictionary
        return {
            'status': 'ok',
            'colorchart': colorchart.to_dict()
        }, 200
    #elif no colorchart :
    else:
        #create color chart with client ID and user ID
        # , user_id=user.id, porosity=' ', hair_texture=' ', elasticity=' ', scalp_condition=' ', natural_level=' ', desired_level=' ', contrib_pigment=' ', gray_front=' ',gray_sides=' ', gray_back=' ', skin_depth=' ', skin_tone=' ', eye_color=' '
        colorchart = Colorchart(client_id=client_id, user_id=user.id)
        colorchart.saveToDB()
        print(colorchart.to_dict())
        return {
            'status': 'ok',
            'colorchart': colorchart.to_dict()
        }, 200
    

@api.post('/client/<int:client_id>/updatecolorchart')
@token_auth_required
def updateColorChartAPI(user, client_id):
    data = request.json
    chart = Colorchart.query.filter_by(client_id=client_id).first()

    if chart:
        chart.user_id = data['user_id']
        chart.porosity = data['porosity']
        chart.hair_texture = data['hair_texture']
        chart.elasticity = data['elasticity']
        chart.scalp_condition = data['scalp_condition']
        chart.natural_level = data['natural_level']
        chart.desired_level = data['desired_level']
        chart.contrib_pigment = data['contrib_pigment']
        chart.gray_front = data['gray_front']
        chart.gray_sides = data['gray_sides']
        chart.gray_back = data['gray_back']
        chart.skin_depth = data['skin_depth']
        chart.skin_tone = data['skin_tone']
        chart.eye_color = data['eye_color']
        try:
            chart.saveToDB()
                    
            return {
                'status': 'ok',
                'message': 'Colorchart information updated!',
            }, 201
        except:
            return {
                'status': 'not ok',
                'message': 'Error updating colorchart.'
            }, 400
