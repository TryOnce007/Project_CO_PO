# Professor is the record of every faculty including HODs that are in service
# and providing their services to the Institute




from app import db
from werkzeug.security import generate_password_hash, check_password_hash



class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    branch = db.Column(
            db.String(100),
            db.ForeignKey('branch.code'),
            nullable=False
        )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)