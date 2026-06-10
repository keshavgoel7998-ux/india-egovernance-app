import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="India e-Governance Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar hidden
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Header */
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 40px;
        font-weight: bold;
        color: #1a1a1a;
    }
    .subtitle-text {
        font-size: 18px;
        color: #555;
    }
    
    /* Feature Cards */
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Tabs styling */
    .stTabs {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
    }
    
    /* Metric Cards */
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    /* Custom Button */
    .stButton>button {
        background-color: #FF9933;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #e58b2e;
    }
    
    /* Alert Boxes */
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        padding: 15px;
        background-color: #fff3cd;
        color: #856404;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATA ---
STATES_DATA = {
    "Maharashtra": {"cases": 1250, "hospitals": 450, "active": "Metro Phase 3"},
    "Delhi": {"cases": 980, "hospitals": 320, "active": "Swachh Bharat"},
    "Karnataka": {"cases": 1100, "hospitals": 380, "active": "Digital Bangalore"},
    "Tamil Nadu": {"cases": 900, "hospitals": 410, "active": "Tamil Nadu Vision"},
    "Uttar Pradesh": {"cases": 1500, "hospitals": 600, "active": "One District One Product"},
}

GOVT_JOBS = [
    {"post": "UPSC CSE 2024", "last_date": "2024-03-15", "qualification": "Graduate", "vacancies": 1105},
    {"post": "SSC CHSL", "last_date": "2024-04-01", "qualification": "12th Pass", "vacancies": 4500},
    {"post": "Railway NTPC", "last_date": "2024-04-10", "qualification": "Graduate", "vacancies": 3500},
    {"post": "Bank PO", "last_date": "2024-02-28", "qualification": "Graduate", "vacancies": 5000},
    {"post": "State PSC", "last_date": "2024-05-15", "qualification": "Graduate", "vacancies": 200},
]

SCHEMES = [
    {"name": "PM Kisan", "amount": "₹6000/yr", "category": "Agriculture"},
    {"name": "Ayushman Bharat", "amount": "₹5L", "category": "Health"},
    {"name": "PM Awas Yojana", "amount": "₹1.5L", "category": "Housing"},
    {"name": "Beti Bachao", "amount": "Variable", "category": "Education"},
    {"name": "Saubhagya Yojana", "amount": "Free Connection", "category": "Electricity"},
]

UNIVERSITIES = [
    {"name": "University of Delhi", "result_status": "Declared", "exam": "Semester 4"},
    {"name": "JNU", "result_status": "Pending", "exam": "Entrance 2024"},
    {"name": "BHU", "result_status": "Declared", "exam": "Entrance Test"},
]

# --- FUNCTIONS ---
def show_landing_page():
    """Main Landing Page with Navigation Tiles"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="title-text">🇮🇳 Digital India e-Governance Portal</div>
        <div class="subtitle-text">One Nation - One Platform - One Solution</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aadhaar Cards", "1.35B +")
    col2.metric("DigiLocker Docs", "650Cr +")
    col3.metric("Govt Schemes", "1500+")
    col4.metric("Digital Payments", "₹8000B")
    
    st.markdown("---")
    
    # Main Feature Grid
    st.markdown("### 🖥️ Select Service")
    
    # Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>💰 Schemes</h3>
            <p>Find Government Benefits & Subsidies</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Schemes", key="nav_schemes"):
            st.session_state['active_tab'] = 'Schemes'
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>📄 Documents</h3>
            <p>Verify GST, PAN, Aadhaar & DL</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Utilities", key="nav_docs"):
            st.session_state['active_tab'] = 'Utilities'
            st.rerun()
            
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>💼 Jobs</h3>
            <p>Sarkari Naukri & Recruitment</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Jobs", key="nav_jobs"):
            st.session_state['active_tab'] = 'Jobs'
            st.rerun()
            
    with col4:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>🧮 Tax</h3>
            <p>Income Tax Calculator</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Tax", key="nav_tax"):
            st.session_state['active_tab'] = 'Tax'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>🏥 Healthcare</h3>
            <p>Hospitals & Insurance Claim</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Health", key="nav_health"):
            st.session_state['active_tab'] = 'Healthcare'
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>🗳️ Jan Sewa</h3>
            <p>File Grievance & Complaints</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Grievance", key="nav_grievance"):
            st.session_state['active_tab'] = 'Grievance'
            st.rerun()
            
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>🎓 Education</h3>
            <p>Verify Degrees & Results</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Education", key="nav_edu"):
            st.session_state['active_tab'] = 'Education'
            st.rerun()
            
    with col4:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>🚛 Transport</h3>
            <p>Driving License & Vehicle RC</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Transport", key="nav_transport"):
            st.session_state['active_tab'] = 'Transport'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 3
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>🗺️ GIS Map</h3>
            <p>State-wise Data Visualization</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to GIS", key="nav_gis"):
            st.session_state['active_tab'] = 'GIS'
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>📁 Digital Locker</h3>
            <p>Access & Sync Documents</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Locker", key="nav_locker"):
            st.session_state['active_tab'] = 'Locker'
            st.rerun()
            
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align:center">
            <h3>⚠️ Disaster</h3>
            <p>Weather & Emergency Alerts</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Disaster", key="nav_disaster"):
            st.session_state['active_tab'] = 'Disaster'
            st.rerun()

# --- FEATURES MODULES ---

def show_schemes():
    st.title("💰 Government Schemes & Subsidies")
    
    col1, col2, col3 = st.columns(3)
    income = col1.number_input("Annual Income (₹)", 0, 5000000, 100000, 5000)
    age = col2.number_input("Age", 18, 100, 30)
    occupation = col3.selectbox("Occupation", ["Farmer", "Student", "Business", "Employee", "Unemployed"])
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    state = st.selectbox("State", ["All States"] + list(STATES_DATA.keys()))
    
    if st.button("Find Eligible Schemes", type="primary"):
        st.markdown("### ✅ Recommended Schemes")
        
        # Filter logic (Mock)
        for scheme in SCHEMES:
            with st.expander(f"{scheme['name']} ({scheme['category']})"):
                st.markdown(f"""
                - **Benefit Amount:** {scheme['amount']}
                - **Eligibility:** {occupation}, Age {age}+, Income < ₹{income:,}
                - **Documents Required:** Aadhaar, Bank Account, Residence Proof
                """)
                st.button("Apply Now", key=f"apply_{scheme['name']}")

def show_utilities():
    st.title("📄 Document Verification Utilities")
    
    tab1, tab2, tab3, tab4 = st.tabs(["GSTIN", "PAN", "Aadhaar", "Voter ID"])
    
    with tab1:
        st.subheader("Verify GST Registration")
        gstin = st.text_input("Enter GSTIN", placeholder="e.g., 27AAAAA1234A1A1")
        if st.button("Verify GST", key="verify_gst"):
            if len(gstin) == 15:
                st.markdown("""
                <div class="success-box">
                    <b>✅ Verified</b><br>
                    Legal Name: SAMPLE INDIA PVT LTD<br>
                    Status: Active<br>
                    State: Maharashtra<br>
                    Taxpayer Type: Regular
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Invalid GSTIN. Must be 15 characters.")
    
    with tab2:
        st.subheader("Verify PAN Card")
        pan = st.text_input("Enter PAN Number").upper()
        if st.button("Verify PAN", key="verify_pan"):
            if len(pan) == 10 and pan[:5].isalpha():
                st.markdown("""
                <div class="success-box">
                    <b>✅ Valid PAN</b><br>
                    Name: AS PER AADHAAR<br>
                    DOB: 01/01/1990<br>
                    Linked Aadhaar: Yes
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Invalid PAN Format")
    
    with tab3:
        st.subheader("Aadhaar Validation")
        aadhaar = st.text_input("Enter Aadhaar Number", max_length=12)
        if st.button("Verify Aadhaar", key="verify_adhar"):
            if len(aadhaar) == 12 and aadhaar.isdigit():
                st.success(f"✅ Aadhaar {aadhaar} is Valid and Verified with UIDAI")
            else:
                st.error("Invalid Aadhaar Number")
                
    with tab4:
        st.subheader("Voter ID Status")
        voter_id = st.text_input("Enter EPIC No").upper()
        if st.button("Check Status", key="check_voter"):
            st.success("✅ Voter ID Active. Assembly Constituency: Mumbai North")

def show_jobs():
    st.title("💼 Sarkari Naukri Portal")
    
    st.markdown("### 🔍 Search Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        q_qual = col1.selectbox("Qualification", ["10th", "12th", "Graduate", "Post Graduate", "Diploma"])
    with col2:
        q_dept = col2.selectbox("Department", ["UPSC", "SSC", "Railway", "Banking", "State PSC"])
    with col3:
        q_loc = col3.selectbox("Location", ["All India", "Delhi", "Maharashtra", "Karnataka"])
    
    st.markdown("---")
    
    st.markdown("### 📢 Latest Notifications")
    for job in GOVT_JOBS:
        with st.expander(f"📌 {job['post']}"):
            col1, col2 = st.columns(2)
            col1.markdown(f"**Qualification:** {job['qualification']}")
            col2.markdown(f"**Vacancies:** {job['vacancies']}")
            col1.markdown(f"**Last Date:** {job['last_date']}")
            col2.markdown(f"**Apply Link:** [Click Here](#)")
    
    st.markdown("### 📊
