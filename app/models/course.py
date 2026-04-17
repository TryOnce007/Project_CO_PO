# COurse, is the various subjects a student will will learn during his course duration




from app import db



class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    branch = db.Column(db.String(50), nullable=False)

    cos = db.relationship('CO', backref='course', lazy=True)