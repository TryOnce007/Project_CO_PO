from backend.models.co import CO
from backend.models.po import PO
from backend.models.course import Course
from backend.models.professor import Professor
from backend.models.course_assignment import CourseAssignment
from backend.utils.co_po_calculator import calculate_po_stats, calculate_co_stats


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

    cos = CO.query.filter_by(course_id=course_id).all()
    co_stats, co_final_scores = calculate_co_stats(cos, session_id)

    pos = PO.query.all()
    po_stats = calculate_po_stats(pos, co_final_scores)

    return {
        "course": course,
        "po_stats": po_stats,
        "session_id": session_id
    }, None