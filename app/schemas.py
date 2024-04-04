from enum import Enum
from pydantic import EmailStr, BaseModel, Field


class UserEmailSchema(BaseModel):
    email: EmailStr


class ClientFitnessGoalsEnum(Enum):
    GAIN_WEIGHT = "Gain Weight"
    LOSE_WEIGHT = "Lose Weight"
    BUILD_MUSCLES = "Build Muscles"
    IMPROVE_SLEEP = "Improve Sleep"
    REDUCE_STRESS = "Reduce Stress"
    GET_STRONGER = "Get Stronger"
    GET_FLEXY = "Get Flexy"
    OTHER = "Other"


class ClientActivityEnum(Enum):
    VERY_ACTIVE = "Very Active"
    ACTIVE = "Active"
    MODERATE_ACTIVITY = "Moderate Activity"
    LOW_ACTIVITY = "Low Activity"
    VERY_LOW_ACTIVITY = "Very Low Activity"


class ClientFavoriteSportEnum(Enum):
    WEIGHT_LIFTING = "Weight Lifting"
    CALISTHENICS = "Calisthenics"


class ClientWorkoutIntensityEnum(Enum):
    VERY_INTENSE = "Very Intense"
    INTENSE = "Intense"
    MODERATE_INTENSITY = "Moderate Intensity"
    LOW_INTENSITY = "Low Intensity"
    VERY_LOW_INTENSITY = "Very Low Intensity"


class ClientFitnessLevelEnum(Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ATHLETE = "Athlete"


class ClientProfileSchema(BaseModel):
    fitness_goal: ClientFitnessGoalsEnum = Field(...)
    is_preparing: bool = Field(default=False)
    training_days: int = Field(..., gt=1, lt=8)
    activity: ClientActivityEnum = Field(...)
    has_injuries: bool = Field(default=False)
    sport: ClientFavoriteSportEnum = Field(...)
    has_training_experience: bool = Field(...)
    training_experience: float = Field(default=0)
    fitness_level: ClientFitnessLevelEnum = Field(...)
    instructions: str
