import secrets
import string
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUr1

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
                clicks INTEGER NOT NULL DEFAULT 0
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

init_db = create_table()

