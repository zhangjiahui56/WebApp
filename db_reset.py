from app import db, models

users = models.User.query.all()
for user in users:
    db.session.delete(user)

posts = models.Post.query.all()
for post in posts:
    db.session.delete(post)

db.session.commit()