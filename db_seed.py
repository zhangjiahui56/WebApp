from app import db, models
from werkzeug.security import generate_password_hash
import datetime

u = models.User(username="anh14", password=generate_password_hash("123456"), name="anh", timestamp=datetime.datetime.utcnow())
db.session.add(u)

u = models.User(username="vutuananh", password=generate_password_hash("123456"), name="tuananh", is_admin=1,  timestamp=datetime.datetime.utcnow())
db.session.add(u)

u = models.User(username="anh17", password=generate_password_hash("1234567"), name="tuananh", timestamp=datetime.datetime.utcnow())
db.session.add(u)

db.session.commit()


