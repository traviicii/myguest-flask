from . import api
from flask import request
from flask_httpauth import HTTPTokenAuth
from .auth_helper import token_auth_required, token_auth
from ..models import Client, Colorchart, Formula, Image

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


@api.post('/userclients')
@token_auth_required
def getClientsAPI(user):
    # user = token_auth.current_user()
    clients = Client.query.filter_by(user_id = user.id).all()

    data = request.json
    sortby = data["sortby"]

    if clients:
        return {
            'status': 'ok',
            'results': len(clients),
            'clients': sorted([client.to_dict() for client in clients], key=lambda client: client[sortby].lower())
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

@api.post('/client/<int:client_id>/createformula')
@token_auth_required
def addFormulaAPI(user, client_id):
    try:
        data = request.json
        
        date = data['date']
        price = data['price']
        type = data["type"]
        notes = data["notes"]

        new_formula = Formula(client_id=client_id, notes=notes, price=price, type=type, date=date)
        new_formula.saveToDB()

        formula = Formula.query.filter_by(date=date, client_id=client_id).first()
        
        return {
                'status': 'ok',
                'message': 'Successfully added new appointment entry.',
                "forumula_id": formula.id
            }, 201
    except:
        return {
            'status': 'not ok',
            'message': 'Error within create formula API route. An entry with that date might already exist.'
        }, 400
    
@api.post('/client/<int:client_id>/addimages')
@token_auth_required
def addImagesAPI(user, client_id):
    data = request.json 
    date = data['date']
    try:
        formula = Formula.query.filter_by(date=date, client_id=client_id).first()
        print(formula.id, "FORMULA ID")

        if data["image1_url"]:
            image1_url = data["image1_url"]
            image1_name = data["image1_name"]
            URL1 = Image(client_id=client_id, formula_id=formula.id, image_url=image1_url, image_name=image1_name)
            URL1.saveToDB()

        if data["image2_url"]:
            image2_url = data["image2_url"]
            image2_name = data["image2_name"]
            URL1 = Image(client_id=client_id, formula_id=formula.id, image_url=image2_url, image_name=image2_name)
            URL1.saveToDB()

        if data["image3_url"]:
            image3_url = data["image3_url"]
            image3_name = data["image3_name"]
            URL1 = Image(client_id=client_id, formula_id=formula.id, image_url=image3_url, image_name=image3_name)
            URL1.saveToDB()
        
        return {
            'status': 'ok',
            'message': 'Successfully saved images to database.',
        }, 201
    except:
        return {
            'status': 'not ok',
            'message': 'Error within add images API route.'
        }, 400
    
@api.get('/client/<int:client_id>/getformulas')
@token_auth_required
def getFormulasAPI(user, client_id):
    formulas = Formula.query.filter_by(client_id = client_id).all()
    # data = request.json
    # sortby = data["sortby"]

    if formulas:
        return {
            'status': 'ok',
            'results': len(formulas),
            'formulas': sorted([formula.to_dict() for formula in formulas], reverse=True, key=lambda formula: formula["date"])
        }, 200
    else:
        return {
            'status': 'ok',
            'message': 'No formulas to show'
        }
    
@api.get('/formula/<int:formula_id>/getimages')
@token_auth_required
def getImagesAPI(user, formula_id):
    try:
        images = Image.query.filter_by(formula_id = formula_id).all()
        if images:
            return {
                'status': 'ok',
                'results': len(images),
                'images': [image.to_dict() for image in images]
            }, 200
        
        else:
            return {
                'status': 'ok',
                'message': f'No images available for formula {formula_id}'
            }, 200
    except:
        return {
            'status': 'not ok',
            'message': 'Error getting images from API'
        }
    
@api.get('/formula/<int:formula_id>/getformula')
@token_auth_required
def getFormulaAPI(user, formula_id):
    formula = Formula.query.get(formula_id)
    images = Image.query.filter_by(formula_id=formula_id).all()

    if formula:
        if images:
            return {
                'status': 'ok',
                'formula': formula.to_dict(),
                'images': [image.to_dict() for image in images]
            }, 200
        else:
            return {
                'status': 'ok',
                'formula': formula.to_dict()
            }, 200
        
@api.post('/formula/<int:formula_id>/updateformula')
@token_auth_required
def updateFormulaAPI(user, formula_id):
    data = request.json 

    formula = Formula.query.get(formula_id)

    notes = data['notes']
    price = data['price']
    type = data['type']
    date = data['date']
    trash_can = data['imageTrashCan']

    if formula:
        formula.notes = notes
        formula.price = price
        formula.type = type
        formula.date = date
        formula.saveToDB()
        if trash_can:
            for id in trash_can:
                image = Image.query.get(id)
                image.deleteFromDB()
            return {
                'status': 'ok',
                'message': 'Successfully update entry and images!'
            }, 200
        
        return {
            'status': 'ok',
            'message': 'Successfully updated entry!'
        }, 200
    else:
        return {
            'status': 'not ok',
            'message': 'Error occured updating formula. Try again?'
        }, 404

@api.post('/formula/<int:formula_id>/deleteformula')
@token_auth_required
def deleteFormulaAPI(user, formula_id):
    formula = Formula.query.get(formula_id)

    if formula:
        formula.deleteFromDB()
        return {
            'status': 'ok',
            'message': "Appointment successfully deleted!"
        }, 200
    else:
        return {
            'status': 'not ok',
            'meaasge': 'That appointment does not exist.'
        }, 404

