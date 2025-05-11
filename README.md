# Workout Plan Generator

A mini AI engine that generates personalized 12-session workout plans based on a user's profile. This application creates progressive workout routines tailored to individual goals, experience levels, and available equipment.

## Features

- Generates a 12-session progressive workout plan (3 sessions/week for 4 weeks)
- Each workout contains 3 primary sections: Warm-Up, Main Exercises, Cool-Down
- Optional custom sections: Circuit or Superset (for intermediate and advanced users)
- Progressive overload strategy (increasing sets/reps over weeks)
- Smart workout splits based on days per week (Push-Pull-Legs, Upper-Lower, Full Body)
- PDF export functionality
- JSON export functionality
- Web-based UI for easy interaction
- RESTful API implementation

## Tech Stack

- Flask: Lightweight web framework for building APIs and serving web content
- Python 3.7+: Core programming language
- FPDF: PDF generation
- Bootstrap 5: Frontend UI components

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/workout-generator.git
   cd workout-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Access the application:
   - Web UI: http://localhost:8000/
   - API Docs: http://localhost:8000/api

## API Usage

### Generate a Workout Plan

**Endpoint:** `POST /generate-workout-plan`

**Request Body Example:**
```json
{
  "name": "Aarav",
  "age": 35,
  "gender": "male",
  "goal": "muscle_gain",
  "experience": "intermediate",
  "equipment": ["dumbbells", "bench", "resistance_band"],
  "days_per_week": 3
}
```

**Response:** A complete workout plan in JSON format

### Generate a PDF Workout Plan

**Endpoint:** `POST /generate-workout-pdf`

Uses the same request body as above but returns a downloadable PDF.

### Export Workout Plan as JSON

**Endpoint:** `POST /export-workout-json`

Uses the same request body as above but returns a downloadable JSON file.

## Deployment

The application can be deployed on platforms like Render, Railway, Heroku, or any cloud VM.

### Deploying to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment Variable: `PORT=10000`

### Deploying to Heroku

1. Create a new Heroku app
2. Connect your GitHub repository
3. Deploy the application
   - The included Procfile will automatically configure the application

## Architecture

The Workout Plan Generator follows a simple MVC-like architecture:

1. **Data Layer**: Exercise database stored in JSON format
2. **Business Logic**: 
   - Exercise selection based on user profile
   - Progressive overload calculation
   - PDF generation
3. **API Layer**: RESTful endpoints for accessing functionality
4. **Presentation Layer**: Simple Bootstrap-based UI

## License

MIT
