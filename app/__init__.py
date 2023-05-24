from flask import Flask
from .models import db, User
from flask_migrate import Migrate
from config import Config
from .api import api
from flask_cors import CORS
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
cors = CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(api)

from . import routes
#from . import models (doesn't exist yet, just save it for later)