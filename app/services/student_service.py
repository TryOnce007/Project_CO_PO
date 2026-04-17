from app import db
from app.models.student import Student
from app.models.professor import Professor


class StudentService:

    @staticmethod
    def add_student(form, hod_id):

        batch = form.get('batch')
        roll_no = form.get('roll_no')

        if not batch:
            return False, "Batch is required!"

        if not roll_no:
            return False, "Roll number is required!"

        existing = Student.query.filter_by(roll_no=roll_no).first()
        if existing:
            return False, "Student already exists!"

        hod = Professor.query.get(hod_id)

        if not hod:
            return False, "Unauthorized access!"

        student = Student(
            batch_id=int(batch),
            roll_no=roll_no,
            branch=hod.branch
        )

        db.session.add(student)
        db.session.commit()

        return True, "Student added successfully!"




    @staticmethod
    def get_students(batch, branch):

        if not batch or not branch:
            return []

        query = Student.query.filter_by(branch=branch)

        if batch:
            query = query.filter(Student.batch_id == batch)

        students = query.all()

        return [
            {"id": s.id, "roll_no": s.roll_no}
            for s in students
        ]