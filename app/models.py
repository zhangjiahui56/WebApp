from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, index=True, unique=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(20))
    is_admin = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime)
    images = db.relationship('Image', backref='user_images', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    avatar = db.Column(db.String(100), default="default-image.jpg")
    timestamp = db.Column(db.DateTime)
    phases = db.relationship('Phase', backref='plant_phases', lazy='dynamic')

    def __repr__(self):
        return '<Plant %r>' % (self.name)

class Phase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    order = db.Column(db.Integer)
    number_of_days = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))
    images = db.relationship('Image', backref='phase_images', lazy='dynamic')
    plant = db.relationship("Plant", back_populates="phases", uselist=False)

    def __repr__(self):
        return '<Phase %r>' % (self.name)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    phase_id = db.Column(db.Integer, db.ForeignKey('phase.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phase = db.relationship("Phase", back_populates="images", uselist=False)
    user = db.relationship("User", back_populates="images", uselist=False)

    def __repr__(self):
        return '<Image %r>' % (self.filename)