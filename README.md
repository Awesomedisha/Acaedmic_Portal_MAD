# Academic Placement Portal V1

The Academic Placement Portal is a comprehensive, production-ready web application designed to facilitate the recruitment process within educational institutions. This platform serves as a centralized bridge between students, corporate recruiters, and university administrators, ensuring a transparent and efficient hiring lifecycle.

Developed by Disha Kumari

---

## Deployment Information

### Vercel Deployment
This project is pre-configured for Vercel. Simply connect your GitHub repository to Vercel, and it will automatically handle the build process using the provided `vercel.json` and the optimized `app.py` entrypoint.

### Netlify Deployment
To deploy on Netlify, this project utilized Netlify Functions via the `serverless-wsgi` adapter. 
- Connect your repository to Netlify.
- Netlify will auto-detect the `netlify.toml` configuration.
- The backend logic is served via the function located in `netlify/functions/app.py`.
- **Note:** External dependencies are managed through the `requirements.txt` file which is automatically processed during the Netlify build step.

---

## Core Modules

### 1. Student Module
The student experience is focused on career growth and opportunity discovery.
- **Profile Management:** Secure editing of personal details and contact information.
- **Job Discovery:** Real-time browsing of job openings with detailed requirements and CTC information.
- **Application Tracking:** A dedicated dashboard to monitor the status of every application from submission to final decision.
- **Professional Vault:** Support for resume uploads to streamline the recruiter review process.

### 2. Recruiter Module
Designed for efficiency in talent acquisition.
- **Job Posting:** Intuitive forms to publish vacancies with specific eligibility criteria.
- **Applicant Management:** Streamlined views to review student profiles and resumes.
- **Hiring Pipeline:** Capability to manage the selection process through different stages.

### 3. Administrative Module
Provides complete governance and oversight of the placement ecosystem.
- **Student Validation:** Oversight to approve or manage student eligibility.
- **Application Governance:** Ability to review and update the status of any application across the platform.

---

## Key Technical Features
- **Modern User Interface:** Built with advanced CSS techniques, including glassmorphism and smooth micro-interactions for a premium feel.
- **Real-Time Data Sync:** Instant updates across dashboards for new job postings and status changes.
- **Responsive Layout:** Optimized for desktop and mobile browsers to ensure accessibility.
- **Secure Authentication:** Robust login and registration system with role-based access control.

---

## Project Structure

- **app.py:** The central entry point and Flask application configuration.
- **netlify/functions/app.py:** The specialized entrypoint for Netlify serverless deployment.
- **modules/:** Contains backend logic for Authentication, Student, Recruiter, and Admin functionalities.
- **templates/:** Organized HTML templates for all dashboards and the landing page.
- **static/:**
    - **css/:** Global stylesheets and premium UI components.
    - **js/:** Client-side interactivity and data visualization.
    - **img/:** High-quality corporate imagery and profile assets.
- **database/:** SQL schema definitions and database initialization scripts.

---

## Technology Stack
- **Backend Framework:** Flask (Python)
- **Database:** SQLite (Local persistent storage)
- **Frontend Tools:** HTML5, CSS3, Vanilla JavaScript
- **Deployment Compatibility:** Vercel & Netlify

---

## Installation and Setup

1. **Repository Setup:**
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Awesomedisha/Acaedmic_Portal_MAD.git
   ```

2. **Dependency Management:**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Initialization:**
   Run the initialization script to set up the local database:
   ```bash
   python database/init_db.py
   ```

4. **Launch Application:**
   Start the development server:
   ```bash
   python app.py
   ```

---
Developed by Disha Kumari
