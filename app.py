from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


def save(obj):
    """Add and commit an object; return an error response tuple or None."""
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        return {"error": str(err.orig)}, 409
    return None


# ---------- Workouts ----------

@app.get("/workouts")
def get_workouts():
    return workouts_schema.dump(Workout.query.all()), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found."}, 404
    return workout_schema.dump(workout), 200


@app.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
        workout = Workout(**data)
    except ValidationError as err:
        return {"errors": err.messages}, 422
    except ValueError as err:
        return {"error": str(err)}, 400

    error = save(workout)
    if error:
        return error
    return workout_schema.dump(workout), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found."}, 404
    db.session.delete(workout)
    db.session.commit()
    return {}, 204


# ---------- Exercises ----------

@app.get("/exercises")
def get_exercises():
    return exercises_schema.dump(Exercise.query.all()), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {"error": "Exercise not found."}, 404
    return exercise_schema.dump(exercise), 200


@app.post("/exercises")
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
        exercise = Exercise(**data)
    except ValidationError as err:
        return {"errors": err.messages}, 422
    except ValueError as err:
        return {"error": str(err)}, 400

    error = save(exercise)
    if error:
        return error
    return exercise_schema.dump(exercise), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {"error": "Exercise not found."}, 404
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204


# ---------- Add exercise to workout ----------

@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>")
def add_exercise_to_workout(workout_id, exercise_id):
    if not db.session.get(Workout, workout_id):
        return {"error": "Workout not found."}, 404
    if not db.session.get(Exercise, exercise_id):
        return {"error": "Exercise not found."}, 404

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
        link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    except ValidationError as err:
        return {"errors": err.messages}, 422
    except ValueError as err:
        return {"error": str(err)}, 400

    error = save(link)
    if error:
        return error
    return workout_exercise_schema.dump(link), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)