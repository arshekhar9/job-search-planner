"""FastAPI application for job search daily planner."""
from datetime import datetime, date
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from pathlib import Path

from database import get_db, init_db
from models import Task, JobApplication, DailyGoal, JobPosting
from config import CORS_ORIGINS, TASK_CATEGORIES, APPLICATION_STATUSES
from job_search_service import get_all_jobs, get_outreach_template

app = FastAPI(title="Job Search Daily Planner", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    date: datetime
    time_spent_minutes: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    completed: Optional[bool] = None
    time_spent_minutes: Optional[int] = None


class JobApplicationCreate(BaseModel):
    company_name: str
    position_title: str
    job_url: Optional[str] = None
    applied_date: datetime
    status: str = "applied"
    notes: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    contact_person: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[datetime] = None


class JobApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    position_title: Optional[str] = None
    job_url: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    contact_person: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[datetime] = None


class DailyGoalCreate(BaseModel):
    date: datetime
    applications_goal: int = 0
    networking_goal: int = 0
    learning_hours_goal: int = 0
    notes: Optional[str] = None


class DailyGoalUpdate(BaseModel):
    applications_goal: Optional[int] = None
    networking_goal: Optional[int] = None
    learning_hours_goal: Optional[int] = None
    notes: Optional[str] = None


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Task endpoints
@app.post("/api/tasks", response_model=dict)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """Create a new task."""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.flush()
    await db.refresh(db_task)
    return db_task.to_dict()


@app.get("/api/tasks", response_model=List[dict])
async def get_tasks(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get tasks with optional filters."""
    query = select(Task)

    if date_from:
        query = query.where(Task.date >= datetime.fromisoformat(date_from))
    if date_to:
        query = query.where(Task.date <= datetime.fromisoformat(date_to))
    if category:
        query = query.where(Task.category == category)
    if completed is not None:
        query = query.where(Task.completed == completed)

    query = query.order_by(Task.date.desc(), Task.created_at.desc())
    result = await db.execute(query)
    tasks = result.scalars().all()
    return [task.to_dict() for task in tasks]


@app.get("/api/tasks/{task_id}", response_model=dict)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific task."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@app.patch("/api/tasks/{task_id}", response_model=dict)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    """Update a task."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(task)
    return task.to_dict()


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a task."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    return {"message": "Task deleted successfully"}


# Job Application endpoints
@app.post("/api/applications", response_model=dict)
async def create_application(application: JobApplicationCreate, db: AsyncSession = Depends(get_db)):
    """Create a new job application."""
    db_application = JobApplication(**application.model_dump())
    db.add(db_application)
    await db.flush()
    await db.refresh(db_application)
    return db_application.to_dict()


@app.get("/api/applications", response_model=List[dict])
async def get_applications(
    status: Optional[str] = None,
    company: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get job applications with optional filters."""
    query = select(JobApplication)

    if status:
        query = query.where(JobApplication.status == status)
    if company:
        query = query.where(JobApplication.company_name.contains(company))

    query = query.order_by(JobApplication.applied_date.desc())
    result = await db.execute(query)
    applications = result.scalars().all()
    return [app.to_dict() for app in applications]


@app.get("/api/applications/{application_id}", response_model=dict)
async def get_application(application_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific job application."""
    result = await db.execute(select(JobApplication).where(JobApplication.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application.to_dict()


@app.patch("/api/applications/{application_id}", response_model=dict)
async def update_application(
    application_id: int,
    application_update: JobApplicationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a job application."""
    result = await db.execute(select(JobApplication).where(JobApplication.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    for field, value in application_update.model_dump(exclude_unset=True).items():
        setattr(application, field, value)

    application.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(application)
    return application.to_dict()


@app.delete("/api/applications/{application_id}")
async def delete_application(application_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a job application."""
    result = await db.execute(select(JobApplication).where(JobApplication.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    await db.delete(application)
    return {"message": "Application deleted successfully"}


# Daily Goal endpoints
@app.post("/api/goals", response_model=dict)
async def create_or_update_goal(goal: DailyGoalCreate, db: AsyncSession = Depends(get_db)):
    """Create or update daily goal."""
    goal_date = goal.date.date()
    result = await db.execute(
        select(DailyGoal).where(
            and_(
                extract('year', DailyGoal.date) == goal_date.year,
                extract('month', DailyGoal.date) == goal_date.month,
                extract('day', DailyGoal.date) == goal_date.day
            )
        )
    )
    existing_goal = result.scalar_one_or_none()

    if existing_goal:
        for field, value in goal.model_dump(exclude={'date'}).items():
            setattr(existing_goal, field, value)
        existing_goal.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(existing_goal)
        return existing_goal.to_dict()
    else:
        db_goal = DailyGoal(**goal.model_dump())
        db.add(db_goal)
        await db.flush()
        await db.refresh(db_goal)
        return db_goal.to_dict()


@app.get("/api/goals/{goal_date}", response_model=dict)
async def get_daily_goal(goal_date: str, db: AsyncSession = Depends(get_db)):
    """Get daily goal for a specific date."""
    try:
        target_date = datetime.fromisoformat(goal_date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    result = await db.execute(
        select(DailyGoal).where(
            and_(
                extract('year', DailyGoal.date) == target_date.year,
                extract('month', DailyGoal.date) == target_date.month,
                extract('day', DailyGoal.date) == target_date.day
            )
        )
    )
    goal = result.scalar_one_or_none()

    if not goal:
        # Return empty goal if not found
        return {
            "date": goal_date,
            "applications_goal": 0,
            "networking_goal": 0,
            "learning_hours_goal": 0,
            "notes": None
        }

    return goal.to_dict()


# Analytics endpoints
@app.get("/api/analytics/summary")
async def get_analytics_summary(db: AsyncSession = Depends(get_db)):
    """Get analytics summary."""
    # Total applications
    total_apps_result = await db.execute(select(func.count(JobApplication.id)))
    total_applications = total_apps_result.scalar()

    # Applications by status
    status_result = await db.execute(
        select(JobApplication.status, func.count(JobApplication.id))
        .group_by(JobApplication.status)
    )
    applications_by_status = {status: count for status, count in status_result.all()}

    # Tasks by category
    category_result = await db.execute(
        select(Task.category, func.count(Task.id))
        .group_by(Task.category)
    )
    tasks_by_category = {category: count for category, count in category_result.all()}

    # Completed tasks percentage
    total_tasks_result = await db.execute(select(func.count(Task.id)))
    total_tasks = total_tasks_result.scalar()

    completed_tasks_result = await db.execute(
        select(func.count(Task.id)).where(Task.completed == True)
    )
    completed_tasks = completed_tasks_result.scalar()

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return {
        "total_applications": total_applications,
        "applications_by_status": applications_by_status,
        "tasks_by_category": tasks_by_category,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": round(completion_rate, 2)
    }


# Configuration endpoints
@app.get("/api/config/categories")
async def get_task_categories():
    """Get available task categories."""
    return {"categories": TASK_CATEGORIES}


@app.get("/api/config/statuses")
async def get_application_statuses():
    """Get available application statuses."""
    return {"statuses": APPLICATION_STATUSES}


# Job Search endpoints

@app.get("/api/job-search/jobs")
async def get_jobs():
    """Return the curated list of product job openings."""
    return {"jobs": get_all_jobs()}


@app.get("/api/job-search/outreach/{company_key}")
async def get_outreach(company_key: str):
    """Return cold outreach templates for a given company."""
    template = get_outreach_template(company_key)
    if not template:
        raise HTTPException(status_code=404, detail="Company not found")
    return template


@app.post("/api/job-search/apply/{job_index}")
async def mark_job_applied(job_index: int, db: AsyncSession = Depends(get_db)):
    """Save an applied job to the database for tracking."""
    jobs = get_all_jobs()
    if job_index < 0 or job_index >= len(jobs):
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_index]

    # Check if already tracked
    result = await db.execute(
        select(JobPosting).where(
            and_(
                JobPosting.company_name == job["company"],
                JobPosting.position_title == job["role"]
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.is_applied = True
        existing.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(existing)
        return existing.to_dict()

    db_job = JobPosting(
        company_name=job["company"],
        position_title=job["role"],
        job_url=job["url"],
        location=job["location"],
        job_type=job["type"],
        source="Company Careers Page",
        is_applied=True,
    )
    db.add(db_job)
    await db.flush()
    await db.refresh(db_job)
    return db_job.to_dict()


@app.get("/api/job-search/applied")
async def get_applied_jobs(db: AsyncSession = Depends(get_db)):
    """Get all jobs marked as applied."""
    result = await db.execute(
        select(JobPosting).where(JobPosting.is_applied == True)
        .order_by(JobPosting.updated_at.desc())
    )
    return [p.to_dict() for p in result.scalars().all()]


# Serve frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/assets", StaticFiles(directory=frontend_path), name="frontend")

    @app.get("/")
    async def serve_frontend():
        """Serve the frontend index.html."""
        return FileResponse(frontend_path / "index.html")


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT

    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)
