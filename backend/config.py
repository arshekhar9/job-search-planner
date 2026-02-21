"""Configuration settings for the job search planner."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "job_search.db"

# Database settings
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Task categories
TASK_CATEGORIES = [
    "applying",      # Submitting job applications
    "researching",   # Researching companies and opportunities
    "networking",    # Networking activities (LinkedIn, events, coffee chats)
    "learning",      # Skill development, courses, certifications
    "interview_prep", # Preparing for interviews
    "resume_cv",     # Updating resume, CV, portfolio
    "other",         # Other job search activities
]

# Application statuses
APPLICATION_STATUSES = [
    "applied",
    "screening",
    "interview_scheduled",
    "interviewed",
    "offer",
    "rejected",
    "withdrawn",
]
