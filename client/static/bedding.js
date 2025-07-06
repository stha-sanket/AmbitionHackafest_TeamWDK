// User authentication and profile functionality for Bedding page
let currentUser = null;

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    if (localStorage.getItem('isLoggedIn') !== 'true') {
        window.location.href = '/login';
        return;
    }
    // Load current user data
    const userData = localStorage.getItem('currentUser');
    if (userData) {
        currentUser = JSON.parse(userData);
        updateUserInterface();
    } else {
        window.location.href = '/login';
        return;
    }
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const dropdown = document.getElementById('profileDropdown');
        const avatar = document.getElementById('profileAvatar');
        if (!avatar.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    });
    loadProfileFromStorage();
});

function updateUserInterface() {
    if (!currentUser) return;
    // Update profile avatar with user initials
    const avatar = document.getElementById('profileAvatar');
    const initials = getInitials(currentUser.username);
    avatar.textContent = initials;
}

function getInitials(username) {
    if (!username) return 'U';
    const words = username.trim().split(' ');
    if (words.length === 1) {
        return words[0].charAt(0).toUpperCase();
    } else {
        return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
    }
}

function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('show');
}

function logout() {
    const confirmed = confirm('Are you sure you want to log out?');
    if (confirmed) {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('currentUser');
        localStorage.removeItem('userProfile'); // Clear profile data
        window.location.href = '/login';
    }
}

// Profile synchronization functions
function loadProfileFromStorage() {
    const storedProfile = localStorage.getItem('userProfile');
    if (storedProfile) {
        const profileData = JSON.parse(storedProfile);
        updateProfileDisplay(profileData);
    }
}

function updateProfileDisplay(profileData) {
    // Update profile avatar
    const avatar = document.getElementById('profileAvatar');
    if (profileData.name && profileData.name.trim()) {
        const initials = getInitials(profileData.name);
        avatar.textContent = initials;
    } else {
        avatar.textContent = 'U';
    }
}

// Listen for profile updates from other pages
window.addEventListener('profileUpdated', function(event) {
    updateProfileDisplay(event.detail);
}); 