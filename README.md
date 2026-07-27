````markdown
# Flask SQLAlchemy Workout Application Backend

A RESTful backend API built with Flask, Flask-SQLAlchemy, and SQLite to manage workouts, exercises, and user tracking.

## Description

This application provides a RESTful API to manage Users, Workouts, Exercises, and Workout-Exercise join records. It includes database schema constraints, model-level validations, custom error handling with appropriate HTTP status codes, and JSON serialization.

## Prerequisites

- Python 3.8+
- `pip` package manager

## Installation

1. **Clone the repository:**
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd flask-workout-backend
   ```
````

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

## Database Setup & Seeding

1. **Initialize and run migrations:**

```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

```

2. **Seed the database with test data:**

```bash
python seed.py

```

## Running the Application

Start the development server:

```bash
python app.py

```

The server will run at `http://127.0.0.1:5555`.

## API Endpoints

| `GET` | `/users` | Retrieve all users |
| `POST` | `/users` | Create a new user |
| `GET` | `/users/:id` | Retrieve user by ID |
| `DELETE` | `/users/:id` | Delete user by ID |
| `GET` | `/workouts` | Retrieve all workouts |
| `POST` | `/workouts` | Create a new workout |
| `GET` | `/workouts/:id` | Retrieve workout by ID |
| `DELETE` | `/workouts/:id` | Delete workout by ID |
| `GET` | `/exercises` | Retrieve all exercises |
| `POST` | `/exercises` | Create a new exercise |
| `POST` | `/workout_exercises` | Link an exercise to a workout |

```

```
