# Branch, is the stream in which students is currently enrolled for the duration of course
# code here specifies the unique code given to each branch




from backend import db 

class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    professors = db.relationship('Professor', backref='branch_ref', lazy=True)

    def __repr__(self):
        return f"<Branch {self.code}>"