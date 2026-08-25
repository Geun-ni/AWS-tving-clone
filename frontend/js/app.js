/**
 * TVING 클론 - 프론트엔드 공통 JavaScript
 */

const api = {
    async get(url) {
        const response = await fetch(url, { headers: getAuthHeaders() });
        if (!response.ok) throw await response.json();
        return response.json();
    },
    async post(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw await response.json();
        return response.json();
    },
    async put(url, data) {
        const response = await fetch(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw await response.json();
        return response.json();
    },
    async delete(url) {
        const response = await fetch(url, { method: 'DELETE', headers: getAuthHeaders() });
        if (!response.ok) throw await response.json();
        return response.json();
    }
};

function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

function checkAuth() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const authButtons = document.getElementById('auth-buttons');
    const userMenu = document.getElementById('user-menu');
    const userName = document.getElementById('user-name');
    if (token && authButtons && userMenu) {
        authButtons.style.display = 'none';
        userMenu.style.display = 'flex';
        if (userName) userName.textContent = `${username}님`;
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

function requireAuth() {
    if (!localStorage.getItem('token')) {
        alert('로그인이 필요합니다.');
        window.location.href = '/pages/login.html';
        return false;
    }
    return true;
}

function getQueryParam(key) {
    return new URLSearchParams(window.location.search).get(key);
}
