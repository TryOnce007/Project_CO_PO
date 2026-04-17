from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.models.batch import Batch
from app.services.student_service import StudentService

student_bp = Blueprint('student_bp', __name__)



@student_bp.route('/add_student', methods=['GET', 'POST'])
def add_student():

    batches = Batch.query.all()

    if request.method == 'POST':

        success, message = StudentService.add_student(
            request.form,
            session.get('user_id')
        )

        flash(message, "success" if success else "danger")
        return redirect(url_for('student_bp.add_student'))

    return render_template('add_student.html', batches=batches)




@student_bp.route('/get_students')
def get_students():

    batch = request.args.get('batch', type=int)
    branch = request.args.get('branch')

    data = StudentService.get_students(batch, branch)

    return jsonify(data)