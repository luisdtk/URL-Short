import secrets
import string
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI()

DB_PATH = "urls.db"
ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6 

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

init_db = create_table()

class ShortRequest(BaseModel):
    original_url: HttpUrl

def generate_code():
    return ''.join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))

@app.get("/shorten")
def home():
    return {"message": "Welcome to the URL Shortener API!"}

@app.post("/shorten")
def shorten_url(request: ShortRequest):
    code = generate_code()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (code, original_url) VALUES (?, ?)",
            (code, request.original_url)
        )
        conn.commit()
    return {"shortened_url": f"http://localhost:8000/{code}"}  

