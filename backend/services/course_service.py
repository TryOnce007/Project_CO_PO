from backend import db
from backend.models.course import Course
from backend.models.professor import Professor


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
    

    @staticmethod
    def add_course(hod_id, form):
       

        course_name = form.get("course_name", "").strip()
        course_code = form.get("course_code", "").strip().upper()

        if not course_name or not course_code:
            return {
                "status": "error",
                "message": "Both Course Name and Course Code are required!"
            }

        hod = Professor.query.get(hod_id)

        if not hod:
            return {
                "status": "error",
                "message": "Unauthorized access!"
            }

        existing = Course.query.filter_by(
            code=course_code,
            branch=hod.branch
        ).first()

        if existing:
            return {
                "status": "error",
                "message": "Course already exists in your branch!",
                "category": "danger"
            }

        try:
            new_course = Course(
                name=course_code,
                code=course_name,
                branch=hod.branch
            )

            db.session.add(new_course)
            db.session.commit()

            return {
                "status": "success",
                "message": "Course added successfully under your branch!",
                "category": "success"
            }

        except Exception as e:
            db.session.rollback()

            return {
                "status": "error",
                "message": f"Error adding course: {str(e)}",
                "category": "danger"
            }