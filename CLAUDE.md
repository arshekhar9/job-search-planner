# CLAUDE.md

This file provides guidance to Claude Code when working with the Job Search Daily Planner codebase.

## Development Commands

**Start the application:**
```bash
chmod +x run.sh
./run.sh
```

**Manual start:**
```bash
cd backend
uv run uvicorn app:app --reload --port 8000
```

**Install dependencies:**
```bash
cd backend
uv sync
```

**Environment setup:**
Create `backend/.env` file with:
```
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*
ENVIRONMENT=development
```

**Access points:**
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Architecture Overview

This is a **job search daily planner** web application with a FastAPI backend and vanilla JavaScript frontend.

### Core Components

**app.py** - FastAPI application with REST endpoints:
- Task management (CRUD operations)
- Job application tracking (CRUD operations)
- Daily goals management
- Analytics and reporting
- Serves static frontend files

**models.py** - SQLAlchemy database models:
- `Task`: Daily tasks with categories, completion status, time tracking
- `JobApplication`: Job application tracking with status pipeline
- `DailyGoal`: Daily goal setting for applications, networking, learning

**database.py** - Async SQLAlchemy setup:
- SQLite with aiosqlite
- Async session management
- Database initialization

**config.py** - Configuration settings:
- Task categories (applying, researching, networking, learning, etc.)
- Application statuses (applied, screening, interview, offer, etc.)
- API settings

### Frontend Structure

**index.html** - Single-page application with tabs:
- Daily Plan tab (goals, tasks, quick add)
- Applications tab (full application management)
- Analytics tab (progress tracking)

**style.css** - Modern, responsive design:
- Gradient purple theme
- Card-based layouts
- Mobile-friendly responsive grid
- Modal dialogs

**script.js** - Vanilla JavaScript:
- API communication
- Dynamic rendering
- Form handling
- Tab navigation
- Real-time updates

### Data Flow

1. **User Input** → Frontend form submission
2. **API Call** → Fetch request to FastAPI endpoint
3. **Database** → SQLAlchemy async operations
4. **Response** → JSON data back to frontend
5. **Render** → Dynamic DOM updates

### Key Features

- **Date-based planning**: Tasks and goals organized by date
- **Category tracking**: Tasks categorized by job search activity type
- **Status pipeline**: Applications tracked through hiring process
- **Time tracking**: Record time spent on tasks
- **Analytics**: Summary statistics and breakdowns
- **Quick actions**: Fast task and application entry

## Database Schema

**tasks table:**
- id, title, description, category
- date, completed, time_spent_minutes
- created_at, updated_at

**job_applications table:**
- id, company_name, position_title, job_url
- status, applied_date, location, salary_range
- contact_person, notes, next_action, next_action_date
- created_at, updated_at

**daily_goals table:**
- id, date (unique)
- applications_goal, networking_goal, learning_hours_goal
- notes, created_at, updated_at

## Important Notes

- **Always use `uv`** for Python package management and running scripts
- **No pip directly** - UV handles all dependency management
- **Database is SQLite** - File-based, auto-created on first run
- **Async everywhere** - All database operations are async
- **CORS enabled** - Configured for development (can be restricted)
- **No authentication** - This is a personal tool (add auth if deploying publicly)

## Common Tasks

### Add a new task category:
1. Update `TASK_CATEGORIES` in `config.py`
2. Update category select in `index.html`
3. Add emoji mapping in `script.js` categoryEmojis

### Add a new application status:
1. Update `APPLICATION_STATUSES` in `config.py`
2. Update status select options in `index.html`
3. Add CSS class in `style.css` (e.g., `.status-newstatus`)

### Add a new API endpoint:
1. Define Pydantic models in `app.py` (if needed)
2. Create endpoint function with proper async/await
3. Add database query using SQLAlchemy
4. Update frontend to call new endpoint

## Testing and Development

- No test framework currently configured
- Manual testing via the web interface
- API testing via `/docs` (Swagger UI)
- Database can be reset by deleting `backend/job_search.db`

## Future Enhancement Ideas

- User authentication and multi-user support
- Email reminders for next actions
- Calendar integration
- Export to CSV/PDF
- Mobile app version
- Interview prep notes and questions
- Networking contact management
- Resume version tracking

When making changes, maintain the clean separation between frontend and backend, and ensure all database operations remain async.
