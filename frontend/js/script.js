/**
 * Main JavaScript for HostelEase Management System
 * Handles UI interactions, modals, dark mode, tables, and dashboard
 */

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    // Initialize all modules
    initializeApp();
});

async function initializeApp() {
    // Initialize authentication
    await initAuth();

    // Initialize UI components
    initNavbar();
    initModals();
    initDarkMode();
    initSmoothScroll();
    initAnimations();

    // Initialize event listeners
    initEventListeners();

    // Load initial data if on dashboard
    if (document.getElementById('adminSection') || document.getElementById('dashboard Section')) {
        loadDashboardData();
    }
}

// ============================================
// NAVBAR FUNCTIONALITY
// ============================================

function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');

    // Navbar scroll shadow
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', () => {
            navbarMenu.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navbarToggle.contains(e.target) && !navbarMenu.contains(e.target)) {
                navbarMenu.classList.remove('active');
            }
        });
    }
}

// ============================================
// MODAL FUNCTIONALITY
// ============================================

function initModals() {
    // Close modal when clicking on overlay
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                closeModal(overlay.id.replace('Overlay', ''));
            }
        });
    });

    // Close modal with close button
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal');
            if (modal) {
                const modalId = modal.closest('.modal-overlay').id.replace('Overlay', '');
                closeModal(modalId);
            }
        });
    });
}

function openModal(modalId) {
    const overlay = document.getElementById(modalId + 'Overlay') || document.getElementById(modalId);
    if (overlay) {
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const overlay = document.getElementById(modalId + 'Overlay') || document.getElementById(modalId);
    if (overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============================================
// DARK MODE
// ============================================

function initDarkMode() {
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    // Apply saved theme
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Toggle theme
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const theme = document.documentElement.getAttribute('data-theme');
            const newTheme = theme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

// ============================================
// LOADING OVERLAY
// ============================================

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('active');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// ============================================
// TOAST NOTIFICATIONS
// ============================================

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer') || createToastContainer();

    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// ============================================
// TABLE SEARCH & FILTER
// ============================================

function initTableSearch(searchInputId, tableId) {
    const searchInput = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);

    if (!searchInput || !table) return;

    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

function filterTable(tableId, columnIndex, filterValue) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = table.querySelectorAll('tbody tr');

    rows.forEach(row => {
        if (filterValue === 'all') {
            row.style.display = '';
        } else {
            const cell = row.cells[columnIndex];
            const cellValue = cell ? cell.textContent.trim().toLowerCase() : '';
            row.style.display = cellValue === filterValue.toLowerCase() ? '' : 'none';
        }
    });
}

// ============================================
// DASHBOARD DATA LOADING
// ============================================

async function loadDashboardData() {
    try {
        showLoading();
        const stats = await dashboardAPI.getStats();
        updateDashboardStats(stats);

        // Load tables based on user role
        const user = getCurrentUser();
        if (user) {
            if (user.role === 'admin') {
                await loadAdminDashboard();
            } else if (user.role === 'warden') {
                await loadWardenDashboard();
            } else if (user.role === 'student') {
                await loadStudentDashboard();
            }
        }
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        showToast('Failed to load dashboard data', 'error');
    } finally {
        hideLoading();
    }
}

function updateDashboardStats(stats) {
    // Update stat cards with animated counters
    Object.keys(stats).forEach(key => {
        const element = document.getElementById(`stat-${key}`);
        if (element) {
            element.setAttribute('data-count', stats[key]);
            animateCounter(element, stats[key]);
        }
    });
}

async function loadAdminDashboard() {
    try {
        // Load rooms
        const rooms = await roomsAPI.getAll();
        renderRoomsTable(rooms);

        // Load students
        const students = await studentsAPI.getAll();
        renderStudentsTable(students.results || students);

        // Load fees
        const fees = await feesAPI.getAll();
        renderFeesTable(fees.results || fees);
    } catch (error) {
        console.error('Failed to load admin dashboard:', error);
    }
}

async function loadWardenDashboard() {
    try {
        // Load today's attendance
        const today = new Date().toISOString().split('T')[0];
        const attendance = await attendanceAPI.getAll({ date: today });
        renderAttendanceTable(attendance.results || attendance);

        // Load pending complaints
        const complaints = await complaintsAPI.getAll({ status: 'pending' });
        renderComplaintsTable(complaints.results || complaints);

        // Load today's visitors
        const visitors = await visitorsAPI.getAll({ today: true });
        renderVisitorsTable(visitors.results || visitors);
    } catch (error) {
        console.error('Failed to load warden dashboard:', error);
    }
}

async function loadStudentDashboard() {
    try {
        const user = getCurrentUser();

        // Load student's attendance summary
        const summary = await attendanceAPI.getSummary();
        updateAttendanceSummary(summary);

        // Load student's fees
        const fees = await feesAPI.getAll();
        renderStudentFees(fees.results || fees);

        // Load student's complaints
        const complaints = await complaintsAPI.getAll();
        renderStudentComplaints(complaints.results || complaints);

        // Load today's mess menu
        try {
            const menu = await messMenuAPI.getToday();
            renderMessMenu(menu);
        } catch (error) {
            console.log('No mess menu for today');
        }
    } catch (error) {
        console.error('Failed to load student dashboard:', error);
    }
}

// ============================================
// TABLE RENDERING FUNCTIONS
// ============================================

function renderRoomsTable(rooms) {
    const tbody = document.querySelector('#roomsTable tbody');
    if (!tbody) return;

    tbody.innerHTML = rooms.map(room => `
        <tr>
            <td>${room.room_no}</td>
            <td>${room.room_type}</td>
            <td>${room.capacity}</td>
            <td>${room.current_occupancy || 0}</td>
            <td>
                <span class="badge badge-${room.status === 'vacant' ? 'success' : room.status === 'occupied' ? 'warning' : 'danger'}">
                    ${room.status}
                </span>
            </td>
            <td class="table-actions">
                <button class="table-action-btn" onclick="editRoom(${room.id})" title="Edit">✏️</button>
                <button class="table-action-btn danger" onclick="deleteRoom(${room.id})" title="Delete">🗑️</button>
            </td>
        </tr>
    `).join('');
}

function renderStudentsTable(students) {
    const tbody = document.querySelector('#studentsTable tbody');
    if (!tbody) return;

    tbody.innerHTML = students.map(student => `
        <tr>
            <td>${student.id}</td>
            <td>${student.user?.first_name || ''} ${student.user?.last_name || ''}</td>
            <td>${student.room_details?.room_no || 'Unassigned'}</td>
            <td>${student.contact}</td>
            <td>
                <span class="badge badge-${student.is_active ? 'success' : 'secondary'}">
                    ${student.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td class="table-actions">
                <button class="table-action-btn" onclick="editStudent(${student.id})" title="Edit">✏️</button>
                <button class="table-action-btn" onclick="assignRoomToStudent(${student.id})" title="Assign Room">🏠</button>
            </td>
        </tr>
    `).join('');
}

function renderFeesTable(fees) {
    const tbody = document.querySelector('#feesTable tbody');
    if (!tbody) return;

    tbody.innerHTML = fees.map(fee => `
        <tr>
            <td>${fee.student_name || fee.student_username}</td>
            <td>$${fee.amount}</td>
            <td>${fee.due_date}</td>
            <td>
                <span class="badge badge-${fee.status === 'paid' ? 'success' : fee.status === 'overdue' ? 'danger' : 'warning'}">
                    ${fee.status}
                </span>
            </td>
            <td class="table-actions">
                ${fee.status !== 'paid' ? `<button class="btn btn-sm btn-success" onclick="markFeePaid(${fee.id})">Mark Paid</button>` : ''}
            </td>
        </tr>
    `).join('');
}

function renderAttendanceTable(records) {
    const tbody = document.querySelector('#attendanceTable tbody');
    if (!tbody) return;

    tbody.innerHTML = records.map(record => `
        <tr>
            <td>${record.student_name || record.student_username}</td>
            <td>${record.date}</td>
            <td>
                <span class="badge badge-${record.status === 'present' ? 'success' : record.status === 'absent' ? 'danger' : 'warning'}">
                    ${record.status}
                </span>
            </td>
            <td>${record.marked_by_name || ''}</td>
        </tr>
    `).join('');
}

function renderComplaintsTable(complaints) {
    const tbody = document.querySelector('#complaintsTable tbody');
    if (!tbody) return;

    tbody.innerHTML = complaints.map(complaint => `
        <tr>
            <td>${complaint.title}</td>
            <td>${complaint.student_name || ''}</td>
            <td>${complaint.category}</td>
            <td>
                <span class="badge badge-${complaint.status === 'resolved' ? 'success' : complaint.status === 'in_progress' ? 'warning' : 'danger'}">
                    ${complaint.status}
                </span>
            </td>
            <td class="table-actions">
                ${complaint.status !== 'resolved' ? `<button class="btn btn-sm btn-success" onclick="resolveComplaint(${complaint.id})">Resolve</button>` : ''}
            </td>
        </tr>
    `).join('');
}

function renderVisitorsTable(visitors) {
    const tbody = document.querySelector('#visitorsTable tbody');
    if (!tbody) return;

    tbody.innerHTML = visitors.map(visitor => `
        <tr>
            <td>${visitor.visitor_name}</td>
            <td>${visitor.student_name || ''}</td>
            <td>${visitor.purpose}</td>
            <td>${new Date(visitor.in_time).toLocaleString()}</td>
            <td>${visitor.out_time ? new Date(visitor.out_time).toLocaleString() : 'Still visiting'}</td>
        </tr>
    `).join('');
}

function renderMessMenu(menu) {
    const container = document.getElementById('messMenuContainer');
    if (!container) return;

    container.innerHTML = `
        <div class="mess-menu-card">
            <div class="menu-date">${menu.date}</div>
            <div class="menu-item">
                <div class="menu-time">Breakfast</div>
                <div class="menu-items">${menu.breakfast}</div>
            </div>
            <div class="menu-item">
                <div class="menu-time">Lunch</div>
                <div class="menu-items">${menu.lunch}</div>
            </div>
            ${menu.snacks ? `
                <div class="menu-item">
                    <div class="menu-time">Snacks</div>
                    <div class="menu-items">${menu.snacks}</div>
                </div>
            ` : ''}
            <div class="menu-item">
                <div class="menu-time">Dinner</div>
                <div class="menu-items">${menu.dinner}</div>
            </div>
        </div>
    `;
}

// ============================================
// EVENT LISTENERS
// ============================================

function initEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Complaint form
    const complaintForm = document.getElementById('complaintForm');
    if (complaintForm) {
        complaintForm.addEventListener('submit', handleComplaintSubmit);
    }

    // Contact form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }

    // Initialize table search
    initTableSearch('roomsSearch', 'roomsTable');
    initTableSearch('studentsSearch', 'studentsTable');
    initTableSearch('feesSearch', 'feesTable');
}

// ============================================
// FORM HANDLERS
// ============================================

async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        await login(username, password);
        closeModal('loginModal');

        // Reload page to show appropriate dashboard
        window.location.reload();
    } catch (error) {
        // Error already shown by login function
    }
}

async function handleComplaintSubmit(e) {
    e.preventDefault();

    const title = document.getElementById('complaintTitle').value;
    const description = document.getElementById('complaintDescription').value;
    const category = document.getElementById('complaintCategory').value;
    const priority = document.getElementById('complaintPriority').value;

    try {
        await complaintsAPI.create({
            title,
            description,
            category,
            priority
        });

        showToast('Complaint submitted successfully', 'success');
        e.target.reset();

        // Reload complaints
        const complaints = await complaintsAPI.getAll();
        renderStudentComplaints(complaints.results || complaints);
    } catch (error) {
        showToast('Failed to submit complaint', 'error');
    }
}

async function handleContactSubmit(e) {
    e.preventDefault();

    const name = document.getElementById('contactName').value;
    const email = document.getElementById('contactEmail').value;
    const role = document.getElementById('contactRole').value;
    const message = document.getElementById('contactMessage').value;

    try {
        await contactAPI.create({ name, email, role, message });
        showToast('Message sent successfully!', 'success');
        e.target.reset();
    } catch (error) {
        showToast('Failed to send message', 'error');
    }
}

// ============================================
// ACTION FUNCTIONS
// ============================================

async function markFeePaid(feeId) {
    if (!confirm('Mark this fee as paid?')) return;

    try {
        await feesAPI.markPaid(feeId, 'Cash');
        showToast('Fee marked as paid', 'success');
        loadDashboardData();
    } catch (error) {
        showToast('Failed to update fee status', 'error');
    }
}

async function resolveComplaint(complaintId) {
    const notes = prompt('Enter resolution notes:');
    if (!notes) return;

    try {
        await complaintsAPI.resolve(complaintId, notes);
        showToast('Complaint resolved', 'success');
        loadDashboardData();
    } catch (error) {
        showToast('Failed to resolve complaint', 'error');
    }
}

// Placeholder functions for CRUD operations
function editRoom(id) {
    showToast('Edit room feature - implement modal form', 'info');
}

function deleteRoom(id) {
    if (confirm('Delete this room?')) {
        showToast('Delete functionality - to be implemented', 'info');
    }
}

function editStudent(id) {
    showToast('Edit student feature - implement modal form', 'info');
}

function assignRoomToStudent(id) {
    showToast('Assign room feature - implement modal form', 'info');
}

function renderStudentFees(fees) {
    // Implementation for student fees view
    renderFeesTable(fees);
}

function renderStudentComplaints(complaints) {
    // Implementation for student complaints view
    renderComplaintsTable(complaints);
}

function updateAttendanceSummary(summary) {
    // Update attendance summary display
    const container = document.getElementById('attendanceSummary');
    if (container && summary) {
        container.innerHTML = `
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-card-title">Total Days</div>
                    <div class="info-card-value">${summary.total_days || 0}</div>
                </div>
                <div class="info-card">
                    <div class="info-card-title">Present</div>
                    <div class="info-card-value">${summary.present || 0}</div>
                </div>
                <div class="info-card">
                    <div class="info-card-title">Attendance %</div>
                    <div class="info-card-value">${summary.percentage || 0}%</div>
                </div>
            </div>
        `;
    }
}
