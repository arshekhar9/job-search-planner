"""Database models for the job search planner."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Task(Base):
    """Daily task model for job search activities."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # applying, networking, learning, etc.
    date = Column(DateTime, nullable=False, index=True)
    completed = Column(Boolean, default=False)
    time_spent_minutes = Column(Integer, nullable=True)  # Time spent on task
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "date": self.date.isoformat() if self.date else None,
            "completed": self.completed,
            "time_spent_minutes": self.time_spent_minutes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class JobApplication(Base):
    """Job application tracking model."""

    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    position_title = Column(String(200), nullable=False)
    job_url = Column(Text, nullable=True)
    status = Column(String(50), default="applied")  # applied, screening, interview, etc.
    applied_date = Column(DateTime, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    salary_range = Column(String(100), nullable=True)
    location = Column(String(200), nullable=True)
    contact_person = Column(String(200), nullable=True)
    next_action = Column(Text, nullable=True)
    next_action_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "position_title": self.position_title,
            "job_url": self.job_url,
            "status": self.status,
            "applied_date": self.applied_date.isoformat() if self.applied_date else None,
            "notes": self.notes,
            "salary_range": self.salary_range,
            "location": self.location,
            "contact_person": self.contact_person,
            "next_action": self.next_action,
            "next_action_date": self.next_action_date.isoformat() if self.next_action_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DailyGoal(Base):
    """Daily goal setting model."""

    __tablename__ = "daily_goals"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, unique=True, index=True)
    applications_goal = Column(Integer, default=0)
    networking_goal = Column(Integer, default=0)
    learning_hours_goal = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "applications_goal": self.applications_goal,
            "networking_goal": self.networking_goal,
            "learning_hours_goal": self.learning_hours_goal,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
