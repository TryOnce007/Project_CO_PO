from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from backend.services.co_service import COService, get_cos_by_role

co_bp = Blueprint('co_bp', __name__)


@co_bp.route('/add_co', methods=['GET', 'POST'])
def add_co():

    if 'user_id' not in session or session.get('role') != 'Faculty':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':

        description = request.form.get('description')
        course_id = request.form.get('course_id')

        result = COService.add_co(
            session['user_id'],
            description,
            course_id
        )

        flash(result["message"], f"add_co_{result['category']}")
        return redirect(url_for('co_bp.add_co'))

    courses = COService.get_faculty_courses(session['user_id'])

    return render_template('add_co.html', courses=courses)



@co_bp.route('/attainment')
def attainment():

    if 'user_id' not in session:
        flash("Please login first.", "danger")
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session.get('role')

    selected_course_id = request.args.get('course_id', type=int)
    selected_session_id = request.args.get('session_id', type=int)

    # 🔹 Get base data for dropdowns always
    result = COService.get_attainment(
        user_id=user_id,
        role=role,
        course_id=selected_course_id,
        session_id=selected_session_id
    )

    return render_template(
        'attainment.html',
        data=result.get("data", []),
        courses=result.get("courses", []),
        sessions=result.get("sessions", []),
        selected_course_id=selected_course_id,
        selected_session_id=selected_session_id
    )


@co_bp.route('/co_attainment_ajax')
def co_attainment_ajax():

    if 'user_id' not in session:
        return jsonify([])

    user_id = session['user_id']
    role = session.get('role')

    session_id = request.args.get('session_id', type=int)
    course_id = request.args.get('course_id', type=int)

    result = COService.get_attainment(
        user_id=user_id,
        role=role,
        course_id=course_id,
        session_id=session_id
    )

    return jsonify(result.get("data", []))


@co_bp.route('/get_cos')
def get_cos():

    course_id = request.args.get('course_id', type=int)

    data = COService.get_cos_by_course(course_id)

    return jsonify(data)



@co_bp.route('/my_cos')
def my_cos():

    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id or not role:
        flash("Session expired. Please login again.", "danger")
        return redirect(url_for("auth.login"))

    course_id = request.args.get("course_id")

    cos = get_cos_by_role(
        user_id=user_id,
        role=role,
        course_id=course_id
    )

    return render_template(
        "my_cos.html",
        cos=cos
    )