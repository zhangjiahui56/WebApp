from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from LeafCounting.model import *
model = LeafCountingModel()
model.load_weights('./LeafCounting/model_weights/model_125_final_backup.h5')

from app import views, models

from . import admin_views
app.register_blueprint(admin_views.bp)