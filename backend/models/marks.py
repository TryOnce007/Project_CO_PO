# Marks, is the marks scored by student in different course-outcome
# during their session




from backend import db


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    co_id = db.Column(db.Integer, db.ForeignKey('cos.id'), nullable=False)
    
    obtained = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=True)

    indirect_obtained = db.Column(db.Float, nullable=True)
    indirect_total = db.Column(db.Float, nullable=True)

    session = db.Column(db.Integer, db.ForeignKey('academic_sessions.id'))

    student = db.relationship('Student', backref='marks')
    co = db.relationship('CO', backref='marks')


    __table_args__ = (
        db.UniqueConstraint('student_id', 'co_id', 'session', name='uq_mark_entry'),
    )