import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from backend.extension import limiter

db = SQLAlchemy()

def create_app():

    load_dotenv()

    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    limiter.init_app(app)

    db.init_app(app)
    

    from backend.routes.auth_routes import auth_bp
    from backend.routes.admin_routes import admin_bp
    from backend.routes.co_po_routes import co_po_bp
    from backend.routes.co_routes import co_bp
    from backend.routes.course_routes import course_bp
    from backend.routes.dashboard_routes import dashboard_bp
    from backend.routes.hod_routes import hod_bp
    from backend.routes.marks_routes import marks_bp
    from backend.routes.po_routes import po_bp
    from backend.routes.profile_routes import profile_bp
    from backend.routes.student_routes import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(co_po_bp)
    app.register_blueprint(co_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(hod_bp)
    app.register_blueprint(marks_bp)
    app.register_blueprint(po_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(student_bp)

    return app



