from config import db
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import CheckConstraint

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-workouts.user', '-workouts.workout_exercises')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)

    workouts = db.relationship('Workout', backref='user', cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Invalid email address: must contain '@'")
        return address


class Workout(db.Model, SerializerMixin):
    __tablename__ = 'workouts'

    serialize_rules = ('-user.workouts', '-workout_exercises.workout')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan')

    # Validation: Name cannot be empty
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Workout name cannot be empty")
        return name


class Exercise(db.Model, SerializerMixin):
    __tablename__ = 'exercises'

    serialize_rules = ('-workout_exercises.exercise',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)

    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan')


class WorkoutExercise(db.Model, SerializerMixin):
    __tablename__ = 'workout_exercises'

    serialize_rules = ('-workout.workout_exercises', '-exercise.workout_exercises')

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint('sets > 0', name='check_sets_positive'),
        CheckConstraint('reps > 0', name='check_reps_positive'),
        CheckConstraint('weight >= 0', name='check_weight_non_negative'),
    )

    @validates('sets', 'reps')
    def validate_positive_counts(self, key, value):
        if value is None or value <= 0:
            raise ValueError(f"{key.capitalize()} must be greater than 0")
        return value