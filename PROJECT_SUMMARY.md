# Workout Plan Generator - Project Summary

## Overview
This web application generates personalized 12-session workout plans based on user goals, experience level, and available equipment. It follows a progressive overload approach and creates structured workouts with warm-up, main exercises, and cool-down sections.

## Key Features

### Personalization
- Adapts to user goals (weight loss, muscle gain, endurance, strength, flexibility)
- Scales difficulty based on experience level (beginner, intermediate, advanced)
- Customizes exercises based on available equipment
- Creates appropriate workout split based on training frequency

### Progressive Overload
- Increases sets by 1 in weeks 3 and 4
- Adds 2 reps progressively each week
- Includes appropriate rest periods and exercise tempo

### Workout Structure
- Warm-up section with dynamic stretches and mobility exercises
- Main workout section targeting specific muscle groups
- Cool-down section with static stretches
- Optional circuit/superset for intermediate and advanced users

### Exercise Selection Logic
- Push/Pull/Legs split for 3 days/week
- Upper/Lower split for 4 days/week
- Full-body workouts for other frequencies
- Balanced muscle group targeting

### Export Options
- Web-based preview of the workout plan
- PDF download with detailed instructions
- JSON export for integration with other applications

## Technology
- Flask web framework
- Clean responsive UI with Bootstrap
- RESTful API for workout generation
- PDF generation capability

## Deployment
The application is ready for deployment on cloud platforms like Render, Railway, or Heroku using the included configuration files.

## Future Enhancements
- User accounts for saving workout history
- Exercise illustrations and video links
- Nutrition recommendations
- Mobile application

## About This Project
This project was created as part of an AI Intern Assignment with a focus on creating a workout plan generator that implements exercise science principles while providing a user-friendly interface.
