// Check authentication
if (localStorage.getItem('isLoggedIn') !== 'true') {
    window.location.href = 'hms.html';
}

// Get current user info
const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');

// Enhanced content map with detailed sections
const contentMap = {
    main: {
        title: 'Dashboard',
        subtitle: 'Welcome to your healthcare management portal',
        content: `
            <div class="dashboard-grid fade-in">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Total Patients</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #4CAF50, #45a049);">
                            <i class="fas fa-users"></i>
                        </div>
                    </div>
                    <div class="card-value">1,247</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">+12% from last month</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Available Beds</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #2196F3, #1976D2);">
                            <i class="fas fa-bed"></i>
                        </div>
                    </div>
                    <div class="card-value">89</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">Available now</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">ICU Occupancy</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF9800, #F57C00);">
                            <i class="fas fa-procedures"></i>
                        </div>
                    </div>
                    <div class="card-value">78%</div>
                    <div class="card-description">
                        <span class="status-indicator status-occupied">22 of 28 beds</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Staff on Duty</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2);">
                            <i class="fas fa-user-md"></i>
                        </div>
                    </div>
                    <div class="card-value">156</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">85 doctors, 71 nurses</span>
                    </div>
                </div>
            </div>
            
            <div class="data-table fade-in">
                <h3 style="padding: 1.5rem 1.5rem 0; color: #334155; font-size: 1.25rem; font-weight: 600;">Recent Activities</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Activity</th>
                            <th>Department</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>10:30 AM</td>
                            <td>Patient admission - John Doe</td>
                            <td>Emergency</td>
                            <td><span class="status-indicator status-available">Completed</span></td>
                        </tr>
                        <tr>
                            <td>10:15 AM</td>
                            <td>Surgery scheduled - Jane Smith</td>
                            <td>OR-3</td>
                            <td><span class="status-indicator status-occupied">In Progress</span></td>
                        </tr>
                        <tr>
                            <td>09:45 AM</td>
                            <td>Medicine restocked</td>
                            <td>Pharmacy</td>
                            <td><span class="status-indicator status-available">Completed</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `
    },
    icu: {
        title: 'ICU Management',
        subtitle: 'Intensive Care Unit monitoring and updates',
        content: `
            <div class="dashboard-grid fade-in">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">ICU Beds Total</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF5722, #D84315);">
                            <i class="fas fa-procedures"></i>
                        </div>
                    </div>
                    <div class="card-value">28</div>
                    <div class="card-description">Critical care units</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Occupied</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF9800, #F57C00);">
                            <i class="fas fa-bed"></i>
                        </div>
                    </div>
                    <div class="card-value">22</div>
                    <div class="card-description">
                        <span class="status-indicator status-occupied">78% occupancy</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Available</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #4CAF50, #388E3C);">
                            <i class="fas fa-check-circle"></i>
                        </div>
                    </div>
                    <div class="card-value">6</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">Ready for admission</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Critical Patients</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #F44336, #C62828);">
                            <i class="fas fa-exclamation-triangle"></i>
                        </div>
                    </div>
                    <div class="card-value">8</div>
                    <div class="card-description">
                        <span class="status-indicator status-critical">Requires immediate attention</span>
                    </div>
                </div>
            </div>
            
            <div class="data-table fade-in">
                <h3 style="padding: 1.5rem 1.5rem 0; color: #334155; font-size: 1.25rem; font-weight: 600;">ICU Patient Status</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Bed No.</th>
                            <th>Patient Name</th>
                            <th>Condition</th>
                            <th>Admitted</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>ICU-01</td>
                            <td>Robert Johnson</td>
                            <td>Post-surgery recovery</td>
                            <td>2 days ago</td>
                            <td><span class="status-indicator status-available">Stable</span></td>
                        </tr>
                        <tr>
                            <td>ICU-02</td>
                            <td>Mary Williams</td>
                            <td>Cardiac monitoring</td>
                            <td>1 day ago</td>
                            <td><span class="status-indicator status-critical">Critical</span></td>
                        </tr>
                        <tr>
                            <td>ICU-03</td>
                            <td>David Brown</td>
                            <td>Respiratory support</td>
                            <td>3 days ago</td>
                            <td><span class="status-indicator status-occupied">Moderate</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `
    },
    bed: {
        title: 'Hospital Bed Management',
        subtitle: 'Monitor and manage hospital bed availability',
        content: `
            <div class="dashboard-grid fade-in">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Total Beds</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #2196F3, #1976D2);">
                            <i class="fas fa-bed"></i>
                        </div>
                    </div>
                    <div class="card-value">320</div>
                    <div class="card-description">Across all departments</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Available</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #4CAF50, #388E3C);">
                            <i class="fas fa-check"></i>
                        </div>
                    </div>
                    <div class="card-value">89</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">28% availability</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Occupied</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF9800, #F57C00);">
                            <i class="fas fa-user"></i>
                        </div>
                    </div>
                    <div class="card-value">231</div>
                    <div class="card-description">
                        <span class="status-indicator status-occupied">72% occupied</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Reserved</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2);">
                            <i class="fas fa-bookmark"></i>
                        </div>
                    </div>
                    <div class="card-value">24</div>
                    <div class="card-description">Scheduled admissions</div>
                </div>
            </div>
            
            <div class="data-table fade-in">
                <h3 style="padding: 1.5rem 1.5rem 0; color: #334155; font-size: 1.25rem; font-weight: 600;">Department-wise Bed Status</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Department</th>
                            <th>Total Beds</th>
                            <th>Available</th>
                            <th>Occupied</th>
                            <th>Occupancy Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>General Ward</td>
                            <td>120</td>
                            <td>34</td>
                            <td>86</td>
                            <td><span class="status-indicator status-occupied">72%</span></td>
                        </tr>
                        <tr>
                            <td>Emergency</td>
                            <td>50</td>
                            <td>12</td>
                            <td>38</td>
                            <td><span class="status-indicator status-occupied">76%</span></td>
                        </tr>
                        <tr>
                            <td>Pediatrics</td>
                            <td>40</td>
                            <td>18</td>
                            <td>22</td>
                            <td><span class="status-indicator status-available">55%</span></td>
                        </tr>
                        <tr>
                            <td>Maternity</td>
                            <td>30</td>
                            <td>8</td>
                            <td>22</td>
                            <td><span class="status-indicator status-occupied">73%</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `
    },
    medicine: {
        title: 'Medicine Inventory',
        subtitle: 'Track and manage pharmaceutical supplies',
        content: `
            <div class="dashboard-grid fade-in">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Total Medicines</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #4CAF50, #388E3C);">
                            <i class="fas fa-pills"></i>
                        </div>
                    </div>
                    <div class="card-value">1,456</div>
                    <div class="card-description">Different medications</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">In Stock</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #2196F3, #1976D2);">
                            <i class="fas fa-check-circle"></i>
                        </div>
                    </div>
                    <div class="card-value">1,289</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">88% availability</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Low Stock</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF9800, #F57C00);">
                            <i class="fas fa-exclamation-triangle"></i>
                        </div>
                    </div>
                    <div class="card-value">124</div>
                    <div class="card-description">
                        <span class="status-indicator status-low">Requires reorder</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Out of Stock</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #F44336, #C62828);">
                            <i class="fas fa-times-circle"></i>
                        </div>
                    </div>
                    <div class="card-value">43</div>
                    <div class="card-description">
                        <span class="status-indicator status-critical">Urgent restock needed</span>
                    </div>
                </div>
            </div>
            
            <div class="data-table fade-in">
                <h3 style="padding: 1.5rem 1.5rem 0; color: #334155; font-size: 1.25rem; font-weight: 600;">Critical Stock Levels</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Medicine Name</th>
                            <th>Category</th>
                            <th>Current Stock</th>
                            <th>Minimum Required</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Paracetamol 500mg</td>
                            <td>Pain Relief</td>
                            <td>150 units</td>
                            <td>200 units</td>
                            <td><span class="status-indicator status-low">Low Stock</span></td>
                        </tr>
                        <tr>
                            <td>Amoxicillin 250mg</td>
                            <td>Antibiotic</td>
                            <td>0 units</td>
                            <td>100 units</td>
                            <td><span class="status-indicator status-critical">Out of Stock</span></td>
                        </tr>
                        <tr>
                            <td>Insulin Aspart</td>
                            <td>Diabetes</td>
                            <td>25 units</td>
                            <td>50 units</td>
                            <td><span class="status-indicator status-low">Low Stock</span></td>
                        </tr>
                        <tr>
                            <td>Aspirin 75mg</td>
                            <td>Cardiovascular</td>
                            <td>300 units</td>
                            <td>150 units</td>
                            <td><span class="status-indicator status-available">In Stock</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="action-buttons fade-in">
                <button class="btn btn-primary">
                    <i class="fas fa-cart-plus"></i>
                    Order Medicines
                </button>
                <button class="btn btn-secondary">
                    <i class="fas fa-file-export"></i>
                    Export Report
                </button>
            </div>
        `
    },
    doctor: {
        title: 'Doctor Management',
        subtitle: 'Manage doctor schedules, specializations, and availability',
        content: `
            <div class="dashboard-grid fade-in">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Total Doctors</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #2196F3, #1976D2);">
                            <i class="fas fa-user-md"></i>
                        </div>
                    </div>
                    <div class="card-value">85</div>
                    <div class="card-description">Across all specializations</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">On Duty</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #4CAF50, #388E3C);">
                            <i class="fas fa-clock"></i>
                        </div>
                    </div>
                    <div class="card-value">62</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">Currently available</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">In Surgery</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF9800, #F57C00);">
                            <i class="fas fa-procedures"></i>
                        </div>
                    </div>
                    <div class="card-value">12</div>
                    <div class="card-description">
                        <span class="status-indicator status-occupied">Performing operations</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Off Duty</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2);">
                            <i class="fas fa-moon"></i>
                        </div>
                    </div>
                    <div class="card-value">11</div>
                    <div class="card-description">Not scheduled today</div>
                </div>
            </div>
            
            <div class="data-table fade-in">
                <h3 style="padding: 1.5rem 1.5rem 0; color: #334155; font-size: 1.25rem; font-weight: 600;">Doctor Availability</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Doctor Name</th>
                            <th>Specialization</th>
                            <th>Department</th>
                            <th>Shift</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Dr. Sarah Mitchell</td>
                            <td>Cardiology</td>
                            <td>Cardiac Unit</td>
                            <td>8:00 AM - 4:00 PM</td>
                            <td><span class="status-indicator status-available">Available</span></td>
                        </tr>
                        <tr>
                            <td>Dr. James Wilson</td>
                            <td>Emergency Medicine</td>
                            <td>Emergency Dept</td>
                            <td>12:00 PM - 12:00 AM</td>
                            <td><span class="status-indicator status-occupied">In Surgery</span></td>
                        </tr>
                        <tr>
                            <td>Dr. Emily Chen</td>
                            <td>Pediatrics</td>
                            <td>Children's Ward</td>
                            <td>9:00 AM - 5:00 PM</td>
                            <td><span class="status-indicator status-available">Available</span></td>
                        </tr>
                        <tr>
                            <td>Dr. Michael Torres</td>
                            <td>Orthopedics</td>
                            <td>Bone & Joint</td>
                            <td>7:00 AM - 3:00 PM</td>
                            <td><span class="status-indicator status-occupied">In Consultation</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="action-buttons fade-in">
                <button class="btn btn-primary">
                    <i class="fas fa-calendar-plus"></i>
                    Schedule Doctor
                </button>
                <button class="btn btn-success">
                    <i class="fas fa-user-plus"></i>
                    Add New Doctor
                </button>
            </div>
        `
    },
    patient: {
        title: 'Patient Management',
        subtitle: 'Manage patient records, admissions, and discharges',
        content: `
            <div class="dashboard-grid fade-in">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Total Patients</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #4CAF50, #388E3C);">
                            <i class="fas fa-users"></i>
                        </div>
                    </div>
                    <div class="card-value">1,247</div>
                    <div class="card-description">Registered patients</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Admitted Today</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #2196F3, #1976D2);">
                            <i class="fas fa-user-plus"></i>
                        </div>
                    </div>
                    <div class="card-value">23</div>
                    <div class="card-description">
                        <span class="status-indicator status-available">New admissions</span>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Discharged Today</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #FF9800, #F57C00);">
                            <i class="fas fa-user-minus"></i>
                        </div>
                    </div>
                    <div class="card-value">18</div>
                    <div class="card-description">Successful treatments</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <h3 class="card-title">Critical Patients</h3>
                        <div class="card-icon" style="background: linear-gradient(135deg, #F44336, #C62828);">
                            <i class="fas fa-exclamation-triangle"></i>
                        </div>
                    </div>
                    <div class="card-value">15</div>
                    <div class="card-description">
                        <span class="status-indicator status-critical">Requires attention</span>
                    </div>
                </div>
            </div>
            
            <div class="data-table fade-in">
                <h3 style="padding: 1.5rem 1.5rem 0; color: #334155; font-size: 1.25rem; font-weight: 600;">Recent Patient Activities</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Patient ID</th>
                            <th>Patient Name</th>
                            <th>Age</th>
                            <th>Department</th>
                            <th>Admission Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>P001247</td>
                            <td>John Anderson</td>
                            <td>45</td>
                            <td>Emergency</td>
                            <td>Today, 10:30 AM</td>
                            <td><span class="status-indicator status-occupied">Under Treatment</span></td>
                        </tr>
                        <tr>
                            <td>P001246</td>
                            <td>Maria Garcia</td>
                            <td>32</td>
                            <td>Maternity</td>
                            <td>Yesterday, 8:15 PM</td>
                            <td><span class="status-indicator status-available">Stable</span></td>
                        </tr>
                        <tr>
                            <td>P001245</td>
                            <td>Robert Taylor</td>
                            <td>67</td>
                            <td>Cardiology</td>
                            <td>2 days ago</td>
                            <td><span class="status-indicator status-critical">Critical</span></td>
                        </tr>
                        <tr>
                            <td>P001244</td>
                            <td>Lisa Thompson</td>
                            <td>28</td>
                            <td>General</td>
                            <td>3 days ago</td>
                            <td><span class="status-indicator status-available">Discharged</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="action-buttons fade-in">
                <button class="btn btn-primary">
                    <i class="fas fa-user-plus"></i>
                    Admit Patient
                </button>
                <button class="btn btn-success">
                    <i class="fas fa-search"></i>
                    Search Patient
                </button>
                <button class="btn btn-warning">
                    <i class="fas fa-file-medical"></i>
                    Medical Records
                </button>
            </div>
        `
    }
};

// Sidebar functionality
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const navItems = document.querySelectorAll('.nav-item');
const pageTitle = document.getElementById('pageTitle');
const pageSubtitle = document.getElementById('pageSubtitle');
const contentBody = document.getElementById('contentBody');

// Toggle sidebar
sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

// Mobile sidebar handling
function handleMobileSidebar() {
    if (window.innerWidth <= 768) {
        sidebar.classList.add('mobile');
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('mobile-open');
        });
    } else {
        sidebar.classList.remove('mobile', 'mobile-open');
    }
}

// Handle window resize
window.addEventListener('resize', handleMobileSidebar);
handleMobileSidebar();

// Navigation functionality with animations
navItems.forEach(item => {
    item.addEventListener('click', function() {
        const section = this.getAttribute('data-section');
        
        // Handle logout
        if (section === 'logout') {
            if (confirm('Are you sure you want to logout?')) {
                localStorage.removeItem('isLoggedIn');
                localStorage.removeItem('currentUser');
                
                // Add logout animation
                document.body.style.opacity = '0';
                document.body.style.transform = 'scale(0.95)';
                
                setTimeout(() => {
                    window.location.href = 'hms.html';
                }, 300);
            }
            return;
        }
        
        // Update active state
        navItems.forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');
        
        // Update content with animation
        if (contentMap[section]) {
            // Fade out current content
            contentBody.style.opacity = '0';
            contentBody.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                // Update header
                pageTitle.textContent = contentMap[section].title;
                pageSubtitle.textContent = contentMap[section].subtitle;
                
                // Update content
                contentBody.innerHTML = contentMap[section].content;
                
                // Fade in new content
                contentBody.style.opacity = '1';
                contentBody.style.transform = 'translateY(0)';
                
                // Close mobile sidebar after selection
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('mobile-open');
                }
            }, 200);
        }
    });
});

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Set initial content
    if (contentMap.main) {
        pageTitle.textContent = contentMap.main.title;
        pageSubtitle.textContent = contentMap.main.subtitle;
        contentBody.innerHTML = contentMap.main.content;
    }
    
    // Set user info if available
    if (currentUser && currentUser.username) {
        const userNameElement = document.querySelector('.user-name');
        if (userNameElement) {
            userNameElement.textContent = currentUser.username;
        }
    }
    
    // Add entrance animations
    setTimeout(() => {
        document.querySelectorAll('.fade-in').forEach((element, index) => {
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }, 100);
});

// Add smooth transitions to content
contentBody.style.transition = 'opacity 0.3s ease, transform 0.3s ease';

// Card hover effects
document.addEventListener('click', function(e) {
    if (e.target.matches('.dashboard-card') || e.target.closest('.dashboard-card')) {
        const card = e.target.closest('.dashboard-card') || e.target;
        card.style.transform = 'scale(0.98)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);
    }
});

// Auto-refresh data simulation
setInterval(() => {
    // Simulate real-time updates
    const valueElements = document.querySelectorAll('.card-value');
    valueElements.forEach(element => {
        if (Math.random() > 0.95) { // 5% chance to update
            element.style.color = '#4CAF50';
            setTimeout(() => {
                element.style.color = '';
            }, 1000);
        }
    });
}, 10000);
