import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.extension import limiter

db = SQLAlchemy()

def create_app():

    load_dotenv()

    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    limiter.init_app(app)

    db.init_app(app)
    

    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.co_po_routes import co_po_bp
    from app.routes.co_routes import co_bp
    from app.routes.course_routes import course_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.hod_routes import hod_bp
    from app.routes.marks_routes import marks_bp
    from app.routes.po_routes import po_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.student_routes import student_bp

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



