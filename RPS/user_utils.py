import os
import pandas as pd
from datetime import datetime

class UserManager:
    def __init__(self, excel_path="users.xlsx"):
        self.excel_path = excel_path
        self.current_user = None
        
        # Create users file if it doesn't exist
        if not os.path.exists(self.excel_path):
            df = pd.DataFrame(columns=["username", "password", "email", "created_at", "last_login"])
            df.to_excel(self.excel_path, index=False)
    
    def register_user(self, username, password, email):
        """Register a new user"""
        # Read existing users
        df = pd.read_excel(self.excel_path)
        
        # Check if username exists
        if username in df["username"].values:
            return False, "Username already exists"
        
        # Add new user
        new_user = {
            "username": username,
            "password": password,  # Not hashing as requested
            "email": email,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": ""
        }
        
        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
        df.to_excel(self.excel_path, index=False)
        return True, "Registration successful"
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        df = pd.read_excel(self.excel_path)
        
        # Check if user exists and password matches
        user_row = df[df["username"] == username]
        if len(user_row) == 0:
            return False, "User not found"
        
        if user_row["password"].values[0] != password:
            return False, "Incorrect password"
        
        # Update last login
        df.loc[df["username"] == username, "last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_excel(self.excel_path, index=False)
        
        # Set current user
        self.current_user = username
        return True, "Login successful"
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        
    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.current_user is not None
        
    def get_current_user(self):
        """Get current username"""
        return self.current_user
