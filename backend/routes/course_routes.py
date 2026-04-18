from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.services.course_service import CourseService

course_bp = Blueprint('course_bp', __name__)


@course_bp.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'user_id' not in session or session.get('role') != 'HOD':
        flash('Access denied! HOD only.', 'danger')
        return redirect(url_for('login'))

    hod_id = session['user_id']

    if request.method == 'POST':

        result = CourseService.add_course(hod_id, request.form)

        flash(result["message"], result["category"])
        return redirect(url_for('course_bp.add_course'))

    courses = CourseService.get_courses_by_hod(hod_id)

    return render_template('add_course.html', courses=courses)