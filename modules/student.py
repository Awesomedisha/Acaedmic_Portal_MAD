"""
student.py — Blueprint for all student-facing routes.
"""

import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from .helpers import get_db, login_required, allowed_file, UPLOAD_FOLDER

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
@login_required(role='student')
def dashboard():
    conn = get_db()
    user_id = session['user_id']

    # Gather quick stats for the student
    total_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1").fetchone()[0]
    my_applications = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE student_id = ?", (user_id,)
    ).fetchone()[0]
    approved_count = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE student_id = ? AND status = 'approved'", (user_id,)
    ).fetchone()[0]

    # Recent 3 active jobs
    recent_jobs = conn.execute(
        "SELECT * FROM jobs WHERE is_active = 1 ORDER BY created_at DESC LIMIT 3"
    ).fetchall()
    conn.close()

    return render_template('student/dashboard.html',
                           total_jobs=total_jobs,
                           my_applications=my_applications,
                           approved_count=approved_count,
                           recent_jobs=recent_jobs)


@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required(role='student')
def profile():
    conn = get_db()
    user_id = session['user_id']

    if request.method == 'POST':
        branch = request.form.get('branch', '').strip()
        year = request.form.get('year', 1)
        cgpa = request.form.get('cgpa', 0.0)
        skills = request.form.get('skills', '').strip()
        phone = request.form.get('phone', '').strip()
        resume_filename = None

        # Handle resume file upload
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"resume_{user_id}_{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                resume_filename = filename

        # Update student profile
        if resume_filename:
            conn.execute(
                """UPDATE student_profiles
                   SET branch=?, year=?, cgpa=?, skills=?, phone=?, resume_filename=?
                   WHERE user_id=?""",
                (branch, year, cgpa, skills, phone, resume_filename, user_id)
            )
        else:
            conn.execute(
                """UPDATE student_profiles
                   SET branch=?, year=?, cgpa=?, skills=?, phone=?
                   WHERE user_id=?""",
                (branch, year, cgpa, skills, phone, user_id)
            )
        conn.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))

    # Fetch existing profile data
    profile_data = conn.execute(
        "SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)
    ).fetchone()
    user_data = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    return render_template('student/profile.html', profile=profile_data, user=user_data)


@student_bp.route('/jobs')
@login_required(role='student')
def jobs():
    conn = get_db()
    user_id = session['user_id']

    # IDs of jobs already applied to (to disable apply button)
    applied_ids = [
        row[0] for row in conn.execute(
            "SELECT job_id FROM applications WHERE student_id = ?", (user_id,)
        ).fetchall()
    ]

    all_jobs = conn.execute(
        "SELECT * FROM jobs WHERE is_active = 1 ORDER BY created_at DESC"
    ).fetchall()
    conn.close()

    return render_template('student/jobs.html', jobs=all_jobs, applied_ids=applied_ids)


@student_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required(role='student')
def apply(job_id):
    conn = get_db()
    user_id = session['user_id']

    job = conn.execute("SELECT * FROM jobs WHERE id = ? AND is_active = 1", (job_id,)).fetchone()
    if not job:
        conn.close()
        flash('Job not found or no longer active.', 'danger')
        return redirect(url_for('student.jobs'))

    # Prevent duplicate applications
    already_applied = conn.execute(
        "SELECT id FROM applications WHERE student_id = ? AND job_id = ?",
        (user_id, job_id)
    ).fetchone()
    if already_applied:
        conn.close()
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('student.jobs'))

    if request.method == 'POST':
        cover_note = request.form.get('cover_note', '').strip()
        conn.execute(
            "INSERT INTO applications (student_id, job_id, cover_note) VALUES (?, ?, ?)",
            (user_id, job_id, cover_note)
        )
        conn.commit()
        conn.close()
        flash(f'Successfully applied for {job["title"]} at {job["company"]}!', 'success')
        return redirect(url_for('student.applications'))

    conn.close()
    return render_template('student/apply.html', job=job)


@student_bp.route('/applications')
@login_required(role='student')
def applications():
    conn = get_db()
    user_id = session['user_id']

    # Join with jobs table to get job details
    my_apps = conn.execute(
        """SELECT a.id, a.status, a.applied_at, a.cover_note,
                  j.title, j.company, j.location
           FROM applications a
           JOIN jobs j ON a.job_id = j.id
           WHERE a.student_id = ?
           ORDER BY a.applied_at DESC""",
        (user_id,)
    ).fetchall()
    conn.close()

    return render_template('student/applications.html', applications=my_apps)
