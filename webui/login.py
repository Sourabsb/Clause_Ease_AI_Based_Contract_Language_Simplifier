import hashlib
import json
import os

class LoginSystem:
    """Simple login system for Streamlit app"""
    def __init__(self):
        self.users_file = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
        self.current_user = None
        self.load_users()

    def load_users(self):
        """Load user credentials from data/users.json"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            # Create default users if file doesn't exist
            self.users = {
                "admin": self.hash_password("admin123"),
                "user": self.hash_password("user123")
            }
            self.save_users()

    def save_users(self):
        """Save user credentials to file"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username, password):
        """Check if username and password are correct"""
        if username in self.users:
            return self.users[username] == self.hash_password(password)
        return False

    def register(self, username, password):
        """Register a new user. Returns (success: bool, message: str)"""
        # Validate username
        if not username or len(username.strip()) == 0:
            return False, "Username cannot be empty"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        # Check if username already exists
        if username in self.users:
            return False, "Username already exists"
        
        # Validate password
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Register the user
        self.users[username] = self.hash_password(password)
        self.save_users()
        return True, "Registration successful! You can now login."
