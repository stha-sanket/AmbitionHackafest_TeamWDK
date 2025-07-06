// User authentication and profile functionality
let currentUser = null;

// Initialize user data and UI on page load
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

// Update UI with user data
function updateUserInterface() {
    if (!currentUser) return;

    const avatar = document.getElementById('profileAvatar');
    const initials = getInitials(currentUser.username);
    avatar.textContent = initials;

    const welcomeTitle = document.getElementById('welcomeTitle');
    welcomeTitle.textContent = `Welcome Back, ${currentUser.username}!`;

    const profileAvatarLarge = document.querySelector('.profile-avatar-large');
    if (profileAvatarLarge) {
        profileAvatarLarge.textContent = initials;
    }

    const profileName = document.querySelector('.profile-section h2');
    if (profileName) {
        profileName.textContent = currentUser.username;
    }
}

function getInitials(username) {
    if (!username) return 'U';
    const words = username.trim().split(' ');
    return words.length === 1
        ? words[0].charAt(0).toUpperCase()
        : (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
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
        localStorage.removeItem('userProfile');
        window.location.href = '/login';
    }
}

// ✅ FIXED: Navigation with active link handling
function showSection(sectionId, event) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active'));

    // Show selected section
    document.getElementById(sectionId).classList.add('active');

    // Update nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));

    if (event && event.target) {
        event.target.closest('.nav-link').classList.add('active');
    }

    // Load section-specific data
    if (sectionId === 'icu') {
        loadICUData();
    } else if (sectionId === 'bedding') {
        loadBeddingData();
    }
}

// Chatbot functionality
function sendMessage() {
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const message = input.value.trim();

    if (message) {
        messages.innerHTML += `
            <div style="text-align: right; margin: 1rem 0;">
                <div style="background: var(--primary-color); color: white; padding: 0.75rem; border-radius: 1rem; display: inline-block; max-width: 70%;">
                    ${message}
                </div>
            </div>
        `;

        setTimeout(() => {
            messages.innerHTML += `
                <div style="text-align: left; margin: 1rem 0;">
                    <div style="background: var(--light-bg); padding: 0.75rem; border-radius: 1rem; display: inline-block; max-width: 70%;">
                        Thank you for your question about "${message}". I'm here to help with your medical inquiries. For specific medical concerns, please consult with your healthcare provider.
                    </div>
                </div>
            `;
            messages.scrollTop = messages.scrollHeight;
        }, 1000);

        input.value = '';
        messages.scrollTop = messages.scrollHeight;
    }
}

document.getElementById('chat-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// ICU Data
async function loadICUData() {
    try {
        const response = await fetch('/patients/api/icu/');
        const data = await response.json();

        if (data.success) {
            const tableBody = document.getElementById('icu-table');
            tableBody.innerHTML = '';

            data.data.forEach(bed => {
                const statusClass = bed.status === 'Available' ? 'status-available' : 'status-occupied';
                const row = `
                    <tr>
                        <td>${bed.bed_number}</td>
                        <td>${bed.room_number}</td>
                        <td><span class="status-badge ${statusClass}">${bed.status}</span></td>
                        <td>${bed.patient_name}</td>
                        <td><span class="status-badge status-stable">Stable</span></td>
                        <td>${bed.admission_date}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading ICU data:', error);
    }
}

// Bedding Data
async function loadBeddingData() {
    try {
        const response = await fetch('/patients/api/beds/');
        const data = await response.json();

        if (data.success) {
            const tableBody = document.getElementById('bedding-table');
            tableBody.innerHTML = '';

            data.data.forEach(bed => {
                const statusClass = bed.status === 'Available' ? 'status-available' : 'status-occupied';
                const row = `
                    <tr>
                        <td>${bed.bed_number}</td>
                        <td>${bed.ward_name}</td>
                        <td>${bed.room_number}</td>
                        <td><span class="status-badge ${statusClass}">${bed.status}</span></td>
                        <td>${bed.current_patient}</td>
                        <td>${bed.admission_date}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading bedding data:', error);
    }
}

// Profile data
function loadProfileFromStorage() {
    const storedProfile = localStorage.getItem('userProfile');
    if (storedProfile) {
        const profileData = JSON.parse(storedProfile);
        updateProfileDisplay(profileData);
    }
}

function updateProfileDisplay(profileData) {
    const avatar = document.getElementById('profileAvatar');
    if (profileData.name && profileData.name.trim()) {
        const initials = getInitials(profileData.name);
        avatar.textContent = initials;
    } else {
        avatar.textContent = 'U';
    }

    const welcomeTitle = document.getElementById('welcomeTitle');
    if (welcomeTitle && profileData.name && profileData.name.trim()) {
        welcomeTitle.textContent = `Welcome Back, ${profileData.name.split(' ')[0]}!`;
    }
}

// Listen for profile updates
window.addEventListener('profileUpdated', function(event) {
    updateProfileDisplay(event.detail);
});
