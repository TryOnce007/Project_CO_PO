from flask import Blueprint, render_template, request, redirect, url_for, flash, session as flask_session, jsonify, session
from backend.services.marks_service import  MarksService, get_static_academic_data, get_assigned_courses

marks_bp = Blueprint('marks', __name__)


@marks_bp.route('/upload_marks', methods=['GET', 'POST'])
def upload_marks():

    branches = MarksService.get_all_branches()
    batches = MarksService.get_batches()
    sessions = MarksService.get_sessions()

    if request.method == 'POST':

        file = request.files.get('file')

        if not file:
            flash("Please upload a file", "danger")
            return redirect(url_for("marks.upload_marks"))

        if not file.filename.endswith(('.xlsx', '.xls')):
            flash("Only Excel files are allowed", "danger")
            return redirect(url_for("marks.upload_marks"))
        

        branch = request.form.get('branch')

        batch_id = request.form.get('batch_id')
        session_id = request.form.get('session_id')

        

        if not file:
            flash("Please upload a file", "danger")
            return redirect(url_for("marks.upload_marks"))

        if not branch or not batch_id or not session_id:
            flash("Please select branch, batch and session", "danger")
            return redirect(url_for("marks.upload_marks"))

        try:
            batch_id = int(batch_id)
            session_id = int(session_id)
        except ValueError:
            flash("Invalid batch or session selection", "danger")
            return redirect(url_for("marks.upload_marks"))

      

        preview_data = MarksService.process_upload(
            file=file,
            session_id=session_id,
            branch=branch,
            batch_id=batch_id
        )

        flask_session["upload_preview"] = preview_data

        return render_template(
            "upload_preview.html",
            data=preview_data
        )

    return render_template(
        "upload_marks.html",
        branches=branches,
        batches=batches,
        sessions=sessions
    )


@marks_bp.route('/confirm_upload_marks', methods=['POST'])
def confirm_upload_marks():

    total_rows = int(request.form.get("total_rows", 0))

    data = []

    for i in range(total_rows):

        data.append({
            "roll_no": request.form.get(f"roll_no_{i}"),
            "co_id": int(request.form.get(f"co_id_{i}")),
            "obtained": request.form.get(f"obtained_{i}"),
            "total": request.form.get(f"total_{i}"),
            "indirect_obtained": request.form.get(f"indirect_obtained_{i}"),
            "indirect_total": request.form.get(f"indirect_total_{i}"),
            "session_id": int(request.form.get(f"session_id_{i}")),
            "branch": request.form.get(f"branch_{i}"),
            "batch_id": int(request.form.get(f"batch_id_{i}"))
        })

    success, failed, skipped = MarksService.confirm_upload(data)

    flash(
        f"Upload complete → Success: {success}, Failed: {failed}, Skipped (duplicates): {skipped}",
        "success"
    )

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