import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import hashlib
import re
import os
from datetime import datetime, timedelta
import pytz

# Page configuration
st.set_page_config(
    page_title="GitLab Analytics - Secure Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .login-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
        margin: 2rem 0;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .domain-info {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2196f3;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .success-message {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        color: #2e7d32;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);
    }
    
    .error-message {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
        color: #c62828;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #f44336;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.1);
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fff3e0 0%, #fdf2e5 100%);
        color: #ef6c00;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.1);
    }
    
    .feature-list {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    .feature-item {
        margin: 0.8rem 0;
        padding: 0.5rem;
        display: flex;
        align-items: center;
    }
    
    .feature-icon {
        margin-right: 0.8rem;
        font-size: 1.2em;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .hide-streamlit-style {
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    }
</style>
""", unsafe_allow_html=True)

# Configuration for allowed domains and user management
ALLOWED_DOMAINS = [
    "bits-pilani.ac.in",
    "hyderabad.bits-pilani.ac.in", 
    "pilani.bits-pilani.ac.in",
    "goa.bits-pilani.ac.in",
    "dubai.bits-pilani.ac.in",
    "swecha.org",
     # You can remove this if you want to restrict to only institutional emails
]

# Configuration file path
CONFIG_FILE = "config/auth_config.yaml"

def load_config():
    """Load authentication configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        # Create default configuration if file doesn't exist
        return create_default_config()

def create_default_config():
    """Create default authentication configuration"""
    # Create config directory if it doesn't exist
    os.makedirs("config", exist_ok=True)
    
    # Default configuration with sample users
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@bits-pilani.ac.in',
                    'name': 'Administrator',
                    'password': '$2b$12$EXAMPLE_HASHED_PASSWORD',  # This would be a real hash
                    'role': 'admin',
                    'last_login': None,
                    'login_count': 0
                }
            }
        },
        'cookie': {
            'name': 'gitlab_analytics_auth',
            'key': 'your_secret_key_here',  # Change this to a secure random key
            'expiry_days': 7
        },
        'preauthorized': []
    }
    
    # Save default configuration
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    return config

def validate_email_domain(email):
    """Validate if email belongs to allowed domains"""
    if not email or '@' not in email:
        return False
    
    domain = email.split('@')[-1].lower()
    return domain in [d.lower() for d in ALLOWED_DOMAINS]

def hash_password(password):
    """Hash password using bcrypt"""
    return stauth.Hasher([password]).generate()[0]

def register_new_user(username, email, name, password):
    """Register a new user with domain validation"""
    if not validate_email_domain(email):
        return False, f"Email domain not allowed. Allowed domains: {', '.join(ALLOWED_DOMAINS)}"
    
    # Load current config
    config = load_config()
    
    # Check if username already exists
    if username in config['credentials']['usernames']:
        return False, "Username already exists"
    
    # Check if email already exists
    for user_data in config['credentials']['usernames'].values():
        if user_data.get('email', '').lower() == email.lower():
            return False, "Email already registered"
    
    # Add new user
    config['credentials']['usernames'][username] = {
        'email': email,
        'name': name,
        'password': hash_password(password),
        'role': 'user',
        'last_login': None,
        'login_count': 0,
        'registered_date': datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
    }
    
    # Save updated configuration
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    return True, "User registered successfully"

def update_login_stats(username, config):
    """Update user login statistics"""
    if username in config['credentials']['usernames']:
        config['credentials']['usernames'][username]['last_login'] = datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
        config['credentials']['usernames'][username]['login_count'] = config['credentials']['usernames'][username].get('login_count', 0) + 1
        
        # Save updated configuration
        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Secure Access Portal</h1>
        <h2>GitLab Analytics Dashboard</h2>
        <p style="font-size: 1.1em; opacity: 0.9;">BITS Pilani Internship Program</p>
        <p style="font-size: 0.95em; opacity: 0.8;">Comprehensive GitLab Contributions Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load configuration
    config = load_config()

    if not config or 'credentials' not in config:
        st.error("⚠️ Config loading failed or missing 'credentials' key")
        st.stop()

    
    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        auto_hash=False  # We're handling password hashing manually
    )
    
    # Initialize session state
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'show_registration' not in st.session_state:
        st.session_state['show_registration'] = False
    
    # Main authentication logic
    if st.session_state['authentication_status'] is None:
        # Show login form
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Tab selection for Login/Register
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            st.markdown("Please enter your credentials to access the GitLab Analytics Dashboard.")
            
            # Login form
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                remember_me = st.checkbox("Remember me for 7 days")
                
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if login_button:
                    if username and password:
                        # Check credentials
                        if username in config['credentials']['usernames']:
                            stored_password = config['credentials']['usernames'][username]['password']
                            if stauth.Hasher.verify_password(password, stored_password):
                                # Successful login
                                st.session_state['authentication_status'] = True
                                st.session_state['name'] = config['credentials']['usernames'][username]['name']
                                st.session_state['username'] = username
                                
                                # Update login statistics
                                update_login_stats(username, config)
                                
                                st.success("✅ Login successful! Redirecting to dashboard...")
                                st.rerun()
                            else:
                                st.error("❌ Invalid username or password")
                        else:
                            st.error("❌ Invalid username or password")
                    else:
                        st.warning("⚠️ Please enter both username and password")
        
        with tab2:
            st.markdown("### Join Our Platform!")
            st.markdown("Register with your institutional email to get access.")
            
            # Domain information
            st.markdown(f"""
            <div class="domain-info">
                <h4>📧 Allowed Email Domains:</h4>
                <ul>
                    {"".join([f"<li>@{domain}</li>" for domain in ALLOWED_DOMAINS])}
                </ul>
                <p><strong>Note:</strong> Only users with emails from these domains can register.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Registration form
            with st.form("registration_form"):
                new_username = st.text_input("Choose Username", placeholder="e.g., john_doe")
                new_email = st.text_input("Email Address", placeholder="your.email@bits-pilani.ac.in")
                new_name = st.text_input("Full Name", placeholder="John Doe")
                new_password = st.text_input("Password", type="password", placeholder="Choose a strong password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
                # Password strength indicator
                if new_password:
                    strength_score = 0
                    if len(new_password) >= 8:
                        strength_score += 1
                    if re.search(r'[A-Z]', new_password):
                        strength_score += 1
                    if re.search(r'[a-z]', new_password):
                        strength_score += 1
                    if re.search(r'\d', new_password):
                        strength_score += 1
                    if re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                        strength_score += 1
                    
                    strength_colors = ["#ff4444", "#ff8800", "#ffaa00", "#88dd00", "#00dd00"]
                    strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
                    
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <small>Password Strength: 
                        <span style="color: {strength_colors[min(strength_score, 4)]}; font-weight: bold;">
                        {strength_labels[min(strength_score, 4)]}
                        </span></small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Terms and conditions
                agree_terms = st.checkbox("I agree to the terms and conditions and privacy policy")
                
                register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
                
                if register_button:
                    # Validation
                    if not all([new_username, new_email, new_name, new_password, confirm_password]):
                        st.error("❌ Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 8:
                        st.error("❌ Password must be at least 8 characters long")
                    elif not agree_terms:
                        st.error("❌ Please agree to the terms and conditions")
                    elif not re.match(r'^[a-zA-Z0-9_]+$', new_username):
                        st.error("❌ Username can only contain letters, numbers, and underscores")
                    else:
                        # Attempt registration
                        success, message = register_new_user(new_username, new_email, new_name, new_password)
                        if success:
                            st.success(f"✅ {message}")
                            st.info("🔑 You can now login with your new account!")
                        else:
                            st.error(f"❌ Registration failed: {message}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Information section
        st.markdown("---")
        st.markdown("## 🎯 Platform Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4>📊 Analytics Dashboard</h4>
                <div class="feature-list">
                    <div class="feature-item">
                        <span class="feature-icon">📈</span>
                        <span>Real-time GitLab activity tracking</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">👥</span>
                        <span>User contribution analysis</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🗂️</span>
                        <span>Project-based insights</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📅</span>
                        <span>Timeline visualization</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4>🔒 Security Features</h4>
                <div class="feature-list">
                    <div class="feature-item">
                        <span class="feature-icon">🏛️</span>
                        <span>Domain-restricted access</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🔐</span>
                        <span>Secure password hashing</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🍪</span>
                        <span>Session management</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📝</span>
                        <span>Login activity tracking</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Platform statistics (you can update these based on actual usage)
        st.markdown("## 📊 Platform Statistics")
        
        # Calculate some basic stats
        total_users = len(config['credentials']['usernames'])
        active_users = sum(1 for user in config['credentials']['usernames'].values() 
                          if user.get('last_login') and 
                          datetime.fromisoformat(user['last_login'].replace('Z', '+00:00')) > 
                          datetime.now(pytz.UTC) - timedelta(days=30))
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <h3 style="color: #667eea; margin: 0;">👥 {total_users}</h3>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">Registered Users</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #28a745; margin: 0;">🔥 {active_users}</h3>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">Active This Month</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #17a2b8; margin: 0;">🏢 {len(ALLOWED_DOMAINS)}</h3>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">Allowed Domains</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #ffc107; margin: 0;">🔒 100%</h3>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">Secure Access</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif st.session_state['authentication_status'] == True:
        # User is logged in - show dashboard or redirect
        st.markdown(f"""
        <div class="success-message">
            <h3>✅ Welcome back, {st.session_state['name']}!</h3>
            <p>You are successfully logged in as <strong>@{st.session_state['username']}</strong></p>
            <p>🚀 Redirecting to GitLab Analytics Dashboard...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show user info
        user_info = config['credentials']['usernames'][st.session_state['username']]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📧 Email: {user_info.get('email', 'N/A')}")
            st.info(f"👤 Role: {user_info.get('role', 'user').title()}")
        
        with col2:
            if user_info.get('last_login'):
                last_login = datetime.fromisoformat(user_info['last_login'].replace('Z', '+00:00'))
                st.info(f"🕒 Last Login: {last_login.strftime('%Y-%m-%d %H:%M IST')}")
            st.info(f"📊 Login Count: {user_info.get('login_count', 0)}")
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state['authentication_status'] = None
            st.session_state['name'] = None
            st.session_state['username'] = None
            st.rerun()
        
        # Dashboard access button
        st.markdown("---")
        st.markdown("### 🎯 Access Dashboard")
        
        if st.button("🚀 Open GitLab Analytics Dashboard", use_container_width=True):
            st.success("🔄 Redirecting to main dashboard...")
            # In a real application, you would redirect to your main dashboard
            # For now, we'll show a placeholder
            st.info("💡 **Integration Note:** Connect this to your main dashboard by:")
            st.code("""
# In your main dashboard file, add:
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.switch_page("login.py")  # Redirect to login page
            """)
    
    else:
        # Authentication failed
        st.markdown("""
        <div class="error-message">
            <h3>❌ Authentication Failed</h3>
            <p>Please check your credentials and try again.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Try Again"):
            st.session_state['authentication_status'] = None
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>🔐 Secured by Streamlit Authenticator | 🏛️ BITS Pilani Internship Program</p>
        <p style="font-size: 0.9em;">For technical support, contact your system administrator</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()