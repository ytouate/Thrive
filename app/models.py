from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MaxValueValidator, MinValueValidator
from .schemas import (
    ClientActivityEnum,
    ClientFavoriteSportEnum,
    ClientFitnessGoalsEnum,
    ClientFitnessLevelEnum,
)


class ClientProfile(Model):
    fitness_goal = fields.CharEnumField(
        enum_type=ClientFitnessGoalsEnum,
        description="Represents the fitness goals of the client",
    )
    is_preparing = fields.BooleanField(
        description="Represents whether the client is preparing for an event or milestone",
    )
    training_days = fields.SmallIntField(
        validators=[MaxValueValidator(7), MinValueValidator(2)],
        description="Represents how many days the client is willing to train",
    )
    activity = fields.CharEnumField(
        enum_type=ClientActivityEnum,
        description="Represents how active the client is during the day",
    )
    has_injuries = fields.BooleanField(
        description="Represents whether the client has some injuries or not",
    )
    sport = fields.CharEnumField(
        enum_type=ClientFavoriteSportEnum,
        description="Represents the type of sport the client is willing to do to achieve his goals",
    )
    has_training_experience = fields.BooleanField(
        description="Represents whether the client has training experience or not"
    )
    training_experience = fields.DecimalField(
        max_digits=10,
        decimal_places=1,
        description="How many years the client has been training for",
        default=0,
    )
    fitness_level = fields.CharEnumField(
        enum_type=ClientFitnessLevelEnum,
        description="Represents the fitness level of the client",
    )

    instructions = fields.TextField()


class User(Model):
    name = fields.CharField(max_length=(64))
    email = fields.CharField(max_length=128, unique=True)
    email_verified = fields.BooleanField(default=False)
    profile = fields.ForeignKeyField(
        "models.ClientProfile", related_name="profile", null=True
    )


class Workouts(Model):
    workout = fields.JSONField()
    owner = fields.ForeignKeyField("models.User")
