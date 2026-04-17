# CO, is the Course-Outcomes of varoius Courses




from app import db


class CO(db.Model):
    __tablename__ = 'cos'  
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)

   
    copo_maps = db.relationship('COPOMap', backref='cos', lazy=True)