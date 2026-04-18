from flask import Blueprint, render_template, request, redirect, url_for, flash, session as flask_session, jsonify, session
from backend.services.marks_service import process_upload, confirm_upload, MarksService, get_static_academic_data, get_assigned_courses

marks_bp = Blueprint('marks', __name__)


@marks_bp.route('/upload_marks', methods=['GET', 'POST'])
def upload_marks():

    if request.method == 'POST':

        file = request.files.get('file')

        if not file:
            flash("No file uploaded", "danger")
            return redirect(request.url)

        preview_data, error_rows, session_name = process_upload(file)

        flask_session["upload_preview"] = preview_data

        return render_template(
            "upload_preview.html",
            data=preview_data,
            error_rows=error_rows,
            sessions=[session_name]
        )

    return render_template("upload_marks.html")



@marks_bp.route('/confirm_upload_marks', methods=['POST'])
def confirm_upload_marks():

    success, failed = confirm_upload()

    flash(f"Upload complete → Success: {success}, Failed: {failed}", "success")

    return redirect(url_for("marks.upload_marks"))



@marks_bp.route('/get_student_marks_grid')
def get_student_marks_grid():

    batch = request.args.get('batch')
    branch = request.args.get('branch')
    co_id = request.args.get('co_id')
    session_id = request.args.get('session')

    data = MarksService.get_student_marks_grid(
        batch, branch, co_id, session_id
    )

    return jsonify(data)



@marks_bp.route('/save_mark_row', methods=['POST'])
def save_mark_row():

    data = request.get_json()

    result = MarksService.save_mark_row(data)

    return jsonify(result)



@marks_bp.route('/add_marks')
def add_marks():

    if 'user_id' not in session or session.get('role') != 'Faculty':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    faculty_id = session['user_id']

    courses = get_assigned_courses(faculty_id)
    data = get_static_academic_data()

    return render_template(
        'add_mark.html',
        courses=courses,
        batches=data["batches"],
        branches=data["branches"],
        sessions=data["sessions"]
    )