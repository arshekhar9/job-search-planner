// API Base URL
const API_BASE = 'http://localhost:8000/api';

// State
let currentDate = new Date();
let tasks = [];
let applications = [];

// Category emoji map
const categoryEmojis = {
    'applying': '📝',
    'researching': '🔍',
    'networking': '🤝',
    'learning': '📚',
    'interview_prep': '💼',
    'resume_cv': '📄',
    'other': '📌'
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeDatePicker();
    initializeTabNavigation();
    initializeEventListeners();
    loadDailyData();
});

// Date Picker
function initializeDatePicker() {
    const dateInput = document.getElementById('currentDate');
    dateInput.valueAsDate = currentDate;

    dateInput.addEventListener('change', (e) => {
        currentDate = new Date(e.target.value);
        loadDailyData();
    });

    document.getElementById('todayBtn').addEventListener('click', () => {
        currentDate = new Date();
        dateInput.valueAsDate = currentDate;
        loadDailyData();
    });
}

// Tab Navigation
function initializeTabNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            // Load data when switching tabs
            if (targetTab === 'applications') {
                loadApplications();
            } else if (targetTab === 'analytics') {
                loadAnalytics();
            }
        });
    });
}

// Event Listeners
function initializeEventListeners() {
    // Goals
    document.getElementById('saveGoalsBtn').addEventListener('click', saveGoals);

    // Tasks
    document.getElementById('addTaskBtn').addEventListener('click', showTaskForm);
    document.getElementById('saveTaskBtn').addEventListener('click', saveTask);
    document.getElementById('cancelTaskBtn').addEventListener('click', hideTaskForm);

    // Quick Add Application
    document.getElementById('quickAddAppBtn').addEventListener('click', quickAddApplication);

    // Application Modal
    document.getElementById('addApplicationBtn').addEventListener('click', () => showApplicationModal());
    document.querySelector('.modal .close').addEventListener('click', hideApplicationModal);
    document.querySelector('.close-modal').addEventListener('click', hideApplicationModal);
    document.getElementById('applicationForm').addEventListener('submit', saveApplication);

    // Filters
    document.getElementById('statusFilter').addEventListener('change', loadApplications);
    document.getElementById('companyFilter').addEventListener('input', debounce(loadApplications, 500));

    // Close modal on background click
    document.getElementById('applicationModal').addEventListener('click', (e) => {
        if (e.target.id === 'applicationModal') {
            hideApplicationModal();
        }
    });
}

// Load Daily Data
async function loadDailyData() {
    await Promise.all([
        loadDailyGoals(),
        loadTasks()
    ]);
}

// Goals
async function loadDailyGoals() {
    try {
        const dateStr = currentDate.toISOString().split('T')[0];
        const response = await fetch(`${API_BASE}/goals/${dateStr}`);
        const data = await response.json();

        document.getElementById('applicationsGoal').value = data.applications_goal || 0;
        document.getElementById('networkingGoal').value = data.networking_goal || 0;
        document.getElementById('learningGoal').value = data.learning_hours_goal || 0;
        document.getElementById('goalNotes').value = data.notes || '';
    } catch (error) {
        console.error('Error loading goals:', error);
    }
}

async function saveGoals() {
    try {
        const data = {
            date: currentDate.toISOString(),
            applications_goal: parseInt(document.getElementById('applicationsGoal').value) || 0,
            networking_goal: parseInt(document.getElementById('networkingGoal').value) || 0,
            learning_hours_goal: parseInt(document.getElementById('learningGoal').value) || 0,
            notes: document.getElementById('goalNotes').value
        };

        await fetch(`${API_BASE}/goals`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        showNotification('Goals saved successfully!');
    } catch (error) {
        console.error('Error saving goals:', error);
        showNotification('Error saving goals', 'error');
    }
}

// Tasks
async function loadTasks() {
    try {
        const dateStr = currentDate.toISOString().split('T')[0];
        const startOfDay = new Date(currentDate);
        startOfDay.setHours(0, 0, 0, 0);
        const endOfDay = new Date(currentDate);
        endOfDay.setHours(23, 59, 59, 999);

        const response = await fetch(`${API_BASE}/tasks?date_from=${startOfDay.toISOString()}&date_to=${endOfDay.toISOString()}`);
        tasks = await response.json();

        renderTasks();
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function renderTasks() {
    const tasksList = document.getElementById('tasksList');

    if (tasks.length === 0) {
        tasksList.innerHTML = '<p class="empty-state">No tasks for today. Click "Add Task" to get started!</p>';
        return;
    }

    tasksList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <div class="task-info">
                <div class="task-title">${task.title}</div>
                ${task.description ? `<div class="task-description">${task.description}</div>` : ''}
                <div class="task-meta">
                    <span class="task-category">${categoryEmojis[task.category]} ${task.category.replace('_', ' ')}</span>
                    ${task.time_spent_minutes ? `<span>⏱️ ${task.time_spent_minutes} min</span>` : ''}
                </div>
            </div>
            <div class="task-actions">
                ${!task.completed ? `<button class="complete-btn" onclick="toggleTaskComplete(${task.id}, true)">✓ Complete</button>` : ''}
                <button class="delete-btn" onclick="deleteTask(${task.id})">🗑️</button>
            </div>
        </div>
    `).join('');
}

function showTaskForm() {
    document.getElementById('taskForm').style.display = 'block';
    document.getElementById('taskTitle').focus();
}

function hideTaskForm() {
    document.getElementById('taskForm').style.display = 'none';
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('taskTimeSpent').value = '';
}

async function saveTask() {
    const title = document.getElementById('taskTitle').value.trim();
    if (!title) {
        showNotification('Please enter a task title', 'error');
        return;
    }

    try {
        const data = {
            title,
            description: document.getElementById('taskDescription').value,
            category: document.getElementById('taskCategory').value,
            date: currentDate.toISOString(),
            time_spent_minutes: parseInt(document.getElementById('taskTimeSpent').value) || null
        };

        await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        hideTaskForm();
        await loadTasks();
        showNotification('Task added successfully!');
    } catch (error) {
        console.error('Error saving task:', error);
        showNotification('Error saving task', 'error');
    }
}

async function toggleTaskComplete(taskId, completed) {
    try {
        await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed })
        });

        await loadTasks();
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
        await fetch(`${API_BASE}/tasks/${taskId}`, { method: 'DELETE' });
        await loadTasks();
        showNotification('Task deleted');
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

// Quick Add Application
async function quickAddApplication() {
    const company = document.getElementById('quickCompany').value.trim();
    const position = document.getElementById('quickPosition').value.trim();

    if (!company || !position) {
        showNotification('Please enter company and position', 'error');
        return;
    }

    try {
        const data = {
            company_name: company,
            position_title: position,
            job_url: document.getElementById('quickUrl').value,
            applied_date: currentDate.toISOString(),
            status: 'applied'
        };

        await fetch(`${API_BASE}/applications`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        document.getElementById('quickCompany').value = '';
        document.getElementById('quickPosition').value = '';
        document.getElementById('quickUrl').value = '';

        showNotification('Application added successfully!');
    } catch (error) {
        console.error('Error adding application:', error);
        showNotification('Error adding application', 'error');
    }
}

// Applications
async function loadApplications() {
    try {
        const status = document.getElementById('statusFilter').value;
        const company = document.getElementById('companyFilter').value;

        let url = `${API_BASE}/applications?`;
        if (status) url += `status=${status}&`;
        if (company) url += `company=${company}`;

        const response = await fetch(url);
        applications = await response.json();

        renderApplications();
    } catch (error) {
        console.error('Error loading applications:', error);
    }
}

function renderApplications() {
    const appsList = document.getElementById('applicationsList');

    if (applications.length === 0) {
        appsList.innerHTML = '<p class="empty-state">No applications found.</p>';
        return;
    }

    appsList.innerHTML = applications.map(app => `
        <div class="application-item">
            <div class="app-header">
                <div>
                    <div class="app-title">${app.position_title}</div>
                    <div class="app-company">${app.company_name}</div>
                </div>
                <span class="app-status status-${app.status}">${app.status.replace('_', ' ')}</span>
            </div>
            <div class="app-details">
                ${app.location ? `📍 ${app.location}<br>` : ''}
                ${app.salary_range ? `💰 ${app.salary_range}<br>` : ''}
                📅 Applied: ${new Date(app.applied_date).toLocaleDateString()}<br>
                ${app.next_action ? `🎯 Next: ${app.next_action}` : ''}
                ${app.next_action_date ? ` (${new Date(app.next_action_date).toLocaleDateString()})` : ''}
            </div>
            ${app.notes ? `<div class="app-details" style="margin-top: 10px;">📝 ${app.notes}</div>` : ''}
            ${app.job_url ? `<div class="app-details"><a href="${app.job_url}" target="_blank">🔗 View Job Posting</a></div>` : ''}
            <div class="app-actions">
                <button class="edit-btn" onclick="editApplication(${app.id})">Edit</button>
                <button class="delete-btn" onclick="deleteApplication(${app.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function showApplicationModal(appData = null) {
    const modal = document.getElementById('applicationModal');
    const form = document.getElementById('applicationForm');
    const title = document.getElementById('applicationModalTitle');

    if (appData) {
        title.textContent = 'Edit Application';
        document.getElementById('appId').value = appData.id;
        document.getElementById('appCompany').value = appData.company_name;
        document.getElementById('appPosition').value = appData.position_title;
        document.getElementById('appUrl').value = appData.job_url || '';
        document.getElementById('appLocation').value = appData.location || '';
        document.getElementById('appSalary').value = appData.salary_range || '';
        document.getElementById('appStatus').value = appData.status;
        document.getElementById('appAppliedDate').value = appData.applied_date.split('T')[0];
        document.getElementById('appContact').value = appData.contact_person || '';
        document.getElementById('appNotes').value = appData.notes || '';
        document.getElementById('appNextAction').value = appData.next_action || '';
        document.getElementById('appNextActionDate').value = appData.next_action_date ? appData.next_action_date.split('T')[0] : '';
    } else {
        title.textContent = 'Add Application';
        form.reset();
        document.getElementById('appAppliedDate').valueAsDate = new Date();
    }

    modal.style.display = 'flex';
}

function hideApplicationModal() {
    document.getElementById('applicationModal').style.display = 'none';
    document.getElementById('applicationForm').reset();
}

async function saveApplication(e) {
    e.preventDefault();

    const appId = document.getElementById('appId').value;
    const data = {
        company_name: document.getElementById('appCompany').value,
        position_title: document.getElementById('appPosition').value,
        job_url: document.getElementById('appUrl').value || null,
        location: document.getElementById('appLocation').value || null,
        salary_range: document.getElementById('appSalary').value || null,
        status: document.getElementById('appStatus').value,
        applied_date: new Date(document.getElementById('appAppliedDate').value).toISOString(),
        contact_person: document.getElementById('appContact').value || null,
        notes: document.getElementById('appNotes').value || null,
        next_action: document.getElementById('appNextAction').value || null,
        next_action_date: document.getElementById('appNextActionDate').value ?
            new Date(document.getElementById('appNextActionDate').value).toISOString() : null
    };

    try {
        if (appId) {
            await fetch(`${API_BASE}/applications/${appId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            await fetch(`${API_BASE}/applications`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        hideApplicationModal();
        await loadApplications();
        showNotification('Application saved successfully!');
    } catch (error) {
        console.error('Error saving application:', error);
        showNotification('Error saving application', 'error');
    }
}

async function editApplication(appId) {
    try {
        const response = await fetch(`${API_BASE}/applications/${appId}`);
        const appData = await response.json();
        showApplicationModal(appData);
    } catch (error) {
        console.error('Error loading application:', error);
    }
}

async function deleteApplication(appId) {
    if (!confirm('Are you sure you want to delete this application?')) return;

    try {
        await fetch(`${API_BASE}/applications/${appId}`, { method: 'DELETE' });
        await loadApplications();
        showNotification('Application deleted');
    } catch (error) {
        console.error('Error deleting application:', error);
    }
}

// Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/analytics/summary`);
        const data = await response.json();

        document.getElementById('totalApps').textContent = data.total_applications;
        document.getElementById('totalTasks').textContent = data.total_tasks;
        document.getElementById('completionRate').textContent = `${data.completion_rate}%`;

        // Status breakdown
        const statusBreakdown = document.getElementById('statusBreakdown');
        statusBreakdown.innerHTML = Object.entries(data.applications_by_status || {})
            .map(([status, count]) => `
                <div class="breakdown-item">
                    <span>${status.replace('_', ' ')}</span>
                    <strong>${count}</strong>
                </div>
            `).join('') || '<p class="empty-state">No data</p>';

        // Category breakdown
        const categoryBreakdown = document.getElementById('categoryBreakdown');
        categoryBreakdown.innerHTML = Object.entries(data.tasks_by_category || {})
            .map(([category, count]) => `
                <div class="breakdown-item">
                    <span>${categoryEmojis[category]} ${category.replace('_', ' ')}</span>
                    <strong>${count}</strong>
                </div>
            `).join('') || '<p class="empty-state">No data</p>';
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Utilities
function showNotification(message, type = 'success') {
    // Simple alert for now - could be enhanced with a toast notification
    alert(message);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
