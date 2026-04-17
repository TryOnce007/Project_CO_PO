from app.models.professor import Professor
from app.models.course import Course
from app.models.po import PO
from app.models.batch import Batch
from app.models.course_assignment import CourseAssignment
from app.models.session import AcademicSession
from app import db


class HODService:

    @staticmethod
    def add_teacher(hod_id, form):

        hod = Professor.query.get(hod_id)

        if not hod:
            return {"message": "Unauthorized access!", "category": "danger"}

        username = form.get("username")
        phone = form.get("phone")
        password = form.get("password")
        role = form.get("role")

        if not all([username, phone, password, role]):
            return {"message": "All fields required!", "category": "danger"}

        if Professor.query.filter_by(username=username).first():
            return {"message": "Username already exists!", "category": "danger"}

        teacher = Professor(
            username=username,
            phone=phone,
            role=role,
            branch=hod.branch
        )

        teacher.set_password(password)

        db.session.add(teacher)
        db.session.commit()

        return {"message": "Teacher added successfully!", "category": "success"}



    @staticmethod
    def add_po(hod_id, form):

        hod = Professor.query.get(hod_id)

        description = form.get("description")

        if not description:
            return {"message": "Description required!", "category": "danger"}

        po = PO(description=description, branch=hod.branch)

        db.session.add(po)
        db.session.commit()

        return {"message": "PO added successfully!", "category": "success"}



    @staticmethod
    def assign_course(form):

        batch_id = form.get("batch_id")
        course_id = form.get("course_id")
        faculty_id = form.get("faculty_id")
        session_id = form.get("session_id")

        if not all([batch_id, course_id, faculty_id, session_id]):
            return {"message": "All fields required!", "category": "danger"}

        existing = CourseAssignment.query.filter_by(
            batch_id=batch_id,
            course_id=course_id,
            faculty_id=faculty_id,
            session_id=session_id
        ).first()

        if existing:
            return {"message": "Assignment already exists!", "category": "warning"}

        db.session.add(CourseAssignment(
            batch_id=batch_id,
            course_id=course_id,
            faculty_id=faculty_id,
            session_id=session_id
        ))

        db.session.commit()

        return {"message": "Course assigned successfully!", "category": "success"}



    @staticmethod
    def get_assignments(hod_id):

        hod = Professor.query.get(hod_id)

        if not hod:
            return {}

        assignments = (
            CourseAssignment.query
            .join(Course, Course.id == CourseAssignment.course_id)
            .filter(Course.branch == hod.branch)
            .all()
        )

        faculty = Professor.query.filter_by(
            role='Faculty',
            branch=hod.branch
        ).all()

        return {
            "assignments": assignments,
            "faculty": faculty,
            "sessions": AcademicSession.query.all(),
            "batches": Batch.query.all()
        }



    @staticmethod
    def add_session(form):

        name = form.get("name")
        start_date = form.get("start_date")
        end_date = form.get("end_date")

        if not name:
            return {"message": "Session name required!", "category": "danger"}

        if AcademicSession.query.filter_by(name=name).first():
            return {"message": "Session already exists!", "category": "warning"}

        db.session.add(AcademicSession(
            name=name,
            start_date=start_date or None,
            end_date=end_date or None
        ))

        db.session.commit()

        return {"message": "Session created successfully!", "category": "success"}