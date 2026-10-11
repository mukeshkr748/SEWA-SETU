from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="Sewa Setu API",
    description="A platform to report and track civic issues",
    version="1.0.0"
)

DATABASE = "sewa_setu.db"


class Complaint(BaseModel):
    name: str
    category: str
    description: str
    location: str


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.get("/")
def home():
    return {
        "message": "Welcome to Sewa Setu!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Sewa Setu"
    }


@app.post("/complaints")
def create_complaint(complaint: Complaint):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO complaints (name, category, description, location)
        VALUES (?, ?, ?, ?)
        """,
        (
            complaint.name,
            complaint.category,
            complaint.description,
            complaint.location
        )
    )

    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "message": "Complaint submitted successfully!",
        "complaint_id": complaint_id,
        "status": "registered"
    }


@app.get("/complaints")
def get_complaints():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    rows = cursor.fetchall()

    complaints = [dict(row) for row in rows]
    conn.close()

    return {
        "total": len(complaints),
        "complaints": complaints
    }
