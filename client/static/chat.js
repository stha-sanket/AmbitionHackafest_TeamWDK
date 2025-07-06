// User authentication and profile functionality
let currentUser = null;

// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Chat page loaded');
    
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
    
    // Initialize chat functionality
    initializeChat();

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

// Initialize chat functionality
function initializeChat() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');

    // Load initial chat history from server
    loadChatHistory();

    async function loadChatHistory() {
        try {
            const response = await fetch('/api/get_chat_history');
            if (response.ok) {
                const messages = await response.json();
                if (messages.length > 0) {
                    // Add welcome message only if no history exists
                    addWelcomeMessage();

                    // Add all messages from history
                    messages.forEach((msg) => {
                        addMessageToChat('user', msg.user_query);
                        addMessageToChat('bot', msg.ai_response);
                    });
                } else {
                    // No history - show welcome message
                    addWelcomeMessage();
                }
            } else {
                console.error('Failed to load chat history');
                addWelcomeMessage();
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
            addWelcomeMessage();
        }
    }

    function addWelcomeMessage() {
        const welcomeMessage = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p>👋 Hello! I'm HMS AI Assistant, your medical information assistant.</p>
                        <p>You can ask me about:</p>
                        <ul>
                            <li>Disease symptoms and causes</li>
                            <li>Diagnosis and treatment options</li>
                            <li>Prevention strategies</li>
                            <li>When to see a doctor</li>
                        </ul>
                        <p><strong>Remember:</strong> I provide general information only. Always consult a healthcare professional for medical advice.</p>
                    </div>
                </div>
            </div>`;
        chatMessages.innerHTML += welcomeMessage;
        scrollToBottom();
    }

    // Function to convert Markdown to HTML
    function renderMarkdown(markdown) {
        const rawHTML = marked.parse(markdown);
        return DOMPurify.sanitize(rawHTML);
    }

    function createTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-animation">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                </div>
            </div>
        `;
        return typingDiv;
    }

    function addMessageToChat(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        const time = new Date().toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });

        if (type === 'user') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-bubble">
                        <p>${content}</p>
                    </div>
                    <div class="message-time">${time}</div>
                </div>
                <div class="message-avatar">
                    <i class="fas fa-user"></i>
                </div>
            `;
        } else {
            // Convert markdown to HTML for bot messages
            const htmlContent = renderMarkdown(content);

            messageDiv.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="markdown-content">${htmlContent}</div>
                    </div>
                    <div class="message-time">${time}</div>
                </div>
            `;
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Send message function
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        addMessageToChat('user', message);
        messageInput.value = '';
        messageInput.style.height = 'auto';

        const typingIndicator = createTypingIndicator();
        chatMessages.appendChild(typingIndicator);
        scrollToBottom();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ user_message: message })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            const data = await response.json();
            chatMessages.removeChild(typingIndicator);

            if (data.error) {
                addMessageToChat('bot', data.error);
            } else {
                addMessageToChat('bot', data.response);
            }
        } catch (error) {
            chatMessages.removeChild(typingIndicator);
            addMessageToChat('bot', error.message || 'Sorry, there was an error processing your request.');
            console.error('Error:', error);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // Clear chat functionality
    const clearChatBtn = document.getElementById('clearChatBtn');
    clearChatBtn.addEventListener('click', clearChatHistory);

    async function clearChatHistory() {
        const confirmed = confirm('Are you sure you want to clear the chat history? This action cannot be undone.');
        if (!confirmed) return;

        try {
            // Clear chat history from server
            const response = await fetch('/api/clear_history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Clear the chat messages container
                chatMessages.innerHTML = '';
                
                // Show welcome message again
                addWelcomeMessage();
                
                console.log('Chat history cleared successfully');
            } else {
                console.error('Failed to clear chat history from server');
                // Still clear the UI even if server request fails
                chatMessages.innerHTML = '';
                addWelcomeMessage();
            }
        } catch (error) {
            console.error('Error clearing chat history:', error);
            // Clear the UI even if there's an error
            chatMessages.innerHTML = '';
            addWelcomeMessage();
        }
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