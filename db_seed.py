from app import db, models
from werkzeug.security import generate_password_hash
import datetime

u = models.User(username="anh14", password=generate_password_hash("123456"), name="anh", address="abc", phone_number="1202102010", timestamp=datetime.datetime.utcnow())
db.session.add(u)

u = models.User(username="vutuananh", password=generate_password_hash("123456"), name="tuananh", is_admin=1, address="abc", phone_number="1202102010",  timestamp=datetime.datetime.utcnow())
db.session.add(u)

u = models.User(username="anh17", password=generate_password_hash("1234567"), name="tuananh", address="abc", phone_number="1202102010", timestamp=datetime.datetime.utcnow())
db.session.add(u)

p = models.Plant(name="Cây cải", number_of_days=23, timestamp=datetime.datetime.utcnow())
db.session.add(p)

db.session.commit()

ph = models.Phase(name="Nảy mầm", order=1, number_of_days=6, plant_id=p.id, timestamp=datetime.datetime.utcnow())
db.session.add(ph)

ph = models.Phase(name="Mở rộng thân", order=2, number_of_days=10, plant_id=p.id, timestamp=datetime.datetime.utcnow())
db.session.add(ph)

ph = models.Phase(name="Tăng lá", order=3, number_of_days=7, plant_id=p.id, timestamp=datetime.datetime.utcnow())
db.session.add(ph)

# img = models.Image(filename='04202020220307445491_rgb_00_000_05.png', phase_id=14, user_id=98, timestamp=datetime.datetime.utcnow())
# db.session.add(img)
# img = models.Image(filename='04212020094726461185_rgb_00_001_00.png', phase_id=13, user_id=99, timestamp=datetime.datetime.utcnow())
# db.session.add(img)
# img = models.Image(filename='04212020180127683270_rgb_00_008_04.png', phase_id=14, user_id=97, timestamp=datetime.datetime.utcnow())
# db.session.add(img)
# img = models.Image(filename='05092020125657052294_rgb_04_009_04.png', phase_id=15, user_id=99, timestamp=datetime.datetime.utcnow())
# db.session.add(img)
# img = models.Image(filename='04212020175214517025_rgb_00_001_00.png', phase_id=15, user_id=99, timestamp=datetime.datetime.utcnow())
# db.session.add(img)

db.session.commit()


