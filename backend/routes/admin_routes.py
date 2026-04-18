from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from backend.services.admin_service import (
    get_dashboard_data,
    update_record,
    delete_record
)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard1')
def dashboard1():

    if 'user_id' not in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    data = get_dashboard_data(session['user_id'], session.get('role'))

    return render_template(
        'dashboard1.html',
        cos_list=data['cos_list'],
        students_list=data['students_list'],
        marks_list=data['marks_list'],
        copomap_list=data['copomap_list']
    )


@admin_bp.route('/update/<table>/<int:id>', methods=['POST'])
def update_row(table, id):

    success, message = update_record(table, id, request.form)

    return jsonify({
        "success": success,
        "message": message
    })


@admin_bp.route('/delete/<table>/<int:id>', methods=['POST'])
def delete_row(table, id):

    success, message = delete_record(table, id)

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(url_for('admin.dashboard1', active=table))