# 📋 Job Search Daily Planner

A web-based daily planner designed specifically for managing your job search activities. Track applications, plan daily tasks, set goals, and monitor your progress all in one place.

## ✨ Features

### 📅 Daily Planning
- **Date-based task management** - Organize tasks by day
- **Task categories** - Applying, researching, networking, learning, interview prep, resume/CV work
- **Time tracking** - Record time spent on each task
- **Task completion** - Mark tasks as complete and track your progress

### 🎯 Daily Goals
- Set daily targets for applications, networking activities, and learning hours
- Add notes and focus areas for each day
- Track your progress against your goals

### 💼 Job Application Tracker
- **Comprehensive tracking** - Company, position, salary, location, and more
- **Status management** - Track applications through the entire process (applied, screening, interview, offer, etc.)
- **Next actions** - Never forget follow-ups with reminders
- **Contact tracking** - Store contact person information
- **Notes** - Keep detailed notes for each application

### 📊 Analytics Dashboard
- View total applications and tasks
- Track completion rates
- See breakdowns by application status
- Analyze tasks by category
- Monitor your job search activity over time

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **uv** (Python package manager) - [Install here](https://astral.sh/uv/install.sh)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd job-search-planner
   ```

2. **Run the application:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   The script will:
   - Check for UV installation
   - Create a `.env` file from the example
   - Install all dependencies
   - Start the server

3. **Access the application:**
   - **Web Interface:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs

### Manual Setup

If you prefer to set things up manually:

```bash
cd backend

# Create environment file
cp .env.example .env

# Install dependencies
uv sync

# Run the server
uv run uvicorn app:app --reload --port 8000
```

## 📖 How to Use

### 1. Set Daily Goals
Start each day by setting your goals:
- How many applications do you want to submit?
- How many networking activities will you do?
- How many hours will you spend learning?
- Add any notes about your focus for the day

### 2. Plan Your Tasks
Click "Add Task" to create tasks for the day:
- Choose a category (applying, networking, learning, etc.)
- Add a title and description
- Track time spent on each task
- Mark tasks complete as you finish them

### 3. Track Applications
When you apply for a job:
- Use "Quick Add Application" on the Daily Plan tab, OR
- Go to the Applications tab and click "Add Application" for more details
- Update the status as you progress through the interview process
- Add notes, contact information, and next actions

### 4. Monitor Progress
Check the Analytics tab to see:
- Total applications submitted
- Tasks completed
- Completion rates
- Application statuses
- Activity by category

## 🏗️ Technical Architecture

### Backend
- **Framework:** FastAPI (async)
- **Database:** SQLite with SQLAlchemy (async)
- **API:** RESTful with automatic OpenAPI documentation

### Frontend
- **Pure vanilla JavaScript** - No framework dependencies
- **Responsive design** - Works on desktop and mobile
- **Clean, modern UI** - Easy to use and navigate

### Data Models

**Tasks**
- Title, description, category
- Date, completion status
- Time tracking

**Job Applications**
- Company, position, URL
- Status tracking
- Applied date, next action date
- Contact person, notes
- Salary range, location

**Daily Goals**
- Applications goal
- Networking goal
- Learning hours goal
- Daily notes

## 🎨 Customization

### Change Port
Edit `backend/.env`:
```env
API_PORT=8080
```

### CORS Configuration
To allow only specific origins:
```env
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## 📁 Project Structure

```
job-search-planner/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── models.py           # Database models
│   ├── database.py         # Database configuration
│   ├── config.py           # Application settings
│   ├── pyproject.toml      # Dependencies
│   ├── .env.example        # Environment template
│   └── .gitignore
├── frontend/
│   ├── index.html          # Main HTML
│   ├── style.css           # Styling
│   └── script.js           # JavaScript logic
├── docs/                   # Documentation (optional)
├── run.sh                  # Startup script
└── README.md
```

## 🔧 API Endpoints

### Tasks
- `GET /api/tasks` - Get tasks (with filters)
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get specific task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Applications
- `GET /api/applications` - Get applications (with filters)
- `POST /api/applications` - Create application
- `GET /api/applications/{id}` - Get specific application
- `PATCH /api/applications/{id}` - Update application
- `DELETE /api/applications/{id}` - Delete application

### Goals
- `GET /api/goals/{date}` - Get daily goal
- `POST /api/goals` - Create/update daily goal

### Analytics
- `GET /api/analytics/summary` - Get analytics summary

### Configuration
- `GET /api/config/categories` - Get task categories
- `GET /api/config/statuses` - Get application statuses

Full API documentation available at http://localhost:8000/docs

## 🛠️ Development

### Database
The SQLite database (`job_search.db`) is created automatically on first run. It's stored in the `backend/` directory.

### Reset Database
To start fresh, simply delete the database file:
```bash
rm backend/job_search.db
```

The database will be recreated on next startup.

## 📝 Tips for Effective Job Searching

1. **Set realistic daily goals** - Start small and build up
2. **Track everything** - Even rejected applications are progress
3. **Review analytics weekly** - Identify patterns and adjust strategy
4. **Use categories effectively** - Balance different types of activities
5. **Update application statuses** - Keep your pipeline current
6. **Add detailed notes** - Your future self will thank you

## 🤝 Contributing

This is a personal project, but feel free to fork and customize for your own needs!

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🆘 Troubleshooting

### UV not found
Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Port already in use
Change the port in `backend/.env`:
```env
API_PORT=8001
```

### Database errors
Delete and recreate:
```bash
rm backend/job_search.db
./run.sh
```

### Frontend not loading
Make sure you're accessing the root URL:
- ✅ http://localhost:8000
- ❌ http://localhost:8000/frontend

---

**Good luck with your job search! 🎯**

Remember: Job searching is a marathon, not a sprint. This tool is here to help you stay organized and motivated throughout your journey.
