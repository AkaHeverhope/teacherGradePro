import streamlit as st
import pandas as pd
import hashlib
import pickle
from streamlit_extras.switch_page import switch_page
from pathlib import Path

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.session_state["credentials"]["usernames"]:
            user = st.session_state["credentials"]["usernames"][st.session_state["username"]]
            if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == user["password"]:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password
                return True
            else:
                st.session_state["password_correct"] = False
                st.error("😕 Password incorrect")
                return False
        else:
            st.session_state["password_correct"] = False
            st.error("😕 User not found")
            return False

    # Return True if the password is validated or already cached.
    if st.session_state.get("password_correct", False):
        return True

    # Show login input fields
    st.write("# Welcome to the Teacher Dashboard")
    st.write("Please enter your credentials to continue:")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text_input("Username", key="username")
    with col2:
        st.text_input("Password", type="password", key="password")
    
    # Add login button
    login_button = st.button("Login")
    
    if login_button:
        if password_entered():
            st.success(f"Welcome, {st.session_state['username']}!")
            return True
        
    return False

def load_credentials():
    # In a real app, you would load credentials from a secure database
    # This is a simple example using hardcoded credentials
    return {
        "usernames": {
            "teacher1": {
                "name": "Anand",
                "password": hashlib.sha256("123".encode()).hexdigest(),
                "email": "john.smith@school.edu",
                "role": "Math Teacher"
            },
            "teacher2": {
                "name": "Manohari",
                "password": hashlib.sha256("456".encode()).hexdigest(),
                "email": "jane.doe@school.edu",
                "role": "Science Teacher"
            },
            "admin": {
                "name": "Admin User",
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "email": "admin@school.edu",
                "role": "Administrator"
            }
        }
    }

# Initialize session state variables
if "credentials" not in st.session_state:
    st.session_state["credentials"] = load_credentials()
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

# Main app
def main():
    # Apply custom CSS for better appearance
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    div[data-testid="stHeader"] {
        background-color: #1E3A8A;
    }
    .stButton button {
        background-color: #1E40AF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .school-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if check_password():
        # If the password is correct, show the main application
        st.success("You are now logged in to the Teacher Dashboard!")
        st.write(f"Welcome, {st.session_state['credentials']['usernames'][st.session_state['username']]['name']}")
        
        # Here you would integrate with your existing dashboard code
        
    switch_page("website")
        
        # Add logout button
        if st.button("Log Out"):
            st.session_state["password_correct"] = False
            st.rerun()
    else:
        # Show login page with some additional info
        st.markdown("""
        <div class="login-container">
            <div class="school-logo">
                <h1>🏫 School Dashboard</h1>
                <p>A comprehensive tool for teachers to track student progress</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display some features
        st.markdown("### Features")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("📊 **Grade Management**")
            st.write("Easily track and manage student grades")
        with col2:
            st.markdown("👨‍👩‍👧‍👦 **Student Profiles**")
            st.write("View comprehensive student information")
        with col3:
            st.markdown("📝 **Assignment Tracking**")
            st.write("Keep track of assignments and due dates")

if __name__ == "__main__":
    main()
