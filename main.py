import os
import requests
import urllib3
from random import randint, choice
from todoist_api_python.api import TodoistAPI

# 1. Setup SSL-agnostic Session
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.verify = False

TODOIST_TOKEN = os.environ.get("TODOIST_KEY")
api = TodoistAPI(TODOIST_TOKEN, session=session)

# 2. Define a helper for comments since the SDK model is failing
def add_comment_with_attachment(task_id, content, file_url, file_name):
    url = "https://api.todoist.com/rest/v2/comments" # Force REST v2 for stability
    headers = {"Authorization": f"Bearer {TODOIST_TOKEN}"}
    payload = {
        "task_id": task_id,
        "content": content,
        "attachment": {
            "resource_type": "file",
            "file_url": file_url,
            "file_type": "image/png",
            "file_name": file_name,
        }
    }
    # Use the SAME session to maintain the verify=False setting
    resp = session.post(url, headers=headers, json=payload)
    return resp

workout_config = {
    "Legs, Butt and Calf": {
        "workouts": ["Side Lunge Thruster", "Sumo Squat", "Calf Raise", "Fire Hydrant", "Hamstring Curl", "Curtsy Lunge", "Glute Bridge", "Bulgarian Lunge", "Donkey Kick", "Leg Extension"]
    },
    "Fat Burning": {
        "workouts": ["Step Up", "Swing", "Thruster", "Burpee", "V Up", "Russian Twist", "Hollow Body Sweeper", "Bow Extension", "Hollow Fly"],
    },
    "Arms, Chest and Shoulders": {
        "workouts": ["Single Arm Lateral Raise", "L Raise", "Chest Fly", "Dumbbell Pullover", "Alternating Curl", "Single Arm Upright Row", "Alternating Front Raise", "Push Up", "Curl to Overhead Press", "Wrist Curl", "Bench Press", "Grip Curl", "Side Raise", "Shoulder Shrug", "Single Arm Tricep Extension"],
    },
    "Strengthen Back": {
        "workouts": ["Bent Over Row", "Renegade Row", "Floor T Raise", "Bird Dog Row", "Single Arm Row"]
    },
    "_meta": {
        "minWorkouts": 4,
        "maxWorkouts": 8,
        "sets": {"minSets": 3, "maxSets": 5},
        "reps": {"minReps": 12, "maxReps": 15},
    },
}

def get_workout_by_category(category):
    return workout_config.get(category, {}).get("workouts", [])

# Selection Logic
num_workouts = randint(workout_config["_meta"]["minWorkouts"], workout_config["_meta"]["maxWorkouts"])
categories = [k for k in workout_config.keys() if k != "_meta"]
selected_categories = ["Fat Burning", "Fat Burning"]
while len(selected_categories) < num_workouts:
    selected_categories.append(choice(categories))

try:
    # 1. Create Parent Task
    parent_task = api.add_task(
        content="🏃Workout and 🚿Shower",
        description="Workout, either 10k steps, cardio or weights.",
        labels=["health"],
        priority=3,
        due_string="today",
    )
    
    # 2. Add Parent Attachment (Manual call to avoid SDK 500/AttributeError)
    add_comment_with_attachment(
        parent_task.id, 
        "Workout reference", 
        "https://lifeprofitness.com/cdn/shop/products/Untitleddesign.png", 
        "workout_overview.png"
    )

    # 3. Create Subtasks
    for category in selected_categories:
        workout_name = choice(get_workout_by_category(category))
        sets = randint(workout_config["_meta"]["sets"]["minSets"], workout_config["_meta"]["sets"]["maxSets"])
        reps = randint(workout_config["_meta"]["reps"]["minReps"], workout_config["_meta"]["reps"]["maxReps"])
        lbs = choice([15, 20])
        
        subtask = api.add_task(
            content=f"{workout_name}: {sets}x{reps} @ {lbs}lbs",
            parent_id=parent_task.id,
            due_string="today",
            labels=["health"],
            priority=1
        )

        img_slug = workout_name.lower().replace(' ', '_')
        add_comment_with_attachment(
            subtask.id,
            f"Form guide for {workout_name}",
            f"https://raw.githubusercontent.com/mike-bailey/auto-workouts/refs/heads/main/img/{img_slug}.png",
            f"{img_slug}.png"
        )

    print("Success! All tasks and images synced.")

except Exception as error:
    print(f"Error during execution: {error}")