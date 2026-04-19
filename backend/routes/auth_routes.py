from backend.extension import limiter
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.services.auth_service import (
    get_index_data,
    get_home_redirect,
    login_user, 
    reset_user_password,
    register_professor,
    get_all_branches,
    get_professor_dashboard,
    verify_forgot_password
)


auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/')
def home():
    return get_home_redirect(session)

@auth_bp.route('/index')
def index():

    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    role = session.get('role')

    if role == 'Faculty':
        professors = get_index_data()
        return render_template('index.html', professors=professors)

    elif role == 'HOD' or 'admin':
        return redirect(url_for('hod_bp.hod_dashboard'))

    return redirect(url_for('auth.login'))



@auth_bp.route('/signup_professor', methods=['GET', 'POST'])
def signup_professor():

    branches = get_all_branches()

    if request.method == 'POST':

        success, message = register_professor(request.form)

        if not success:
            flash(message, "danger")
            return redirect(url_for('auth.signup_professor'))

        flash(message, "success")
        return redirect(url_for('auth.login'))

    return render_template('signup_professor.html', branches=branches)


@auth_bp.route('/professor')
def professor():

    if 'user_id' not in session:
        flash("Please login to access the dashboard.", "login_warning")
        return redirect(url_for('auth.login'))

    professor = get_professor_dashboard(session['user_id'])

    return render_template('professor.html', professor=professor)


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        success, message = verify_forgot_password(request.form)

        if not success:
            flash(message, "danger")
            return redirect(url_for('auth.forgot_password'))

        flash(message, "success")
        return redirect(url_for('auth.reset_password'))

    return render_template('forgot_password.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
# @limiter.limit("5 per minute")

def login():

    if 'user_id' in session:
        if session.get('role') == 'HOD' or 'admin':
            return redirect(url_for('hod_bp.hod_dashboard'))
        return redirect(url_for('auth.professor'))

    if request.method == 'POST':

        success, message, redirect_url, user = login_user(request.form)

        if not success:
            flash(message, "danger")
            return render_template('login.html')

        session['user_id'] = user.id
        session['role'] = user.role

        flash(message, "success")
        return redirect(redirect_url)

    return render_template('login.html')


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if 'reset_user_id' not in session:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        success, message = reset_user_password(
            session['reset_user_id'],
            request.form
        )

        if not success:
            flash(message, "danger")
            return redirect(url_for('auth.reset_password'))

        session.pop('reset_user_id', None)

        flash(message, "success")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')


@auth_bp.route('/logout')
def logout():

    session.clear()
    flash("You have been logged out.", "info")

    return redirect(url_for('auth.login'))


@auth_bp.errorhandler(429)
def ratelimit_handler(e):
    return render_template(
        "429.html",
        retry_after=e.description if hasattr(e, "description") else None
    ), 429

