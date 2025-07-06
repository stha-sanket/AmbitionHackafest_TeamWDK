// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded"); // Debug check
    
    // Tab switching elements
    const loginTab = document.getElementById('loginTab');
    const signupTab = document.getElementById('signupTab');
    const loginFormDiv = document.getElementById('loginForm');
    const signupFormDiv = document.getElementById('signupForm');

    console.log("Elements found:", {loginTab, signupTab, loginFormDiv, signupFormDiv}); // Debug check

    // Initialize forms - make sure only login form is visible initially
    if (loginFormDiv && signupFormDiv) {
        loginFormDiv.classList.add('active');
        signupFormDiv.classList.remove('active');
    }

    // Tab switching function
    function switchTab(activeTab, activeForm, inactiveTab, inactiveForm) {
        console.log("Switching tabs"); // Debug check
        
        // Update tab states
        activeTab.classList.add('active');
        inactiveTab.classList.remove('active');
        
        // Hide inactive form
        inactiveForm.classList.remove('active');
        
        // Show active form with animation
        setTimeout(() => {
            activeForm.classList.add('active');
        }, 10);
    }

    // Tab event listeners
    if (loginTab && signupTab) {
        loginTab.addEventListener('click', (e) => {
            e.preventDefault();
            console.log("Login tab clicked"); // Debug check
            switchTab(loginTab, loginFormDiv, signupTab, signupFormDiv);
        });

        signupTab.addEventListener('click', (e) => {
            e.preventDefault();
            console.log("Signup tab clicked"); // Debug check
            switchTab(signupTab, signupFormDiv, loginTab, loginFormDiv);
        });
    } else {
        console.error("Tab elements not found!");
    }

    // Helper functions
    function getUsers() {
        return JSON.parse(localStorage.getItem('users')) || [];
    }

    function saveUsers(users) {
        localStorage.setItem('users', JSON.stringify(users));
    }

    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Message display
    function showMessage(messageElement, text, type = 'error') {
        messageElement.textContent = text;
        messageElement.className = `message ${type}`;
        
        // Auto-hide success messages
        if (type === 'success') {
            setTimeout(() => {
                messageElement.textContent = '';
                messageElement.className = 'message';
            }, 3000);
        }
    }

    // Button loading state
    function setButtonLoading(button, loading) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }

    // Signup form submission
    const signupForm = document.querySelector('#signupForm form');
    const signupMessage = document.getElementById('signupMessage');

    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitButton = this.querySelector('button[type="submit"]');
            const username = document.getElementById('signupUsername').value.trim();
            const email = document.getElementById('signupEmail').value.trim().toLowerCase();
            const password = document.getElementById('signupPassword').value;
            
            // Validation
            if (!username || !email || !password) {
                showMessage(signupMessage, 'Please fill in all fields.', 'error');
                return;
            }
            
            if (username.length < 3) {
                showMessage(signupMessage, 'Username must be at least 3 characters.', 'error');
                return;
            }
            
            if (!isValidEmail(email)) {
                showMessage(signupMessage, 'Please enter a valid email address.', 'error');
                return;
            }
            
            if (password.length < 6) {
                showMessage(signupMessage, 'Password must be at least 6 characters.', 'error');
                return;
            }
            
            // Simulate loading
            setButtonLoading(submitButton, true);
            
            setTimeout(() => {
                let users = getUsers();
                
                // Check if email already exists
                if (users.some(u => u.email === email)) {
                    showMessage(signupMessage, 'An account with this email already exists.', 'error');
                    setButtonLoading(submitButton, false);
                    return;
                }
                
                // Check if username already exists
                if (users.some(u => u.username.toLowerCase() === username.toLowerCase())) {
                    showMessage(signupMessage, 'Username already taken. Please choose another.', 'error');
                    setButtonLoading(submitButton, false);
                    return;
                }
                
                // Create new user
                const newUser = { 
                    username, 
                    email, 
                    password,
                    createdAt: new Date().toISOString()
                };
                
                users.push(newUser);
                saveUsers(users);
                
                showMessage(signupMessage, 'Account created successfully! Redirecting to login...', 'success');
                signupForm.reset();
                setButtonLoading(submitButton, false);
                
                // Auto-switch to login tab after successful signup
                setTimeout(() => {
                    switchTab(loginTab, loginFormDiv, signupTab, signupFormDiv);
                    document.getElementById('loginEmail').value = email;
                    document.getElementById('loginEmail').focus();
                }, 1500);
                
            }, 800); // Simulate network delay
        });
    }

    // Login form submission
    const loginForm = document.querySelector('#loginForm form');
    const loginMessage = document.getElementById('loginMessage');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitButton = this.querySelector('button[type="submit"]');
            const email = document.getElementById('loginEmail').value.trim().toLowerCase();
            const password = document.getElementById('loginPassword').value;
            
            // Validation
            if (!email || !password) {
                showMessage(loginMessage, 'Please enter both email and password.', 'error');
                return;
            }
            
            if (!isValidEmail(email)) {
                showMessage(loginMessage, 'Please enter a valid email address.', 'error');
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
                        console.log('Redirecting to patient homepage...'); // Debug log
                        window.location.href = '/patient-homepage';
                    }, 1200);
                } else {
                    showMessage(loginMessage, 'Invalid email or password. Please try again.', 'error');
                    setButtonLoading(submitButton, false);
                }
            }, 800); // Simulate network delay
        });
    }

    // Input focus effects
    document.querySelectorAll('.input-wrapper input').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.boxShadow = '0 0 0 2px rgba(25, 118, 210, 0.2)';
            this.parentElement.style.borderColor = '#1976d2';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.boxShadow = 'none';
            this.parentElement.style.borderColor = '#ddd';
        });
    });

    // Show password toggle (bonus feature)
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        const wrapper = input.parentElement;
        const toggle = document.createElement('span');
        toggle.innerHTML = '<i class="fas fa-eye"></i>';
        toggle.style.cursor = 'pointer';
        toggle.style.marginLeft = '10px';
        toggle.style.color = '#777';
        
        toggle.addEventListener('click', function() {
            if (input.type === 'password') {
                input.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                input.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
        
        wrapper.appendChild(toggle);
    });

    // Check if user is already logged in
    if (localStorage.getItem('isLoggedIn') === 'true') {
        console.log('User already logged in, redirecting...'); // Debug log
        window.location.href = '/patient-homepage';
    }

    // Auto-focus first input
    const firstInput = document.querySelector('.form-container.active input');
    if (firstInput) {
        firstInput.focus();
    }
});