# Django Mentorship Platform (PSW13)

## Description

This is a Django-based web application designed to manage mentorship relationships and schedule meetings between mentors and mentees. It includes user authentication and specific features for managing mentorship stages, navigator assignments, and appointment availability.

## Features

*   **User Management:** Registration, login, and logout functionality (`users` app).
*   **Mentorship Management:**
    *   Registering mentees with details like name, photo, stage, and assigned navigator.
    *   Viewing mentees based on their stage.
    *   (Assumed) Navigator management (likely via Django Admin).
*   **Scheduling:**
    *   Mentors can set their available appointment slots (`mentorship/meeting/`).
    *   Mentees can authenticate via a token (`mentorship/auth/`).
    *   Mentees can view available dates (`mentorship/schedule_date/`).
    *   Mentees can view available times for a specific date (`mentorship/schedule_meeting/`).
    *   (Assumed) Functionality to finalize meeting scheduling (POST endpoint for `schedule_meeting` might be missing or not yet implemented in the provided views).
*   **Media Handling:** Upload and display mentee photos.

## Technology Stack

*   **Backend:** Python, Django
*   **Database:** SQLite
*   **Frontend:** Django Templates, HTML

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd PSW13
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **(Optional) Create a superuser** (to access Django Admin):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  Access the application at `http://127.0.0.1:8000/`.

## Usage

*   **Register/Login:** Access `/users/register/` or `/users/login/`.
*   **Mentorship Dashboard (Mentor):** After login, access `/mentorship/`.
*   **Set Availability (Mentor):** After login, access `/mentorship/meeting/`.
*   **Mentee Authentication:** Access `/mentorship/auth/` to enter a token.
*   **View Available Dates (Mentee):** Access `/mentorship/schedule_date/` after authenticating with a token.
*   **Schedule Meeting (Mentee):** Access `/mentorship/schedule_meeting/?date=DD-MM-YYYY` after authenticating with a token.