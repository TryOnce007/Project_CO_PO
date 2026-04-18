from app.models.co import CO
from app.models.course import Course
from app.models.course_assignment import CourseAssignment
from app.models.marks import Mark
from app.models.session import AcademicSession
from app.models.professor import Professor
from app import db


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

        courses = []

        if role == 'HOD':

            hod = Professor.query.get(user_id)

            if hod:
                courses = Course.query.filter_by(branch=hod.branch).all()

            cos_query = CO.query

            if course_id:
                cos_query = cos_query.filter_by(course_id=course_id)

            cos = cos_query.all()

        else:

            assigned_course_ids = db.session.query(
            CourseAssignment.course_id
        ).filter(
            CourseAssignment.faculty_id == user_id
        ).subquery()

        courses = Course.query.filter(
            Course.id.in_(assigned_course_ids)
        ).all()

        cos_query = CO.query.filter(
            CO.course_id.in_(assigned_course_ids)
        )

        # ✅ IMPORTANT FIX: block everything if no course selected
        if not course_id:
            cos = []   # or cos_query.limit(0).all()
        else:
            cos_query = cos_query.filter(CO.course_id == course_id)
            cos = cos_query.all()

        attainment_data = []

        for co in cos:

            if session_id:
                marks = Mark.query.filter_by(
                    co_id=co.id,
                    session_id=session_id
                ).all()
            else:
                marks = Mark.query.filter_by(co_id=co.id).all()

            if not marks:
                level = 'No data'
                percentage = 'N/A'
            else:
                total_obtained = sum(m.obtained for m in marks)
                total_max = sum(m.total for m in marks)

                percentage = round(
                    (total_obtained / total_max) * 100, 2
                ) if total_max else 0

                level = (
                    3 if percentage >= 70 else
                    2 if percentage >= 60 else
                    1 if percentage >= 50 else
                    0
                )

            attainment_data.append({
                'co': co,
                'level': level,
                'percentage': percentage
            })

        return {
            "data": attainment_data,
            "courses": courses,
            "sessions": sessions
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