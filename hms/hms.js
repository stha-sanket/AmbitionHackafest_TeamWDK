// Tab switching with enhanced animation
const loginTab = document.getElementById('loginTab');
const signupTab = document.getElementById('signupTab');
const loginFormDiv = document.getElementById('loginForm');
const signupFormDiv = document.getElementById('signupForm');

// Enhanced tab switching with animations
function switchTab(activeTab, activeForm, inactiveTab, inactiveForm) {
    // Update tab states
    activeTab.classList.add('active');
    inactiveTab.classList.remove('active');
    
    // Animate form transition
    inactiveForm.style.opacity = '0';
    inactiveForm.style.transform = 'translateX(-20px)';
    
    setTimeout(() => {
        inactiveForm.classList.remove('active');
        activeForm.classList.add('active');
        activeForm.style.opacity = '0';
        activeForm.style.transform = 'translateX(20px)';
        
        // Animate in the new form
        requestAnimationFrame(() => {
            activeForm.style.opacity = '1';
            activeForm.style.transform = 'translateX(0)';
        });
    }, 150);
}

loginTab.addEventListener('click', () => {
    switchTab(loginTab, loginFormDiv, signupTab, signupFormDiv);
});

signupTab.addEventListener('click', () => {
    switchTab(signupTab, signupFormDiv, loginTab, loginFormDiv);
});

// Helper functions
function getUsers() {
    return JSON.parse(localStorage.getItem('users') || '[]');
}

function saveUsers(users) {
    localStorage.setItem('users', JSON.stringify(users));
}

// Enhanced message display
function showMessage(messageElement, text, type = 'error') {
    messageElement.textContent = text;
    messageElement.className = `message ${type}`;
    messageElement.style.opacity = '0';
    messageElement.style.transform = 'translateY(-10px)';
    
    requestAnimationFrame(() => {
        messageElement.style.opacity = '1';
        messageElement.style.transform = 'translateY(0)';
    });
    
    // Auto-hide success messages
    if (type === 'success') {
        setTimeout(() => {
            messageElement.style.opacity = '0';
            setTimeout(() => {
                messageElement.textContent = '';
                messageElement.className = 'message';
            }, 300);
        }, 3000);
    }
}

// Enhanced button loading state
function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Enhanced signup logic with better UX
const signupForm = signupFormDiv.querySelector('form');
const signupMessage = document.getElementById('signupMessage');

signupForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const submitButton = this.querySelector('button[type="submit"]');
    const username = document.getElementById('signupUsername').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    
    // Basic validation
    if (!username || !email || !password) {
        showMessage(signupMessage, 'Please fill in all fields.', 'error');
        return;
    }
    
    if (password.length < 6) {
        showMessage(signupMessage, 'Password must be at least 6 characters long.', 'error');
        return;
    }
    
    // Simulate loading
    setButtonLoading(submitButton, true);
    
    setTimeout(() => {
        let users = getUsers();
        
        if (users.find(u => u.email === email)) {
            showMessage(signupMessage, 'An account with this email already exists.', 'error');
            setButtonLoading(submitButton, false);
            return;
        }
        
        // Create new user
        users.push({ username, email, password });
        saveUsers(users);
        
        showMessage(signupMessage, 'Account created successfully! You can now log in.', 'success');
        signupForm.reset();
        setButtonLoading(submitButton, false);
        
        // Auto-switch to login tab after successful signup
        setTimeout(() => {
            switchTab(loginTab, loginFormDiv, signupTab, signupFormDiv);
        }, 2000);
        
    }, 1000); // Simulate network delay
});

// Enhanced login logic with better UX
const loginForm = loginFormDiv.querySelector('form');
const loginMessage = document.getElementById('loginMessage');

loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const submitButton = this.querySelector('button[type="submit"]');
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    // Basic validation
    if (!email || !password) {
        showMessage(loginMessage, 'Please enter both email and password.', 'error');
        return;
    }
    
    // Simulate loading
    setButtonLoading(submitButton, true);
    
    setTimeout(() => {
        const users = getUsers();
        const user = users.find(u => u.email === email && u.password === password);
        
        if (user) {
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('currentUser', JSON.stringify(user));
            showMessage(loginMessage, 'Login successful! Redirecting...', 'success');
            
            // Redirect after success message
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
        } else {
            showMessage(loginMessage, 'Invalid email or password. Please try again.', 'error');
            setButtonLoading(submitButton, false);
        }
    }, 1000); // Simulate network delay
});

// Input focus animations
document.querySelectorAll('.input-wrapper input').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Initialize form animations
document.addEventListener('DOMContentLoaded', function() {
    // Set initial form styles for animation
    const forms = document.querySelectorAll('.form-container');
    forms.forEach(form => {
        form.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    });
    
    // Add entrance animation to auth card
    const authCard = document.querySelector('.auth-card');
    if (authCard) {
        authCard.style.opacity = '0';
        authCard.style.transform = 'translateY(20px)';
        
        requestAnimationFrame(() => {
            authCard.style.opacity = '1';
            authCard.style.transform = 'translateY(0)';
        });
    }
});

// Enhanced form validation feedback
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', function() {
        // Remove error styling when user starts typing
        if (this.classList.contains('error')) {
            this.classList.remove('error');
        }
    });
    
    input.addEventListener('invalid', function() {
        this.classList.add('error');
    });
});
