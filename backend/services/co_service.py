from backend.models.co import CO
from backend.models.course import Course
from backend.models.course_assignment import CourseAssignment
from backend.models.marks import Mark
from backend.models.session import AcademicSession
from backend.models.professor import Professor
from backend.utils.co_po_calculator import calculate_co_stats
from backend import db



def get_courses_by_role(user_id, role):

    if role == 'HOD':
        hod = Professor.query.get(user_id)
        if not hod:
            return []
        return Course.query.filter_by(branch=hod.branch).all()

    assigned_course_ids = db.session.query(
        CourseAssignment.course_id
    ).filter(
        CourseAssignment.faculty_id == user_id
    ).subquery()

    return Course.query.filter(
        Course.id.in_(assigned_course_ids)
    ).all()



def get_cos_by_role(user_id, role, course_id=None):

    if role == 'HOD':
        query = CO.query
        if course_id:
            query = query.filter_by(course_id=course_id)
        return query.all()

    assigned_course_ids = db.session.query(
        CourseAssignment.course_id
    ).filter(
        CourseAssignment.faculty_id == user_id
    ).subquery()

    query = CO.query.filter(
        CO.course_id.in_(assigned_course_ids)
    )

    if course_id:
        query = query.filter(CO.course_id == course_id)

    return query.all()


class COService:

    @staticmethod
    def get_faculty_courses(faculty_id):

        return db.session.query(Course).join(CourseAssignment).filter(
            CourseAssignment.faculty_id == faculty_id
        ).all()
    

    


    @staticmethod
    def add_co(faculty_id, description, course_id):

        if not description or not course_id:
            return {
                "message": "CO description and course required!",
                "category": "danger"
            }

        valid = CourseAssignment.query.filter_by(
            faculty_id=faculty_id,
            course_id=course_id
        ).first()

        if not valid:
            return {
                "message": "You are not assigned to this course!",
                "category": "danger"
            }

        try:
            co = CO(
                description=description,
                course_id=int(course_id)
            )
            db.session.add(co)
            db.session.commit()

            return {
                "message": "CO added successfully!",
                "category": "success"
            }

        except Exception as e:
            db.session.rollback()
            return {
                "message": f"Error: {str(e)}",
                "category": "danger"
            }

    @staticmethod
    def get_attainment(user_id, role, course_id, session_id):

        sessions = AcademicSession.query.all()
        courses = get_courses_by_role(user_id, role)

        cos_query = CO.query

        if role != 'HOD':
            assigned_course_ids = db.session.query(
                CourseAssignment.course_id
            ).filter(
                CourseAssignment.faculty_id == user_id
            ).subquery()

            cos_query = cos_query.filter(
                CO.course_id.in_(assigned_course_ids)
            )

        if session_id:
            co_ids_with_session = db.session.query(Mark.co_id).filter(
                Mark.session == session_id
            ).distinct()

            cos_query = cos_query.filter(CO.id.in_(co_ids_with_session))

        if course_id:
            cos_query = cos_query.filter(CO.course_id == course_id)

        cos = cos_query.all()

        co_stats, _ = calculate_co_stats(cos, session_id)

        return {
            "data": [
                {
                    "co": item["co"],
                    "level": item["level"],
                    "percent": item["percent"]
                }
                for item in co_stats
            ],
            "courses": [{"id": c.id, "name": c.name} for c in courses],
            "sessions": [{"id": s.id, "name": s.name} for s in sessions],
            "selected_course_id": course_id,
            "selected_session_id": session_id
        }

    @staticmethod
    def get_cos_by_course(course_id):
        if not course_id:
            return []

        cos = CO.query.filter_by(course_id=course_id).all()

        return [
            {
                "id": co.id,
                "description": co.description
            }
            for co in cos
        ]
    

    