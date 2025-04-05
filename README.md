# Django Mentorship Platform (PSW13)

## Description

This is a Django-based web application designed to facilitate mentorship relationships. It allows mentors to manage mentees, set availability, assign tasks, and review uploaded videos. Mentees can authenticate using unique tokens, view available meeting slots, schedule meetings, and manage their assigned tasks.

## Features

*   **User Management (Mentors):**
    *   Registration, login, and logout (`users` app).
    *   Uses standard Django authentication.
*   **Mentee Authentication:**
    *   Mentees authenticate via a unique token (`/mentorship/auth/`).
    *   Session managed via a secure HTTP-only cookie (`auth_token`).
    *   Mentee logout functionality (`/mentorship/mentee_logout/`).
*   **Mentorship Management (Mentor View):**
    *   Registering mentees with name, photo, stage, and assigned navigator (`/mentorship/`).
    *   Viewing mentees, filterable by stage (visualized with a pie chart).
    *   Viewing assigned tasks and uploaded videos for a specific mentee (`/mentorship/task/<id>/`).
    *   Assigning new tasks to a mentee.
    *   Uploading videos related to a mentee.
*   **Scheduling:**
    *   Mentors can define their available appointment slots (`/mentorship/meeting/`).
    *   Mentees view available dates based on mentor availability (`/mentorship/schedule_date/`).
    *   Mentees view available time slots for a chosen date and schedule a meeting (`/mentorship/schedule_meeting/`).
*   **Task Management:**
    *   Mentors assign tasks to specific mentees (`/mentorship/task/<id>/`).
    *   Mentees view their assigned tasks (`/mentorship/mentee_tasks/`).
    *   Mentees can mark tasks as done/undone via an asynchronous request (`/mentorship/task_status/<id>/`).
*   **Media Handling:** Upload and storage of mentee photos and task-related videos.
*   **Security:**
    *   Uses Django's CSRF protection.
    *   Decorators enforce login requirements and ownership checks (e.g., mentor can only access their own mentees/tasks).
    *   Mentee access controlled via secure cookies.

## Technology Stack

*   **Backend:** Python, Django
*   **Database:** SQLite (default)
*   **Frontend:** Django Templates, HTML, Tailwind CSS (via CDN), Chart.js (via CDN), HTMX (for task status updates)
*   **Code Quality:** Custom decorators used for DRY view validation.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd PSW13
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **(Optional) Create a superuser** (to access Django Admin at `/admin/`):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  Access the application at `http://127.0.0.1:8000/`.

## Usage Guide

### Mentor Access

*   **Register:** `/users/register/`
*   **Login:** `/users/login/`
*   **Logout:** `/users/logout/` (Link available in header when logged in)
*   **Mentorship Dashboard:** `/mentorship/` (View/Register Mentees, View Chart)
*   **Set Availability/View Scheduled Meetings:** `/mentorship/meeting/`
*   **View/Manage Mentee Tasks & Uploads:** `/mentorship/task/<mentee_id>/`

### Mentee Access

*   **Authenticate:** `/mentorship/auth/` (Enter provided token)
*   **View Available Dates:** `/mentorship/schedule_date/`
*   **View Available Times / Schedule Meeting:** `/mentorship/schedule_meeting/` (Requires `?date=DD-MM-YYYY` parameter from available dates page)
*   **View Tasks:** `/mentorship/mentee_tasks/`
*   **Logout:** `/mentorship/mentee_logout/` (Link available on mentee pages)

### Task Status Update (Mentee)

*   The checkbox next to a task in the mentee task view (`/mentorship/mentee_tasks/`) uses HTMX to send a POST request to `/mentorship/task_status/<task_id>/` to toggle the task's completion status without a full page reload.
