from app import db, models

images = models.Image.query.all()
for image in images:
    db.session.delete(image)

phases = models.Phase.query.all()
for phase in phases:
    db.session.delete(phase)

plants = models.Plant.query.all()
for plant in plants:
    db.session.delete(plant)

users = models.User.query.all()
for user in users:
    db.session.delete(user)

db.session.commit()