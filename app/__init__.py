from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# from werkzeug.wsgi import SharedDataMiddleware
# app.add_url_rule('/images/uploads/<filename>', 'uploaded_file',
#                  build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/images/uploads':  app.config['UPLOAD_FOLDER']
# })

# from LeafCounting.model import *
# model = LeafCountingModel()
# model.load_weights('./LeafCounting/model_weights/model_125_final_backup.h5')

from app import views, models

from . import admin_views
app.register_blueprint(admin_views.bp)