# Marks, is the marks scored by student in different course-outcome
# during their session




from backend import db


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    co_id = db.Column(db.Integer, db.ForeignKey('cos.id'), nullable=False)
    obtained = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    session = db.Column(db.Integer, db.ForeignKey('academic_sessions.id'))

    student = db.relationship('Student', backref='marks')
    co = db.relationship('CO', backref='marks')