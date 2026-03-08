"""
recruiter.py — Blueprint for recruiter-facing routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .helpers import get_db, login_required

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')


@recruiter_bp.route('/dashboard')
@login_required(role='recruiter')
def dashboard():
    conn = get_db()
    user_id = session['user_id']

    my_jobs = conn.execute(
        "SELECT COUNT(*) FROM jobs WHERE posted_by = ?", (user_id,)
    ).fetchone()[0]
    total_applicants = conn.execute(
        """SELECT COUNT(*) FROM applications a
           JOIN jobs j ON a.job_id = j.id
           WHERE j.posted_by = ?""", (user_id,)
    ).fetchone()[0]

    recent_jobs = conn.execute(
        "SELECT * FROM jobs WHERE posted_by = ? ORDER BY created_at DESC LIMIT 5", (user_id,)
    ).fetchall()
    conn.close()

    return render_template('recruiter/dashboard.html',
                           my_jobs=my_jobs,
                           total_applicants=total_applicants,
                           recent_jobs=recent_jobs)


@recruiter_bp.route('/post-job', methods=['GET', 'POST'])
@login_required(role='recruiter')
def post_job():
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
            return render_template('recruiter/post_job.html')

        conn = get_db()
        conn.execute(
            """INSERT INTO jobs (title, company, description, requirements, location, salary, deadline, posted_by)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, company, description, requirements, location, salary, deadline, session['user_id'])
        )
        conn.commit()
        conn.close()
        flash(f'Job "{title}" posted successfully!', 'success')
        return redirect(url_for('recruiter.my_jobs'))

    return render_template('recruiter/post_job.html')


@recruiter_bp.route('/my-jobs')
@login_required(role='recruiter')
def my_jobs():
    conn = get_db()
    jobs = conn.execute(
        "SELECT * FROM jobs WHERE posted_by = ? ORDER BY created_at DESC",
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('recruiter/my_jobs.html', jobs=jobs)


@recruiter_bp.route('/applicants/<int:job_id>')
@login_required(role='recruiter')
def applicants(job_id):
    conn = get_db()
    # Verify the recruiter owns this job
    job = conn.execute(
        "SELECT * FROM jobs WHERE id = ? AND posted_by = ?",
        (job_id, session['user_id'])
    ).fetchone()

    if not job:
        conn.close()
        flash('Job not found or access denied.', 'danger')
        return redirect(url_for('recruiter.my_jobs'))

    applicant_list = conn.execute(
        """SELECT u.name, u.email, a.status, a.applied_at, a.cover_note,
                  sp.branch, sp.cgpa, sp.skills, sp.resume_filename
           FROM applications a
           JOIN users u ON a.student_id = u.id
           LEFT JOIN student_profiles sp ON a.student_id = sp.user_id
           WHERE a.job_id = ?
           ORDER BY a.applied_at DESC""",
        (job_id,)
    ).fetchall()
    conn.close()

    return render_template('recruiter/applicants.html', job=job, applicants=applicant_list)
