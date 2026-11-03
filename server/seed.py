from datetime import date

from app import app
from models import Exercise, Workout, WorkoutExercise, db

with app.app_context():
    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="balance", equipment_needed=False)
    stretch = Exercise(name="Hamstring Stretch", category="flexibility")
    db.session.add_all([squat, pushup, run, plank, stretch])

    print("Creating workouts...")
    w1 = Workout(date=date(2026, 10, 28), duration_minutes=45, notes="Leg day")
    w2 = Workout(date=date(2026, 10, 30), duration_minutes=30, notes="Cardio and core")
    w3 = Workout(date=date(2026, 11, 1), duration_minutes=60)
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print("Linking exercises to workouts...")
    links = [
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, sets=4, reps=10),
        WorkoutExercise(workout_id=w1.id, exercise_id=stretch.id, duration_seconds=120),
        WorkoutExercise(workout_id=w2.id, exercise_id=run.id, duration_seconds=1200),
        WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, sets=3, duration_seconds=60),
        WorkoutExercise(workout_id=w3.id, exercise_id=pushup.id, sets=3, reps=15),
        WorkoutExercise(workout_id=w3.id, exercise_id=squat.id, sets=3, reps=12),
    ]
    db.session.add_all(links)
    db.session.commit()
    print("Done seeding!")