# PO, is the Departmental Program-outcome, which are used to provide quality education and to
# evaluate the overall performance of the student during course




from app import db 


class PO(db.Model):
    __tablename__ = 'pos'  
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    description = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(50), nullable=False)

    copo_maps = db.relationship('COPOMap', backref='po', lazy=True)