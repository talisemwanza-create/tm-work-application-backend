from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from models import CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)
    workouts = fields.List(
        fields.Nested(lambda: WorkoutSchema(only=("id", "date", "duration_minutes"))),
        dump_only=True,
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=0), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=0), allow_none=True)
    exercise = fields.Nested(ExerciseSchema(exclude=("workouts",)), dump_only=True)

    @validates_schema
    def require_reps_or_duration(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError(
                "Provide either reps or duration_seconds.", field_name="reps"
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(validate=validate.Length(max=500), allow_none=True)
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workouts",))
workout_exercise_schema = WorkoutExerciseSchema()