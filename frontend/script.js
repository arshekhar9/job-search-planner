// API Base URL
const API_BASE = 'http://localhost:8000/api';

const COMPANY_BADGE = {
    'google_deepmind': 'badge-deepmind',
    'anthropic':       'badge-anthropic',
    'openai':          'badge-openai',
};

let allJobs = [];
let appliedJobIndices = new Set();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadJobPostings();
});

function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });
}

// ── Job Table ────────────────────────────────────────────────────────────────

async function loadJobPostings() {
    try {
        const [jobsRes, appliedRes] = await Promise.all([
            fetch(`${API_BASE}/job-search/jobs`),
            fetch(`${API_BASE}/job-search/applied`)
        ]);

        const jobsData = await jobsRes.json();
        allJobs = jobsData.jobs || [];

        const appliedData = await appliedRes.json();
        appliedJobIndices = new Set(
            appliedData.map(a => allJobs.findIndex(
                j => j.company === a.company_name && j.role === a.position_title
            ))
        );

        renderJobsTable();
        refreshOutreachPanel();
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

function renderJobsTable() {
    const tbody = document.getElementById('jobsTableBody');
    if (!tbody) return;

    tbody.innerHTML = allJobs.map((job, index) => {
        const isApplied = appliedJobIndices.has(index);
        return `
        <tr>
            <td style="color:#6c757d;font-size:0.9em;">${index + 1}</td>
            <td>
                <span class="company-badge ${COMPANY_BADGE[job.company_key] || ''}">
                    ${job.company}
                </span>
            </td>
            <td style="font-weight:600;color:#212529;">${job.role}</td>
            <td style="color:#6c757d;font-size:0.92em;">📍 ${job.location}</td>
            <td style="color:#6c757d;font-size:0.92em;">${job.type}</td>
            <td>
                <select class="status-select ${isApplied ? 'applied' : ''}"
                        onchange="handleStatusChange(${index}, this)">
                    <option value="not_applied" ${!isApplied ? 'selected' : ''}>— Not Applied</option>
                    <option value="applied" ${isApplied ? 'selected' : ''}>✓ Applied</option>
                </select>
            </td>
            <td>
                <a href="${job.url}" target="_blank" class="job-link">View Role ↗</a>
            </td>
        </tr>`;
    }).join('');
}

async function handleStatusChange(index, selectEl) {
    const job = allJobs[index];
    if (!job) return;

    if (selectEl.value === 'applied') {
        selectEl.classList.add('applied');
        appliedJobIndices.add(index);
        await fetch(`${API_BASE}/job-search/apply/${index}`, { method: 'POST' });
        await showOutreachForCompany(job.company_key, job.company, job.role);
    } else {
        selectEl.classList.remove('applied');
        appliedJobIndices.delete(index);
        refreshOutreachPanel();
    }
}

// ── Cold Outreach Panel ───────────────────────────────────────────────────────

async function showOutreachForCompany(companyKey, companyName, role) {
    try {
        const res = await fetch(`${API_BASE}/job-search/outreach/${companyKey}`);
        const data = await res.json();

        const panel = document.getElementById('outreachPanel');
        const content = document.getElementById('outreachContent');

        panel.style.display = 'block';
        panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        content.innerHTML = `
            <p style="color:#6c757d;margin-bottom:15px;font-size:0.95em;">
                Outreach templates for <strong>${companyName}</strong> — ${role}
            </p>
            <div class="outreach-tabs">
                <button class="outreach-tab-btn active"
                        onclick="switchOutreachTab(this, 'linkedin', ${JSON.stringify(data).replace(/"/g, '&quot;')})">
                    LinkedIn Message
                </button>
                <button class="outreach-tab-btn"
                        onclick="switchOutreachTab(this, 'email', ${JSON.stringify(data).replace(/"/g, '&quot;')})">
                    Email Template
                </button>
                <button class="outreach-tab-btn"
                        onclick="switchOutreachTab(this, 'tips', ${JSON.stringify(data).replace(/"/g, '&quot;')})">
                    Tips
                </button>
            </div>
            <div id="outreachBody">
                <div class="outreach-text">${data.linkedin || ''}</div>
            </div>`;
    } catch (error) {
        console.error('Error loading outreach template:', error);
    }
}

function switchOutreachTab(btn, type, data) {
    // data may arrive as a string if passed via HTML attribute
    if (typeof data === 'string') {
        try { data = JSON.parse(data); } catch (e) { return; }
    }

    document.querySelectorAll('.outreach-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const body = document.getElementById('outreachBody');
    if (type === 'linkedin') {
        body.innerHTML = `<div class="outreach-text">${data.linkedin || ''}</div>`;
    } else if (type === 'email') {
        body.innerHTML = `<div class="outreach-text">${data.email || ''}</div>`;
    } else {
        const tips = (data.tips || []).map(t => `<li>${t}</li>`).join('');
        body.innerHTML = `
            <div class="outreach-tips">
                <h4>Company-specific tips:</h4>
                <ul>${tips}</ul>
            </div>`;
    }
}

function refreshOutreachPanel() {
    if (appliedJobIndices.size === 0) {
        document.getElementById('outreachPanel').style.display = 'none';
    }
}
