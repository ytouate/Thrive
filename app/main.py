from fastapi import FastAPI, HTTPException, BackgroundTasks, Response, Request
from fastapi.responses import JSONResponse
from .schemas import UserEmailSchema, ClientProfileSchema
from dotenv import load_dotenv
from os import environ
from tortoise.contrib.fastapi import register_tortoise
import jwt
import json

load_dotenv()

from .utils import send_mail, ask_ai, format_prompt, encode_pyaload

DB_NAME = environ.get("POSTGRES_DB")
DB_USER = environ.get("POSTGRES_USER")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD")
DB_PORT = environ.get("POSTGRES_PORT")
DB_HOST = environ.get("POSTGRES_HOST")
BASE_URL = environ.get("BASE_URL")

DB_URL = f"psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI()

register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.post("/get-email")
async def get_email(data: UserEmailSchema, background_tasks: BackgroundTasks):
    payload = data.model_dump()
    encoded = await encode_pyaload(payload, 900)
    url = f"{BASE_URL}/verify-email/{encoded}"
    background_tasks.add_task(send_mail, payload["email"], url)
    return data


@app.get("/verify-email/{token}")
async def verify_email(token: str, response: Response):
    try:
        payload = jwt.decode(token, "secret", algorithms="HS256")
        response = JSONResponse(
            content={"detail": "your account has been verified"}, status_code=200
        )
        response.set_cookie(key="email", value=payload["email"])
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/generate")
async def get_data(data: ClientProfileSchema, request: Request):
    prompt = format_prompt(data.model_dump())
    response = await ask_ai(prompt)
    if response.ok:
        try:
            parsed_data = json.loads(response.json()["output"])
            return JSONResponse(content=parsed_data, status_code=200)
        except Exception:
            return JSONResponse(
                content={
                    "detail": "failed to generate workout",
                },
                status_code=422,
            )
    return JSONResponse(content={"detail": "an error occured"}, status_code=500)
