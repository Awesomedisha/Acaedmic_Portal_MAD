"""
app.py — Main entry point for the Placement Portal application.
Run with: python app.py
"""

import os
from flask import Flask, render_template, session
from database.init_db import init_database
from modules.auth import auth_bp
from modules.student import student_bp
from modules.admin import admin_bp
from modules.recruiter import recruiter_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'placement_portal_secret_key_2026'

    # Configure upload folder for resumes
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

    # Register all blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(recruiter_bp)

    @app.route('/')
    def index():
        # Redirect logged-in users to their dashboards
        role = session.get('role')
        if role == 'admin':
            from flask import redirect, url_for
            return redirect(url_for('admin.dashboard'))
        elif role == 'student':
            from flask import redirect, url_for
            return redirect(url_for('student.dashboard'))
        elif role == 'recruiter':
            from flask import redirect, url_for
            return redirect(url_for('recruiter.dashboard'))
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    return app


# Initialize the database on first run
init_database()
app = create_app()

if __name__ == '__main__':
    print("\n🚀 Placement Portal running at http://127.0.0.1:5000")
    print("   Admin login: admin@portal.com / admin123\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
