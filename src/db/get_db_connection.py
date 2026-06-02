import os
import psycopg2

from fastapi import HTTPException

def get_db_connection():
    host = os.getenv("POSTGRES_HOST", "postgres")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    if not database or not user or not password:
        raise HTTPException(status_code=500, detail="Missing PostgreSQL configuration")

    try:
        return psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=5432,
        )
    except psycopg2.Error as exc:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}") from exc