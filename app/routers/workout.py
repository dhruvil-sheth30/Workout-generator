from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import json
import os
from typing import Dict

from app.models.models import UserProfile
from app.utils.workout_generator import generate_plan_json, generate_pdf

router = APIRouter()

@router.post("/generate-workout-plan", response_model=Dict)
async def generate_workout_plan(user_profile: UserProfile):
    """
    Generate a workout plan based on the user profile.
    Returns the workout plan as JSON.
    """
    try:
        workout_plan = generate_plan_json(user_profile)
        return workout_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-workout-pdf")
async def generate_workout_pdf(user_profile: UserProfile):
    """
    Generate a workout plan based on the user profile.
    Returns the workout plan as a PDF file.
    """
    try:
        workout_plan = generate_plan_json(user_profile)
        pdf_path = generate_pdf(workout_plan)
        
        return FileResponse(
            path=pdf_path, 
            filename="workout_plan.pdf", 
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export-workout-json")
async def export_workout_json(user_profile: UserProfile):
    """
    Generate a workout plan based on the user profile.
    Returns the workout plan as a downloadable JSON file.
    """
    try:
        workout_plan = generate_plan_json(user_profile)
        
        # Save the JSON to a file
        with open("workout_plan.json", "w") as f:
            json.dump(workout_plan, f, indent=4, default=str)
        
        return FileResponse(
            path="workout_plan.json", 
            filename="workout_plan.json", 
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
