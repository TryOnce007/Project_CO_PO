# Session is the different Educational year in which various courses will be taught
# to students of various branches




from app import db 


class AcademicSession(db.Model):
    __tablename__ = 'academic_sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)  
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    course_assignments = db.relationship('CourseAssignment', backref='session', lazy=True)