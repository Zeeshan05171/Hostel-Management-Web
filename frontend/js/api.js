/**
 * API Client for HostelEase Management System
 * Handles all HTTP requests to the Django backend
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api';

/**
 * Centralized API client with error handling
 */
class APIClient {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
    }

    /**
     * Get CSRF token from cookies
     */
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Make HTTP request
     * @param {string} endpoint - API endpoint
     * @param {object} options - Fetch options
     * @returns {Promise} Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken(),
            },
            credentials: 'include', // Include cookies for session auth
        };

        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);

            // Handle 204 No Content
            if (response.status === 204) {
                return { success: true };
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.detail || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    /**
     * PATCH request
     */
    async patch(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Create global API instance
const api = new APIClient();

/**
 * Authentication API
 */
const authAPI = {
    async login(username, password) {
        return api.post('/auth/login/', { username, password });
    },

    async logout() {
        return api.post('/auth/logout/');
    },

    async register(userData) {
        return api.post('/auth/register/', userData);
    },

    async getCurrentUser() {
        return api.get('/auth/me/');
    },

    async updateProfile(data) {
        return api.put('/auth/profile/', data);
    },
};

/**
 * Rooms API
 */
const roomsAPI = {
    async getAll(params = {}) {
        return api.get('/rooms/', params);
    },

    async getById(id) {
        return api.get(`/rooms/${id}/`);
    },

    async create(data) {
        return api.post('/rooms/', data);
    },

    async update(id, data) {
        return api.put(`/rooms/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/rooms/${id}/`);
    },

    async updateStatus(id, status) {
        return api.post(`/rooms/${id}/update_status/`, { status });
    },
};

/**
 * Students API
 */
const studentsAPI = {
    async getAll(params = {}) {
        return api.get('/students/', params);
    },

    async getById(id) {
        return api.get(`/students/${id}/`);
    },

    async create(data) {
        return api.post('/students/', data);
    },

    async update(id, data) {
        return api.put(`/students/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/students/${id}/`);
    },

    async assignRoom(id, roomId) {
        return api.post(`/students/${id}/assign_room/`, { room_id: roomId });
    },
};

/**
 * Fees API
 */
const feesAPI = {
    async getAll(params = {}) {
        return api.get('/fees/', params);
    },

    async getById(id) {
        return api.get(`/fees/${id}/`);
    },

    async create(data) {
        return api.post('/fees/', data);
    },

    async update(id, data) {
        return api.put(`/fees/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/fees/${id}/`);
    },

    async markPaid(id, paymentMethod) {
        return api.post(`/fees/${id}/mark_paid/`, { payment_method: paymentMethod });
    },
};

/**
 * Attendance API
 */
const attendanceAPI = {
    async getAll(params = {}) {
        return api.get('/attendance/', params);
    },

    async getById(id) {
        return api.get(`/attendance/${id}/`);
    },

    async create(data) {
        return api.post('/attendance/', data);
    },

    async update(id, data) {
        return api.put(`/attendance/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/attendance/${id}/`);
    },

    async getSummary(studentId = null) {
        const params = studentId ? { student_id: studentId } : {};
        return api.get('/attendance/summary/', params);
    },
};

/**
 * Visitors API
 */
const visitorsAPI = {
    async getAll(params = {}) {
        return api.get('/visitors/', params);
    },

    async getById(id) {
        return api.get(`/visitors/${id}/`);
    },

    async create(data) {
        return api.post('/visitors/', data);
    },

    async update(id, data) {
        return api.put(`/visitors/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/visitors/${id}/`);
    },
};

/**
 * Complaints API
 */
const complaintsAPI = {
    async getAll(params = {}) {
        return api.get('/complaints/', params);
    },

    async getById(id) {
        return api.get(`/complaints/${id}/`);
    },

    async create(data) {
        return api.post('/complaints/', data);
    },

    async update(id, data) {
        return api.put(`/complaints/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/complaints/${id}/`);
    },

    async resolve(id, resolutionNotes) {
        return api.post(`/complaints/${id}/resolve/`, { resolution_notes: resolutionNotes });
    },
};

/**
 * Mess Menu API
 */
const messMenuAPI = {
    async getAll(params = {}) {
        return api.get('/mess-menu/', params);
    },

    async getById(id) {
        return api.get(`/mess-menu/${id}/`);
    },

    async create(data) {
        return api.post('/mess-menu/', data);
    },

    async update(id, data) {
        return api.put(`/mess-menu/${id}/`, data);
    },

    async delete(id) {
        return api.delete(`/mess-menu/${id}/`);
    },

    async getToday() {
        return api.get('/mess-menu/today/');
    },
};

/**
 * Contact Messages API
 */
const contactAPI = {
    async getAll() {
        return api.get('/contact/');
    },

    async create(data) {
        return api.post('/contact/', data);
    },
};

/**
 * Dashboard Statistics API
 */
const dashboardAPI = {
    async getStats() {
        return api.get('/dashboard/stats/');
    },
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        api,
        authAPI,
        roomsAPI,
        studentsAPI,
        feesAPI,
        attendanceAPI,
        visitorsAPI,
        complaintsAPI,
        messMenuAPI,
        contactAPI,
        dashboardAPI,
    };
}
