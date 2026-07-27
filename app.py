from flask import request, jsonify
from config import app, db
from models import User, Workout, Exercise, WorkoutExercise

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Workout Application Backend API"}), 200

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200

    elif request.method == 'POST':
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')

        if not username or not email:
            return jsonify({"error": "Validation Error: 'username' and 'email' are required."}), 400

        try:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400


@app.route('/users/<int:id>', methods=['GET', 'DELETE'])
def handle_user_by_id(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": f"User with ID {id} not found."}), 404

    if request.method == 'GET':
        return jsonify(user.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {id} deleted successfully."}), 200


@app.route('/workouts', methods=['GET', 'POST'])
def handle_workouts():
    if request.method == 'GET':
        workouts = Workout.query.all()
        return jsonify([w.to_dict() for w in workouts]), 200

    elif request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name')
        date = data.get('date')
        user_id = data.get('user_id')

        if not name or not date or not user_id:
            return jsonify({"error": "Validation Error: 'name', 'date', and 'user_id' are required."}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with ID {user_id} does not exist."}), 404

        try:
            new_workout = Workout(name=name, date=date, user_id=user_id)
            db.session.add(new_workout)
            db.session.commit()
            return jsonify(new_workout.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400


@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def handle_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": f"Workout with ID {id} not found."}), 404

    if request.method == 'GET':
        return jsonify(workout.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message": f"Workout {id} deleted successfully."}), 200


@app.route('/exercises', methods=['GET', 'POST'])
def handle_exercises():
    if request.method == 'GET':
        exercises = Exercise.query.all()
        return jsonify([e.to_dict() for e in exercises]), 200

    elif request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name')
        category = data.get('category')

        if not name or not category:
            return jsonify({"error": "Validation Error: 'name' and 'category' are required."}), 400

        try:
            new_exercise = Exercise(name=name, category=category)
            db.session.add(new_exercise)
            db.session.commit()
            return jsonify(new_exercise.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400


@app.route('/workout_exercises', methods=['POST'])
def handle_workout_exercises():
    data = request.get_json() or {}
    workout_id = data.get('workout_id')
    exercise_id = data.get('exercise_id')
    sets = data.get('sets')
    reps = data.get('reps')
    weight = data.get('weight')

    missing_fields = [field for field in ['workout_id', 'exercise_id', 'sets', 'reps', 'weight'] if data.get(field) is None]
    if missing_fields:
        return jsonify({"error": f"Validation Error: Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        new_we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            sets=sets,
            reps=reps,
            weight=weight
        )
        db.session.add(new_we)
        db.session.commit()
        return jsonify(new_we.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)