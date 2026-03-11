"""
admin.py — Blueprint for all admin-facing routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .helpers import get_db, login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required(role='admin')
def dashboard():
    conn = get_db()
    stats = {
        'total_students': conn.execute(
            "SELECT COUNT(*) FROM users WHERE role='student'"
        ).fetchone()[0],
        'total_jobs': conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0],
        'active_jobs': conn.execute("SELECT COUNT(*) FROM jobs WHERE is_active=1").fetchone()[0],
        'total_applications': conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0],
        'pending_applications': conn.execute(
            "SELECT COUNT(*) FROM applications WHERE status='pending'"
        ).fetchone()[0],
        'total_recruiters': conn.execute(
            "SELECT COUNT(*) FROM users WHERE role='recruiter'"
        ).fetchone()[0],
    }
    recent_apps = conn.execute(
        """SELECT a.id, a.status, a.applied_at,
                  u.name AS student_name, j.title, j.company
           FROM applications a
           JOIN users u ON a.student_id = u.id
           JOIN jobs j ON a.job_id = j.id
           ORDER BY a.applied_at DESC LIMIT 5"""
    ).fetchall()
    conn.close()
    return render_template('admin/dashboard.html', stats=stats, recent_apps=recent_apps)


@admin_bp.route('/students')
@login_required(role='admin')
def students():
    conn = get_db()
    all_students = conn.execute(
        """SELECT u.id, u.name, u.email, u.created_at,
                  sp.branch, sp.year, sp.cgpa, sp.skills
           FROM users u
           LEFT JOIN student_profiles sp ON u.id = sp.user_id
           WHERE u.role = 'student'
           ORDER BY u.created_at DESC"""
    ).fetchall()
    conn.close()
    return render_template('admin/students.html', students=all_students)


@admin_bp.route('/students/delete/<int:student_id>', methods=['POST'])
@login_required(role='admin')
def delete_student(student_id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ? AND role = 'student'", (student_id,))
    conn.commit()
    conn.close()
    flash('Student removed successfully.', 'success')
    return redirect(url_for('admin.students'))


@admin_bp.route('/jobs')
@login_required(role='admin')
def jobs():
    conn = get_db()
    all_jobs = conn.execute(
        """SELECT j.*, u.name AS posted_by_name
           FROM jobs j JOIN users u ON j.posted_by = u.id
           ORDER BY j.created_at DESC"""
    ).fetchall()
    conn.close()
    return render_template('admin/jobs.html', jobs=all_jobs)


@admin_bp.route('/jobs/create', methods=['GET', 'POST'])
@login_required(role='admin')
def create_job():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        company = request.form.get('company', '').strip()
        description = request.form.get('description', '').strip()
        requirements = request.form.get('requirements', '').strip()
        location = request.form.get('location', '').strip()
        salary = request.form.get('salary', '').strip()
        deadline = request.form.get('deadline', '').strip()

        if not title or not company or not description or not deadline:
            flash('Title, company, description, and deadline are required.', 'danger')
            return render_template('admin/create_job.html')

        conn = get_db()
        conn.execute(
            """INSERT INTO jobs (title, company, description, requirements, location, salary, deadline, posted_by)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, company, description, requirements, location, salary, deadline, session['user_id'])
        )
        conn.commit()
        conn.close()
        flash(f'Job "{title}" posted successfully!', 'success')
        return redirect(url_for('admin.jobs'))

    return render_template('admin/create_job.html')


@admin_bp.route('/jobs/toggle/<int:job_id>', methods=['POST'])
@login_required(role='admin')
def toggle_job(job_id):
    conn = get_db()
    job = conn.execute("SELECT is_active FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if job:
        new_status = 0 if job['is_active'] else 1
        conn.execute("UPDATE jobs SET is_active = ? WHERE id = ?", (new_status, job_id))
        conn.commit()
        label = 'activated' if new_status else 'deactivated'
        flash(f'Job {label} successfully.', 'success')
    conn.close()
    return redirect(url_for('admin.jobs'))


@admin_bp.route('/jobs/delete/<int:job_id>', methods=['POST'])
@login_required(role='admin')
def delete_job(job_id):
    conn = get_db()
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    flash('Job deleted successfully.', 'success')
    return redirect(url_for('admin.jobs'))


@admin_bp.route('/applications')
@login_required(role='admin')
def applications():
    conn = get_db()
    status_filter = request.args.get('status', 'all')

    query = """SELECT a.id, a.status, a.applied_at, a.cover_note,
                      u.name AS student_name, u.email AS student_email,
                      j.title, j.company,
                      sp.cgpa, sp.branch, sp.resume_filename
               FROM applications a
               JOIN users u ON a.student_id = u.id
               JOIN jobs j ON a.job_id = j.id
               LEFT JOIN student_profiles sp ON a.student_id = sp.user_id"""

    if status_filter in ('pending', 'approved', 'rejected'):
        all_apps = conn.execute(query + " WHERE a.status = ? ORDER BY a.applied_at DESC",
                                (status_filter,)).fetchall()
    else:
        all_apps = conn.execute(query + " ORDER BY a.applied_at DESC").fetchall()

    conn.close()
    return render_template('admin/applications.html', applications=all_apps, status_filter=status_filter)


@admin_bp.route('/applications/update/<int:app_id>/<string:new_status>', methods=['POST'])
@login_required(role='admin')
def update_application(app_id, new_status):
    if new_status not in ('approved', 'rejected', 'pending'):
        flash('Invalid status.', 'danger')
        return redirect(url_for('admin.applications'))
    conn = get_db()
    conn.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()
    flash(f'Application {new_status} successfully.', 'success')
    return redirect(url_for('admin.applications'))
