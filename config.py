import os

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_APPLICATION_CREDENTIALS = os.path.abspath(os.path.dirname("client-keeper-a2e91-firebase-adminsdk-tvdur-917c3f59a9"))

temp = 'GOOGLE_APPLICATION_CREDENTIALS'