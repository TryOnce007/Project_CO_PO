from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from backend.services.po_service import (
    get_course_list_for_role,
    get_po_attainment_data
)
from backend.models.session import AcademicSession
from backend.models.course_assignment import CourseAssignment

po_bp = Blueprint('po', __name__)



@po_bp.route('/select_course_for_po', methods=['GET', 'POST'])
def select_course_for_po():

    if 'user_id' not in session:
        flash("Access denied!", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session.get('role')

    courses = get_course_list_for_role(user_id, role)

    sessions = AcademicSession.query.all()

    if request.method == 'POST':

        course_id = request.form.get('course_id')

        if not course_id:
            flash("Please select a course.", "warning")
            return redirect(url_for('po.select_course_for_po'))

        if role == "Faculty":


            valid = CourseAssignment.query.filter_by(
                faculty_id=user_id,
                course_id=course_id
            ).first()

            if not valid:
                flash("You are not assigned to this course!", "danger")
                return redirect(url_for('po.select_course_for_po'))

        return redirect(url_for(
            'po.po_attainment_course',
            course_id=course_id
        ))

    return render_template(
        'select_course.html',
        courses=courses,
        sessions=sessions
    )



@po_bp.route('/po_attainment_course')
def po_attainment_course():

    course_id = request.args.get('course_id', type=int)
    session_id = request.args.get('session_id', type=int)

    data, error = get_po_attainment_data(course_id, session_id)

    if error:
        flash(error, "danger")
        return redirect(url_for('index'))

    return render_template(
        'po_attainment_course.html',
        course=data["course"],
        po_stats=data["po_stats"],
        selected_session_id=data["session_id"]
    )