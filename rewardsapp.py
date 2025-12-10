import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="HR Reward & Engagement Platform",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Custom card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Dark theme cards */
    .dark-card {
        background: #1e293b;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    
    /* Light theme cards */
    .light-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin-bottom: 20px;
    }
    
    /* Profile section */
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        margin-bottom: 30px;
    }
    
    /* Level indicator */
    .level-badge {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 8px 16px;
        display: inline-block;
        font-weight: 600;
        margin: 8px 4px;
    }
    
    /* Stats cards */
    .stat-card {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-number {
        font-size: 32px;
        font-weight: 700;
        margin: 8px 0;
    }
    
    .stat-label {
        font-size: 14px;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* KPI bars */
    .kpi-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .kpi-title {
        font-size: 14px;
        margin-bottom: 8px;
        color: #94a3b8;
    }
    
    .kpi-bar {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .kpi-progress {
        height: 100%;
        background: linear-gradient(90deg, #4ade80 0%, #3b82f6 100%);
        transition: width 1s ease;
    }
    
    /* Activity feed */
    .activity-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        margin-bottom: 8px;
    }
    
    .activity-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 14px;
    }
    
    /* Engagement score gauge */
    .engagement-score {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-radius: 20px;
        color: white;
    }
    
    .score-number {
        font-size: 64px;
        font-weight: 800;
        background: linear-gradient(135deg, #4ade80 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 16px 0;
    }
    
    .score-label {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .score-benchmark {
        font-size: 14px;
        color: #4ade80;
        margin-top: 8px;
    }
    
    /* Metric cards for organization dashboard */
    .org-metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .org-metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
    }
    
    .org-metric-icon {
        font-size: 32px;
        margin-bottom: 12px;
    }
    
    .org-metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #3b82f6;
        margin: 8px 0;
    }
    
    .org-metric-label {
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Award badge */
    .award-badge {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px;
        background: white;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
    }
    
    .award-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    
    .award-name {
        flex: 1;
        font-weight: 600;
        color: #1e293b;
    }
    
    .award-count {
        font-size: 24px;
        font-weight: 700;
        color: #3b82f6;
    }
    
    /* Streamlit tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 12px;
        padding: 0 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Fake Employee Data with Alkhorayef Rewards System
employee_data = {
    "name": "Andrei Spitzer",
    "role": "Digital Designer",
    "department": "PR & Marketing",
    "tenure_days": 168,
    "level": 3,  # Gold level
    "level_name": "Gold",
    "level_icon": "🥇",
    "points_current": 3580,
    "points_required": 5000,  # Next level: Champion
    "points_lifetime": 3580,
    "coins": 358,  # 10 points = 1 SAR (coin)
    "league": "Gold",
    "aura": "Advanced",
    "rank": 7,  # Company-wide rank
    "rank_department": 2,  # Department rank
    
    # Organized by Category with REAL Alkhorayef points
    "training_learning": {
        "mandatory_training_hours": 42,  # hours completed
        "mandatory_training_points": 840,  # 20 points per hour avg
        "elective_training_hours": 24,
        "elective_training_points": 480,
        "certifications": 2,  
        "certifications_points": 500,  # 250 points each
        "safety_training_hours": 8,
        "safety_training_points": 160,
        "compliance_modules": 6,
        "compliance_modules_points": 180  # 30 points each
    },
    
    "hr_engagement": {
        "engagement_surveys": 3,
        "engagement_surveys_points": 30,  # 10 points each
        "hr_sessions_townhalls": 4,
        "hr_sessions_points": 40,  # 10 points each
        "perfect_attendance_months": 0,  # 3-month periods
        "perfect_attendance_points": 0  # 1000 points per 3 months
    },
    
    "innovation": {
        "innovation_ideas_submitted": 2,
        "innovation_ideas_points": 60,  # Base submission
        "ideas_accepted": 1,
        "ideas_accepted_points": 1000,  # Digital Champion
        "digital_surveys": 6,
        "digital_surveys_points": 48  # 8 points each
    },
    
    "events_participation": {
        "corporate_events": 4,
        "corporate_events_points": 80,  # 20 points each
        "csr_activities": 2,
        "csr_activities_points": 200,  # 100 points each
        "wellness_sessions": 3,
        "wellness_sessions_points": 45  # 15 points each
    },
    
    # Points breakdown
    "points_breakdown": {
        "training": 2160,
        "surveys": 78,
        "innovation": 1108,
        "engagement": 70,
        "events": 325,
        "special": 0
    },
    
    # Certification details
    "certifications_list": ["Azure Fundamentals", "Lean Six Sigma Yellow Belt"],
    
    # Redemption history
    "points_redeemed": 0,
    "pending_redemptions": 0
}

# Alkhorayef Level System
level_system = [
    {"level": 1, "name": "Bronze", "icon": "🥉", "points": 0, "color": "#cd7f32"},
    {"level": 2, "name": "Silver", "icon": "🥈", "points": 500, "color": "#c0c0c0"},
    {"level": 3, "name": "Gold", "icon": "🥇", "points": 1000, "color": "#ffd700"},
    {"level": 4, "name": "Champion", "icon": "🏅", "points": 3000, "color": "#4169e1"},
    {"level": 5, "name": "Platinum", "icon": "💎", "points": 5000, "color": "#e5e4e2"},
    {"level": 6, "name": "Grand Master", "icon": "👑", "points": 8000, "color": "#9966cc"}
]

# Redemption options
redemption_options = [
    {"name": "Vacation Days", "points": 4000, "value": "2 Days", "icon": "🏖️", "category": "Time Off"},
    {"name": "Shopping Voucher", "points": 5000, "value": "500 SAR", "icon": "🛍️", "category": "Vouchers"},
    {"name": "Cash Reward", "points": 1500, "value": "150 SAR", "icon": "💵", "category": "Cash"},
    {"name": "Gym Membership", "points": 3000, "value": "3 Months", "icon": "🏋️", "category": "Wellness"},
    {"name": "Training Course", "points": 2500, "value": "Course Credit", "icon": "📚", "category": "Learning"},
    {"name": "Tech Gadget", "points": 8000, "value": "800 SAR", "icon": "📱", "category": "Electronics"}
]

# KPI Data
kpi_data = [
    {"name": "Grow number of website visitors by 5%", "progress": 100, "deadline": "Q2 2023"},
    {"name": "Increase conversion rate by 10%", "progress": 75, "deadline": "Q4 2023"},
    {"name": "Improve brand engagement by 8%", "progress": 40, "deadline": "Q1 2024"}
]

# Competencies Data
competencies = {
    "Expertise": 70,
    "Innovation": 40,
    "Protection": 50,
    "Integration": 60,
    "Dominance": 30
}

# Activity Feed
activity_feed = [
    {"name": "Alena Q.", "action": "reached Ruby League", "time": "2 hours ago"},
    {"name": "Arthur M.", "action": "got Last Epsilon achievement", "time": "5 hours ago"},
    {"name": "Alina S.", "action": "reached Emerald League", "time": "1 day ago"},
    {"name": "Andrei", "action": "completed Compliance Module Set A", "time": "2 days ago"}
]

# Organization Engagement Data
org_data = {
    "engagement_score": 79,
    "benchmark_diff": 12,
    "total_likes": 30000,
    "total_comments": 5000,
    "total_appreciations": 1200,
    "total_recognitions": 1400
}

# Award Distribution Data
award_distribution = pd.DataFrame({
    "Year": [2019, 2020, 2021, 2022, 2023, 2024],
    "Recognitions": [820, 720, 1320, 980, 1180, 1400]
})

# Top Awards Data
top_awards = [
    {"name": "Standout Performer", "count": 654, "icon": "🏆"},
    {"name": "Spot Award", "count": 562, "icon": "⚡"},
    {"name": "Make a Difference", "count": 477, "icon": "🎯"}
]

# Performance Data (Quarterly)
performance_data = pd.DataFrame({
    "Quarter": ["Q1/22", "Q2/22", "Q3/22", "Q4/22", "Q1/23", "Q2/23"],
    "KPIs_25": [15, 18, 22, 25, 20, 24],
    "KPIs_40": [25, 28, 32, 38, 35, 40],
    "KPIs_20": [12, 15, 18, 20, 19, 22],
    "KPIs_10": [8, 10, 12, 10, 11, 13]
})

# Main App
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🏆 HR Reward & Engagement Platform</h1>", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["👤 Employee Dashboard", "📊 Organization Dashboard"])

# ==================== TAB 1: EMPLOYEE DASHBOARD (DARK THEME) ====================
with tab1:
    # Apply dark theme background
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0f1425 0%, #1a1f3a 100%);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Profile Header with Alkhorayef Level System
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 24px; padding: 40px; margin-bottom: 40px;
                    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);">
            <div style="display: grid; grid-template-columns: 1fr auto; gap: 40px; align-items: center;">
                <div>
                    <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 12px; color: white;'>{employee_data['name']}</h1>
                    <p style='font-size: 20px; opacity: 0.95; margin-bottom: 24px; color: white;'>
                        {employee_data['role']} • {employee_data['department']}
                    </p>
                    <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;">
                        <span style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); 
                                     border-radius: 12px; padding: 10px 20px; font-weight: 600; 
                                     font-size: 15px; color: white; border: 1px solid rgba(255,255,255,0.3);">
                            {employee_data['level_icon']} {employee_data['level_name']} Level
                        </span>
                        <span style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); 
                                     border-radius: 12px; padding: 10px 20px; font-weight: 600; 
                                     font-size: 15px; color: white; border: 1px solid rgba(255,255,255,0.3);">
                            📅 {employee_data['tenure_days']} days
                        </span>
                        <span style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); 
                                     border-radius: 12px; padding: 10px 20px; font-weight: 600; 
                                     font-size: 15px; color: white; border: 1px solid rgba(255,255,255,0.3);">
                            🏆 Rank #{employee_data['rank']} Company | #{employee_data['rank_department']} Dept
                        </span>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.15); padding: 16px; border-radius: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="font-size: 14px; font-weight: 600;">Progress to Next Level</span>
                            <span style="font-size: 14px; font-weight: 600;">{employee_data['points_current']:,} / {employee_data['points_required']:,} pts</span>
                        </div>
                        <div style="height: 12px; background: rgba(255, 255, 255, 0.2); border-radius: 6px; overflow: hidden;">
                            <div style="width: {(employee_data['points_current'] / employee_data['points_required']) * 100}%; 
                                        height: 100%; background: linear-gradient(90deg, #4ade80 0%, #10b981 100%); 
                                        transition: width 1s ease;"></div>
                        </div>
                        <div style="font-size: 12px; margin-top: 6px; opacity: 0.9;">
                            {employee_data['points_required'] - employee_data['points_current']:,} points to {level_system[employee_data['level']]['name']} level
                        </div>
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="width: 200px; height: 200px; border-radius: 50%; 
                                background: linear-gradient(135deg, {level_system[employee_data['level']-1]['color']} 0%, rgba(255,255,255,0.3) 100%);
                                display: flex; align-items: center; justify-content: center;
                                position: relative; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);">
                        <div style="width: 175px; height: 175px; border-radius: 50%; 
                                    background: rgba(255, 255, 255, 0.95); display: flex; flex-direction: column; 
                                    align-items: center; justify-content: center;">
                            <div style="font-size: 64px; margin-bottom: 8px;">{employee_data['level_icon']}</div>
                            <div style="font-size: 24px; font-weight: 800; color: {level_system[employee_data['level']-1]['color']};">
                                {employee_data['level_name']}
                            </div>
                            <div style="font-size: 14px; color: #64748b; margin-top: 4px;">
                                Level {employee_data['level']}/6
                            </div>
                            <div style="font-size: 20px; font-weight: 700; color: #3b82f6; margin-top: 8px;">
                                {employee_data['points_lifetime']:,} pts
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Row - Improved Design
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_config = [
        ("🎯", "Missions", 365, "#4ade80", col1),
        ("💬", "Social Activity", 125, "#3b82f6", col2),
        ("🌟", "Competencies", 160, "#a78bfa", col3),
        ("❤️", "Helpfulness", 15, "#ec4899", col4),
        ("🪙", "Coins", employee_data['coins'], "#fbbf24", col5)
    ]
    
    for icon, label, value, color, col in metrics_config:
        with col:
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px);
                            border-radius: 20px; padding: 28px 20px; text-align: center;
                            border: 1px solid rgba(148, 163, 184, 0.2);
                            transition: all 0.3s ease;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);"
                     onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 24px rgba(0, 0, 0, 0.2)';"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0, 0, 0, 0.1)';">
                    <div style="font-size: 42px; margin-bottom: 16px;">{icon}</div>
                    <div style="font-size: 36px; font-weight: 800; color: {color}; margin-bottom: 8px;">
                        {value}
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 1px;">
                        {label}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # KPIs Section
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 30px;">
                <h3 style='color: white; margin-bottom: 24px; font-size: 24px; font-weight: 700;'>
                    📈 Key Performance Indicators
                </h3>
        """, unsafe_allow_html=True)
        
        for kpi in kpi_data:
            color = "#4ade80" if kpi['progress'] >= 75 else "#fbbf24" if kpi['progress'] >= 50 else "#ef4444"
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.5); border-radius: 16px; 
                            padding: 20px; margin-bottom: 16px; border: 1px solid rgba(148, 163, 184, 0.15);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <div style="color: #e2e8f0; font-weight: 500; font-size: 15px; flex: 1;">
                            {kpi['name']}
                        </div>
                        <div style="background: {color}20; color: {color}; font-weight: 700; 
                                    font-size: 20px; padding: 8px 16px; border-radius: 10px;
                                    border: 2px solid {color}40;">
                            {kpi['progress']}%
                        </div>
                    </div>
                    <div style="height: 12px; background: rgba(148, 163, 184, 0.15); 
                                border-radius: 8px; overflow: hidden; position: relative;">
                        <div style="width: {kpi['progress']}%; height: 100%; 
                                    background: linear-gradient(90deg, {color} 0%, {color}80 100%);
                                    border-radius: 8px; transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
                                    box-shadow: 0 0 20px {color}40;">
                        </div>
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 10px; display: flex; align-items: center; gap: 8px;">
                        <span>⏰</span>
                        <span>Deadline: {kpi['deadline']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Performance Chart
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 30px;">
                <h3 style='color: white; margin-bottom: 24px; font-size: 24px; font-weight: 700;'>
                    📊 Performance Trends
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        fig_performance = go.Figure()
        
        # Add traces with improved styling
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_25'],
            name='25% KPIs',
            mode='lines+markers',
            line=dict(color='#4ade80', width=4, shape='spline'),
            marker=dict(size=10, color='#4ade80', line=dict(color='white', width=2))
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_40'],
            name='40% KPIs',
            mode='lines+markers',
            line=dict(color='#3b82f6', width=4, shape='spline'),
            marker=dict(size=10, color='#3b82f6', line=dict(color='white', width=2))
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_20'],
            name='20% KPIs',
            mode='lines+markers',
            line=dict(color='#a78bfa', width=4, shape='spline'),
            marker=dict(size=10, color='#a78bfa', line=dict(color='white', width=2))
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_10'],
            name='10% KPIs',
            mode='lines+markers',
            line=dict(color='#ec4899', width=4, shape='spline'),
            marker=dict(size=10, color='#ec4899', line=dict(color='white', width=2))
        ))
        
        fig_performance.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
            font={'color': "white", 'family': "Outfit", 'size': 12},
            height=380,
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='rgba(148, 163, 184, 0.3)',
                borderwidth=1,
                font=dict(size=11)
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(148, 163, 184, 0.1)',
                gridwidth=1,
                zeroline=False,
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(148, 163, 184, 0.1)',
                gridwidth=1,
                zeroline=False,
                title="Progress %",
                titlefont=dict(size=13)
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='rgba(30, 41, 59, 0.95)',
                font_size=12,
                font_family="Outfit"
            )
        )
        
        st.plotly_chart(fig_performance, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Competencies Radar Chart
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);">
                <h3 style='color: white; margin-bottom: 24px; font-size: 24px; font-weight: 700;'>
                    🎯 Competencies Assessment
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        fig_radar = go.Figure()
        
        categories = list(competencies.keys())
        values = list(competencies.values())
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#4ade80', line=dict(color='white', width=2)),
            name='Current Level'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(15, 23, 42, 0.5)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=True,
                    ticks='',
                    gridcolor='rgba(148, 163, 184, 0.2)',
                    tickfont=dict(color='white', size=11),
                    ticksuffix='%'
                ),
                angularaxis=dict(
                    gridcolor='rgba(148, 163, 184, 0.2)',
                    tickfont=dict(color='white', size=13, family='Outfit'),
                    linecolor='rgba(148, 163, 184, 0.3)'
                )
            ),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font={'color': "white", 'family': "Outfit"},
            height=450,
            margin=dict(l=80, r=80, t=40, b=40),
            showlegend=False,
            hoverlabel=dict(
                bgcolor='rgba(30, 41, 59, 0.95)',
                font_size=12,
                font_family="Outfit"
            )
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Activity Feed
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 30px;">
                <h3 style='color: white; margin-bottom: 24px; font-size: 24px; font-weight: 700;'>
                    📣 Recent Activity
                </h3>
        """, unsafe_allow_html=True)
        
        avatar_colors = ["#667eea", "#764ba2", "#f093fb", "#4facfe"]
        for idx, activity in enumerate(activity_feed):
            initials = "".join([name[0] for name in activity['name'].split()])
            color = avatar_colors[idx % len(avatar_colors)]
            st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 16px; 
                            padding: 16px; background: rgba(15, 23, 42, 0.5); 
                            border-radius: 16px; margin-bottom: 12px;
                            border: 1px solid rgba(148, 163, 184, 0.15);
                            transition: all 0.3s ease;"
                     onmouseover="this.style.transform='translateX(8px)'; this.style.borderColor='rgba(102, 126, 234, 0.4)';"
                     onmouseout="this.style.transform='translateX(0)'; this.style.borderColor='rgba(148, 163, 184, 0.15)';">
                    <div style="min-width: 50px; height: 50px; border-radius: 50%; 
                                background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                                display: flex; align-items: center; justify-content: center; 
                                font-weight: 700; font-size: 16px; color: white;
                                box-shadow: 0 4px 12px {color}40;">
                        {initials}
                    </div>
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-weight: 600; color: white; margin-bottom: 4px; font-size: 15px;">
                            {activity['name']}
                        </div>
                        <div style="font-size: 13px; color: #94a3b8; margin-bottom: 4px;">
                            {activity['action']}
                        </div>
                        <div style="font-size: 11px; color: #64748b; display: flex; align-items: center; gap: 4px;">
                            <span>🕐</span>
                            <span>{activity['time']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Training & Learning Activities
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style='color: white; font-size: 22px; font-weight: 700; margin: 0;'>
                        📚 Training & Learning
                    </h3>
                    <span style="background: rgba(59, 130, 246, 0.2); color: #3b82f6; 
                                 padding: 6px 14px; border-radius: 8px; font-size: 11px; 
                                 font-weight: 600; border: 1px solid rgba(59, 130, 246, 0.3);">
                        LMS / Oracle Learning
                    </span>
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-bottom: 20px;">
                    Automatically tracked through learning management systems
                </div>
        """, unsafe_allow_html=True)
        
        training_activities = {
            "📚 Mandatory Training Completed": (employee_data['training_learning']['mandatory_training'], "#3b82f6"),
            "📖 Elective Training Completed": (employee_data['training_learning']['elective_training'], "#8b5cf6"),
            "🎓 Certifications Completed": (employee_data['training_learning']['certifications'], "#10b981"),
            "🛡️ Safety Training Completed": (employee_data['training_learning']['safety_training'], "#ef4444"),
            "✅ Compliance Modules Completed": (employee_data['training_learning']['compliance_modules'], "#06b6d4")
        }
        
        for label, (value, color) in training_activities.items():
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 14px 18px; background: rgba(15, 23, 42, 0.5); 
                            border-radius: 12px; margin-bottom: 8px;
                            border: 1px solid rgba(148, 163, 184, 0.15);
                            transition: all 0.3s ease;"
                     onmouseover="this.style.borderColor='{color}40'; this.style.transform='scale(1.02)';"
                     onmouseout="this.style.borderColor='rgba(148, 163, 184, 0.15)'; this.style.transform='scale(1)';">
                    <span style="color: #e2e8f0; font-size: 13px; font-weight: 500;">{label}</span>
                    <span style="background: {color}20; color: {color}; font-weight: 700; 
                                font-size: 18px; padding: 4px 14px; border-radius: 8px;
                                min-width: 45px; text-align: center; border: 2px solid {color}40;">
                        {value}
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # HR Engagement Activities
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style='color: white; font-size: 22px; font-weight: 700; margin: 0;'>
                        👥 HR Engagement
                    </h3>
                    <span style="background: rgba(139, 92, 246, 0.2); color: #8b5cf6; 
                                 padding: 6px 14px; border-radius: 8px; font-size: 11px; 
                                 font-weight: 600; border: 1px solid rgba(139, 92, 246, 0.3);">
                        Oracle HCM / MS Teams
                    </span>
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-bottom: 20px;">
                    Tracked through HCM, Teams attendance, and HR surveys
                </div>
        """, unsafe_allow_html=True)
        
        hr_activities = {
            "📋 Completed Engagement Survey": (employee_data['hr_engagement']['engagement_surveys'], "#a78bfa"),
            "🎤 Attended HR Session / Town Hall": (employee_data['hr_engagement']['hr_sessions_townhalls'], "#8b5cf6"),
            "⭐ Perfect Attendance (Monthly)": (employee_data['hr_engagement']['perfect_attendance'], "#ec4899")
        }
        
        for label, (value, color) in hr_activities.items():
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 14px 18px; background: rgba(15, 23, 42, 0.5); 
                            border-radius: 12px; margin-bottom: 8px;
                            border: 1px solid rgba(148, 163, 184, 0.15);
                            transition: all 0.3s ease;"
                     onmouseover="this.style.borderColor='{color}40'; this.style.transform='scale(1.02)';"
                     onmouseout="this.style.borderColor='rgba(148, 163, 184, 0.15)'; this.style.transform='scale(1)';">
                    <span style="color: #e2e8f0; font-size: 13px; font-weight: 500;">{label}</span>
                    <span style="background: {color}20; color: {color}; font-weight: 700; 
                                font-size: 18px; padding: 4px 14px; border-radius: 8px;
                                min-width: 45px; text-align: center; border: 2px solid {color}40;">
                        {value}
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Innovation Activities
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style='color: white; font-size: 22px; font-weight: 700; margin: 0;'>
                        💡 Innovation
                    </h3>
                    <span style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; 
                                 padding: 6px 14px; border-radius: 8px; font-size: 11px; 
                                 font-weight: 600; border: 1px solid rgba(245, 158, 11, 0.3);">
                        SharePoint / Power Automate
                    </span>
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-bottom: 20px;">
                    Tracked through digital idea submission systems
                </div>
        """, unsafe_allow_html=True)
        
        innovation_activities = {
            "💡 Submitted Innovation Idea": (employee_data['innovation']['innovation_ideas_submitted'], "#f59e0b"),
            "🎯 Idea Accepted for Evaluation": (employee_data['innovation']['ideas_accepted'], "#10b981"),
            "📊 Participated in Digital Survey": (employee_data['innovation']['digital_surveys'], "#06b6d4")
        }
        
        for label, (value, color) in innovation_activities.items():
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 14px 18px; background: rgba(15, 23, 42, 0.5); 
                            border-radius: 12px; margin-bottom: 8px;
                            border: 1px solid rgba(148, 163, 184, 0.15);
                            transition: all 0.3s ease;"
                     onmouseover="this.style.borderColor='{color}40'; this.style.transform='scale(1.02)';"
                     onmouseout="this.style.borderColor='rgba(148, 163, 184, 0.15)'; this.style.transform='scale(1)';">
                    <span style="color: #e2e8f0; font-size: 13px; font-weight: 500;">{label}</span>
                    <span style="background: {color}20; color: {color}; font-weight: 700; 
                                font-size: 18px; padding: 4px 14px; border-radius: 8px;
                                min-width: 45px; text-align: center; border: 2px solid {color}40;">
                        {value}
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Events & Participation Activities
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);
                        margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style='color: white; font-size: 22px; font-weight: 700; margin: 0;'>
                        🎪 Events & Participation
                    </h3>
                    <span style="background: rgba(236, 72, 153, 0.2); color: #ec4899; 
                                 padding: 6px 14px; border-radius: 8px; font-size: 11px; 
                                 font-weight: 600; border: 1px solid rgba(236, 72, 153, 0.3);">
                        HR / Event Logs
                    </span>
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-bottom: 20px;">
                    Logged by HR, CSR teams, or event attendance lists
                </div>
        """, unsafe_allow_html=True)
        
        events_activities = {
            "🎪 Attended Corporate Event": (employee_data['events_participation']['corporate_events'], "#a78bfa"),
            "❤️ Participated in CSR Activity": (employee_data['events_participation']['csr_activities'], "#ec4899"),
            "🧘 Participated in Wellness Session": (employee_data['events_participation']['wellness_sessions'], "#84cc16")
        }
        
        for label, (value, color) in events_activities.items():
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 14px 18px; background: rgba(15, 23, 42, 0.5); 
                            border-radius: 12px; margin-bottom: 8px;
                            border: 1px solid rgba(148, 163, 184, 0.15);
                            transition: all 0.3s ease;"
                     onmouseover="this.style.borderColor='{color}40'; this.style.transform='scale(1.02)';"
                     onmouseout="this.style.borderColor='rgba(148, 163, 184, 0.15)'; this.style.transform='scale(1)';">
                    <span style="color: #e2e8f0; font-size: 13px; font-weight: 500;">{label}</span>
                    <span style="background: {color}20; color: {color}; font-weight: 700; 
                                font-size: 18px; padding: 4px 14px; border-radius: 8px;
                                min-width: 45px; text-align: center; border: 2px solid {color}40;">
                        {value}
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Certifications
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 30px; border: 1px solid rgba(148, 163, 184, 0.2);">
                <h3 style='color: white; margin-bottom: 24px; font-size: 24px; font-weight: 700;'>
                    🏅 Certifications Earned
                </h3>
        """, unsafe_allow_html=True)
        
        cert_colors = ["#667eea", "#f093fb"]
        for idx, cert in enumerate(employee_data['certifications_list']):
            color = cert_colors[idx % len(cert_colors)]
            st.markdown(f"""
                <div style="padding: 20px; 
                            background: linear-gradient(135deg, {color}25 0%, {color}15 100%); 
                            border-radius: 16px; margin-bottom: 16px; 
                            border: 2px solid {color}40;
                            box-shadow: 0 4px 12px {color}20;
                            transition: all 0.3s ease;"
                     onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 24px {color}30';"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px {color}20';">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="font-size: 32px;">🎓</div>
                        <div>
                            <div style="font-weight: 600; color: white; font-size: 16px; margin-bottom: 4px;">
                                {cert}
                            </div>
                            <div style="font-size: 12px; color: {color}; font-weight: 500;">
                                ✓ Certified
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 2: ORGANIZATION DASHBOARD (LIGHT THEME) ====================
with tab2:
    # Apply light theme background
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background: #f5f7fb;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px; color: #1e293b;'>Organization Engagement Overview</h2>", unsafe_allow_html=True)
    
    # Top Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # Engagement Score Gauge
        st.markdown(f"""
            <div class="engagement-score">
                <div class="score-label">Feed Engagement Score</div>
                <div class="score-number">{org_data['engagement_score']}</div>
                <div class="score-benchmark">↗ {org_data['benchmark_diff']} above benchmark</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="org-metric-card">
                <div class="org-metric-icon">👍</div>
                <div class="org-metric-value">{org_data['total_likes']:,}</div>
                <div class="org-metric-label">Total Likes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="org-metric-card">
                <div class="org-metric-icon">💬</div>
                <div class="org-metric-value">{org_data['total_comments']:,}</div>
                <div class="org-metric-label">Total Comments</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="org-metric-card">
                <div class="org-metric-icon">📋</div>
                <div class="org-metric-value">{org_data['total_appreciations']:,}</div>
                <div class="org-metric-label">Total Appreciation</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class="org-metric-card">
                <div class="org-metric-icon">🏆</div>
                <div class="org-metric-value">{org_data['total_recognitions']:,}</div>
                <div class="org-metric-label">Total Recognitions</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("<h3 style='color: #1e293b; margin-bottom: 20px;'>📊 Award Distribution by Year</h3>", unsafe_allow_html=True)
        
        fig_awards = go.Figure()
        
        fig_awards.add_trace(go.Bar(
            x=award_distribution['Year'],
            y=award_distribution['Recognitions'],
            marker=dict(
                color=award_distribution['Recognitions'],
                colorscale='Blues',
                line=dict(color='#3b82f6', width=2)
            ),
            text=award_distribution['Recognitions'],
            textposition='outside',
            textfont=dict(size=14, color='#1e293b', family='Outfit', weight='bold')
        ))
        
        fig_awards.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font={'color': "#1e293b", 'family': "Outfit"},
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(
                title="Year",
                showgrid=False,
                zeroline=False,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="Number of Recognitions",
                showgrid=True,
                gridcolor='rgba(0, 0, 0, 0.05)',
                zeroline=False
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig_awards, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: #1e293b; margin-bottom: 20px;'>🏅 Top Awards Given</h3>", unsafe_allow_html=True)
        
        for award in top_awards:
            st.markdown(f"""
                <div class="award-badge">
                    <div class="award-icon">{award['icon']}</div>
                    <div class="award-name">{award['name']}</div>
                    <div class="award-count">{award['count']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Pie Chart of Award Distribution
        fig_pie = go.Figure(data=[go.Pie(
            labels=[award['name'] for award in top_awards],
            values=[award['count'] for award in top_awards],
            hole=0.4,
            marker=dict(colors=['#3b82f6', '#8b5cf6', '#06b6d4']),
            textinfo='percent',
            textfont=dict(size=14, color='white', family='Outfit', weight='bold')
        )])
        
        fig_pie.update_layout(
            paper_bgcolor='white',
            font={'color': "#1e293b", 'family': "Outfit"},
            height=250,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional Insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="light-card">
                <h4 style='color: #1e293b; margin-bottom: 16px;'>📈 Year-over-Year Growth</h4>
                <div style='font-size: 36px; font-weight: 700; color: #10b981; margin: 16px 0;'>+18.6%</div>
                <p style='color: #64748b; font-size: 14px;'>Recognitions increased from 1,180 to 1,400 in 2024</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="light-card">
                <h4 style='color: #1e293b; margin-bottom: 16px;'>👥 Most Active Month</h4>
                <div style='font-size: 36px; font-weight: 700; color: #3b82f6; margin: 16px 0;'>December</div>
                <p style='color: #64748b; font-size: 14px;'>Peak engagement period with 156 recognitions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="light-card">
                <h4 style='color: #1e293b; margin-bottom: 16px;'>⭐ Average per Employee</h4>
                <div style='font-size: 36px; font-weight: 700; color: #8b5cf6; margin: 16px 0;'>3.2</div>
                <p style='color: #64748b; font-size: 14px;'>Recognitions per employee in 2024</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 20px; font-size: 14px;'>
        <p>🏆 HR Reward & Engagement Platform • Built with Streamlit</p>
        <p style='font-size: 12px; margin-top: 8px;'>Demo Version • All data is simulated for demonstration purposes</p>
    </div>
""", unsafe_allow_html=True)
