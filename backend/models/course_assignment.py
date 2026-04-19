#  Courseassignment, is the Relationship between which course will be taught by which faculty during different
# sessions




from backend import db


class CourseAssignment(db.Model):
    __tablename__ = 'course_assignments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('academic_sessions.id'), nullable=False)

    assigned_on = db.Column(db.DateTime, default=db.func.now())

    course = db.relationship('Course', backref='assignments')
    faculty = db.relationship('Professor', backref='assignments')
    batch = db.relationship('Batch', backref='assignments')


    __table_args__ = (
        db.UniqueConstraint('course_id', 'session_id', name='unique_course_session'),
    )
