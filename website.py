import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from PIL import Image
import time
import random
import altair as alt
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
# Set page config
st.set_page_config(
    page_title="TeachGrade Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define custom CSS for animations and styling
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .dashboard-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #3B82F6;
        animation: fadeIn 1.5s;
    }
    
    .grade-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .grade-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-container {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        animation: slideIn 0.8s;
    }
    
    .student-list {
        animation: fadeIn 1s;
    }
    
    .success-msg {
        color: #047857;
        background-color: #D1FAE5;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        animation: pulse 2s;
    }
    
    .warning-msg {
        color: #B45309;
        background-color: #FEF3C7;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 1.2s;
    }
    
    .section-header {
        color: #1E40AF;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        animation: slideIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(4, 120, 87, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(4, 120, 87, 0); }
        100% { box-shadow: 0 0 0 0 rgba(4, 120, 87, 0); }
    }
    /* Sidebar styling */
    .css-1lcbmhc.e1fqkh3o0 {
        background-color: #1E3A8A;
    }
    
    .css-1v3fvcr {
        background-color: #F8FAFC;
    }
    
    /* Custom button styles */
    .custom-button {
        background-color: #3B82F6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .custom-button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
    }
    
    .custom-info-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0 8px 8px 0;
    }
    
    /* Progress bar animation */
    .progress-container {
        width: 100%;
        height: 8px;
        background-color: #E5E7EB;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #3B82F6, #2563EB);
        transition: width 0.5s ease;
    }
    
    /* Table styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
        font-size: 0.9em;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .styled-table thead tr {
        background-color: #1E3A8A;
        color: #ffffff;
        text-align: left;
    }
    
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #1E3A8A;
    }
    
    /* Animations for dashboard elements */
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .animate-slide-up {
        animation: slideUp 0.8s forwards;
    }
    
    /* Navigation menu styling */
    .nav-link {
        color: #1E3A8A !important;
        font-weight: 500;
    }
    
    .nav-link:hover {
        color: #3B82F6 !important;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #1E3A8A;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize session state for data storage
if 'students' not in st.session_state:
    # Initialize with sample data
    st.session_state['students'] = pd.DataFrame({
        'ID': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
        'Name': ['Saran Senthil', 'Gokul Raj', 'Harshith K', 'Selvi K', 'Guhan Sambandam', 
                'Isabella  Garcia', 'Praketh K', ' M Charles', 'Hitler F', 'Elil Nandhan' ],
        'Grade': ['A', 'B+', 'C', 'A-', 'B', 'A+', 'B-', 'C+', 'A', 'B+'],
        'Score': [92, 87, 75, 90, 85, 96, 82, 78, 94, 88],
        'Attendance': [95, 88, 75, 92, 85, 98, 80, 82, 91, 86],
        'Behavior': ['Excellent', 'Good', 'Fair', 'Excellent', 'Good', 'Excellent', 'Good', 'Fair', 'Excellent', 'Good'],
        'Strengths': ['Critical thinking, Leadership', 'Creativity, Communication', 'Mathematics, Problem-solving', 
                     'Writing, Analytical skills', 'Science, Teamwork', 'Reading, Public speaking', 
                     'History, Research', 'Art, Collaboration', 'Languages, Debate', 'Technology, Organization'],
        'Weaknesses': ['Time management', 'Test anxiety', 'Writing skills', 'Group work', 'Attention to detail', 
                      'Mathematics', 'Reading comprehension', 'Public speaking', 'Organization', 'Critical analysis'],
        'Comments': ['Excellent performance in all areas. Shows leadership qualities.', 
                    'Creative student with good communication. Needs to work on test-taking skills.', 
                    'Struggles with writing but excels in math. Attendance needs improvement.', 
                    'Outstanding analytical skills. Could contribute more to group discussions.', 
                    'Consistent performance. Needs to double-check work for errors.', 
                    'Top of the class. Has potential for advanced placement.', 
                    'Good progress but inconsistent attendance affecting overall performance.', 
                    'Improving steadily. Benefits from additional practice.', 
                    'Exceptional student with diverse skills. Well-balanced performance.', 
                    'Organized and methodical. Could develop more critical thinking skills.'],
        'Last Updated': pd.date_range(start='2025-03-15', periods=10)
    })

if 'subjects' not in st.session_state:
    st.session_state['subjects'] = pd.DataFrame({
        'Student_ID': [1001, 1001, 1001, 1002, 1002, 1002, 1003, 1003, 1003, 1004, 1004, 1004,
                     1005, 1005, 1005, 1006, 1006, 1006, 1007, 1007, 1007, 1008, 1008, 1008,
                     1009, 1009, 1009, 1010, 1010, 1010],
        'Subject': ['Mathematics', 'English', 'Science', 'Mathematics', 'English', 'Science',
                  'Mathematics', 'English', 'Science', 'Mathematics', 'English', 'Science',
                  'Mathematics', 'English', 'Science', 'Mathematics', 'English', 'Science',
                  'Mathematics', 'English', 'Science', 'Mathematics', 'English', 'Science',
                  'Mathematics', 'English', 'Science', 'Mathematics', 'English', 'Science'],
        'Score': [94, 90, 92, 85, 90, 86, 78, 70, 77, 92, 95, 83, 88, 82, 85, 98, 95, 95,
                80, 84, 82, 75, 82, 77, 96, 92, 94, 85, 90, 89],
        'Grade': ['A', 'A-', 'A', 'B', 'A-', 'B', 'C+', 'C-', 'C+', 'A', 'A', 'B', 'B+', 'B', 'B', 
                'A+', 'A', 'A', 'B-', 'B', 'B', 'C', 'B', 'C+', 'A', 'A', 'A', 'B', 'A-', 'B+']
    })

if 'assignments' not in st.session_state:
    st.session_state['assignments'] = pd.DataFrame({
        'Student_ID': [1001, 1001, 1002, 1002, 1003, 1003, 1004, 1004, 1005, 1005,
                     1006, 1006, 1007, 1007, 1008, 1008, 1009, 1009, 1010, 1010],
        'Subject': ['Mathematics', 'English', 'Mathematics', 'English', 'Mathematics', 'English',
                  'Mathematics', 'English', 'Mathematics', 'English', 'Mathematics', 'English',
                  'Mathematics', 'English', 'Mathematics', 'English', 'Mathematics', 'English',
                  'Mathematics', 'English'],
        'Assignment': ['Calculus Project', 'Essay Writing', 'Algebra Quiz', 'Book Report', 
                     'Geometry Test', 'Grammar Exercise', 'Statistics Project', 'Literature Analysis',
                     'Probability Quiz', 'Creative Writing', 'Advanced Math Test', 'Research Paper',
                     'Trigonometry Quiz', 'Poetry Analysis', 'Basic Math Test', 'Comprehension Exercise',
                     'Math Olympiad', 'Critical Essay', 'Linear Algebra', 'Narrative Writing'],
        'Due_Date': pd.date_range(start='2025-04-01', periods=20),
        'Status': ['Submitted', 'Submitted', 'Submitted', 'Late', 'Submitted', 'Missing', 
                 'Submitted', 'Submitted', 'Late', 'Submitted', 'Submitted', 'Submitted',
                 'Missing', 'Submitted', 'Submitted', 'Late', 'Submitted', 'Submitted',
                 'Submitted', 'Submitted'],
        'Score': [95, 92, 88, 84, 76, 0, 94, 95, 82, 85, 98, 96, 0, 83, 75, 80, 97, 93, 86, 89]
    })

if 'attendance' not in st.session_state:
    st.session_state['attendance'] = pd.DataFrame({
        'Student_ID': [1001, 1001, 1001, 1002, 1002, 1002, 1003, 1003, 1003, 1004, 1004, 1004,
                     1005, 1005, 1005, 1006, 1006, 1006, 1007, 1007, 1007, 1008, 1008, 1008,
                     1009, 1009, 1009, 1010, 1010, 1010],
        'Date': pd.date_range(start='2025-03-01', periods=30),
        'Status': ['Present', 'Present', 'Present', 'Present', 'Absent', 'Present', 'Present', 'Absent', 'Late',
                 'Present', 'Present', 'Present', 'Present', 'Late', 'Present', 'Present', 'Present', 'Present',
                 'Absent', 'Present', 'Late', 'Present', 'Late', 'Present', 'Present', 'Present', 'Present',
                 'Present', 'Absent', 'Present']
    })

if 'progress' not in st.session_state:
    # Generate some historical progress data for each student
    students = st.session_state['students']['ID'].unique()
    data = []
    for student_id in students:
        for month in range(1, 5):  # Jan to Apr 2025
            for subject in ['Mathematics', 'English', 'Science']:
                # Random score between 65 and 98 with general improvement trend
                base_score = np.random.randint(65, 85)
                improvement = np.random.randint(0, 5) * month / 2
                score = min(98, base_score + improvement)
                
                data.append({
                    'Student_ID': student_id,
                    'Month': pd.Timestamp(f'2025-{month}-01'),
                    'Subject': subject,
                    'Score': score
                })
    
    st.session_state['progress'] = pd.DataFrame(data)

if 'username' not in st.session_state:
    st.session_state['username'] = 'Mr.Anand'

if 'show_welcome' not in st.session_state:
    st.session_state['show_welcome'] = True

if 'notification_count' not in st.session_state:
    st.session_state['notification_count'] = 3

if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

# Function to convert grade to numeric value
def grade_to_numeric(grade):
    grade_map = {
        'A+': 4.3, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }
    return grade_map.get(grade, 0)

# Function to convert numeric value to grade
def numeric_to_grade(score):
    if score >= 97:
        return 'A+'
    elif score >= 93:
        return 'A'
    elif score >= 90:
        return 'A-'
    elif score >= 87:
        return 'B+'
    elif score >= 83:
        return 'B'
    elif score >= 80:
        return 'B-'
    elif score >= 77:
        return 'C+'
    elif score >= 73:
        return 'C'
    elif score >= 70:
        return 'C-'
    elif score >= 67:
        return 'D+'
    elif score >= 63:
        return 'D'
    elif score >= 60:
        return 'D-'
    else:
        return 'F'

# Function to generate random performance data
def generate_random_data(n_students=30):
    names = [
        'Saran', 'Selvi', 'Guhan', 'Senthil', 'Shivani',
        'Sarvash', 'Nikash', 'Harshith', 'Suhil', 'Dhanajith',
        'Nidhisha', 'Dharaneesh', 'Manigandan', 'Bhadhrinath', 'Anand',
        'Prajith', 'Rhishava', 'Daniel ', 'Sherlock Holmes', 'T sharan',
        'Monish', 'Rakshan', 'Roshan', 'Tejash', 'Dhakshina',
        'Jacob', 'Sophia', 'David Beckham', 'Messi', 'Ronaldo'
    ]
    
    data = []
    for i in range(n_students):
        score = np.random.randint(60, 99)
        grade = numeric_to_grade(score)
        attendance = np.random.randint(70, 100)
        behavior_options = ['Excellent', 'Good', 'Fair', 'Needs Improvement']
        behavior_weights = [0.4, 0.3, 0.2, 0.1]
        behavior = np.random.choice(behavior_options, p=behavior_weights)
        
        strengths = [
            'Critical thinking', 'Problem solving', 'Communication', 'Leadership',
            'Creativity', 'Collaboration', 'Organization', 'Self-motivation',
            'Research skills', 'Public speaking', 'Writing', 'Mathematics',
            'Science', 'Reading', 'Art', 'Music', 'Technology', 'Analysis'
        ]
        
        weaknesses = [
            'Time management', 'Test anxiety', 'Group work', 'Attention to detail',
            'Meeting deadlines', 'Note-taking', 'Verbal participation', 'Organization',
            'Reading comprehension', 'Writing skills', 'Mathematics', 'Public speaking',
            'Critical analysis', 'Following directions', 'Independent work', 'Focus'
        ]
        
        # Select 2 random strengths and 1 weakness
        student_strengths = ', '.join(np.random.choice(strengths, 2, replace=False))
        student_weakness = np.random.choice(weaknesses)
        
        comment_templates = [
            "Demonstrates strong {0} skills. Could improve {1}.",
            "Excellent at {0}. Needs to work on {1}.",
            "Shows great potential in {0}. {1} needs attention.",
            "Proficient in {0}. Should focus on developing {1}.",
            "Talented in {0} areas. {1} is an area for growth."
        ]
        
        comment = np.random.choice(comment_templates).format(student_strengths.split(', ')[0], student_weakness)
        
        data.append({
            'ID': 1011 + i,
            'Name': names[i],
            'Grade': grade,
            'Score': score,
            'Attendance': attendance,
            'Behavior': behavior,
            'Strengths': student_strengths,
            'Weaknesses': student_weakness,
            'Comments': comment,
            'Last Updated': pd.Timestamp('2025-03-15') + pd.Timedelta(days=np.random.randint(0, 20))
        })
    
    return pd.DataFrame(data)

# Function to create downloadable link
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    
    # Create a bytes buffer
    b64 = base64.b64encode(object_to_download.encode()).decode()
    
    # Create download link
    href = f'<a href="data:file/csv;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    return href

# Function for loading animation
def loading_animation():
    progress_text = "Processing data..."
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)
    time.sleep(0.5)
    my_bar.empty()

# Sidebar navigation
with st.sidebar:
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background-color: #3B82F6; color: white; width: 40px; height: 40px; 
                  border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                  font-weight: bold; font-size: 18px; margin-right: 10px;">TG</div>
        <h2 style="margin: 0; color: #1E3A8A;">TeachGrade Pro</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <div style="background-color: #3B82F6; color: white; width: 36px; height: 36px; 
                  border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                  font-weight: bold; font-size: 16px; margin-right: 10px;">
            {st.session_state['username'][0]}
        </div>
        <div>
            <div style="font-weight: 500; color: #1E3A8A;">{st.session_state['username']}</div>
            <div style="font-size: 0.8rem; color: #6B7280;">Math Department</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Students", "Gradebook", "Performance", "Reports", "Settings"],
        icons=["speedometer2", "people", "journal-check", "graph-up", "file-earmark-text", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#3B82F6", "font-size": "1rem"},
            "nav-link": {"font-size": "0.9rem", "text-align": "left", "margin": "0px", "--hover-color": "#EFF6FF"},
            "nav-link-selected": {"background-color": "#DBEAFE", "color": "#1E40AF"},
        }
    )
    
    st.sidebar.markdown("""
    <div style="margin-top: 30px; padding: 15px; background-color: #DBEAFE; border-radius: 10px;">
        <h4 style="color: #1E40AF; margin-top: 0;">Quick Actions</h4>
        <div style="margin-bottom: 10px;">
            <button class="custom-button" style="width: 100%; background-color: #3B82F6;">
                Add New Student
            </button>
        </div>
        <div style="margin-bottom: 10px;">
            <button class="custom-button" style="width: 100%; background-color: #3B82F6;">
                Create Report
            </button>
        </div>
        <div>
            <button class="custom-button" style="width: 100%; background-color: #3B82F6;">
                Schedule Meeting
            </button>
        </div>
    </div>
    
    <div style="position: absolute; bottom: 20px; left: 20px; right: 20px;">
        <div style="padding: 15px; background-color: #F3F4F6; border-radius: 10px;">
            <h4 style="color: #1F2937; margin-top: 0; font-size: 0.9rem;">Need Help?</h4>
            <p style="font-size: 0.8rem; color: #4B5563; margin-bottom: 10px;">
                Check our documentation or contact support for assistance.
            </p>
            <button class="custom-button" style="width: 100%; background-color: #6B7280; font-size: 0.8rem;">
                Support Center
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Welcome message animation (only shown once)
if st.session_state['show_welcome']:
    st.markdown("""
    <div style="text-align: center; padding: 20px; animation: fadeIn 1.5s;">
        <h1 style="color: #1E3A8A; font-size: 2.5rem;">Welcome to TeachGrade Pro</h1>
        <p style="font-size: 1.2rem; color: #4B5563;">Your comprehensive student performance management system</p>
    </div>
    """, unsafe_allow_html=True)
    
    loading_animation()
    st.session_state['show_welcome'] = False
    st.rerun()
# Dashboard page
if selected == "Dashboard":
    st.markdown('<h1 class="dashboard-title">Teacher Dashboard</h1>', unsafe_allow_html=True)
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_score = st.session_state['students']['Score'].mean()
    top_students = len(st.session_state['students'][st.session_state['students']['Score'] >= 90])
    needs_improvement = len(st.session_state['students'][st.session_state['students']['Score'] < 75])
    attendance_rate = st.session_state['students']['Attendance'].mean()
    
    with col1:
        st.markdown("""
         <div class="metric-container">
            <h3 style="margin: 0; font-size: 1rem; color: #6B7280;">Average Score</h3>
            <p style="font-size: 1.8rem; font-weight: 600; color: #1E40AF; margin: 5px 0;">{:.1f}%</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {}%;"></div>
            </div>
        </div>
        """.format(avg_score, avg_score), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3 style="margin: 0; font-size: 1rem; color: #6B7280;">Top Students (A)</h3>
            <p style="font-size: 1.8rem; font-weight: 600; color: #047857; margin: 5px 0;">{}</p>
            <div style="font-size: 0.8rem; color: #059669;">+2 from last month</div>
        </div>
        """.format(top_students), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3 style="margin: 0; font-size: 1rem; color: #6B7280;">Needs Improvement</h3>
            <p style="font-size: 1.8rem; font-weight: 600; color: #B91C1C; margin: 5px 0;">{}</p>
            <div style="font-size: 0.8rem; color: #EF4444;">-1 from last month</div>
        </div>
        """.format(needs_improvement), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <h3 style="margin: 0; font-size: 1rem; color: #6B7280;">Attendance Rate</h3>
            <p style="font-size: 1.8rem; font-weight: 600; color: #1E40AF; margin: 5px 0;">{:.1f}%</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {}%;"></div>
            </div>
        </div>
        """.format(attendance_rate, attendance_rate), unsafe_allow_html=True)
    
    # Recent activity and reminders
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">Class Performance Overview</h2>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Grade Distribution", "Subject Performance"])
        
        with tab1:
            # Grade distribution chart
            grade_counts = st.session_state['students']['Grade'].apply(lambda x: x[0] if len(x) > 0 else '').value_counts()
            
            fig = px.pie(
                names=grade_counts.index,
                values=grade_counts.values,
                title="Grade Distribution",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.4,
            )
            fig.update_layout(
                legend_title="Grade",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=40, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="custom-info-box">
                <h4 style="margin-top: 0; color: #1E40AF;">Key Insights</h4>
                <ul style="margin-bottom: 0;">
                    <li>Most students are performing in the B range</li>
                    <li>30% of students achieving A grades</li>
                    <li>Only 10% of students below C level</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with tab2:
            # Subject performance chart
            subject_data = st.session_state['subjects'].groupby('Subject')['Score'].mean().reset_index()
            
            fig = px.bar(
                subject_data,
                x='Subject',
                y='Score',
                title="Average Performance by Subject",
                color='Score',
                color_continuous_scale='Blues',
                text='Score'
            )
            fig.update_layout(
                xaxis_title="Subject",
                yaxis_title="Average Score",
                yaxis=dict(range=[65, 100]),
                coloraxis_showscale=False,
                margin=dict(l=20, r=20, t=40, b=20),
                height=300
            )
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="custom-info-box">
                <h4 style="margin-top: 0; color: #1E40AF;">Subject Analysis</h4>
                <ul style="margin-bottom: 0;">
                    <li>English shows the strongest overall performance</li>
                    <li>Mathematics performance varies most widely among students</li>
                    <li>Science has the most consistent scores across the class</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h2 class="section-header">Upcoming Tasks</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="grade-card">
            <h4 style="margin-top: 0; color: #DC2626;">Due Today</h4>
            <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>Enter science test scores</li>
                <li>Parent-teacher meeting (3 PM)</li>
                <li>Submit monthly department report</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="grade-card">
            <h4 style="margin-top: 0; color: #2563EB;">Upcoming Deadlines</h4>
            <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>Math quiz grading (Apr 12)</li>
                <li>Progress reports (Apr 15)</li>
                <li>Department meeting (Apr 18)</li>
                <li>End of term evaluations (Apr 25)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="grade-card">
            <h4 style="margin-top: 0; color: #047857;">Recent Updates</h4>
            <div style="font-size: 0.9rem;">
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: 500;">Curriculum update</div>
                    <div style="color: #6B7280; font-size: 0.8rem;">Updated 2 hours ago</div>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: 500;">New gradebook features</div>
                    <div style="color: #6B7280; font-size: 0.8rem;">Updated yesterday</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Student highlight and attendance
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<h2 class="section-header">Student Highlights</h2>', unsafe_allow_html=True)
    top_students_df = st.session_state['students'].sort_values('Score', ascending=False).head(3)
    
    for _, student in top_students_df.iterrows():
        # Safely handle name splitting and initials
        Name = [{'Saran': 'Senthil'}, {'Gokul': 'Raj'}, {'Harshith': 'K'}, {'Selvi': 'K'}, {'Guhan': 'Sambandam'},
                {'Isabella': 'Garcia'}, {'Praketh': 'K'}, {'M': 'Charles'}, {'Hitler': 'F'}, {'Elil': 'Nandhan'}]
        
        name = student.get('Name', '')
        
        if isinstance(name, str) and name.strip():
            name_parts = name.strip().split()
            if len(name_parts) >= 2:
                initials = f"{name_parts[0][0]}{name_parts[1][0]}"
            else:
                initials = name_parts[0][0]
        else:
            initials = "?"
        st.markdown(f"""
        <div class="grade-card">
            <div style="display: flex; align-items: center;">
                <div style="background-color: #3B82F6; color: white; width: 40px; height: 40px; 
                          border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                          font-weight: bold; font-size: 16px; margin-right: 10px;">
                    {initials}
                </div>
                <div>
                    <div style="font-weight: 500; color: #1E3A8A;">{student['Name']}</div>
                    <div style="font-size: 0.8rem; color: #6B7280;">Score: {student['Score']}% ({student['Grade']})</div>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 0.9rem;">
                <div><span style="font-weight: 500;">Strengths:</span> {student['Strengths']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    
    with col2:
        st.markdown('<h2 class="section-header">Attendance Overview</h2>', unsafe_allow_html=True)
        
        # Process attendance data
        attendance_counts = st.session_state['attendance']['Status'].value_counts()
        attendance_data = pd.DataFrame({
            'Status': attendance_counts.index,
            'Count': attendance_counts.values,
            'Percentage': (attendance_counts.values / len(st.session_state['attendance']) * 100).round(1)
        })
        
        fig = px.bar(
            attendance_data,
            x='Status',
            y='Count',
            color='Status',
            text='Percentage',
            color_discrete_map={
                'Present': '#047857',
                'Absent': '#DC2626',
                'Late': '#D97706'
            },
            title="Class Attendance Status"
        )
        fig.update_layout(
            xaxis_title="Status",
            yaxis_title="Count",
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show recent absences
        st.markdown("""
        <div class="custom-info-box">
            <h4 style="margin-top: 0; color: #1E40AF;">Students with Recent Absences</h4>
            <div style="font-size: 0.9rem;">
                <ul style="margin-bottom: 0;">
                    <li>Emma Wilson - 2 days</li>
                    <li>Michael Johnson - 3 days</li>
                    <li>Liam Martinez - 1 day</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Students page
if selected == "Students":
    st.markdown('<h1 class="dashboard-title">Student Management</h1>', unsafe_allow_html=True)
    
    # Create tabs for different student management functions
    tab1, tab2, tab3 = st.tabs(["Student List", "Add/Edit Student", "Student Details"])
    
    with tab1:
        # Student search and filter
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("Search by name or ID", placeholder="Enter name or ID...")
        
        with col2:
            grade_filter = st.selectbox("Filter by grade", ["All", "A", "B", "C", "D", "F"])
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Name", "Score (High to Low)", "Score (Low to High)"])
        
        # Filter and sort student data
        filtered_students = st.session_state['students'].copy()
        
        if search_term:
            filtered_students = filtered_students[
                filtered_students['Name'].str.contains(search_term, case=False) | 
                filtered_students['ID'].astype(str).str.contains(search_term)
            ]
        
        if grade_filter != "All":
            filtered_students = filtered_students[filtered_students['Grade'].str.startswith(grade_filter)]
        
        if sort_by == "Name":
            filtered_students = filtered_students.sort_values('Name')
        elif sort_by == "Score (High to Low)":
            filtered_students = filtered_students.sort_values('Score', ascending=False)
        elif sort_by == "Score (Low to High)":
            filtered_students = filtered_students.sort_values('Score')
        
        # Display student list in an interactive table
        st.markdown(f"<p>Showing {len(filtered_students)} students</p>", unsafe_allow_html=True)
        
        # Student list with expandable rows
        for i, (_, student) in enumerate(filtered_students.iterrows()):
            with st.expander(f"{student['Name']} (ID: {student['ID']}) - {student['Grade']} ({student['Score']}%)"):
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="padding: 10px; background-color: #F9FAFB; border-radius: 8px;">
                        <h4 style="margin-top: 0; font-size: 1rem;">Performance</h4>
                        <p style="margin-bottom: 5px;"><strong>Score:</strong> {student['Score']}%</p>
                        <p style="margin-bottom: 5px;"><strong>Grade:</strong> {student['Grade']}</p>
                        <p style="margin-bottom: 0;"><strong>Attendance:</strong> {student['Attendance']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="padding: 10px; background-color: #F9FAFB; border-radius: 8px;">
                        <h4 style="margin-top: 0; font-size: 1rem;">Analysis</h4>
                        <p style="margin-bottom: 5px;"><strong>Strengths:</strong> {student['Strengths']}</p>
                        <p style="margin-bottom: 5px;"><strong>Weaknesses:</strong> {student['Weaknesses']}</p>
                        <p style="margin-bottom: 0;"><strong>Behavior:</strong> {student['Behavior']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style="padding: 10px; background-color: #F9FAFB; border-radius: 8px;">
                        <h4 style="margin-top: 0; font-size: 1rem;">Comments</h4>
                        <p style="margin-bottom: 5px;">{student['Comments']}</p>
                        <p style="margin-bottom: 0; font-size: 0.8rem; color: #6B7280;">
                            Last updated: {student['Last Updated'].strftime('%b %d, %Y')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Action buttons
                c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
                with c1:
                    st.button("Edit Student", key=f"edit_{student['ID']}")
                with c2:
                    st.button("View Details", key=f"view_{student['ID']}")
                with c3:
                    st.button("Generate Report", key=f"report_{student['ID']}")
                with c4:
                    st.button("Contact Parent", key=f"contact_{student['ID']}")
        
        # Pagination
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <div style="display: flex; align-items: center;">
                <button class="custom-button" style="background-color: #6B7280; margin-right: 10px;">Previous</button>
                <span style="margin: 0 10px;">Page 1 of 1</span>
                <button class="custom-button" style="background-color: #6B7280; margin-left: 10px;">Next</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">Add or Edit Student Details</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.number_input("Student ID", min_value=1000, max_value=9999, value=1020)
            student_name = st.text_input("Student Name", placeholder="Enter full name")
            student_score = st.slider("Score (%)", min_value=0, max_value=100, value=85)
            student_grade = numeric_to_grade(student_score)
            st.info(f"Grade based on score: {student_grade}")
            student_attendance = st.slider("Attendance (%)", min_value=0, max_value=100, value=90)
        
        with col2:
            student_behavior = st.selectbox("Behavior", ["Excellent", "Good", "Fair", "Needs Improvement"])
            student_strengths = st.text_area("Strengths", placeholder="Enter student strengths (comma separated)")
            student_weaknesses = st.text_area("Weaknesses", placeholder="Enter areas for improvement")
            student_comments = st.text_area("Teacher Comments", placeholder="Add your comments here...")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Save Student", type="primary"):
                loading_animation()
                st.success("Student information saved successfully!")
        
        with col2:
            if st.button("Clear Form"):
                st.info("Form cleared. Enter new student information.")
                
        st.markdown("---")
        
        st.markdown('<h3 style="color: #1E40AF;">Bulk Student Management</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_file = st.file_uploader("Upload Student Data (CSV)", type="csv")
            if uploaded_file is not None:
                st.success("File uploaded successfully! Click 'Import Data' to process.")
        
        with col2:
            st.download_link = st.markdown(
                download_link(st.session_state['students'], 'student_data_template.csv', 'Download Template CSV'),
                unsafe_allow_html=True)
            
            if st.button("Import Data"):
                loading_animation()
                st.success("Student data imported successfully!")
                
            if st.button("Generate Random Test Data"):
                loading_animation()
                random_data = generate_random_data(10)
                st.session_state['students'] = pd.concat([st.session_state['students'], random_data], ignore_index=True)
                st.success("Random test data generated and added to the database!")
    
    with tab3:
        # Simulate selecting a student for detailed view
        st.markdown('<h2 class="section-header">Student Detailed Profile</h2>', unsafe_allow_html=True)
        
        student_select = st.selectbox(
            "Select a student to view details",
            options=st.session_state['students']['Name'].tolist()
        )
        
        if student_select:
            selected_student = st.session_state['students'][st.session_state['students']['Name'] == student_select].iloc[0]
            student_id = selected_student['ID']
            
            # Get subject scores for this student
            student_subjects = st.session_state['subjects'][st.session_state['subjects']['Student_ID'] == student_id]
            
            # Get assignment data for this student
            student_assignments = st.session_state['assignments'][st.session_state['assignments']['Student_ID'] == student_id]
            
            # Get attendance data for this student
            student_attendance = st.session_state['attendance'][st.session_state['attendance']['Student_ID'] == student_id]
            
            col1, col2 = st.columns([1, 2])
            
            # Define columns first
col1, col2 = st.columns(2)

# Content for first column
with col1:
    # Create a safer way to get initials
    # First, select a student - assuming you want to select a specific student by index or ID
    # You need a way to identify which student to select
    student_index = 0  # or whatever method you use to determine the current student
    selected_student = st.session_state['students'].iloc[student_index]  
    # Or if you have a student ID to select by:
    # student_id = "12345"  # Replace with your selection method
    # selected_student = st.session_state['students'].loc[st.session_state['students']['ID'] == student_id].iloc[0]
    
    # Now process the student's name safely
    name_parts = selected_student['Name'].split()
    initials = name_parts[0][0]  # Always get first initial
    
    # Add second initial only if there's a second name part
    if len(name_parts) > 1:
        initials += name_parts[1][0]
    
    st.markdown(f"""
    <div class="grade-card">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: #3B82F6; color: white; width: 60px; height: 60px;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 24px; margin-right: 15px;">
                {initials}
            </div>
            <div>
                <div style="font-weight: 600; color: #1E3A8A; font-size: 1.2rem;">{selected_student['Name']}</div>
                <div style="color: #6B7280;">ID: {selected_student['ID']}</div>
            </div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="font-weight: 500; margin-bottom: 5px;">Overall Grade</div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: #DBEAFE; color: #1E40AF; width: 40px; height: 40px;
                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                font-weight: bold; font-size: 18px; margin-right: 10px;">
                    {selected_student['Grade'][0]}
                </div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #1E40AF;">{selected_student['Grade']} ({selected_student['Score']}%)</div>
            </div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="font-weight: 500; margin-bottom: 5px;">Attendance</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {selected_student['Attendance']}%;"></div>
            </div>
            <div style="text-align: right; font-size: 0.9rem;">{selected_student['Attendance']}%</div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="font-weight: 500; margin-bottom: 5px;">Behavior</div>
            <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                {selected_student['Behavior']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="grade-card">
        <h4 style="margin-top: 0;">Teacher Comments</h4>
        <p style="font-style: italic;">"{selected_student['Comments']}"</p>
        <div style="font-size: 0.8rem; color: #6B7280; text-align: right;">
            Last updated: {selected_student['Last Updated'].strftime('%b %d, %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Content for second column
# First define the column
col1, col2 = st.columns([1, 2])  # Adjust the ratio as needed

# Define student_subjects dataframe
# You need to replace this with your actual data source
student_subjects = pd.DataFrame({
    'Subject': ['Math', 'Science', 'English', 'History', 'Art'],
    'Score': [85, 92, 78, 88, 95],
    'Grade': ['B+', 'A-', 'C+', 'B+', 'A']
})


# Then use col2 with tabs
with col2:
    tab1, tab2, tab3 = st.tabs(["Academic Performance", "Assignments", "Attendance"])
    
    with tab1:
        # Subject performance chart
        fig = px.bar(
            student_subjects,
            x='Subject',
            y='Score',
            color='Subject',
            title=f"Subject Performance for {selected_student['Name']}",
            text='Grade',
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)  # Don't forget to display the chart
        fig.update_layout(
            xaxis_title="Subject",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100]),
            showlegend=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Subject details table
        st.markdown('<h4 style="color: #1E40AF;">Subject Details</h4>', unsafe_allow_html=True)
        
        subject_data = []
        for _, subject in student_subjects.iterrows():
            subject_data.append({
                "Subject": subject['Subject'],
                "Score": f"{subject['Score']}%",
                "Grade": subject['Grade'],
                "Status": "On Track" if subject['Score'] >= 80 else "Needs Improvement"
            })
        
        subject_df = pd.DataFrame(subject_data)
        st.dataframe(subject_df, use_container_width=True, hide_index=True)
        
        # Strengths and weaknesses
        strength_col1, strength_col2 = st.columns(2)
        
        with strength_col1:
            st.markdown("""
            <div style="padding: 15px; background-color: #DBEAFE; border-radius: 8px;">
                <h4 style="margin-top: 0; color: #1E40AF;">Strengths</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            for strength in selected_student['Strengths'].split(','):
                st.markdown(f"<li>{strength.strip()}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with strength_col2:
            st.markdown("""
            <div style="padding: 15px; background-color: #FEF2F2; border-radius: 8px;">
                <h4 style="margin-top: 0; color: #B91C1C;">Areas for Improvement</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            for weakness in selected_student['Weaknesses'].split(','):
                st.markdown(f"<li>{weakness.strip()}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        # Assignment status chart
        student_assignments = pd.DataFrame({
    'Assignment': ['Math HW 1', 'Science Project', 'English Essay', 'History Quiz', 'Art Portfolio'],
    'Due_Date': ['2025-04-20', '2025-04-25', '2025-04-18', '2025-04-22', '2025-04-30'],
    'Status': ['Completed', 'In Progress', 'Not Started', 'Completed', 'In Progress']
})
        assignment_status = student_assignments['Status'].value_counts().reset_index()
        assignment_status.columns = ['Status', 'Count']
        
        fig = px.pie(
            assignment_status,
            names='Status',
            values='Count',
            title="Assignment Status",
            color='Status',
            color_discrete_map={
                'Submitted': '#047857',
                'Late': '#D97706',
                'Missing': '#DC2626'
            },
            hole=0.4
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Assignment details table
        st.markdown('<h4 style="color: #1E40AF;">Assignment Details</h4>', unsafe_allow_html=True)
        
        student_assignments_display = student_assignments.copy()
        student_assignments_display['Due_Date'] = student_assignments_display['Due_Date'].dt.strftime('%b %d, %Y')
        student_assignments_display = student_assignments_display[['Subject', 'Assignment', 'Due_Date', 'Status', 'Score']]
        
        # Add color to status
        def highlight_status(val):
            if val == 'Submitted':
                return 'background-color: #ECFDF5; color: #047857'
            elif val == 'Late':
                return 'background-color: #FFFBEB; color: #D97706'
            elif val == 'Missing':
                return 'background-color: #FEF2F2; color: #DC2626'
            return ''
        
        st.dataframe(student_assignments_display, use_container_width=True, hide_index=True)
        
        # Assignment actions
        assign_col1, assign_col2 = st.columns(2)
        
        with assign_col1:
            st.button("Add New Assignment", key="add_assignment")
        
        with assign_col2:
            st.button("Send Assignment Reminder", key="send_reminder")
    
    with tab3:
        # Attendance trend chart
        attendance_counts = student_attendance['Status'].value_counts()
        present_pct = attendance_counts.get('Present', 0) / len(student_attendance) * 100
        absent_pct = attendance_counts.get('Absent', 0) / len(student_attendance) * 100
        late_pct = attendance_counts.get('Late', 0) / len(student_attendance) * 100
        
        attendance_data = pd.DataFrame({
            'Status': ['Present', 'Absent', 'Late'],
            'Percentage': [present_pct, absent_pct, late_pct]
        })
        
        fig = px.bar(
            attendance_data,
            x='Status',
            y='Percentage',
            title=f"Attendance Overview for {selected_student['Name']}",
            color='Status',
            color_discrete_map={
                'Present': '#047857',
                'Absent': '#DC2626',
                'Late': '#D97706'
            },
            text_auto='.1f'
        )
        fig.update_layout(
            xaxis_title="Status",
            yaxis_title="Percentage (%)",
            yaxis=dict(range=[0, 100]),
            showlegend=False,
            height=300
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Attendance calendar view
        st.markdown('<h4 style="color: #1E40AF;">Attendance Log</h4>', unsafe_allow_html=True)
        
        student_attendance_display = student_attendance.copy()
        student_attendance_display['Date'] = student_attendance_display['Date'].dt.strftime('%b %d, %Y')
        student_attendance_display = student_attendance_display[['Date', 'Status']]
        
        # Add color to status
        def highlight_attendance(val):
            if val == 'Present':
                return 'background-color: #ECFDF5; color: #047857'
            elif val == 'Absent':
                return 'background-color: #FEF2F2; color: #DC2626'
            elif val == 'Late':
                return 'background-color: #FFFBEB; color: #D97706'
            return ''
        
        st.dataframe(student_attendance_display, use_container_width=True, hide_index=True)
        
        # Attendance actions
        attend_col1, attend_col2 = st.columns(2)
        
        with attend_col1:
            st.button("Record Attendance", key="record_attendance")
        
        with attend_col2:
            st.button("Send Attendance Report", key="send_attendance_report")
# Gradebook page
 
if selected == "Gradebook":
    st.markdown('<h1 class="dashboard-title">Gradebook Management</h1>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Class Gradebook", "Enter Grades", "Grade Analytics"])
    
    with tab1:
        # Class and subject filter
        col1, col2 = st.columns(2)
        
        with col1:
            selected_subject = st.selectbox("Select Subject", ["All Subjects", "Mathematics", "English", "Science"])
        
        with col2:
            sort_option = st.selectbox("Sort By", ["Name (A-Z)", "Name (Z-A)", "Score (High to Low)", "Score (Low to High)"])
        
        # Display subject data
        if selected_subject == "All Subjects":
            gradebook_data = st.session_state['students'][['ID', 'Name', 'Grade', 'Score']]
            
            # Add average subject scores
            subject_averages = st.session_state['subjects'].groupby('Student_ID')['Score'].mean().reset_index()
            subject_averages.columns = ['ID', 'Average_Subject_Score']
            
            gradebook_data = pd.merge(gradebook_data, subject_averages, on='ID', how='left')
            gradebook_data = gradebook_data.sort_values('Name')
        else:
            # Filter by subject
            subject_data = st.session_state['subjects'][st.session_state['subjects']['Subject'] == selected_subject]
            
            # Merge with student data
            gradebook_data = pd.merge(
                st.session_state['students'][['ID', 'Name']],
                subject_data[['Student_ID', 'Score', 'Grade']],
                left_on='ID',
                right_on='Student_ID',
                how='inner'
            )
            gradebook_data = gradebook_data[['ID', 'Name', 'Grade', 'Score']]
        
        # Apply sorting
        if sort_option == "Name (A-Z)":
            gradebook_data = gradebook_data.sort_values('Name')
        elif sort_option == "Name (Z-A)":
            gradebook_data = gradebook_data.sort_values('Name', ascending=False)
        elif sort_option == "Score (High to Low)":
            gradebook_data = gradebook_data.sort_values('Score', ascending=False)
        elif sort_option == "Score (Low to High)":
            gradebook_data = gradebook_data.sort_values('Score')
        
        # Display gradebook
        st.markdown(f"<h3>Gradebook for {selected_subject}</h3>", unsafe_allow_html=True)
        
        # Create styled table
        st.markdown("""
        <style>
        .grade-a-plus, .grade-a, .grade-a-minus {
            background-color: #DCFCE7;
            color: #047857;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
        }
        .grade-b-plus, .grade-b, .grade-b-minus {
            background-color: #DBEAFE;
            color: #1E40AF;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
        }
        .grade-c-plus, .grade-c, .grade-c-minus {
            background-color: #FEF3C7;
            color: #D97706;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
        }
        .grade-d-plus, .grade-d, .grade-d-minus, .grade-f {
            background-color: #FEE2E2;
            color: #B91C1C;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display with table formatting
        st.dataframe(
            gradebook_data,
            column_config={
                "ID": st.column_config.NumberColumn("Student ID"),
                "Name": st.column_config.TextColumn("Student Name"),
                "Grade": st.column_config.TextColumn("Grade Letter"),
                "Score": st.column_config.ProgressColumn(
                    "Score (%)",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Class statistics
        st.markdown('<h3 class="section-header">Class Statistics</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_score = gradebook_data['Score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with col2:
            median_score = gradebook_data['Score'].median()
            st.metric("Median Score", f"{median_score:.1f}%")
        
        with col3:
            highest_score = gradebook_data['Score'].max()
            st.metric("Highest Score", f"{highest_score:.1f}%")
        
        with col4:
            lowest_score = gradebook_data['Score'].min()
            st.metric("Lowest Score", f"{lowest_score:.1f}%")
        
        # Export options
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_link = st.markdown(
                download_link(gradebook_data, f'gradebook_{selected_subject.lower().replace(" ", "_")}.csv', 'Export Gradebook (CSV)'),
                unsafe_allow_html=True)
        
        with col2:
            if st.button("Print Gradebook"):
                st.info("Preparing gradebook for printing...")
                st.success("Gradebook sent to printer!")
    
    with tab2:
        st.markdown('<h2 class="section-header">Enter Student Grades</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_subject = st.selectbox("Subject", ["Mathematics", "English", "Science"], key="grade_subject")
            grade_assignment = st.text_input("Assignment Name", placeholder="Midterm Exam", key="grade_assignment")
            grade_date = st.date_input("Assignment Date", value=pd.Timestamp("2025-04-10"), key="grade_date")
            grade_points = st.number_input("Total Points Possible", min_value=1, max_value=100, value=100, key="grade_points")
        
        with col2:
            grade_weight = st.slider("Assignment Weight (%)", min_value=0, max_value=100, value=10, key="grade_weight")
            grade_category = st.selectbox("Assignment Category", 
                                         ["Exam", "Quiz", "Homework", "Project", "Participation"], 
                                         key="grade_category")
            st.markdown("""
            <div class="custom-info-box">
                <h4 style="margin-top: 0; color: #1E40AF;">Grading Tips</h4>
                <ul style="margin-bottom: 0; font-size: 0.9rem;">
                    <li>Use consistent grading criteria</li>
                    <li>Provide specific feedback when possible</li>
                    <li>Consider using rubrics for complex assignments</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">Student Scores</h3>', unsafe_allow_html=True)
        
        # Create editable dataframe for grades
        students_for_grading = st.session_state['students'][['ID', 'Name']].sort_values('Name')
        students_for_grading['Score'] = 0
        students_for_grading['Submitted'] = True
        
        # Show as an editable dataframe
        edited_df = st.data_editor(
            students_for_grading,
            column_config={
                "ID": st.column_config.NumberColumn("Student ID", disabled=True),
                "Name": st.column_config.TextColumn("Student Name", disabled=True),
                "Score": st.column_config.NumberColumn(
                    "Score",
                    min_value=0,
                    max_value=grade_points,
                    step=1,
                    format="%d",
                ),
                "Submitted": st.column_config.CheckboxColumn("Submitted"),
            },
            use_container_width=True,
            hide_index=True,
            num_rows="fixed"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Save Grades", type="primary"):
                loading_animation()
                st.success("Grades saved successfully!")
        
        with col2:
            if st.button("Clear All"):
                st.info("Form cleared. Enter new grades.")
        
        with col3:
            st.markdown("""
            <div class="custom-info-box" style="margin-top: 10px;">
                <p style="margin: 0; font-size: 0.9rem;">
                    💡 <strong>Quick actions:</strong> 
                    <a href="#" style="color: #2563EB; text-decoration: none;">Set all to maximum</a> | 
                    <a href="#" style="color: #2563EB; text-decoration: none;">Mark all as submitted</a> | 
                    <a href="#" style="color: #2563EB; text-decoration: none;">Import from CSV</a>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-header">Grade Analytics</h2>', unsafe_allow_html=True)
        
        # Subject selection for analytics
        analytics_subject = st.selectbox(
            "Select Subject for Analysis",
            ["All Subjects", "Mathematics", "English", "Science"],
            key="analytics_subject"
        )
        
        # Prepare data based on subject selection
        if analytics_subject == "All Subjects":
            analytics_data = st.session_state['subjects']
        else:
            analytics_data = st.session_state['subjects'][st.session_state['subjects']['Subject'] == analytics_subject]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Grade distribution chart
            grade_counts = analytics_data['Grade'].apply(lambda x: x[0] if len(x) > 0 else '').value_counts()
            
            fig = px.bar(
                x=grade_counts.index,
                y=grade_counts.values,
                title=f"Grade Distribution - {analytics_subject}",
                labels={'x': 'Grade', 'y': 'Number of Students'},
                color=grade_counts.index,
                color_discrete_map={
                    'A': '#047857',
                    'B': '#2563EB',
                    'C': '#D97706',
                    'D': '#DC2626',
                    'F': '#7F1D1D'
                }
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Score distribution histogram
            fig = px.histogram(
                analytics_data,
                x='Score',
                nbins=10,
                title=f"Score Distribution - {analytics_subject}",
                labels={'Score': 'Score (%)', 'count': 'Number of Students'},
                color_discrete_sequence=['#3B82F6']
            )
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
        
        # Score statistics
        st.markdown('<h3 class="section-header">Score Statistics</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_score = analytics_data['Score'].mean()
            st.metric("Average", f"{avg_score:.1f}%")
        
        with col2:
            median_score = analytics_data['Score'].median()
            st.metric("Median", f"{median_score:.1f}%")
        
        with col3:
            std_dev = analytics_data['Score'].std()
            st.metric("Std Dev", f"{std_dev:.1f}")
        
        with col4:
            high_score = analytics_data['Score'].max()
            st.metric("Highest", f"{high_score:.1f}%")
        
        with col5:
            low_score = analytics_data['Score'].min()
            st.metric("Lowest", f"{low_score:.1f}%")
        
        # Performance comparison
        st.markdown('<h3 class="section-header">Subject Performance Comparison</h3>', unsafe_allow_html=True)
        
        # Calculate average scores by subject
        subject_avgs = st.session_state['subjects'].groupby('Subject')['Score'].mean().reset_index()
        
        fig = px.bar(
            subject_avgs,
            x='Subject',
            y='Score',
            title="Average Score by Subject",
            color='Subject',
            text='Score'
        )
        fig.update_layout(showlegend=False, yaxis=dict(range=[70, 100]))
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Grade improvement suggestions
        st.markdown("""
        <div class="grade-card">
            <h3 style="margin-top: 0; color: #1E40AF;">Grade Improvement Suggestions</h3>
            <div style="font-size: 0.9rem;">
                <p><strong>Based on the grade distribution:</strong></p>
                <ul>
                    <li>Consider providing additional support for students in the C and D range</li>
                    <li>Review material for topics where students consistently score lower</li>
                    <li>Implement peer tutoring where high-performing students can assist others</li>
                    <li>Create targeted review sessions for challenging concepts</li>
                    <li>Consider alternative assessment methods to accommodate different learning styles</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Performance page
elif selected == "Performance":
    st.markdown('<h1 class="dashboard-title">Student Performance Analysis</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Performance Trends", "Student Comparison", "Subject Analysis"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Progress Over Time</h2>', unsafe_allow_html=True)
        
        # Filter controls
        col1, col2 = st.columns(2)
        
        with col1:
            trend_subject = st.selectbox("Select Subject", ["All Subjects", "Mathematics", "English", "Science"], key="trend_subject")
        
        with col2:
            trend_student = st.multiselect(
                "Select Students (leave empty for class average)",
                options=st.session_state['students']['Name'].tolist(),
                default=[],
                key="trend_student"
            )
        
        # Prepare trend data
        if trend_subject == "All Subjects":
            trend_data = st.session_state['progress'].copy()
        else:
            trend_data = st.session_state['progress'][st.session_state['progress']['Subject'] == trend_subject].copy()
        
        # Progress chart
        if not trend_student:  # Show class average
            avg_by_month = trend_data.groupby(['Month', 'Subject'])['Score'].mean().reset_index()
            
            fig = px.line(
                avg_by_month,
                x='Month',
                y='Score',
                color='Subject',
                title="Class Average Score Trend",
                markers=True,
                labels={'Score': 'Average Score (%)', 'Month': 'Month'}
            )
            fig.update_layout(yaxis=dict(range=[70, 100]))
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="custom-info-box">
                <h4 style="margin-top: 0; color: #1E40AF;">Class Progress Insights</h4>
                <ul style="margin-bottom: 0;">
                    <li>Overall improvement trend observed across all subjects</li>
                    <li>Mathematics showing the most significant improvement</li>
                    <li>English scores have been consistently high</li>
                    <li>Science had initial challenges but showing steady growth</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        else:  # Show selected students
            # Get student IDs for selected names
            student_ids = st.session_state['students'][st.session_state['students']['Name'].isin(trend_student)]['ID'].tolist()
            student_data = trend_data[trend_data['Student_ID'].isin(student_ids)]
            
            # Merge student names for display
            student_names = st.session_state['students'][['ID', 'Name']]
            student_names.columns = ['Student_ID', 'Name']
            student_data = pd.merge(student_data, student_names, on='Student_ID', how='left')
            
            fig = px.line(
                student_data,
                x='Month',
                y='Score',
                color='Name',
                line_group='Name',
                title="Student Score Trends",
                markers=True,
                labels={'Score': 'Score (%)', 'Month': 'Month'},
                facet_col='Subject' if trend_subject == "All Subjects" else None
            )
            fig.update_layout(yaxis=dict(range=[60, 100]))
            st.plotly_chart(fig, use_container_width=True)
            
            # Student-specific insights
            st.markdown("""
            <div class="custom-info-box">
                <h4 style="margin-top: 0; color: #1E40AF;">Student Progress Insights</h4>
                <p>Analyzing selected student performance trends:</p>
                <ul style="margin-bottom: 0;">
                    <li>Most selected students show steady improvement over time</li>
                    <li>Different learning paces observed among students</li>
                    <li>Consider personalized interventions for students with inconsistent trends</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Performance factors
        st.markdown('<h3 class="section-header">Performance Factors Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate correlation between attendance and score
            attendance_correlation = np.corrcoef(
                st.session_state['students']['Attendance'], 
                st.session_state['students']['Score']
            )[0, 1]
            
            fig = px.scatter(
                st.session_state['students'],
                x='Attendance',
                y='Score',
                title=f"Attendance vs. Score (Correlation: {attendance_correlation:.2f})",
                color='Grade',
                hover_data=['Name'],
                trendline="ols",
                labels={'Attendance': 'Attendance Rate (%)', 'Score': 'Overall Score (%)'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Behavior vs. score
            behavior_map = {
                'Excellent': 4,
                'Good': 3,
                'Fair': 2,
                'Needs Improvement': 1
            }
            st.session_state['students']['Behavior_Score'] = st.session_state['students']['Behavior'].map(behavior_map)
            
            behavior_groups = st.session_state['students'].groupby('Behavior')['Score'].mean().reset_index()
            
            fig = px.bar(
                behavior_groups,
                x='Behavior',
                y='Score',
                title="Average Score by Behavior Rating",
                color='Behavior',
                text='Score',
                color_discrete_map={
                    'Excellent': '#047857',
                    'Good': '#2563EB',
                    'Fair': '#D97706',
                    'Needs Improvement': '#DC2626'
                },
                category_orders={"Behavior": ["Excellent", "Good", "Fair", "Needs Improvement"]},
                labels={'Behavior': 'Behavior Rating', 'Score': 'Average Score (%)'}
            )
            fig.update_layout(showlegend=False, height=350)
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations based on analysis
        st.markdown("""
        <div class="grade-card">
            <h3 style="margin-top: 0; color: #1E40AF;">Performance Improvement Recommendations</h3>
            <div style="font-size: 0.9rem;">
                <p><strong>Based on data analysis:</strong></p>
                <ol>
                    <li><strong>Attendance Focus:</strong> Strong correlation between attendance and performance suggests implementing attendance incentives and follow-ups for frequent absences.</li>
                    <li><strong>Behavior Support:</strong> Students with "Fair" or "Needs Improvement" behavior ratings would benefit from behavioral intervention plans and positive reinforcement strategies.</li>
                    <li><strong>Subject-Specific Strategies:</strong> Identify subjects with lower overall performance and develop targeted instructional approaches.</li>
                    <li><strong>Progress Monitoring:</strong> Continue tracking individual student progress to identify early warning signs and provide timely interventions.</li>
                </ol>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">Student Performance Comparison</h2>', unsafe_allow_html=True)
        
        # Student selection
        col1, col2 = st.columns(2)
        
        with col1:
            student1 = st.selectbox("Select First Student", st.session_state['students']['Name'].tolist(), index=0)
        
        with col2:
            # Exclude first student from options
            remaining_students = st.session_state['students'][st.session_state['students']['Name'] != student1]['Name'].tolist()
            student2 = st.selectbox("Select Second Student", remaining_students, index=0)
        
        # Get student data
        student1_data = st.session_state['students'][st.session_state['students']['Name'] == student1].iloc[0]
        student2_data = st.session_state['students'][st.session_state['students']['Name'] == student2].iloc[0]
        
        student1_id = student1_data['ID']
        student2_id = student2_data['ID']
        
        # Get subject data for both students
        student1_subjects = st.session_state['subjects'][st.session_state['subjects']['Student_ID'] == student1_id]
        student2_subjects = st.session_state['subjects'][st.session_state['subjects']['Student_ID'] == student2_id]
        
        # Combine subject data
        student1_subjects['Student'] = student1
        student2_subjects['Student'] = student2
        combined_subjects = pd.concat([student1_subjects, student2_subjects])
        
        # Subject comparison chart
        fig = px.bar(
            combined_subjects,
            x='Subject',
            y='Score',
            color='Student',
            barmode='group',
            title=f"Subject Performance Comparison: {student1} vs {student2}",
            labels={'Score': 'Score (%)', 'Subject': 'Subject'}
        )
        fig.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)
        
        # Overall comparison
        st.markdown('<h3 class="section-header">Overall Comparison</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Student 1 card
            st.markdown(f"""
            <div class="grade-card">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="background-color: #3B82F6; color: white; width: 50px; height: 50px; 
                              border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                              font-weight: bold; font-size: 20px; margin-right: 15px;">
                        {student1_data['Name'].split()[0][0]}{student1_data['Name'].split()[1][0]}
                    </div>
                    <div>
                        <div style="font-weight: 600; color: #1E3A8A; font-size: 1.2rem;">{student1_data['Name']}</div>
                        <div style="color: #6B7280;">ID: {student1_data['ID']}</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Grade</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student1_data['Grade']}</div>
                    </div>
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Score</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student1_data['Score']}%</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Attendance</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student1_data['Attendance']}%</div>
                    </div>
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Behavior</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student1_data['Behavior']}</div>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <div style="font-weight: 500;">Strengths</div>
                    <p style="margin-top: 5px; margin-bottom: 10px;">{student1_data['Strengths']}</p>
                    
                    <div style="font-weight: 500;">Areas for Improvement</div>
                    <p style="margin-top: 5px; margin-bottom: 0;">{student1_data['Weaknesses']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Student 2 card
            st.markdown(f"""
            <div class="grade-card">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="background-color: #8B5CF6; color: white; width: 50px; height: 50px; 
                              border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                              font-weight: bold; font-size: 20px; margin-right: 15px;">
                        {student2_data['Name'].split()[0][0]}{student2_data['Name'].split()[1][0]}
                    </div>
                    <div>
                        <div style="font-weight: 600; color: #1E3A8A; font-size: 1.2rem;">{student2_data['Name']}</div>
                        <div style="color: #6B7280;">ID: {student2_data['ID']}</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Grade</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student2_data['Grade']}</div>
                    </div>
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Score</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student2_data['Score']}%</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Attendance</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student2_data['Attendance']}%</div>
                    </div>
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Behavior</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{student2_data['Behavior']}</div>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <div style="font-weight: 500;">Strengths</div>
                    <p style="margin-top: 5px; margin-bottom: 10px;">{student2_data['Strengths']}</p>
                    
                    <div style="font-weight: 500;">Areas for Improvement</div>
                    <p style="margin-top: 5px; margin-bottom: 0;">{student2_data['Weaknesses']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Comparative analysis
        st.markdown('<h3 class="section-header">Comparative Analysis</h3>', unsafe_allow_html=True)
        
        # Comparative analysis - complete the section that was cut off
        
        # Calculate differences between students
        score_diff = abs(student1_data['Score'] - student2_data['Score'])
        attendance_diff = abs(student1_data['Attendance'] - student2_data['Attendance'])
        
        # Subject differences
        subject_diff = pd.merge(
            student1_subjects[['Subject', 'Score']].rename(columns={'Score': 'Student1_Score'}),
            student2_subjects[['Subject', 'Score']].rename(columns={'Score': 'Student2_Score'}),
            on='Subject',
            how='outer'
        )
        subject_diff['Difference'] = abs(subject_diff['Student1_Score'] - subject_diff['Student2_Score'])
        
        # Display radar chart for comparing multiple metrics
        categories = ['Mathematics', 'English', 'Science', 'Attendance', 'Behavior_Score']
        
        # Prepare data for radar chart
        student1_metrics = []
        student2_metrics = []
        
        # Get subject scores
        for subject in ['Mathematics', 'English', 'Science']:
            s1_score = student1_subjects[student1_subjects['Subject'] == subject]['Score'].values
            student1_metrics.append(s1_score[0] if len(s1_score) > 0 else 0)
            
            s2_score = student2_subjects[student2_subjects['Subject'] == subject]['Score'].values
            student2_metrics.append(s2_score[0] if len(s2_score) > 0 else 0)
        
        # Add attendance and behavior
        student1_metrics.append(student1_data['Attendance'])
        student1_metrics.append(student1_data['Behavior_Score'] * 25)  # Scale behavior score
        
        student2_metrics.append(student2_data['Attendance'])
        student2_metrics.append(student2_data['Behavior_Score'] * 25)  # Scale behavior score
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=student1_metrics,
            theta=categories,
            fill='toself',
            name=student1
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=student2_metrics,
            theta=categories,
            fill='toself',
            name=student2
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Multi-dimensional Comparison",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Personalized recommendations
        st.markdown("""
        <div class="custom-info-box">
            <h4 style="margin-top: 0; color: #1E40AF;">Personalized Learning Recommendations</h4>
            <p>Based on student comparison analysis:</p>
            <ul style="margin-bottom: 0;">
                <li><strong>Peer Learning Opportunities:</strong> Students can benefit from collaborative projects that leverage complementary strengths</li>
                <li><strong>Target Interventions:</strong> Focus additional support on areas with significant performance gaps</li>
                <li><strong>Success Strategies:</strong> Identify and share effective learning strategies between students</li>
                <li><strong>Mentorship:</strong> Consider peer mentoring where one student excels in areas the other struggles with</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-header">Subject Analysis</h2>', unsafe_allow_html=True)
        
        # Subject selection
        subject_analysis = st.selectbox(
            "Select Subject",
            ["Mathematics", "English", "Science"],
            key="subject_analysis"
        )
        
        # Get subject data
        subject_data = st.session_state['subjects'][st.session_state['subjects']['Subject'] == subject_analysis]
        
        # Student performance in selected subject
        student_names = st.session_state['students'][['ID', 'Name']]
        student_names.columns = ['Student_ID', 'Name']
        subject_data = pd.merge(subject_data, student_names, on='Student_ID', how='left')
        
        # Top and bottom performers
        top_performers = subject_data.sort_values('Score', ascending=False).head(5)
        bottom_performers = subject_data.sort_values('Score').head(5)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<h3 class="section-header">Top Performers in {subject_analysis}</h3>', unsafe_allow_html=True)
            
            for i, row in top_performers.iterrows():
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 10px; margin-bottom: 8px; background-color: #F0F9FF; border-radius: 8px;">
                    <div style="font-weight: 600; margin-right: 10px; color: #0369A1; width: 20px; text-align: center;">
                        {i+1}
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 500;">{row['Name']}</div>
                    </div>
                    <div style="font-weight: 600; color: #0369A1;">
                        {row['Score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<h3 class="section-header">Students Needing Support in {subject_analysis}</h3>', unsafe_allow_html=True)
            
            for i, row in bottom_performers.iterrows():
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 10px; margin-bottom: 8px; background-color: #FEF2F2; border-radius: 8px;">
                    <div style="font-weight: 600; margin-right: 10px; color: #DC2626; width: 20px; text-align: center;">
                        {i+1}
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 500;">{row['Name']}</div>
                    </div>
                    <div style="font-weight: 600; color: #DC2626;">
                        {row['Score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Grade distribution
        st.markdown(f'<h3 class="section-header">{subject_analysis} Grade Distribution</h3>', unsafe_allow_html=True)
        
        grade_counts = subject_data['Grade'].value_counts().reset_index()
        grade_counts.columns = ['Grade', 'Count']
        
        # Order grades properly
        grade_order = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
        grade_counts['Grade_Order'] = grade_counts['Grade'].apply(lambda x: grade_order.index(x) if x in grade_order else 99)
        grade_counts = grade_counts.sort_values('Grade_Order')
        
        # Define grade colors
        grade_colors = {
            'A+': '#047857', 'A': '#047857', 'A-': '#047857',
            'B+': '#2563EB', 'B': '#2563EB', 'B-': '#2563EB',
            'C+': '#D97706', 'C': '#D97706', 'C-': '#D97706',
            'D+': '#DC2626', 'D': '#DC2626', 'D-': '#DC2626',
            'F': '#7F1D1D'
        }
        
        fig = px.bar(
            grade_counts,
            x='Grade',
            y='Count',
            title=f"Grade Distribution - {subject_analysis}",
            color='Grade',
            color_discrete_map=grade_colors,
            text='Count',
            labels={'Count': 'Number of Students', 'Grade': 'Grade'}
        )
        fig.update_layout(showlegend=False, xaxis={'categoryorder': 'array', 'categoryarray': grade_order})
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Subject insights and recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            # Subject statistics
            avg_score = subject_data['Score'].mean()
            median_score = subject_data['Score'].median()
            std_dev = subject_data['Score'].std()
            passing_rate = len(subject_data[subject_data['Score'] >= 60]) / len(subject_data) * 100
            excellence_rate = len(subject_data[subject_data['Score'] >= 90]) / len(subject_data) * 100
            
            st.markdown(f"""
            <div class="grade-card">
                <h3 style="margin-top: 0; color: #1E40AF;">{subject_analysis} Statistics</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Average Score</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{avg_score:.1f}%</div>
                    </div>
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Median Score</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{median_score:.1f}%</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Standard Deviation</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{std_dev:.1f}</div>
                    </div>
                    <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #6B7280;">Passing Rate</div>
                        <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{passing_rate:.1f}%</div>
                    </div>
                </div>
                <div style="padding: 8px; background-color: #F3F4F6; border-radius: 8px; text-align: center; margin-top: 10px;">
                    <div style="font-size: 0.8rem; color: #6B7280;">Excellence Rate (A grades)</div>
                    <div style="font-weight: 600; color: #1E40AF; font-size: 1.2rem;">{excellence_rate:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Subject recommendations
            st.markdown(f"""
            <div class="grade-card">
                <h3 style="margin-top: 0; color: #1E40AF;">{subject_analysis} Action Plan</h3>
                <div style="font-size: 0.9rem;">
                    <p><strong>Based on current performance data:</strong></p>
                    <ol style="padding-left: 20px;">
                        <li>Identify specific topics where students are struggling through item analysis</li>
                        <li>Implement targeted intervention for students scoring below 70%</li>
                        <li>Develop extension activities for high performers to maintain engagement</li>
                        <li>Review teaching strategies for concepts with below-average performance</li>
                        <li>Consider peer tutoring where appropriate</li>
                        <li>Schedule parent-teacher conferences for students needing support</li>
                    </ol>
                    <p><strong>Next Steps:</strong> Schedule departmental meeting to discuss these findings and develop a coordinated approach.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Score distribution histogram
        st.markdown(f'<h3 class="section-header">{subject_analysis} Score Distribution</h3>', unsafe_allow_html=True)
        
        fig = px.histogram(
            subject_data,
            x='Score',
            nbins=20,
            title=f"Score Distribution - {subject_analysis}",
            labels={'Score': 'Score (%)', 'count': 'Number of Students'},
            color_discrete_sequence=['#3B82F6']
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation with other subjects
        st.markdown('<h3 class="section-header">Cross-Subject Correlation</h3>', unsafe_allow_html=True)
        
        # Prepare data for correlation analysis
        all_subjects = st.session_state['subjects'].copy()
        subject_pivot = all_subjects.pivot(index='Student_ID', columns='Subject', values='Score')
        
        correlation_matrix = subject_pivot.corr()
        
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            color_continuous_scale='RdBu',
            title="Subject Score Correlation Matrix",
            labels={'color': 'Correlation'}
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Correlation"))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="custom-info-box">
            <h4 style="margin-top: 0; color: #1E40AF;">Correlation Insights</h4>
            <p>Understanding how performance across subjects correlates can help identify:</p>
            <ul style="margin-bottom: 0;">
                <li>Students with consistent performance across all subjects</li>
                <li>Students who excel in specific areas but struggle in others</li>
                <li>Potential interdisciplinary teaching opportunities</li>
                <li>Common skills that affect performance across multiple subjects</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Student profiles page
elif selected == "Student Profiles":
    st.markdown('<h1 class="dashboard-title">Student Profiles</h1>', unsafe_allow_html=True)
    
    # Student search and filter options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search Students", placeholder="Enter name or ID")
    
    with col2:
        filter_grade = st.selectbox(
            "Filter by Grade",
            ["All Grades", "A", "B", "C", "D", "F"],
            index=0
        )
    
    with col3:
        sort_option = st.selectbox(
            "Sort By",
            ["Name (A-Z)", "Name (Z-A)", "Score (High to Low)", "Score (Low to High)"],
            index=0
        )
    
    # Apply filters
    filtered_students = st.session_state['students'].copy()
    
    if search_term:
        filtered_students = filtered_students[
            filtered_students['Name'].str.contains(search_term, case=False) | 
            filtered_students['ID'].astype(str).str.contains(search_term)
        ]
    
    if filter_grade != "All Grades":
        filtered_students = filtered_students[filtered_students['Grade'].str.startswith(filter_grade)]
    
    # Apply sorting
    if sort_option == "Name (A-Z)":
        filtered_students = filtered_students.sort_values('Name')
    elif sort_option == "Name (Z-A)":
        filtered_students = filtered_students.sort_values('Name', ascending=False)
    elif sort_option == "Score (High to Low)":
        filtered_students = filtered_students.sort_values('Score', ascending=False)
    elif sort_option == "Score (Low to High)":
        filtered_students = filtered_students.sort_values('Score')
    
    # Display student count
    st.markdown(f"<p>Displaying {len(filtered_students)} students</p>", unsafe_allow_html=True)
    
    # Student cards with 3 per row
    for i in range(0, len(filtered_students), 3):
        cols = st.columns(3)
        
        for j in range(3):
            if i + j < len(filtered_students):
                student = filtered_students.iloc[i + j]
                
                # Get grade color
                grade_letter = student['Grade'][0] if len(student['Grade']) > 0 else ''
                
                if grade_letter == 'A':
                    grade_bg_color = '#DCFCE7'
                    grade_text_color = '#047857'
                elif grade_letter == 'B':
                    grade_bg_color = '#DBEAFE'
                    grade_text_color = '#1E40AF'
                elif grade_letter == 'C':
                    grade_bg_color = '#FEF3C7'
                    grade_text_color = '#D97706'
                else:
                    grade_bg_color = '#FEE2E2'
                    grade_text_color = '#B91C1C'
                
                # Get student's subjects
                student_subjects = st.session_state['subjects'][st.session_state['subjects']['Student_ID'] == student['ID']]
                
                with cols[j]:
                    st.markdown(f"""
                    <div class="student-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div style="display: flex; align-items: center;">
                                <div style="background-color: #3B82F6; color: white; width: 40px; height: 40px; 
                                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                        font-weight: bold; font-size: 16px; margin-right: 10px;">
                                    {student['Name'].split()[0][0]}{student['Name'].split()[1][0]}
                                </div>
                                <div>
                                    <div style="font-weight: 600; color: #1E3A8A; font-size: 1.1rem;">{student['Name']}</div>
                                    <div style="color: #6B7280; font-size: 0.8rem;">ID: {student['ID']}</div>
                                </div>
                            </div>
                            <div style="background-color: {grade_bg_color}; color: {grade_text_color}; 
                                    padding: 5px 12px; border-radius: 20px; font-weight: 600; min-width: 36px; text-align: center;">
                                {student['Grade']}
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px;">
                            <div style="padding: 6px; background-color: #F3F4F6; border-radius: 6px; text-align: center;">
                                <div style="font-size: 0.7rem; color: #6B7280;">Overall Score</div>
                                <div style="font-weight: 600; color: #1E40AF; font-size: 1rem;">{student['Score']}%</div>
                            </div>
                            <div style="padding: 6px; background-color: #F3F4F6; border-radius: 6px; text-align: center;">
                                <div style="font-size: 0.7rem; color: #6B7280;">Attendance</div>
                                <div style="font-weight: 600; color: #1E40AF; font-size: 1rem;">{student['Attendance']}%</div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px;">
                            <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 5px;">Subject Scores</div>
                            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 5px; font-size: 0.85rem;">
                    """, unsafe_allow_html=True)
                    
                    # Display subject scores
                    for _, subj in student_subjects.iterrows():
                        st.markdown(f"""
                        <div>{subj['Subject']}</div>
                        <div style="text-align: right; font-weight: 500;">{subj['Score']}%</div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                            </div>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <button style="background-color: #EFF6FF; color: #2563EB; border: none; 
                                    padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer;">
                                View Details
                            </button>
                            <button style="background-color: #EFF6FF; color: #2563EB; border: none; 
                                    padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer;">
                                Contact
                            </button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Add new student section
    st.markdown('<h2 class="section-header">Add New Student</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Full Name", placeholder="Enter student name")
        new_id = st.number_input("Student ID", min_value=1000, max_value=9999, value=1000)
        new_grade = st.selectbox("Grade Level", ["9th Grade", "10th Grade", "11th Grade", "12th Grade"])
    
    with col2:
        new_dob = st.date_input("Date of Birth", value=pd.Timestamp("2010-01-01"))
        new_gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        new_address = st.text_input("Address", placeholder="Enter student address")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_guardian = st.text_input("Parent/Guardian Name", placeholder="Enter guardian name")
    
    with col2:
        new_phone = st.text_input("Contact Phone", placeholder="Enter phone number")
    
    with col3:
        new_email = st.text_input("Contact Email", placeholder="Enter email address")
    
    if st.button("Add Student", type="primary"):
        loading_animation()
        st.success("New student added successfully!")

# Reports page
elif selected == "Reports":
    st.markdown('<h1 class="dashboard-title">Academic Reports</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Progress Reports", "Report Cards", "Custom Reports"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Generate Progress Reports</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_period = st.selectbox(
                "Reporting Period",
                ["Q1 (Aug-Oct)", "Q2 (Nov-Jan)", "Q3 (Feb-Apr)", "Q4 (May-Jun)"],
                index=2
            )
            
            report_subject = st.selectbox(
                "Subject",
                ["All Subjects", "Mathematics", "English", "Science"],
                index=0
            )
        
        with col2:
            report_students = st.multiselect(
                "Select Students (leave empty for all)",
                options=st.session_state['students']['Name'].tolist(),
                default=[]
            )
            
            include_comments = st.checkbox("Include Teacher Comments", value=True)
        
        # Report preview
        st.markdown('<h3 class="section-header">Report Preview</h3>', unsafe_allow_html=True)
        
        if not report_students:  # If no specific students selected, show class summary
            st.markdown(f"""
            <div class="report-preview">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 1.5rem; font-weight: 600; color: #1E3A8A;">CLASS PROGRESS REPORT</div>
                    <div style="font-size: 1.2rem; color: #4B5563;">{report_period} - {report_subject}</div>
                    <div style="font-size: 0.9rem; color: #6B7280;">Generated on April 10, 2025</div>
                    <div style="margin-bottom: 20px;">
                    <div style="font-weight: 600; margin-bottom: 5px;">Class Overview</div>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #F3F4F6;">
                            <th style="padding: 8px; text-align: left; border: 1px solid #E5E7EB;">Subject</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Class Average</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Median Score</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Highest Score</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Lowest Score</th>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Mathematics</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">83.6%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">85.0%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">96.2%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">68.7%</td>
                        </tr>
                        <tr style="background-color: #F9FAFB;">
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">English</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">87.2%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">88.5%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">97.8%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">72.3%</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Science</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">81.9%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">82.7%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">95.1%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">67.0%</td>
                        </tr>
                        <tr style="background-color: #F9FAFB; font-weight: 600;">
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">OVERALL</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">84.2%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">85.4%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">96.4%</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">69.3%</td>
                        </tr>
                    </table>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div style="font-weight: 600; margin-bottom: 5px;">Grade Distribution</div>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #F3F4F6;">
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Grade</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">A</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7# Continuation of Reports page - Grade Distribution table
EB;">B</th>
            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">C</th>
            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">D</th>
            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">F</th>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #E5E7EB;">Number of Students</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">12</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">8</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">5</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">2</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">0</td>
        </tr>
        <tr style="background-color: #F9FAFB;">
            <td style="padding: 8px; border: 1px solid #E5E7EB;">Percentage</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">44.4%</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">29.6%</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">18.5%</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">7.4%</td>
            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">0.0%</td>
        </tr>
    </table>
</div>

<div style="margin-bottom: 20px;">
    <div style="font-weight: 600; margin-bottom: 5px;">Key Observations</div>
    <ul style="margin-top: 5px; padding-left: 20px;">
        <li>Overall class performance is strong with 74% of students achieving B or above</li>
        <li>Mathematics shows the widest performance spread among the subjects</li>
        <li>No failing grades recorded in any subject this quarter</li>
        <li>English has the highest average performance across all subjects</li>
    </ul>
</div>

<div style="margin-top: 25px;">
    <div style="font-weight: 600; margin-bottom: 5px;">Recommendations</div>
    <ol style="margin-top: 5px; padding-left: 20px;">
        <li>Provide additional support for students in the D range</li>
        <li>Maintain current teaching strategies for English</li>
        <li>Consider targeted intervention for mathematics</li>
        <li>Schedule parent-teacher conferences for the lowest 5 performers</li>
    </ol>
</div>
"""
, unsafe_allow_html=True)

            if st.button("Generate Class Report", type="primary"):
                loading_animation()
                st.success("Class report generated successfully!")
        
        else:  # If specific students selected
            student = st.session_state['students'][st.session_state['students']['Name'] == report_students[0]].iloc[0]
            student_subjects = st.session_state['subjects'][st.session_state['subjects']['Student_ID'] == student['ID']]
            
            st.markdown(f"""
            <div class="report-preview">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 1.5rem; font-weight: 600; color: #1E3A8A;">STUDENT PROGRESS REPORT</div>
                    <div style="font-size: 1.2rem; color: #4B5563;">{report_period}</div>
                    <div style="font-size: 0.9rem; color: #6B7280;">Generated on April 10, 2025</div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                    <div>
                        <div><strong>Student:</strong> {student['Name']}</div>
                        <div><strong>ID:</strong> {student['ID']}</div>
                        <div><strong>Grade Level:</strong> 10th Grade</div>
                    </div>
                    <div>
                        <div><strong>Overall Grade:</strong> {student['Grade']}</div>
                        <div><strong>Attendance:</strong> {student['Attendance']}%</div>
                        <div><strong>Behavior Score:</strong> {student['Behavior_Score']}/4</div>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div style="font-weight: 600; margin-bottom: 5px;">Academic Performance</div>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #F3F4F6;">
                            <th style="padding: 8px; text-align: left; border: 1px solid #E5E7EB;">Subject</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Current Score</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Previous Score</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Change</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Grade</th>
                        </tr>
            """, unsafe_allow_html=True)
            
            # Display subject scores
            for i, subj in enumerate(student_subjects.iterrows()):
                subj = subj[1]
                prev_score = subj['Score'] - random.uniform(-5, 5)  # Simulated previous score
                change = subj['Score'] - prev_score
                bg_color = "#F9FAFB" if i % 2 == 1 else "white"
                change_color = "#047857" if change >= 0 else "#DC2626"
                change_arrow = "↑" if change >= 0 else "↓"
                
                st.markdown(f"""
                <tr style="background-color: {bg_color};">
                    <td style="padding: 8px; border: 1px solid #E5E7EB;">{subj['Subject']}</td>
                    <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{subj['Score']:.1f}%</td>
                    <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{prev_score:.1f}%</td>
                    <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB; color: {change_color};">
                        {change_arrow} {abs(change):.1f}%
                    </td>
                    <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{subj['Grade']}</td>
                </tr>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                    </table>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div style="font-weight: 600; margin-bottom: 5px;">Teacher Comments</div>
                    <div style="border: 1px solid #E5E7EB; border-radius: 4px; padding: 10px; background-color: #F9FAFB;">
                        <p><strong>Mathematics:</strong> {student['Name'].split()[0]} demonstrates strong analytical skills and has shown improvement in problem-solving techniques. Continue practicing word problems.</p>
                        <p><strong>English:</strong> Excellent writing skills with thoughtful analysis. Work on developing more concise arguments in essays.</p>
                        <p><strong>Science:</strong> Good understanding of concepts. Participation in class discussions has improved significantly this quarter.</p>
                    </div>
                </div>
                
                <div style="margin-top: 25px;">
                    <div style="font-weight: 600; margin-bottom: 5px;">Goals for Next Quarter</div>
                    <ol style="margin-top: 5px; padding-left: 20px;">
                        <li>Improve note-taking organization</li>
                        <li>Continue to build on recent progress in Science</li>
                        <li>Maintain consistent study schedule</li>
                    </ol>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Download Report", type="primary"):
                    loading_animation()
                    st.success("Report downloaded successfully!")
            with col2:
                if st.button("Email to Parents"):
                    loading_animation()
                    st.success("Report emailed to parents successfully!")

    with tab2:
        st.markdown('<h2 class="section-header">Report Cards</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            rc_period = st.selectbox(
                "Semester",
                ["Semester 1 (Fall)", "Semester 2 (Spring)"],
                index=0,
                key="rc_period"
            )
            
            rc_format = st.selectbox(
                "Report Format",
                ["Standard", "Detailed", "Summary"],
                index=0
            )
        
        with col2:
            rc_student = st.selectbox(
                "Select Student",
                options=st.session_state['students']['Name'].tolist(),
                key="rc_student"
            )
            
            include_graph = st.checkbox("Include Performance Graph", value=True)
        
        # Report card preview
        st.markdown('<h3 class="section-header">Report Card Preview</h3>', unsafe_allow_html=True)
        
        student = st.session_state['students'][st.session_state['students']['Name'] == rc_student].iloc[0]
        student_subjects = st.session_state['subjects'][st.session_state['subjects']['Student_ID'] == student['ID']]
        
        st.markdown(f"""
        <div class="report-card-preview">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 1.5rem; font-weight: 600; color: #1E3A8A;">SEMESTER REPORT CARD</div>
                <div style="font-size: 1.2rem; color: #4B5563;">{rc_period} - 2024-2025</div>
                <div style="font-size: 0.9rem; color: #6B7280;">Oakridge High School</div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div>
                    <div><strong>Student:</strong> {student['Name']}</div>
                    <div><strong>ID:</strong> {student['ID']}</div>
                    <div><strong>Grade Level:</strong> 10th Grade</div>
                </div>
                <div>
                    <div><strong>GPA:</strong> 3.8</div>
                    <div><strong>Attendance:</strong> {student['Attendance']}%</div>
                    <div><strong>Absences:</strong> 3 days</div>
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="font-weight: 600; margin-bottom: 5px;">Academic Grades</div>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #F3F4F6;">
                        <th style="padding: 8px; text-align: left; border: 1px solid #E5E7EB;">Subject</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Q1</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Q2</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Exam</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Final</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Grade</th>
                    </tr>
        """, unsafe_allow_html=True)
        
        # Display subject scores
        for i, subj in enumerate(student_subjects.iterrows()):
            subj = subj[1]
            # Generate random scores for Q1, Q2, and exam
            q1 = subj['Score'] - random.uniform(-5, 5)
            q2 = subj['Score'] - random.uniform(-5, 5)
            exam = subj['Score'] - random.uniform(-8, 8)
            bg_color = "#F9FAFB" if i % 2 == 1 else "white"
            
            st.markdown(f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 8px; border: 1px solid #E5E7EB;">{subj['Subject']}</td>
                <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{q1:.1f}%</td>
                <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{q2:.1f}%</td>
                <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{exam:.1f}%</td>
                <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{subj['Score']:.1f}%</td>
                <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">{subj['Grade']}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                </table>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">Skills Assessment</div>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #F3F4F6;">
                            <th style="padding: 8px; text-align: left; border: 1px solid #E5E7EB;">Skill</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Rating</th>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Critical Thinking</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Excellent</td>
                        </tr>
                        <tr style="background-color: #F9FAFB;">
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Collaboration</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Good</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Communication</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Very Good</td>
                        </tr>
                        <tr style="background-color: #F9FAFB;">
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Self-Direction</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Excellent</td>
                        </tr>
                    </table>
                </div>
                
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">Behavior & Citizenship</div>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #F3F4F6;">
                            <th style="padding: 8px; text-align: left; border: 1px solid #E5E7EB;">Category</th>
                            <th style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Rating</th>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Classroom Conduct</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Excellent</td>
                        </tr>
                        <tr style="background-color: #F9FAFB;">
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Respects Others</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Excellent</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Participation</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Very Good</td>
                        </tr>
                        <tr style="background-color: #F9FAFB;">
                            <td style="padding: 8px; border: 1px solid #E5E7EB;">Work Ethic</td>
                            <td style="padding: 8px; text-align: center; border: 1px solid #E5E7EB;">Excellent</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="font-weight: 600; margin-bottom: 5px;">Teacher Comments</div>
                <div style="border: 1px solid #E5E7EB; border-radius: 4px; padding: 10px; background-color: #F9FAFB;">
                    <p>{student['Name'].split()[0]} has had an exceptional semester, demonstrating consistent growth and dedication to academic excellence. Their critical thinking skills are particularly impressive, as shown in their science and mathematics work. They have been an active participant in class discussions and a positive influence on their peers. Areas for continued growth include further developing written communication skills and taking more intellectual risks in their work.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if include_graph:
            st.markdown('<div style="margin-top: 20px;"><div style="font-weight: 600; margin-bottom: 10px;">Performance Trends</div></div>', unsafe_allow_html=True)
            
            # Create performance trend chart
            fig = go.Figure()
            
            # Sample data for each subject over time
            months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
            
            # Add traces for each subject
            for subj in student_subjects.iterrows():
                subj = subj[1]
                base_score = subj['Score']
                scores = [base_score - random.uniform(5, 15)]
                for _ in range(5):
                    scores.append(scores[-1] + random.uniform(-5, 8))
                
                fig.add_trace(go.Scatter(
                    x=months,
                    y=scores,
                    mode='lines+markers',
                    name=subj['Subject']
                ))
            
            fig.update_layout(
                title="Subject Performance Over Time",
                xaxis_title="Month",
                yaxis_title="Score (%)",
                yaxis=dict(range=[60, 100]),
                legend=dict(y=0.99, x=0.01),
                margin=dict(l=20, r=20, t=40, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Download Report Card", type="primary"):
                loading_animation()
                st.success("Report card downloaded successfully!")
        with col2:
            if st.button("Print Report Card"):
                loading_animation()
                st.success("Report card sent to printer!")
        with col3:
            if st.button("Email to Parents", key="email_rc"):
                loading_animation()
                st.success("Report card emailed to parents!")

    with tab3:
        st.markdown('<h2 class="section-header">Custom Reports</h2>', unsafe_allow_html=True)
        
        report_type = st.selectbox(
            "Report Type",
            [
                "Class Performance Analysis", 
                "Attendance Summary", 
                "Behavior Report",
                "Improvement Trends",
                "Subject Mastery Report",
                "Student Portfolio"
            ]
        )
        
        # Report configuration options based on type
        if report_type == "Class Performance Analysis":
            col1, col2 = st.columns(2)
            
            with col1:
                class_grade = st.selectbox(
                    "Grade Level",
                    ["All Grades", "9th Grade", "10th Grade", "11th Grade", "12th Grade"],
                    index=0
                )
                
                time_period = st.selectbox(
                    "Time Period",
                    ["Current Quarter", "Current Semester", "School Year", "Previous Quarter"],
                    index=0
                )
            
            with col2:
                subjects = st.multiselect(
                    "Subjects",
                    ["Mathematics", "English", "Science", "Social Studies", "Physical Education"],
                    default=["Mathematics", "English", "Science"]
                )
                
                include_demographics = st.checkbox("Include Demographics", value=False)
        
        elif report_type == "Attendance Summary":
            col1, col2 = st.columns(2)
            
            with col1:
                attendance_period = st.selectbox(
                    "Time Period",
                    ["Current Month", "Current Quarter", "Current Semester", "School Year"],
                    index=1
                )
                
                absence_types = st.multiselect(
                    "Include",
                    ["Excused Absences", "Unexcused Absences", "Tardies", "Early Dismissals"],
                    default=["Excused Absences", "Unexcused Absences", "Tardies"]
                )
            
            with col2:
                attendance_threshold = st.slider(
                    "Attendance Concern Threshold",
                    min_value=70,
                    max_value=95,
                    value=85,
                    step=5,
                    help="Flag students below this attendance percentage"
                )
                
                include_charts = st.checkbox("Include Attendance Trend Charts", value=True)
        
        # Generate report button
        if st.button("Generate Custom Report", type="primary"):
            loading_animation()
            st.success(f"{report_type} generated successfully!")
            
            # Sample preview for class performance analysis
            if report_type == "Class Performance Analysis":
                st.markdown('<h3 class="section-header">Report Preview</h3>', unsafe_allow_html=True)
                
                # Sample chart
                fig = go.Figure()
                
                # Sample data
                subject_names = subjects if subjects else ["Mathematics", "English", "Science"]
                avg_scores = [83.2, 87.4, 81.6]
                median_scores = [85.0, 88.5, 82.7]
                
                # Add traces
                fig.add_trace(go.Bar(
                    x=subject_names,
                    y=avg_scores,
                    name="Class Average",
                    marker_color="#3B82F6"
                ))
                
                fig.add_trace(go.Bar(
                    x=subject_names,
                    y=median_scores,
                    name="Median Score",
                    marker_color="#10B981"
                ))
                
                fig.update_layout(
                    title="Class Performance by Subject",
                    xaxis_title="Subject",
                    yaxis_title="Score (%)",
                    legend=dict(y=0.99, x=0.01),
                    margin=dict(l=20, r=20, t=40, b=20),
                    barmode="group"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Sample insights
                st.markdown("""
                <div class="custom-info-box">
                    <h4 style="margin-top: 0; color: #1E40AF;">Key Insights</h4>
                    <ul style="margin-bottom: 0;">
                        <li>English consistently shows the highest overall performance</li>
                        <li>Mathematics has the widest spread between high and low performers</li>
                        <li>Science scores show most improvement compared to previous quarter</li>
                        <li>10th grade students show strongest overall performance</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# Settings page
elif selected == "Settings":
    st.markdown('<h1 class="dashboard-title">Dashboard Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["General", "Notifications", "Data Management"])
    
    with tab1:
        st.markdown('<h2 class="section-header">General Settings</h2>', unsafe_allow_html=True)
        
        # Theme settings
        st.markdown('<h3 class="subsection-header">Theme & Appearance</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox(
                "Color Theme",
                ["Blue (Default)", "Green", "Purple", "Dark Mode"],
                index=0
            )
            
            font_size = st.select_slider(
                "Font Size",
                options=["Small", "Medium", "Large", "Extra Large"],
                value="Medium"
            )
        
        with col2:
            chart_theme = st.selectbox(
                "Chart Theme",
                ["Default", "Minimal", "Colorful", "Monochrome"],
                index=0
            )
            
            date_format = st.selectbox(
                "Date Format",
                ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
                index=0
            )
        
        # Default views
        st.markdown('<h3 class="subsection-header">Default Views</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            default_page = st.selectbox(
                "Default Dashboard Page",
                ["Analytics", "Student Profiles", "Reports", "Settings"],
                index=0
            )
            
            default_chart = st.selectbox(
                "Default Chart Type",
                ["Bar Chart", "Line Chart", "Pie Chart", "Radar Chart"],
                index=0
            )
        
        with col2:
            items_per_page = st.slider(
                "Items Per Page",
                min_value=5,
                max_value=50,
                value=20,
                step=5
            )
            
            default_subject = st.selectbox(
                "Default Subject View",
                ["All Subjects", "Mathematics", "English", "Science"],
                index=0
            )
        
        # Save settings button
        if st.button("Save General Settings", type="primary"):
            loading_animation()
            st.success("Settings saved successfully!")
    
    with tab2:
        st.markdown('<h2 class="section-header">Notification Settings</h2>', unsafe_allow_html=True)
        
        # Email notifications
        st.markdown('<h3 class="subsection-header">Email Notifications</h3>', unsafe_allow_html=True)
        
        email_address = st.text_input("Email Address", placeholder="Enter your email address")
        
        st.markdown('<p>Select the notifications you wish to receive by email:</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_reports = st.checkbox("Weekly Performance Reports", value=True)
            email_alerts = st.checkbox("Performance Alerts", value=True)
            email_attendance = st.checkbox("Attendance Updates", value=False)
        
        with col2:
            email_behavior = st.checkbox("Behavior Reports", value=False)
            email_system = st.checkbox("System Updates", value=True)
            email_digest = st.checkbox("Daily Digest", value=False)
        
        # Alert thresholds
        st.markdown('<h3 class="subsection-header">Alert Thresholds</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_threshold = st.slider(
                "Grade Alert Threshold",
                min_value=60,
                max_value=90,
                value=70,
                step=5,
                help="Alert when student score falls below this percentage"
            )
            
            attendance_alert = st.slider(
                "Attendance Alert Threshold",
                min_value=70,
                max_value=95,
                value=85,
                step=5,
                help="Alert when student attendance falls below this percentage"
            )
        
        with col2:
            behavior_threshold = st.slider(
                "Behavior Alert Threshold",
                min_value=1,
                max_value=4,
                value=3,
                step=1,
                help="Alert when student behavior score falls below this value"
            )
            
            consecutive_absences = st.number_input(
                "Consecutive Absences Alert",
                min_value=1,
                max_value=10,
                value=3,
                help="Alert after this many consecutive absences"
            )
        
        # Save notification settings
        if st.button("Save Notification Settings", type="primary"):
            loading_animation()
            st.success("Notification settings saved successfully!")
    
    with tab3:
        st.markdown('<h2 class="section-header">Data Management</h2>', unsafe_allow_html=True)
        
        # Data import/export
        st.markdown('<h3 class="subsection-header">Import/Export Data</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p>Import student data from external sources:</p>', unsafe_allow_html=True)
            
            import_file = st.file_uploader("Upload Data File", type=["csv", "xlsx", "json"])
            
            import_source = st.selectbox(
                "Import Source",
                ["CSV File", "Excel File", "School Information System", "Google Classroom"],
                index=0
            )
            
            if st.button("Import Data"):
                loading_animation()
                st.success("Data imported successfully!")
        
        with col2:
            st.markdown('<p>Export dashboard data for external use:</p>', unsafe_allow_html=True)
            
            export_format = st.selectbox(
                "Export Format",
                ["CSV", "Excel (.xlsx)", "PDF Report", "JSON"],
                index=0
            )
            
            export_data = st.multiselect(
                "Data to Export",
                ["Student Profiles", "Performance Data", "Attendance Records", "Behavior Reports", "All Data"],
                default=["All Data"]
            )
            
            if st.button("Export Data"):
                loading_animation()
                st.success("Data exported successfully!")
        
        # Data cleanup and backup
        st.markdown('<h3 class="subsection-header">Data Management Tools</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p>Data Cleanup Options:</p>', unsafe_allow_html=True)
            
            cleanup_inactive = st.checkbox("Remove inactive student data", value=False)
            cleanup_old = st.checkbox("Archive previous year data", value=True)
            cleanup_duplicates = st.checkbox("Remove duplicate entries", value=True)
            
            if st.button("Run Data Cleanup"):
                loading_animation()
                st.success("Data cleanup complete!")
        
        with col2:
            st.markdown('<p>Backup Options:</p>', unsafe_allow_html=True)
            
            backup_freq = st.selectbox(
                "Automatic Backup Frequency",
                ["Daily", "Weekly", "Monthly", "Never"],
                index=1
            )
            
            backup_location = st.selectbox(
                "Backup Storage Location",
                ["Cloud Storage", "Local Server", "External Database"],
                index=0
            )
            
            if st.button("Create Manual Backup Now"):
                loading_animation()
                st.success("Manual backup created successfully!")
        
        # Data privacy
        st.markdown('<h3 class="subsection-header">Data Privacy & Security</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            log_retention = st.selectbox(
                "Log Retention Period",
                ["30 days", "60 days", "90 days", "180 days", "1 year"],
                index=2
            )
            
            data_masking = st.checkbox("Enable data masking for sensitive information", value=True)
            encryption = st.checkbox("Enable enhanced encryption", value=True)
        
        with col2:
            access_log = st.checkbox("Enable access logging", value=True)
            two_factor = st.checkbox("Require two-factor authentication", value=False)
            auto_logout = st.slider(
                "Auto Logout (minutes of inactivity)",
                min_value=5,
                max_value=60,
                value=30,
                step=5
            )
        
        if st.button("Save Data Settings", type="primary"):
            loading_animation()
            st.success("Data management settings saved successfully!")

# Help & Support page
elif selected == "Help & Support":
    st.markdown('<h1 class="dashboard-title">Help & Support</h1>', unsafe_allow_html=True)
    
    # Help tabs
    tab1, tab2, tab3, tab4 = st.tabs(["User Guide", "FAQs", "Contact Support", "System Status"])
    
    with tab1:
        st.markdown('<h2 class="section-header">User Guide</h2>', unsafe_allow_html=True)
        
        # Quick start guides
        st.markdown('''
        <div class="help-section">
            <h3 class="subsection-header">Quick Start Guide</h3>
            <p>Welcome to the Student Performance Dashboard! Follow these steps to get started:</p>
            
            <ol>
                <li>
                    <strong>Navigate the Dashboard:</strong> Use the sidebar menu to switch between different sections:
                    <ul>
                        <li><strong>Analytics:</strong> View overall performance metrics and trends</li>
                        <li><strong>Student Profiles:</strong> Access individual student information</li>
                        <li><strong>Reports:</strong> Generate and view different types of reports</li>
                        <li><strong>Settings:</strong> Customize your dashboard experience</li>
                    </ul>
                </li>
                <li>
                    <strong>Analyze Data:</strong> Use filters and selectors to narrow down data and focus on specific metrics, subjects, or student groups.
                </li>
                <li>
                    <strong>Generate Reports:</strong> Visit the Reports section to create custom reports for individuals or classes.
                </li>
                <li>
                    <strong>Export Data:</strong> Most charts and tables have export options - look for download buttons near visualizations.
                </li>
            </ol>
        </div>
        ''', unsafe_allow_html=True)
        
        # Video tutorials
        st.markdown('''
        <div class="help-section">
            <h3 class="subsection-header">Video Tutorials</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
                <div class="video-card">
                    <div style="background-color: #F3F4F6; height: 150px; display: flex; align-items: center; justify-content: center; border-radius: 8px 8px 0 0;">
                        <div style="text-align: center;">
                            <div style="color: #4B5563; font-size: 2rem;">▶️</div>
                            <div style="color: #6B7280; font-size: 0.9rem;">Video Preview</div>
                        </div>
                    </div>
                    <div style="padding: 15px;">
                        <div style="font-weight: 600; margin-bottom: 5px;">Dashboard Overview</div>
                        <div style="color: #6B7280; font-size: 0.8rem; margin-bottom: 10px;">5:32 • Basic introduction to all features</div>
                        <button style="background-color: #EFF6FF; color: #2563EB; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.9rem; width: 100%;">Watch Video</button>
                    </div>
                </div>
                
                <div class="video-card">
                    <div style="background-color: #F3F4F6; height: 150px; display: flex; align-items: center; justify-content: center; border-radius: 8px 8px 0 0;">
                        <div style="text-align: center;">
                            <div style="color: #4B5563; font-size: 2rem;">▶️</div>
                            <div style="color: #6B7280; font-size: 0.9rem;">Video Preview</div>
                        </div>
                    </div>
                    <div style="padding: 15px;">
                        <div style="font-weight: 600; margin-bottom: 5px;">Creating Custom Reports</div>
                        <div style="color: #6B7280; font-size: 0.8rem; margin-bottom: 10px;">7:48 • Learn how to generate tailored reports</div>
                        <button style="background-color: #EFF6FF; color: #2563EB; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.9rem; width: 100%;">Watch Video</button>
                    </div>
                </div>
                
                <div class="video-card">
                    <div style="background-color: #F3F4F6; height: 150px; display: flex; align-items: center; justify-content: center; border-radius: 8px 8px 0 0;">
                        <div style="text-align: center;">
                            <div style="color: #4B5563; font-size: 2rem;">▶️</div>
                            <div style="color: #6B7280; font-size: 0.9rem;">Video Preview</div>
                        </div>
                    </div>
                    <div style="padding: 15px;">
                        <div style="font-weight: 600; margin-bottom: 5px;">Student Data Analysis</div>
                        <div style="color: #6B7280; font-size: 0.8rem; margin-bottom: 10px;">6:15 • Advanced data analysis techniques</div>
                        <button style="background-color: #EFF6FF; color: #2563EB; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.9rem; width: 100%;">Watch Video</button>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Feature guides
        st.markdown('''
        <div class="help-section">
            <h3 class="subsection-header">Feature Guides</h3>
            <div class="accordion">
                <div class="accordion-item">
                    <div class="accordion-header">Analytics Dashboard</div>
                    <div class="accordion-content">
                        <p>The Analytics Dashboard provides a comprehensive overview of student performance data:</p>
                        <ul>
                            <li>View key performance indicators and trends</li>
                            <li>Compare results across different subjects</li>
                            <li>Analyze attendance patterns and their impact on performance</li>
                            <li>Identify students who may need additional support</li>
                        </ul>
                        <p>Use the filters at the top of the page to refine the data display by grade level, time period, or specific student groups.</p>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <div class="accordion-header">Student Profiles</div>
                    <div class="accordion-content">
                        <p>The Student Profiles section allows you to:</p>
                        <ul>
                            <li>View detailed information about individual students</li>
                            <li>Access subject-specific scores and progress</li>
                            <li>Review attendance and behavior records</li>
                            <li>See historical performance data</li>
                        </ul>
                        <p>Use the search and filter options to quickly find specific students or groups of students with similar characteristics.</p>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <div class="accordion-header">Report Generation</div>
                    <div class="accordion-content">
                        <p>The Reports section lets you create various types of reports:</p>
                        <ul>
                            <li>Progress reports for individual students or entire classes</li>
                            <li>Report cards with comprehensive performance data</li>
                            <li>Custom reports focused on specific metrics</li>
                            <li>Attendance and behavior summaries</li>
                        </ul>
                        <p>Reports can be customized, saved, exported, and shared with parents or other educators.</p>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">Frequently Asked Questions</h2>', unsafe_allow_html=True)
        
        # FAQ sections
        st.markdown('''
        <div class="faq-section">
            <div class="faq-item">
                <div class="faq-question">How do I add a new student to the system?</div>
                <div class="faq-answer">
                    <p>To add a new student:</p>
                    <ol>
                        <li>Navigate to the "Student Profiles" page</li>
                        <li>Scroll down to the "Add New Student" section</li>
                        <li>Fill in all required information</li>
                        <li>Click the "Add Student" button</li>
                    </ol>
                    <p>The new student will be added immediately and will appear in all relevant reports and analytics.</p>
                </div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">Can I export reports to send to parents?</div>
                <div class="faq-answer">
                    <p>Yes, you can export reports in several formats:</p>
                    <ol>
                        <li>Generate the desired report in the "Reports" section</li>
                        <li>Click the "Download Report" or "Export" button</li>
                        <li>Choose your preferred format (PDF, Excel, etc.)</li>
                    </ol>
                    <p>You can also email reports directly to parents by clicking the "Email to Parents" button within any report view.</p>
                </div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">How are overall grades calculated?</div>
                <div class="faq-answer">
                    <p>Overall grades are calculated using a weighted average of:</p>
                    <ul>
                        <li>Subject scores (70%)</li>
                        <li>Attendance (15%)</li>
                        <li>Behavior scores (15%)</li>
                    </ul>
                    <p>The grading scale is as follows:</p>
                    <ul>
                        <li>A+ (97-100%)</li>
                        <li>A (93-96%)</li>
                        <li>A- (90-92%)</li>
                        <li>B+ (87-89%)</li>
                        <li>B (83-86%)</li>
                        <li>B- (80-82%)</li>
                        <li>C+ (77-79%)</li>
                        <li>C (73-76%)</li>
                        <li>C- (70-72%)</li>
                        <li>D+ (67-69%)</li>
                        <li>D (63-66%)</li>
                        <li>D- (60-62%)</li>
                        <li>F (Below 60%)</li>
                    </ul>
                </div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">How do I update a student's information?</div>
                <div class="faq-answer">
                    <p>To update student information:</p>
                    <ol>
                        <li>Go to the "Student Profiles" page</li>
                        <li>Find the student using search or filters</li>
                        <li>Click "View Details" on their profile card</li>
                        <li>Click "Edit Information" in the detailed view</li>
                        <li>Make the necessary changes</li>
                        <li>Click "Save Changes"</li>
                    </ol>
                </div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">How often is the data updated?</div>
                <div class="faq-answer">
                    <p>Data is updated as follows:</p>
                    <ul>
                        <li>Attendance: Daily updates at the end of each school day</li>
                        <li>Academic scores: Updated as soon as teachers enter new grades</li>
                        <li>Behavior records: Updated in real-time as incidents are reported</li>
                        <li>Report cards: Generated at the end of each marking period</li>
                    </ul>
                    <p>You can see the last update time at the bottom of each dashboard page.</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-header">Contact Support</h2>', unsafe_allow_html=True)
        
        # Support options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('''
            <div class="contact-card">
                <div style="font-size: 2rem; color: #3B82F6; text-align: center; margin-bottom: 10px;">📧</div>
                <div style="font-weight: 600; text-align: center; margin-bottom: 5px;">Email Support</div>
                <div style="color: #6B7280; text-align: center; margin-bottom: 15px;">Response within 24 hours</div>
                <input type="text" placeholder="Your Email Address" style="width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #D1D5DB; border-radius: 4px;">
                <textarea placeholder="Describe your issue or question" style="width: 100%; height: 100px; padding: 8px; margin-bottom: 10px; border: 1px solid #D1D5DB; border-radius: 4px;"></textarea>
                <button style="background-color: #2563EB; color: white; border: none; padding: 8px 0; width: 100%; border-radius: 4px; cursor: pointer;">Submit Support Request</button>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('''
            <div class="contact-card">
                <div style="font-size: 2rem; color: #3B82F6; text-align: center; margin-bottom: 10px;">📞</div>
                <div style="font-weight: 600; text-align: center; margin-bottom: 5px;">Live Support</div>
                <div style="color: #6B7280; text-align: center; margin-bottom: 15px;">Available Monday-Friday, 8am-5pm</div>
                <div style="text-align: center; font-size: 1.2rem; font-weight: 600; margin-bottom: 10px;">1-800-555-0123</div>
                <div style="margin-bottom: 15px; text-align: center;">Or schedule a callback:</div>
                <input type="text" placeholder="Your Phone Number" style="width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #D1D5DB; border-radius: 4px;">
                <button style="background-color: #2563EB; color: white; border: none; padding: 8px 0; width: 100%; border-radius: 4px; cursor: pointer;">Request Callback</button>
            </div>
            ''', unsafe_allow_html=True)
        
        # Additional support resources
        st.markdown('''
        <div style="margin-top: 30px;">
            <h3 class="subsection-header">Additional Resources</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; margin-top: 15px;">
                <div class="resource-card">
                    <div style="font-size: 1.5rem; color: #3B82F6; text-align: center; margin-bottom: 5px;">📚</div>
                    <div style="font-weight: 600; text-align: center; margin-bottom: 5px;">Knowledge Base</div>
                    <div style="color: #6B7280; text-align: center; font-size: 0.9rem;">Browse articles and tutorials</div>
                </div>
                
                <div class="resource-card">
                    <div style="font-size: 1.5rem; color: #3B82F6; text-align: center; margin-bottom: 5px;">💬</div>
                    <div style="font-weight: 600; text-align: center; margin-bottom: 5px;">Community Forum</div>
                    <div style="color: #6B7280; text-align: center; font-size: 0.9rem;">Connect with other users</div>
                </div>
                
                <div class="resource-card">
                    <div style="font-size: 1.5rem; color: #3B82F6; text-align: center; margin-bottom: 5px;">📝</div>
                    <div style="font-weight: 600; text-align: center; margin-bottom: 5px;">Feature Requests</div>
                    <div style="color: #6B7280; text-align: center; font-size: 0.9rem;">Submit ideas for improvements</div>
                </div>
                
                <div class="resource-card">
                    <div style="font-size: 1.5rem; color: #3B82F6; text-align: center; margin-bottom: 5px;">🔄</div>
                    <div style="font-weight: 600; text-align: center; margin-bottom: 5px;">System Updates</div>
                    <div style="color: #6B7280; text-align: center; font-size: 0.9rem;">View latest release notes</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 class="section-header">System Status</h2>', unsafe_allow_html=True)
        
        # System status display
        st.markdown('''
        <div style="padding: 15px; background-color: #ECFDF5; border-radius: 8px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 12px; height: 12px; background-color: #10B981; border-radius: 50%; margin-right: 10px;"></div>
                <div style="font-weight: 600;">All Systems Operational</div>
            </div>
            <div style="color: #6B7280; font-size: 0.9rem;">Last checked: April 10, 2025, 10:15 AM</div>
        </div>
        
        <div style="margin-bottom: 30px;">
            <h3 class="subsection-header">Service Status</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #F3F4F6;">
                    <th style="padding: 10px; text-align: left; border: 1px solid #E5E7EB;">Service</th>
                    <th style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">Status</th>
                    <th style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">Uptime</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #E5E7EB;">Dashboard Web Application</td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">
                        <span style="color: #10B981; font-weight: 500;">●&nbsp;Operational</span>
                    </td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">99.98%</td>
                </tr>
                <tr style="background-color: #F9FAFB;">
                    <td style="padding: 10px; border: 1px solid #E5E7EB;">Database Services</td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">
                        <span style="color: #10B981; font-weight: 500;">●&nbsp;Operational</span>
                    </td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">99.99%</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #E5E7EB;">Report Generation</td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">
                        <span style="color: #10B981; font-weight: 500;">●&nbsp;Operational</span>
                    </td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">99.95%</td>
                </tr>
                <tr style="background-color: #F9FAFB;">
                    <td style="padding: 10px; border: 1px solid #E5E7EB;">Email Notifications</td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">
                        <span style="color: #10B981; font-weight: 500;">●&nbsp;Operational</span>
                    </td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">99.90%</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #E5E7EB;">Data Import/Export</td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">
                        <span style="color: #10B981; font-weight: 500;">●&nbsp;Operational</span>
                    </td>
                    <td style="padding: 10px; text-align: center; border: 1px solid #E5E7EB;">99.97%</td>
                </tr>
            </table>
        </div>
        
        <div style="margin-bottom: 30px;">
            <h3 class="subsection-header">Recent Incidents</h3>
            <div style="padding: 15px; border: 1px solid #E5E7EB; border-radius: 8px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="font-weight: 600;">Scheduled Maintenance</div>
                    <div style="color: #6B7280; font-size: 0.9rem;">March 15, 2025</div>
                </div>
                <div style="color: #4B5563; margin-bottom: 10px;">System was temporarily unavailable from 2:00 AM to 4:30 AM for scheduled database optimization.</div>
                <div style="padding: 5px 10px; background-color: #ECFDF5; color: #10B981; font-weight: 500; display: inline-block; border-radius: 20px; font-size: 0.8rem;">Resolved</div>
            </div>
            
            <div style="padding: 15px; border: 1px solid #E5E7EB; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="font-weight: 600;">Report Generation Delay</div>
                    <div style="color: #6B7280; font-size: 0.9rem;">February 28, 2025</div>
                </div>
                <div style="color: #4B5563; margin-bottom: 10px;">Some users experienced delays of up to 3 minutes when generating complex reports. The issue was identified and resolved.</div>
                <div style="padding: 5px 10px; background-color: #ECFDF5; color: #10B981; font-weight: 500; display: inline-block; border-radius: 20px; font-size: 0.8rem;">Resolved</div>
            </div>
        </div>
        
        <div>
            <h3 class="subsection-header">System Resources</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">CPU Usage</div>
                    <div style="height: 20px; background-color: #DBEAFE; border-radius: 10px; overflow: hidden;">
                        <div style="width: 32%; height: 100%; background-color: #3B82F6; border-radius: 10px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #6B7280; font-size: 0.8rem; margin-top: 5px;">
                        <div>0%</div>
                        <div style="font-weight: 500; color: #4B5563;">32%</div>
                        <div>100%</div>
                    </div>
                </div>
                
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">Memory Usage</div>
                    <div style="height: 20px; background-color: #DBEAFE; border-radius: 10px; overflow: hidden;">
                        <div style="width: 58%; height: 100%; background-color: #3B82F6; border-radius: 10px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #6B7280; font-size: 0.8rem; margin-top: 5px;">
                        <div>0%</div>
                        <div style="font-weight: 500; color: #4B5563;">58%</div>
                        <div>100%</div>
                    </div>
                </div>
                
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">Storage Usage</div>
                    <div style="height: 20px; background-color: #DBEAFE; border-radius: 10px; overflow: hidden;">
                        <div style="width: 45%; height: 100%; background-color: #3B82F6; border-radius: 10px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #6B7280; font-size: 0.8rem; margin-top: 5px;">
                        <div>0%</div>
                        <div style="font-weight: 500; color: #4B5563;">45%</div>
                        <div>100%</div>
                    </div>
                </div>
                
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">Network Bandwidth</div>
                    <div style="height: 20px; background-color: #DBEAFE; border-radius: 10px; overflow: hidden;">
                        <div style="width: 28%; height: 100%; background-color: #3B82F6; border-radius: 10px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #6B7280; font-size: 0.8rem; margin-top: 5px;">
                        <div>0%</div>
                        <div style="font-weight: 500; color: #4B5563;">28%</div>
                        <div>100%</div>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Scheduled maintenance
        st.markdown('''
        <div style="margin-top: 30px;">
            <h3 class="subsection-header">Scheduled Maintenance</h3>
            <div style="padding: 15px; border: 1px solid #FEF3C7; background-color: #FFFBEB; border-radius: 8px;">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; color: #D97706; margin-right: 10px;">⚠️</div>
                    <div style="font-weight: 600; color: #92400E;">Upcoming Maintenance</div>
                </div>
                <div style="color: #92400E; margin-bottom: 10px;">
                    The system will be unavailable during planned maintenance on <strong>April 20, 2025</strong> from <strong>1:00 AM to 3:00 AM</strong>.
                </div>
                <div style="font-size: 0.9rem; color: #92400E;">
                    This maintenance window will be used to deploy new features and performance improvements.
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Logout option
with st.sidebar:
    st.markdown("<div style='margin-top: auto;'></div>", unsafe_allow_html=True)
    if st.button("Logout", key="logout"):
        st.session_state.clear()
        st.rerun()

# Footer
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #F9FAFB; padding: 10px 20px; border-top: 1px solid #E5E7EB; display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #6B7280;">
    <div>© 2025 Student Performance Dashboard | v2.3.1</div>
    <div>
        <a href="#" style="color: #6B7280; text-decoration: none; margin-right: 15px;">Privacy Policy</a>
        <a href="#" style="color: #6B7280; text-decoration: none; margin-right: 15px;">Terms of Service</a>
        <a href="#" style="color: #6B7280; text-decoration: none;">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Add custom CSS
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    
    /* Dashboard title */
    .dashboard-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #1F2937;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #1F2937;
    }
    
    /* Subsection headers */
    .subsection-header {
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        color: #1F2937;
    }
    
    /* Cards */
    .stat-card, .student-card, .contact-card, .resource-card, .video-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E7EB;
    }
    
    /* Accordion styles */
    .accordion-item {
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        margin-bottom: 10px;
        overflow: hidden;
    }
    
    .accordion-header {
        background-color: #F9FAFB;
        padding: 12px 15px;
        font-weight: 600;
        cursor: pointer;
        color: #1F2937;
    }
    
    .accordion-content {
        padding: 15px;
        border-top: 1px solid #E5E7EB;
    }
    
    /* FAQ styles */
    .faq-item {
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 15px;
        margin-bottom: 15px;
    }
    
    .faq-question {
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 10px;
        cursor: pointer;
    }
    
    .faq-answer {
        color: #4B5563;
    }
    
    /* Help section */
    .help-section {
        margin-bottom: 30px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6;
        border-radius: 6px;
        padding: 5px 15px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #DBEAFE;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .dashboard-title {
            font-size: 1.5rem;
        }
        
        .section-header {
            font-size: 1.3rem;
        }
        
        .subsection-header {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add JavaScript for interactivity
st.markdown("""
<script>
    // Accordion functionality
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        });
    });
    
    // FAQ toggle
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            answer.style.display = answer.style.display === 'none' ? 'block' : 'none';
        });
    });
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        new tippy(tooltip, {
            content: tooltip.getAttribute('data-tooltip'),
            placement: 'top',
            arrow: true
        });
    });
</script>
""", unsafe_allow_html=True)

# Loading animation function
def loading_animation():
    with st.spinner("Processing..."):
        time.sleep(1)