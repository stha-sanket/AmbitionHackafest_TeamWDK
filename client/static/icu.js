// User authentication and profile functionality
let currentUser = null;

// ICU Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('ICU Dashboard loaded');
    
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
        // If no user data, redirect to login
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
    
    // Refresh button functionality
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            refreshData();
        });
    }
    
    // Add loading animation to cards
    addLoadingAnimations();
    
    // Load initial data from database
    loadInitialData();
    
    // Load profile on page load
    loadProfileFromStorage();
});

// Update UI with user data
function updateUserInterface() {
    if (!currentUser) return;
    
    // Update profile avatar with user initials
    const avatar = document.getElementById('profileAvatar');
    const initials = getInitials(currentUser.username);
    avatar.textContent = initials;
}

// Get initials from username
function getInitials(username) {
    if (!username) return 'U';
    
    const words = username.trim().split(' ');
    if (words.length === 1) {
        return words[0].charAt(0).toUpperCase();
    } else {
        return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
    }
}

// Toggle profile dropdown
function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('show');
}

// Logout functionality
function logout() {
    const confirmed = confirm('Are you sure you want to log out?');
    if (confirmed) {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('currentUser');
        localStorage.removeItem('userProfile'); // Clear profile data
        window.location.href = '/login';
    }
}

// Refresh ICU data
function refreshData() {
    console.log('Refreshing ICU data...');
    
    // Add loading state to refresh button
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        refreshBtn.disabled = true;
        console.log('Refresh button set to loading state');
    }
    
    // Fetch real data from API
    fetch('/api/icu-data')
        .then(response => {
            console.log('Refresh API response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Refresh API response data:', data);
            if (data.success) {
                updateICUDisplay(data.data, data.statistics);
                showNotification('Data refreshed successfully!', 'success');
                console.log('Data refreshed and displayed successfully');
            } else {
                showNotification('Failed to fetch data', 'error');
                console.error('API returned error:', data.error);
            }
        })
        .catch(error => {
            console.error('Error fetching ICU data:', error);
            showNotification('Error connecting to server', 'error');
        })
        .finally(() => {
            // Reset refresh button
            if (refreshBtn) {
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Data';
                refreshBtn.disabled = false;
                console.log('Refresh button reset to normal state');
            }
        });
}

// Update ICU display with real data
function updateICUDisplay(icuData, statistics) {
    console.log('Updating ICU display with data:', icuData);
    console.log('Statistics:', statistics);
    
    // Update statistics in header
    updateStatistics(statistics);
    
    // Update existing ICU cards with real data
    updateExistingICUCards(icuData);
}

// Update statistics in header
function updateStatistics(stats) {
    console.log('Updating statistics:', stats);
    const statItems = document.querySelectorAll('.stat-item .stat-number');
    console.log('Found stat items:', statItems.length);
    
    if (statItems.length >= 3) {
        statItems[0].textContent = stats.total;
        statItems[1].textContent = stats.occupied;
        statItems[2].textContent = stats.available;
        console.log('Statistics updated successfully');
    } else {
        console.error('Not enough stat items found');
    }
}

// Update existing ICU cards with real data
function updateExistingICUCards(icuData) {
    const icuCards = document.querySelectorAll('.icu-card');
    console.log('Found ICU cards:', icuCards.length);
    console.log('ICU data to update:', icuData);
    
    // Update cards that have corresponding data
    icuData.forEach((bed, index) => {
        if (icuCards[index]) {
            console.log(`Updating card ${index} with bed data:`, bed);
            updateSingleCard(icuCards[index], bed);
        }
    });
    
    // Hide or mark remaining cards as unavailable if no data
    for (let i = icuData.length; i < icuCards.length; i++) {
        console.log(`Marking card ${i} as unavailable`);
        markCardAsUnavailable(icuCards[i]);
    }
}

// Mark a card as unavailable (no data in database)
function markCardAsUnavailable(card) {
    // Update bed number to show it's not in database
    const unitId = card.querySelector('.unit-id');
    if (unitId) unitId.textContent = 'N/A';
    
    // Mark as available but with no data
    card.className = 'icu-card available';
    const statusBadge = card.querySelector('.status-badge');
    if (statusBadge) {
        statusBadge.className = 'status-badge available';
        const statusText = statusBadge.querySelector('span');
        const statusIcon = statusBadge.querySelector('i');
        if (statusText) statusText.textContent = 'No Data';
        if (statusIcon) statusIcon.className = 'fas fa-question-circle';
    }
    
    // Update patient information
    const patientValue = card.querySelector('.patient-info .info-row:first-child .value');
    if (patientValue) {
        patientValue.textContent = 'No data available';
        patientValue.className = 'value empty';
    }
    
    // Update condition
    const conditionValue = card.querySelector('.patient-info .info-row:last-child .value');
    if (conditionValue) {
        conditionValue.textContent = '-';
        conditionValue.className = 'value empty';
    }
    
    // Update last updated time
    const lastUpdated = card.querySelector('.last-updated span');
    if (lastUpdated) {
        lastUpdated.textContent = 'No data available';
    }
}

// Update a single ICU card with real data
function updateSingleCard(card, bed) {
    // Update bed number and room
    const unitId = card.querySelector('.unit-id');
    const roomNumber = card.querySelector('.room-number');
    if (unitId) unitId.textContent = bed.bed_number;
    if (roomNumber) roomNumber.textContent = bed.room_number;
    
    // Update status badge
    const statusBadge = card.querySelector('.status-badge');
    const statusText = statusBadge.querySelector('span');
    const statusIcon = statusBadge.querySelector('i');
    
    if (bed.is_occupied) {
        card.className = 'icu-card occupied';
        statusBadge.className = 'status-badge occupied';
        statusText.textContent = 'Occupied';
        statusIcon.className = 'fas fa-user';
    } else {
        card.className = 'icu-card available';
        statusBadge.className = 'status-badge available';
        statusText.textContent = 'Available';
        statusIcon.className = 'fas fa-bed';
    }
    
    // Update patient information
    const patientValue = card.querySelector('.patient-info .info-row:first-child .value');
    if (patientValue) {
        patientValue.textContent = bed.assigned_patient;
        if (!bed.is_occupied) {
            patientValue.className = 'value empty';
        } else {
            patientValue.className = 'value';
        }
    }
    
    // Update condition
    const conditionValue = card.querySelector('.patient-info .info-row:last-child .value');
    if (conditionValue) {
        if (bed.is_occupied) {
            conditionValue.className = 'value condition stable';
            conditionValue.innerHTML = '<i class="fas fa-check-circle"></i> Stable';
        } else {
            conditionValue.className = 'value empty';
            conditionValue.textContent = '-';
        }
    }
    
    // Update last updated time
    const lastUpdated = card.querySelector('.last-updated span');
    if (lastUpdated) {
        lastUpdated.textContent = `Last updated: ${bed.last_updated}`;
    }
}

// Load initial ICU data
function loadInitialData() {
    console.log('Loading initial ICU data...');
    fetch('/api/icu-data')
        .then(response => {
            console.log('API response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('API response data:', data);
            if (data.success) {
                updateICUDisplay(data.data, data.statistics);
            } else {
                console.error('Failed to load ICU data:', data.error);
                showNotification('Failed to load ICU data', 'error');
            }
        })
        .catch(error => {
            console.error('Error loading ICU data:', error);
            showNotification('Error connecting to server', 'error');
        });
}

// Add loading animations to cards
function addLoadingAnimations() {
    const cards = document.querySelectorAll('.icu-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--success-color)' : 'var(--primary-color)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R to refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshData();
    }
    
    // Escape to go back
    if (e.key === 'Escape') {
        window.location.href = '/patient-homepage';
    }
});

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