# Batch, means the year in which student is admitted into Institute




from backend import db


class Batch(db.Model):
    __tablename__ = 'batch'

    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.Integer, nullable=False)
