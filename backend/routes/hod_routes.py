from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from backend.services.hod_service import HODService

hod_bp = Blueprint("hod_bp", __name__)



@hod_bp.route('/hod_dashboard')
def hod_dashboard():
    return render_template('hod_dashboard.html')



@hod_bp.route('/hod/add_teacher', methods=['GET', 'POST'])
def add_teacher():

    if request.method == 'POST':
        result = HODService.add_teacher(
            session.get('user_id'),
            request.form
        )

        flash(result["message"], result["category"])
        return redirect(url_for('hod_bp.add_teacher'))

    return render_template('hod_add_teacher.html')



@hod_bp.route('/hod/add_po', methods=['GET', 'POST'])
def add_po():

    if request.method == 'POST':
        result = HODService.add_po(
            session.get('user_id'),
            request.form
        )

        flash(result["message"], result["category"])
        return redirect(url_for('hod_bp.add_po'))

    return render_template('hod_add_po.html')



@hod_bp.route('/hod/assign_course', methods=['GET'])
def assign_course_page():

    data = HODService.get_assignments(session.get('user_id'))

    return render_template('hod_assign_course.html', **data)




@hod_bp.route('/hod/assign_course', methods=['POST'])
def assign_course():

    result = HODService.assign_course(request.form)

    return jsonify(result)



@hod_bp.route('/hod/view_assignments')
def view_assignments():

    data = HODService.get_assignments(session.get('user_id'))

    return render_template(
        'hod_assignments.html',
        assignments=data["assignments"],
        faculty=data["faculty"],
        sessions=data["sessions"],
        batches=data["batches"]
    )


@hod_bp.route('/hod/add_session', methods=['GET', 'POST'])
def add_session():

    if request.method == 'POST':
        result = HODService.add_session(request.form)

        flash(result["message"], result["category"])
        return redirect(url_for('hod_bp.add_session'))

    return render_template('hod_add_session.html')