from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import random
from fpdf import FPDF

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load exercise data
def load_exercises():
    """Load exercises from JSON file."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")  # Debug log
        
        # Try all possible paths
        possible_paths = [
            os.path.join(current_dir, "app", "data", "exercises.json"),
            os.path.join(current_dir, "data", "exercises.json"),
            os.path.join("app", "data", "exercises.json"),
            os.path.join("data", "exercises.json"),
            "exercises.json"
        ]
        
        for path in possible_paths:
            print(f"Trying path: {path}")  # Debug log
            if os.path.exists(path):
                print(f"Found exercises file at: {path}")  # Debug log
                with open(path, 'r') as f:
                    exercises = json.load(f)
                    print(f"Loaded {len(exercises)} exercises")  # Debug log
                    return exercises
        
        raise FileNotFoundError(f"Could not find exercises.json in any of these locations: {', '.join(possible_paths)}")
    except Exception as e:
        print(f"Error loading exercises: {str(e)}")  # Debug log
        raise

# Filter exercises based on equipment, type, level, and muscle group
def filter_exercises(exercises, equipment, exercise_type=None, level=None, muscle_group=None):
    """Filter exercises based on equipment, type, level, and muscle group."""
      # Filter exercises that match any equipment in the list or have no equipment requirement
    filtered = [ex for ex in exercises if ex["equipment"] in equipment or ex["equipment"] == "bodyweight" or ex["equipment"] == "none"]
    
    # If type is specified, filter by type
    if exercise_type:
        filtered = [ex for ex in filtered if ex["type"] == exercise_type]
    
    # If level is specified, filter by level
    if level:
        # For "intermediate" users, include beginner exercises too
        if level == "intermediate":
            filtered = [ex for ex in filtered if ex["level"] in ["beginner", "intermediate"]]
        # For "advanced" users, include all levels
        elif level == "advanced":
            pass  # Keep all exercises
        # For "beginner" users, only include beginner exercises
        else:
            filtered = [ex for ex in filtered if ex["level"] == "beginner"]
    
    # If muscle group is specified, filter by muscle group
    if muscle_group:
        filtered = [ex for ex in filtered if ex["muscle_group"] == muscle_group]
    
    return filtered

# Create exercise object with progressive overload
def create_exercise_object(exercise_data, session_number=1, week_number=1):
    """Create an exercise object with progressive overload based on session and week number."""
    exercise_obj = {}
    
    # Copy the name
    exercise_obj["name"] = exercise_data["name"]
    
    # If exercise has sets and reps, include them
    if "sets" in exercise_data:
        # Apply progressive overload: increase sets by 1 in week 3 and 4
        sets = exercise_data["sets"]
        if week_number >= 3:
            sets += 1
        exercise_obj["sets"] = sets
    
    if "reps" in exercise_data:
        # Apply progressive overload: increase reps by 2 every week
        if isinstance(exercise_data["reps"], int):
            reps = exercise_data["reps"] + (week_number - 1) * 2
            exercise_obj["reps"] = reps
        else:
            exercise_obj["reps"] = exercise_data["reps"]
    
    # If exercise has duration, include it
    if "duration" in exercise_data:
        exercise_obj["duration"] = exercise_data["duration"]
    
    # Add rest time for main exercises
    if exercise_data["type"] == "main":
        exercise_obj["rest"] = "60s"
        
        # For intermediate and advanced, add tempo
        if exercise_data["level"] in ["intermediate", "advanced"]:
            exercise_obj["tempo"] = "2-1-1"
    
    return exercise_obj

# Select push exercises (chest, shoulders, and triceps)
def select_push_exercises(exercises, equipment, level, count=3):
    """Select push exercises (chest, shoulders, and triceps)."""
    chest_exercises = filter_exercises(exercises, equipment, exercise_type="main", level=level, muscle_group="chest")
    shoulder_exercises = filter_exercises(exercises, equipment, exercise_type="main", level=level, muscle_group="shoulders")
    
    # Try to select a balanced mix
    selected = []
    if chest_exercises:
        selected.extend(random.sample(chest_exercises, min(2, len(chest_exercises))))
    if shoulder_exercises:
        selected.extend(random.sample(shoulder_exercises, min(1, len(shoulder_exercises))))
    
    # If we don't have enough, add more from any group
    all_push = chest_exercises + shoulder_exercises
    remaining = count - len(selected)
    if remaining > 0 and all_push:
        # Make sure we don't select duplicates
        remaining_options = [ex for ex in all_push if ex not in selected]
        if remaining_options:
            selected.extend(random.sample(remaining_options, min(remaining, len(remaining_options))))
    
    return selected

# Select pull exercises (back and biceps)
def select_pull_exercises(exercises, equipment, level, count=3):
    """Select pull exercises (back and biceps)."""
    back_exercises = filter_exercises(exercises, equipment, exercise_type="main", level=level, muscle_group="back")
    arm_exercises = filter_exercises(exercises, equipment, exercise_type="main", level=level, muscle_group="arms")
    
    # Try to select a balanced mix
    selected = []
    if back_exercises:
        selected.extend(random.sample(back_exercises, min(2, len(back_exercises))))
    if arm_exercises:
        selected.extend(random.sample(arm_exercises, min(1, len(arm_exercises))))
    
    # If we don't have enough, add more from any group
    all_pull = back_exercises + arm_exercises
    remaining = count - len(selected)
    if remaining > 0 and all_pull:
        # Make sure we don't select duplicates
        remaining_options = [ex for ex in all_pull if ex not in selected]
        if remaining_options:
            selected.extend(random.sample(remaining_options, min(remaining, len(remaining_options))))
    
    return selected

# Select leg exercises
def select_leg_exercises(exercises, equipment, level, count=3):
    """Select leg exercises."""
    leg_exercises = filter_exercises(exercises, equipment, exercise_type="main", level=level, muscle_group="legs")
    
    selected = []
    if leg_exercises:
        selected.extend(random.sample(leg_exercises, min(count, len(leg_exercises))))
    
    return selected

# Select core exercises
def select_core_exercises(exercises, equipment, level, count=2):
    """Select core exercises."""
    core_exercises = filter_exercises(exercises, equipment, exercise_type="main", level=level, muscle_group="core")
    
    selected = []
    if core_exercises:
        selected.extend(random.sample(core_exercises, min(count, len(core_exercises))))
    
    return selected

# Select warmup exercises
def select_warmup_exercises(exercises, equipment, count=3):
    """Select warmup exercises."""
    warmup_exercises = filter_exercises(exercises, equipment, exercise_type="warmup")
    
    selected = []
    if warmup_exercises:
        selected.extend(random.sample(warmup_exercises, min(count, len(warmup_exercises))))
    
    return selected

# Select cooldown exercises
def select_cooldown_exercises(exercises, equipment, count=3):
    """Select cooldown exercises."""
    cooldown_exercises = filter_exercises(exercises, equipment, exercise_type="cooldown")
    
    selected = []
    if cooldown_exercises:
        selected.extend(random.sample(cooldown_exercises, min(count, len(cooldown_exercises))))
    
    return selected

# Generate workout plan
def generate_workout_plan(user_profile):
    """Generate a 12-session workout plan based on user profile."""
    exercises = load_exercises()
    
    # Determine start date (first Monday from today)
    today = datetime.now().date()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # If today is Monday, start next Monday
    start_date = today + timedelta(days=days_until_monday)
    
    # Create workout sessions
    sessions = []
    session_count = user_profile["days_per_week"] * 4  # 4 weeks
    
    # Create workout split
    if user_profile["days_per_week"] == 3:
        # Push-Pull-Legs split
        workout_split = ["push", "pull", "legs"] * 4
    elif user_profile["days_per_week"] == 4:
        # Upper-Lower split
        workout_split = ["upper", "lower", "upper", "lower"] * 3
    else:
        # Full body workouts
        workout_split = ["full"] * session_count
    
    for i in range(session_count):
        session_number = i + 1
        week_number = (i // user_profile["days_per_week"]) + 1
        split_type = workout_split[i]
        
        # Determine workout day date (skipping weekends if days_per_week <= 5)
        if user_profile["days_per_week"] <= 5:
            days_to_add = i
            # Add extra days for weekends
            days_to_add += (i // 5) * 2
            session_date = start_date + timedelta(days=days_to_add)
        else:
            session_date = start_date + timedelta(days=i)
        
        # Select exercises based on split type and generate workout
        main_exercises = []
        
        if split_type == "push":
            main_exercises = select_push_exercises(exercises, user_profile["equipment"], user_profile["experience"], 3)
            # Add 1 core exercise
            main_exercises.extend(select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
        
        elif split_type == "pull":
            main_exercises = select_pull_exercises(exercises, user_profile["equipment"], user_profile["experience"], 3)
            # Add 1 core exercise
            main_exercises.extend(select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
        
        elif split_type == "legs":
            main_exercises = select_leg_exercises(exercises, user_profile["equipment"], user_profile["experience"], 3)
            # Add 1 core exercise
            main_exercises.extend(select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
        
        elif split_type == "upper":
            # Select 2 push and 2 pull
            main_exercises = select_push_exercises(exercises, user_profile["equipment"], user_profile["experience"], 2)
            main_exercises.extend(select_pull_exercises(exercises, user_profile["equipment"], user_profile["experience"], 2))
            # Add 1 core
            main_exercises.extend(select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
        
        elif split_type == "lower":
            # Select 4 leg exercises
            main_exercises = select_leg_exercises(exercises, user_profile["equipment"], user_profile["experience"], 4)
            # Add 1 core
            main_exercises.extend(select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
        
        else:  # full body
            # Select 1 push, 1 pull, 1 leg, 1 core
            main_exercises = select_push_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1)
            main_exercises.extend(select_pull_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
            main_exercises.extend(select_leg_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
            main_exercises.extend(select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 1))
        
        # Select warmup exercises
        warmup_exercises = select_warmup_exercises(exercises, user_profile["equipment"], 3)
        
        # Select cooldown exercises
        cooldown_exercises = select_cooldown_exercises(exercises, user_profile["equipment"], 3)
        
        # Create Exercise objects with progressive overload
        main_exercise_objects = [
            create_exercise_object(ex, session_number, week_number) for ex in main_exercises
        ]
        warmup_exercise_objects = [
            create_exercise_object(ex, session_number, week_number) for ex in warmup_exercises
        ]
        cooldown_exercise_objects = [
            create_exercise_object(ex, session_number, week_number) for ex in cooldown_exercises
        ]
        
        # Create optional circuit or superset for intermediate and advanced users
        circuit_exercises = None
        if user_profile["experience"] in ["intermediate", "advanced"] and session_number % 3 == 0:
            # Create a circuit with 3 exercises
            circuit_candidates = select_core_exercises(exercises, user_profile["equipment"], user_profile["experience"], 3)
            circuit_exercises = [
                create_exercise_object(ex, session_number, week_number) for ex in circuit_candidates
            ]
        
        # Create workout section
        workout_section = {
            "warmup": warmup_exercise_objects,
            "main": main_exercise_objects,
            "cooldown": cooldown_exercise_objects
        }
        
        # Add circuit if created
        if circuit_exercises:
            workout_section["circuit"] = circuit_exercises
        
        # Create workout session
        workout_session = {
            "session": session_number,
            "date": session_date.strftime("%Y-%m-%d"),
            "sections": workout_section
        }
        
        sessions.append(workout_session)
    
    return sessions

# Generate plan JSON
def generate_plan_json(user_profile):
    """Generate the complete workout plan as a dictionary."""
    sessions = generate_workout_plan(user_profile)
    
    workout_plan = {
        "client_name": user_profile["name"],
        "goal": user_profile["goal"],
        "experience": user_profile["experience"],
        "sessions": sessions
    }
    
    return workout_plan

# Generate PDF
def generate_pdf(workout_plan):
    """Generate a PDF of the workout plan."""
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Workout Plan for {workout_plan['client_name']}", 0, 1, "C")
    
    # Add some info
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Goal: {workout_plan['goal'].replace('_', ' ').title()}", 0, 1)
    pdf.cell(0, 10, f"Experience: {workout_plan['experience'].title()}", 0, 1)
    
    # Add each session
    for session in workout_plan["sessions"]:
        pdf.add_page()
        
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Session {session['session']} - {session['date']}", 0, 1)
        
        # Warmup section
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Warm-Up", 0, 1)
        
        pdf.set_font("Arial", "", 10)
        for exercise in session["sections"]["warmup"]:
            description = exercise["name"]
            if "sets" in exercise and "reps" in exercise:
                description += f" - {exercise['sets']} sets x {exercise['reps']} reps"
            elif "duration" in exercise:
                description += f" - {exercise['duration']}"
            pdf.cell(0, 8, description, 0, 1)
        
        # Main section
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Main Exercises", 0, 1)
        
        pdf.set_font("Arial", "", 10)
        for exercise in session["sections"]["main"]:
            description = exercise["name"]
            if "sets" in exercise and "reps" in exercise:
                description += f" - {exercise['sets']} sets x {exercise['reps']} reps"
                if "rest" in exercise:
                    description += f", Rest: {exercise['rest']}"
                if "tempo" in exercise:
                    description += f", Tempo: {exercise['tempo']}"
            pdf.cell(0, 8, description, 0, 1)
        
        # Circuit section (if available)
        if "circuit" in session["sections"] and session["sections"]["circuit"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Circuit (Complete 3 rounds)", 0, 1)
            
            pdf.set_font("Arial", "", 10)
            for exercise in session["sections"]["circuit"]:
                description = exercise["name"]
                if "sets" in exercise and "reps" in exercise:
                    description += f" - {exercise['reps']} reps"
                elif "duration" in exercise:
                    description += f" - {exercise['duration']}"
                pdf.cell(0, 8, description, 0, 1)
        
        # Cooldown section
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Cool-Down", 0, 1)
        
        pdf.set_font("Arial", "", 10)
        for exercise in session["sections"]["cooldown"]:
            description = exercise["name"]
            if "duration" in exercise:
                description += f" - {exercise['duration']}"
            pdf.cell(0, 8, description, 0, 1)
    
    # Save the PDF
    output_path = "workout_plan.pdf"
    pdf.output(output_path)
    
    return output_path

# API routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return jsonify({
        "message": "Welcome to the Workout Plan Generator API",
        "endpoints": [
            "/generate-workout-plan",
            "/generate-workout-pdf",
            "/export-workout-json"
        ]
    })

@app.route('/generate-workout-plan', methods=['POST'])
def generate_workout_plan_route():
    """Generate a workout plan based on the user profile. Returns the workout plan as JSON."""
    try:
        # Handle both JSON and form data
        if request.is_json:
            user_profile = request.json
        else:
            user_profile_str = request.form.get('user_profile', '{}')
            user_profile = json.loads(user_profile_str)
        
        print(f"Received user profile: {user_profile}")  # Debug log
        
        # Validate required fields
        required_fields = ['name', 'goal', 'experience', 'equipment', 'days_per_week']
        missing_fields = [field for field in required_fields if field not in user_profile]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Validate equipment is a list
        if not isinstance(user_profile['equipment'], list):
            return jsonify({"error": "Equipment must be a list"}), 400
            
        workout_plan = generate_plan_json(user_profile)
        return jsonify(workout_plan)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400
    except Exception as e:
        print(f"Error generating workout plan: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

@app.route('/generate-workout-pdf', methods=['POST'])
def generate_workout_pdf_route():
    """Generate a workout plan based on the user profile. Returns the workout plan as a PDF file."""
    try:
        # Handle both JSON and form data
        if request.is_json:
            user_profile = request.json
        else:
            user_profile_str = request.form.get('user_profile', '{}')
            user_profile = json.loads(user_profile_str)
        
        print(f"Received user profile for PDF: {user_profile}")  # Debug log
        
        # Validate required fields
        required_fields = ['name', 'goal', 'experience', 'equipment', 'days_per_week']
        missing_fields = [field for field in required_fields if field not in user_profile]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Validate equipment is a list
        if not isinstance(user_profile['equipment'], list):
            return jsonify({"error": "Equipment must be a list"}), 400
            
        workout_plan = generate_plan_json(user_profile)
        pdf_path = generate_pdf(workout_plan)
        
        return send_file(pdf_path, download_name="workout_plan.pdf")
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

@app.route('/export-workout-json', methods=['POST'])
def export_workout_json_route():
    """Generate a workout plan based on the user profile. Returns the workout plan as a downloadable JSON file."""
    try:
        # Handle both JSON and form data
        if request.is_json:
            user_profile = request.json
        else:
            user_profile_str = request.form.get('user_profile', '{}')
            user_profile = json.loads(user_profile_str)
            
        print(f"Received user profile for JSON export: {user_profile}")  # Debug log
        
        # Validate required fields
        required_fields = ['name', 'goal', 'experience', 'equipment', 'days_per_week']
        missing_fields = [field for field in required_fields if field not in user_profile]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Validate equipment is a list
        if not isinstance(user_profile['equipment'], list):
            return jsonify({"error": "Equipment must be a list"}), 400
            
        workout_plan = generate_plan_json(user_profile)
        
        # Save the JSON to a file
        with open("workout_plan.json", "w") as f:
            json.dump(workout_plan, f, indent=4, default=str)
        
        return send_file("workout_plan.json", download_name="workout_plan.json")
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400
    except Exception as e:
        print(f"Error generating JSON file: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
