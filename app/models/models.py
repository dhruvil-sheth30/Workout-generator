from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Goal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    ENDURANCE = "endurance"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"

class Experience(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class UserProfile(BaseModel):
    name: str
    age: int = Field(..., ge=16, le=80)
    gender: Gender
    goal: Goal
    experience: Experience
    equipment: List[str]
    days_per_week: int = Field(..., ge=1, le=7)

class Exercise(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[Union[int, str]] = None
    rest: Optional[str] = None
    tempo: Optional[str] = None
    duration: Optional[str] = None

class WorkoutSection(BaseModel):
    warmup: List[Exercise]
    main: List[Exercise]
    cooldown: List[Exercise]
    circuit: Optional[List[Exercise]] = None
    superset: Optional[List[Exercise]] = None

class WorkoutSession(BaseModel):
    session: int
    date: date
    sections: WorkoutSection

class WorkoutPlan(BaseModel):
    client_name: str
    goal: str
    experience: str
    sessions: List[WorkoutSession]
