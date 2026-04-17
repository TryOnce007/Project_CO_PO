from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.co_po_service import COPOService

co_po_bp = Blueprint('co_po_bp', __name__)


@co_po_bp.route('/map_co_po', methods=['GET', 'POST'])
def map_co_po():

    hod_id = session.get('user_id')

    if not hod_id:
        flash("Login required!", "danger")
        return redirect(url_for('login'))

    hod, courses, pos = COPOService.get_page_data(hod_id)

    if not hod:
        flash("Invalid user!", "danger")
        return redirect(url_for('login'))

    selected_course_id = request.args.get('course_id')

    if request.method == 'POST':

        selected_course_id = request.form.get('course_id')

        if selected_course_id and not request.form.get('co_id'):
            return redirect(url_for('co_po_bp.map_co_po', course_id=selected_course_id))

        co_id = request.form.get('co_id')
        po_id = request.form.get('po_id')
        level = request.form.get('level')

        success, message = COPOService.save_mapping(
            selected_course_id, co_id, po_id, level
        )

        flash(message, "success" if success else "danger")

        return redirect(url_for('co_po_bp.map_co_po', course_id=selected_course_id))

    cos = COPOService.get_cos(selected_course_id)

    return render_template(
        "map_co_po.html",
        courses=courses,
        pos=pos,
        cos=cos,
        selected_course_id=selected_course_id
    )