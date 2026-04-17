from flask import redirect, url_for
from app.models.professor import Professor
from app.models.professor import Professor
from app.models.branch import Branch
from app import db


def get_index_data():
    return Professor.query.all()


def get_home_redirect(session):
    if 'user_id' in session:
        if session.get('role') == 'HOD':
            return redirect(url_for('hod_bp.hod_dashboard'))
        else:
            return redirect(url_for('professor'))

    return redirect(url_for('auth.login'))



def get_all_branches():
    return Branch.query.all()



def register_professor(form):
    branch = form.get('branch')
    username = form.get('username')
    phone = form.get('phone')
    role = form.get("role")
    password = form.get('password')
    confirm = form.get('confirm_password')

    if not all([branch, username, phone, password, confirm]):
        return False, "All fields are required."

    if password != confirm:
        return False, "Passwords do not match."

    if Professor.query.filter_by(username=username).first():
        return False, "Username already exists."

    new_prof = Professor(
        branch=branch,
        username=username,
        phone=phone,
        role=role
    )

    new_prof.set_password(password)

    db.session.add(new_prof)
    db.session.commit()

    return True, "Professor registered successfully. You can now log in."



def get_professor_dashboard(user_id):
    return Professor.query.get(user_id)



def verify_forgot_password(form):
    username = form.get('username')
    phone = form.get('phone')

    professor = Professor.query.filter_by(
        username=username,
        phone=phone
    ).first()

    if not professor:
        return False, "Invalid username or phone number."

    from flask import session
    session['reset_user_id'] = professor.id

    return True, "Identity verified. Please reset your password."




def login_user(form):

    role = form.get('role')
    username = form.get('username')
    password = form.get('password')

    prof = Professor.query.filter_by(username=username).first()

    if not prof or not prof.check_password(password):
        return False, "Invalid username or password.", None, None

    if prof.role != role:
        return False, "Invalid role selected!", None, None

    redirect_url = 'hod_dashboard' if prof.role == "HOD" else 'professor'

    return True, f"Welcome back, {prof.username}!", redirect_url, prof



def reset_user_password(user_id, form):
    new = form.get('new_password')
    confirm = form.get('confirm_password')

    if not new or not confirm:
        return False, "All fields are required."

    if new != confirm:
        return False, "Passwords do not match."

    professor = Professor.query.get(user_id)

    if not professor:
        return False, "User not found."

    professor.set_password(new)
    db.session.commit()

    return True, "Password reset successful. Please log in."