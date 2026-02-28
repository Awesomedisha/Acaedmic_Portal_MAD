-- Placement Portal Database Schema
-- Users table: stores all users (students, admins, recruiters)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'admin', 'recruiter')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student profiles linked to user accounts
CREATE TABLE IF NOT EXISTS student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    branch TEXT DEFAULT '',
    year INTEGER DEFAULT 1,
    cgpa REAL DEFAULT 0.0,
    skills TEXT DEFAULT '',
    resume_filename TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Job postings created by admins or recruiters
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT DEFAULT '',
    location TEXT DEFAULT '',
    salary TEXT DEFAULT '',
    deadline TEXT NOT NULL,
    posted_by INTEGER NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

-- Applications submitted by students for jobs
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    cover_note TEXT DEFAULT '',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, job_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);
