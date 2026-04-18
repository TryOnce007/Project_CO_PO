from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.services.profile_service import get_professor_profile, update_professor_profile

profile_bp = Blueprint('profile', __name__)



@profile_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("Please log in to view profile.", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session.get('role')

    professor = get_professor_profile(user_id)
    return render_template('profile.html', professor=professor, role=role)



@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    if 'user_id' not in session:
        flash("Please log in to edit your profile.", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session.get('role')

    professor = get_professor_profile(user_id)

    if request.method == 'POST':

        new_username = request.form.get('username')
        new_phone = request.form.get('phone')

        success, message = update_professor_profile(
            professor,
            new_username,
            new_phone
        )

        if not success:
            flash(message, "danger")
            return redirect(url_for('profile.edit_profile'))

        flash(message, "success")

        if role == "HOD":
            return redirect(url_for('hod_bp.hod_dashboard'))   
        else:
            return redirect(url_for('profile.profile'))

    return render_template('edit_profile.html', professor=professor, role=role)