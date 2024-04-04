from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
import requests
import json
from os import environ
from datetime import datetime, timezone, timedelta
import jwt

EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD")
EMAIL_USER = environ.get("EMAIL_USER")

conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USER,
    MAIL_PASSWORD=EMAIL_PASSWORD,
    MAIL_FROM=EMAIL_USER,
    MAIL_PORT=465,
    MAIL_SERVER=EMAIL_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_mail(email: str, url):
    html = f"""
        <h1>Hello</h1>
        <p>please click the following <a href={url}>link</a> to verify your email
    """
    message = MessageSchema(
        subject="Thrive Email Verification",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def ask_ai(prompt):
    url = "https://promptify.adtitan.io/api/meta/templates/894/execute_sync/"

    payload = json.dumps(
        {"contextual_overrides": [], "prompt_params": {"context": prompt}}
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token a78a2818d855cad5295a38df22c62d643b46401c",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def format_prompt(user_data):
    prompt = f"""
        Generate Custom Workout Routine for a client with the following data

        Fitness Goal: {user_data["fitness_goal"]}

        Training Days: the client are willing to train {user_data["training_days"]} per week so the program should include {user_data["training_days"]} workouts

        Activity Level: the client activity level is {user_data["activity"]}

        Sport: {"Bodybuilding so feel free to include any gym exercices" if {user_data["sport"] == "Weight Lifting"} else "Calisthenics so you should only include body weight exercices"}

        Experience Level: { " The client has some training experience " if user_data["has_training_experience"] else " the client has no training experience"}
    
        Fitness Level: the client has {user_data["fitness_level"]} fitness level

        Preparing For: False

        Injuries/Limitations: False

    """
    return prompt


async def encode_pyaload(payload: dict, exp: int):
    expiry = {"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=exp)}
    payload.update(expiry)
    encoded = jwt.encode(payload, "secret")
    return encoded
