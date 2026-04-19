from backend.models.course import Course
from backend.models.professor import Professor
from backend.models.course_assignment import CourseAssignment
from backend.utils.po_engine import calculate_po_attainment


def get_course_list_for_role(user_id, role):


    if role == "Faculty":

        return Course.query.join(CourseAssignment)\
            .filter(CourseAssignment.faculty_id == user_id)\
            .all()

    elif role == "HOD":

        hod = Professor.query.get(user_id)

        if not hod:
            return []

        return Course.query.filter_by(branch=hod.branch).all()
    
    elif role == "Admin":

        return Course.query.all()

    return []




def get_po_attainment_data(course_id, session_id):

    if not course_id or not session_id:
        return None, "Missing course or session"

    course = Course.query.get(course_id)

    if not course:
        return None, "Invalid course"

    po_stats = calculate_po_attainment(course_id, session_id)

    return {
        "course": course,
        "po_stats": po_stats,
        "session_id": session_id
    }, None