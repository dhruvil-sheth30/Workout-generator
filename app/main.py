from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import workout

app = FastAPI(
    title="Workout Plan Generator",
    description="A mini AI engine that generates personalized workout plans",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(workout.router, tags=["workout"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Workout Plan Generator API",
        "docs": "/docs",
        "endpoints": [
            "/generate-workout-plan",
            "/generate-workout-pdf",
            "/export-workout-json"
        ]
    }
