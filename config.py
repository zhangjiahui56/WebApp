import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

dbhost = 'localhost'
dbuser = 'root'
dbpass = ''
dbname = 'webapp'

SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'app/static/uploads/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
PLANT_AVATAR_FOLDER = 'app/static/img/plant-img'

UPLOAD_ZIP_FOLDER = 'app/static/uploads/zip_files'
EXTRACT_ZIP_FOLDER = 'app/static/uploads/zip_folders'

GRAPH_IMAGES_FOLDER = 'app/static/uploads/graph_images'
DOWNLOAD_IMAGES = 'static/uploads/graph_images'