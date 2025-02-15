from random import *
import os
from todoist_api_python.api import TodoistAPI

api = TodoistAPI(os.environ['TODOIST_KEY'])

workout_config = {
    "Legs, Butt and Calf": {
        "workouts": [
            "Side Lunge Thruster",
            "Sumo Squat",
            "Calf Raise",
            "Fire Hydrant",
            "Hamstring Curl",
            "Curtsy Lunge",
            "Glute Bridge",
            "Bulgarian Lunge",
            "Donkey Kick",
            "Leg Extension",
        ]
    },
    "Fat Burning": {
        "workouts": [
            "Step Up",
            "Swing",
            "Thruster",
            "Burpee",
            "V Up",
            "Russian Twist",
            "Hollow Body Sweeper",
            "Bow Extension",
            "Hollow Fly",
        ],
    },
    "Arms, Chest and Shoulders": {
        "workouts": [
            "Single Arm Lateral Raise",
            "L Raise",
            "Chest Fly",
            "Dumbbell Pullover",
            "Alternating Curl",
            "Single Arm Upright Row",
            "Alternating Front Raise",
            "Push Up",
            "Curl to Overhead Press",
            "Wrist Curl",
            "Bench Press",
            "Grip Curl",
            "Side Raise",
            "Shoulder Shrug",
            "Single Arm Tricep Extension",
        ],
    },
    "Strengthen Back": {
        "workouts": [
            "Bent Over Row",
            "Renegade Row",
            "Floor T Raise",
            "Bird Dog Row",
            "Single Arm Row",
        ]
    },
    "_meta": {
        "minWorkouts": 4,
        "maxWorkouts": 8,
        "sets": {
            "minSets": 3,
            "maxSets": 5,
        },
        "reps": {"minReps": 12, "maxReps": 15},
    },
}


def get_workout_by_category(category):
    return workout_config.get(category, {}).get("workouts", [])


workouts = randint(
    workout_config["_meta"]["minWorkouts"], workout_config["_meta"]["maxWorkouts"] + 1
)
selected_workouts = []

# Ensure at least two categories are "Fat burning"
categories = list(workout_config.keys())
categories.remove("_meta")
selected_categories = ["Fat Burning", "Fat Burning"]

# Add more random categories to reach the required number of workouts

while len(selected_categories) < workouts:
    category = choice(categories)
    print(selected_categories)
    selected_categories.append(category)


try:
    task = api.add_task(content="Workout", due_string="today")
    new_comment = api.add_comment(
        task_id=task.id,
        content="Workout reference",
        attachment={
            "resource_type": "file",
            "file_url": "https://lifeprofitness.com/cdn/shop/products/Untitleddesign.png",
            "file_type": "image/png",
            "file_name": "workout.pdf",
        },
    )
    print(task)
except Exception as error:
    print(error)
    raise Exception("Cannot create parent in todoist")

# Select a workout from each category and specify reps and sets
for category in selected_categories:
    workout = choice(get_workout_by_category(category))
    sets = randint(
        workout_config["_meta"]["sets"]["minSets"],
        workout_config["_meta"]["sets"]["maxSets"] + 1,
    )
    reps = randint(
        workout_config["_meta"]["reps"]["minReps"],
        workout_config["_meta"]["reps"]["maxReps"] + 1,
    )
    lbs = choice([15, 20])
    selected_workouts.append(
        {
            "category": category,
            "workout": workout,
            "sets": sets,
            "reps": reps,
            "pounds": lbs,
        }
    )

for work_arr in selected_workouts:
    subtask = api.add_task(
        content=f"{work_arr['workout']}: {work_arr['sets']}x{work_arr['reps']} @ {work_arr['pounds']}lbs",
        due_string="today",
        labels=["health"],
        parent_id=task.id,
        priority=2,
    )
