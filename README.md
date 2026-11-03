# Workout Tracker API

A Flask REST API for personal trainers to track workouts and the exercises in them.
Built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow. Exercises are reusable
across workouts, and each workout-exercise link stores sets, reps, or duration.

## Models and Relationships

- **Exercise**: name, category, equipment_needed
- **Workout**: date, duration_minutes, notes
- **WorkoutExercise** (join model): links a workout to an exercise and stores sets, reps, and duration_seconds
- A workout has many exercises through WorkoutExercise, and an exercise can appear in many workouts.

## Installation

```bash
git clone https://github.com/talisemwanza-create/tm-work-application-backend.git
cd tm-work-application-backend
pipenv install
pipenv shell
export FLASK_APP=server/app.py
flask db upgrade
python server/seed.py
```

## Run

```bash
flask run
```

The API runs at http://127.0.0.1:5000.

## Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get one workout with its exercises, sets, reps, and durations |
| POST | `/workouts` | Create a workout. Body: `duration_minutes` (required), `date` (optional, YYYY-MM-DD), `notes` (optional) |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get one exercise with the workouts it appears in |
| POST | `/exercises` | Create an exercise. Body: `name`, `category`, `equipment_needed` (optional) |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>` | Add an exercise to a workout. Body: `reps` and/or `duration_seconds` (at least one), `sets` (optional) |

Valid categories: strength, cardio, flexibility, balance, other.

### Example requests

```bash
curl -X POST localhost:5000/exercises -H "Content-Type: application/json" \
  -d '{"name":"Deadlift","category":"strength","equipment_needed":true}'

curl -X POST localhost:5000/workouts/1/exercises/6 -H "Content-Type: application/json" \
  -d '{"sets":3,"reps":8}'
```

## Validations

- **Table constraints:** unique exercise names, positive workout duration, non-negative reps/sets/duration, reps or duration required, unique exercise per workout.
- **Model validations:** name length, category choices, positive duration, notes length, non-negative numbers.
- **Schema validations:** required fields, length and range checks, category choices, reps-or-duration rule.

## Error Responses

- `404`: record not found
- `409`: database constraint violation (for example, a duplicate exercise name)
- `422`: request failed schema validation
- `400`: request failed model validation