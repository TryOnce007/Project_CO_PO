from app import db
from app.models.course import Course
from app.models.professor import Professor


class CourseService:


    @staticmethod
    def create_course(hod_id, form):

        hod = Professor.query.get(hod_id)

        if not hod:
            return {
                "success": False,
                "message": "Unauthorized access!",
                "category": "danger"
            }

        course_name = form.get('course_name', '').strip()
        course_code = form.get('course_code', '').strip().upper()

        if not course_name or not course_code:
            return {
                "success": False,
                "message": "Both Course Name and Code required!",
                "category": "danger"
            }

        existing = Course.query.filter_by(
            code=course_code,
            branch=hod.branch
        ).first()

        if existing:
            return {
                "success": False,
                "message": "Course already exists!",
                "category": "warning"
            }

        course = Course(
            name=course_name,
            code=course_code,
            branch=hod.branch
        )

        db.session.add(course)
        db.session.commit()

        return {
            "success": True,
            "message": "Course created successfully!",
            "category": "success"
        }


    @staticmethod
    def get_courses_by_hod(hod_id):

        hod = Professor.query.get(hod_id)

        if not hod:
            return []

        return Course.query.filter_by(branch=hod.branch).all()