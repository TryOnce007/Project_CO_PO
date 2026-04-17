from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.dashboard_service import get_dashboard_context

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    context = get_dashboard_context(
        user_id=session['user_id'],
        role=session.get('role'),
        args=request.args
    )

    return render_template('dashboard.html', **context)