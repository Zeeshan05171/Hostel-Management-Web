/**
 * Authentication Module for HostelEase
 * Handles user login, logout, session management
 */

/**
 * Current user state
 */
let currentUser = null;

/**
 * Initialize authentication
 */
async function initAuth() {
    try {
        currentUser = await authAPI.getCurrentUser();
        updateUIForUser(currentUser);
        return currentUser;
    } catch (error) {
        console.log('User not authenticated');
        currentUser = null;
        return null;
    }
}

/**
 * Login user
 * @param {string} username
 * @param {string} password
 */
async function login(username, password) {
    try {
        showLoading();
        const response = await authAPI.login(username, password);
        currentUser = response.user;
        updateUIForUser(currentUser);
        showToast('Login successful!', 'success');
        return currentUser;
    } catch (error) {
        showToast(error.message || 'Login failed', 'error');
        throw error;
    } finally {
        hideLoading();
    }
}

/**
 * Logout user
 */
async function logout() {
    try {
        await authAPI.logout();
        currentUser = null;
        updateUIForUser(null);
        showToast('Logged out successfully', 'success');
        // Redirect to home
        window.location.href = 'index.html';
    } catch (error) {
        showToast('Logout failed', 'error');
        console.error(error);
    }
}

/**
 * Register new user
 * @param {object} userData
 */
async function register(userData) {
    try {
        showLoading();
        const response = await authAPI.register(userData);
        showToast('Registration successful! Please login.', 'success');
        return response;
    } catch (error) {
        showToast(error.message || 'Registration failed', 'error');
        throw error;
    } finally {
        hideLoading();
    }
}

/**
 * Update UI based on user authentication status
 * @param {object|null} user - User object or null
 */
function updateUIForUser(user) {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const userInfo = document.getElementById('userInfo');

    if (user) {
        // User is logged in
        if (loginBtn) loginBtn.classList.add('hidden');
        if (logoutBtn) logoutBtn.classList.remove('hidden');
        if (userInfo) {
            userInfo.classList.remove('hidden');
            userInfo.textContent = `${user.first_name || user.username} (${user.role})`;
        }

        // Show/hide sections based on role
        updateRoleBasedUI(user.role);
    } else {
        // User is not logged in
        if (loginBtn) loginBtn.classList.remove('hidden');
        if (logoutBtn) logoutBtn.classList.add('hidden');
        if (userInfo) userInfo.classList.add('hidden');

        // Hide all role-specific sections
        hideAllRoleSections();
    }
}

/**
 * Show/hide UI elements based on user role
 * @param {string} role - User role (admin, warden, student)
 */
function updateRoleBasedUI(role) {
    const adminSection = document.getElementById('adminSection');
    const wardenSection = document.getElementById('wardenSection');
    const studentSection = document.getElementById('studentSection');

    // Hide all sections first
    if (adminSection) adminSection.classList.add('hidden');
    if (wardenSection) wardenSection.classList.add('hidden');
    if (studentSection) studentSection.classList.add('hidden');

    // Show relevant section
    if (role === 'admin' && adminSection) {
        adminSection.classList.remove('hidden');
    } else if (role === 'warden' && wardenSection) {
        wardenSection.classList.remove('hidden');
    } else if (role === 'student' && studentSection) {
        studentSection.classList.remove('hidden');
    }
}

/**
 * Hide all role-specific sections
 */
function hideAllRoleSections() {
    const sections = ['adminSection', 'wardenSection', 'studentSection'];
    sections.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.classList.add('hidden');
    });
}

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
function isAuthenticated() {
    return currentUser !== null;
}

/**
 * Check if user has specific role
 * @param {string} role
 * @returns {boolean}
 */
function hasRole(role) {
    return currentUser && currentUser.role === role;
}

/**
 * Get current user
 * @returns {object|null}
 */
function getCurrentUser() {
    return currentUser;
}

/**
 * Require authentication (redirect if not logged in)
 */
function requireAuth() {
    if (!isAuthenticated()) {
        showToast('Please login to access this page', 'warning');
        // Show login modal or redirect
        const loginModal = document.getElementById('loginModal');
        if (loginModal) {
            openModal('loginModal');
        }
        return false;
    }
    return true;
}

/**
 * Require specific role
 * @param {string} role
 */
function requireRole(role) {
    if (!hasRole(role)) {
        showToast('Access denied: Insufficient permissions', 'error');
        return false;
    }
    return true;
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initAuth,
        login,
        logout,
        register,
        isAuthenticated,
        hasRole,
        getCurrentUser,
        requireAuth,
        requireRole,
    };
}
