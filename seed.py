from config import app, db
from models import User, Workout, Exercise, WorkoutExercise

def seed_database():
    with app.app_context():
        print("Clearing existing database tables...")
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        User.query.delete()

        print("Seeding Users...")
        user1 = User(username="john_doe", email="john@example.com")
        user2 = User(username="jane_fit", email="jane@example.com")
        db.session.add_all([user1, user2])
        db.session.commit()

        print("Seeding Exercises...")
        ex1 = Exercise(name="Bench Press", category="Chest")
        ex2 = Exercise(name="Squat", category="Legs")
        ex3 = Exercise(name="Pull-up", category="Back")
        db.session.add_all([ex1, ex2, ex3])
        db.session.commit()

        print("Seeding Workouts...")
        w1 = Workout(name="Upper Body Power", date="2026-03-01", user_id=user1.id)
        w2 = Workout(name="Leg Day Heavy", date="2026-03-02", user_id=user2.id)
        db.session.add_all([w1, w2])
        db.session.commit()

        print("Seeding Workout Exercises...")
        we1 = WorkoutExercise(
            workout_id=w1.id,
            exercise_id=ex1.id,
            sets=4,
            reps=8,
            weight=185.0
        )
        we2 = WorkoutExercise(
            workout_id=w1.id,
            exercise_id=ex3.id,
            sets=3,
            reps=10,
            weight=0.0
        )
        we3 = WorkoutExercise(
            workout_id=w2.id,
            exercise_id=ex2.id,
            sets=5,
            reps=5,
            weight=225.0
        )
        db.session.add_all([we1, we2, we3])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database() 