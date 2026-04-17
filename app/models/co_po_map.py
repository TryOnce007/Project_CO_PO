# COPOMap, is the relationship between Course-Outcome and Program-Outcome, means how much a CO contribute to PO




from app import db 


class COPOMap(db.Model):
    __tablename__ = 'co_po_map'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    co_id = db.Column(db.Integer, db.ForeignKey('cos.id'), nullable=False)
    po_id = db.Column(db.Integer, db.ForeignKey('pos.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)