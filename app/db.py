from dotenv import load_dotenv
from os import environ
from tortoise.contrib.fastapi import register_tortoise

load_dotenv()

DB_NAME = environ.get("POSTGRES_DB")
DB_USER = environ.get("POSTGRES_USER")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD")
DB_PORT = environ.get("POSTGRES_PORT")
DB_HOST = environ.get("POSTGRES_HOST")
DB_URL = f"psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def init_db(app):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
