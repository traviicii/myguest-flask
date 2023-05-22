from flask import Flask
from .models import db
from flask_migrate import Migrate
from config import Config
from .api import api
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
cors = CORS(app)

app.register_blueprint(api)

from . import routes
#from . import models (doesn't exist yet, just save it for later)