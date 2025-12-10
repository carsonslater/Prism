# Prism - A Social Feed Application

Prism is a Django-based social networking application where users can connect, share updates, and interact with friends. It features a personal feed, a friends feed, and robust profile management.

**Live Demo:** [https://prism-rqbv.onrender.com](https://prism-rqbv.onrender.com)  
*(Note: The live demo is hosted on a free tier, so the initial load may take up to a minute while the server wakes up. Please be patient!)*

## Features

*   **User Authentication**: Secure registration, login, and logout functionality.
*   **Profile Management**: Users can create and update their profiles with bios and other details.
*   **Friendships**:
    *   Send and receive friend requests.
    *   View incoming requests and accept them to build your network.
    *   See a list of your current friends.
*   **Posting & Feeds**:
    *   **My Feed**: View a history of your own posts with engagement metrics (likes/comments).
    *   **Friends Feed**: See what your friends are posting in real-time.
    *   **New Post**: Create text and image-based posts to share with your network.
*   **Interactions**:
    *   **Like**: Like posts from your friends.
    *   **Comment**: specific comments pages for each post for longer discussions.

## Tech Stack

*   **Backend**: Python, Django 3.2+
*   **Database**: SQLite (Local), PostgreSQL (Production)
*   **Frontend**: HTML5, Bootstrap 4, Django Template Language
*   **Deployment**: Render (Gunicorn, WhiteNoise)

## Installation & Local Development

Follow these steps to get a local copy up and running.

### Prerequisites

*   Python 3.8+
*   pip
*   virtualenv (recommended)

### Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/carsonslater/Prism.git
    cd Prism
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # MacOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional)**
    To access the Django admin panel:
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

7.  **Visit the App**
    Open your browser and go to `http://127.0.0.1:8000`.

## Deployment

The project is configured for deployment on Render using a `build.sh` script and environment-aware settings.

1.  Push code to GitHub.
2.  Connect repository to a Render **Web Service**.
3.  Set Build Command: `./build.sh`
4.  Set Start Command: `gunicorn FeedProject.wsgi:application`
5.  Add Environment Variables:
    *   `SECRET_KEY`: (Your secret key)
    *   `PYTHON_VERSION`: `3.11.0` (or similar)
    *   `DATABASE_URL`: (Connect to a Render PostgreSQL instance)
