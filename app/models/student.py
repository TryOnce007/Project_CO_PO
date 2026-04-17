# Student is the record of all students of various Batches




from app import db


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.Integer, nullable=False)
    branch = db.Column(db.String(50), nullable=False)

    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)

    batch = db.relationship('Batch', backref='students')

    __table_args__ = (
        db.UniqueConstraint('batch_id', 'roll_no', name='unique_roll_in_batch'),
    )
