from backend.models.professor import Professor
from backend.models.course import Course
from backend.models.po import PO
from backend.models.co import CO
from backend.models.session import AcademicSession
from backend.models.batch import Batch
from backend.models.branch import Branch
from backend.models.course_assignment import CourseAssignment
from backend.utils.co_po_calculator import calculate_co_stats, calculate_po_stats


def get_dashboard_context(user_id, role, args):

    selected_session_id = args.get('session_id', type=int)
    selected_course_id = args.get('course_id', type=int)
    selected_branch_code = args.get('branch_code')

    sessions = AcademicSession.query.all()
    batches = Batch.query.all()

    branch_obj = None
    courses = []
    pos = []
    branches = []


    if role == "HOD":

        hod = Professor.query.get(user_id)

        if hod:
            branch_obj = Branch.query.filter_by(code=hod.branch).first()

            if branch_obj:
                pos = PO.query.filter_by(branch=branch_obj.code).all()
                courses = Course.query.filter_by(branch=branch_obj.code).all()

    else:

        assignments = CourseAssignment.query.filter_by(faculty_id=user_id).all()
        all_courses = [a.course for a in assignments]

        branches = list({c.branch for c in all_courses})

        branch_code = selected_branch_code if selected_branch_code else (
            branches[0] if branches else None
        )

        courses = [c for c in all_courses if c.branch == branch_code] if branch_code else []
        pos = PO.query.filter_by(branch=branch_code).all() if branch_code else []

    cos = CO.query.filter_by(course_id=selected_course_id).all() if selected_course_id else []

    co_stats, co_levels = calculate_co_stats(cos, selected_session_id)

    po_stats = calculate_po_stats(pos, co_levels)

    return {
        "role": role,
        "branch": branch_obj,
        "branches": branches if role == "Faculty" else [],
        "sessions": sessions,
        "batches": batches,
        "courses": courses,
        "selected_course_id": selected_course_id,
        "selected_branch_code": selected_branch_code,
        "selected_session_id": selected_session_id,
        "co_stats": co_stats,
        "po_stats": po_stats
    }


