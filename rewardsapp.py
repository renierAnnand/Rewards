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

# Fake Employee Data
employee_data = {
    "name": "Andrei Spitzer",
    "role": "Digital Designer",
    "department": "PR & Marketing",
    "tenure_days": 168,
    "level": 7,
    "xp_current": 580,
    "xp_required": 800,
    "coins": 72,
    "league": "Sapphire",
    "aura": "Master",
    "trainings": {
        "mandatory": 14,
        "elective": 8,
        "safety": 3,
        "compliance": 6
    },
    "certifications": ["Azure Fundamentals", "Lean Six Sigma Yellow Belt"],
    "activities": {
        "engagement_surveys": 3,
        "hr_sessions": 4,
        "perfect_attendance": 2,
        "innovation_ideas": 5,
        "ideas_accepted": 2,
        "digital_surveys": 6,
        "corporate_events": 4,
        "csr_activities": 2,
        "wellness_sessions": 3
    }
}

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
                background: #0f1425;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Profile Header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div class="profile-header">
                <h1 style='margin-bottom: 8px;'>{employee_data['name']}</h1>
                <p style='font-size: 18px; opacity: 0.9; margin-bottom: 16px;'>{employee_data['role']} • {employee_data['department']}</p>
                <div>
                    <span class="level-badge">🏅 League: {employee_data['league']}</span>
                    <span class="level-badge">📅 In company: {employee_data['tenure_days']} days</span>
                    <span class="level-badge">✨ Aura: {employee_data['aura']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Level Progress Circle
        progress_percent = (employee_data['xp_current'] / employee_data['xp_required']) * 100
        
        fig_level = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=employee_data['xp_current'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Level {employee_data['level']}", 'font': {'size': 24, 'color': 'white'}},
            delta={'reference': employee_data['xp_required'], 'suffix': f" / {employee_data['xp_required']} XP"},
            gauge={
                'axis': {'range': [None, employee_data['xp_required']], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#4ade80"},
                'bgcolor': "rgba(255, 255, 255, 0.1)",
                'borderwidth': 2,
                'bordercolor': "rgba(255, 255, 255, 0.2)",
                'steps': [
                    {'range': [0, employee_data['xp_required']], 'color': 'rgba(255, 255, 255, 0.05)'}
                ],
                'threshold': {
                    'line': {'color': "#3b82f6", 'width': 4},
                    'thickness': 0.75,
                    'value': employee_data['xp_current']
                }
            }
        ))
        
        fig_level.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Outfit"},
            height=250,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig_level, use_container_width=True)
    
    st.markdown("---")
    
    # Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("🎯", "Missions", 365, col1),
        ("💬", "Social Activity", 125, col2),
        ("🌟", "Competencies", 160, col3),
        ("❤️", "Helpfulness", 15, col4),
        ("🪙", "Coins", employee_data['coins'], col5)
    ]
    
    for icon, label, value, col in metrics:
        with col:
            st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size: 28px;">{icon}</div>
                    <div class="stat-number">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # KPIs Section
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>📈 Key Performance Indicators</h3>", unsafe_allow_html=True)
        
        for kpi in kpi_data:
            st.markdown(f"""
                <div class="kpi-item">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div class="kpi-title">{kpi['name']}</div>
                        <div style="color: #4ade80; font-weight: 700; font-size: 18px;">{kpi['progress']}%</div>
                    </div>
                    <div class="kpi-bar">
                        <div class="kpi-progress" style="width: {kpi['progress']}%;"></div>
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 8px;">Deadline: {kpi['deadline']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Performance Chart
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>📊 Performance Trends</h3>", unsafe_allow_html=True)
        
        fig_performance = go.Figure()
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_25'],
            name='25% KPIs',
            mode='lines+markers',
            line=dict(color='#4ade80', width=3),
            marker=dict(size=8)
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_40'],
            name='40% KPIs',
            mode='lines+markers',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8)
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_20'],
            name='20% KPIs',
            mode='lines+markers',
            line=dict(color='#a78bfa', width=3),
            marker=dict(size=8)
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=performance_data['Quarter'],
            y=performance_data['KPIs_10'],
            name='10% KPIs',
            mode='lines+markers',
            line=dict(color='#ec4899', width=3),
            marker=dict(size=8)
        ))
        
        fig_performance.update_layout(
            paper_bgcolor='rgba(30, 41, 59, 0.5)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Outfit"},
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=False,
                title="Progress %"
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_performance, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Competencies Radar Chart
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>🎯 Competencies</h3>", unsafe_allow_html=True)
        
        fig_radar = go.Figure()
        
        categories = list(competencies.keys())
        values = list(competencies.values())
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(59, 130, 246, 0.3)',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8, color='#4ade80')
        ))
        
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(30, 41, 59, 0.5)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=True,
                    ticks='',
                    gridcolor='rgba(255, 255, 255, 0.2)',
                    tickfont=dict(color='white')
                ),
                angularaxis=dict(
                    gridcolor='rgba(255, 255, 255, 0.2)',
                    tickfont=dict(color='white', size=12)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Outfit"},
            height=400,
            margin=dict(l=80, r=80, t=40, b=40),
            showlegend=False
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Activity Feed
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>📣 Activity Feed</h3>", unsafe_allow_html=True)
        
        for activity in activity_feed:
            initials = "".join([name[0] for name in activity['name'].split()])
            st.markdown(f"""
                <div class="activity-item">
                    <div class="activity-avatar">{initials}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: white; margin-bottom: 4px;">{activity['name']}</div>
                        <div style="font-size: 13px; color: #94a3b8;">{activity['action']}</div>
                        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">{activity['time']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Reward Activities Summary
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>🎓 Training & Activities</h3>", unsafe_allow_html=True)
        
        activities_summary = {
            "📚 Mandatory Trainings": employee_data['trainings']['mandatory'],
            "📖 Elective Trainings": employee_data['trainings']['elective'],
            "🛡️ Safety Trainings": employee_data['trainings']['safety'],
            "✅ Compliance Modules": employee_data['trainings']['compliance'],
            "💡 Innovation Ideas": employee_data['activities']['innovation_ideas'],
            "🎯 Ideas Accepted": employee_data['activities']['ideas_accepted'],
            "❤️ CSR Activities": employee_data['activities']['csr_activities'],
            "🧘 Wellness Sessions": employee_data['activities']['wellness_sessions'],
            "🎪 Corporate Events": employee_data['activities']['corporate_events']
        }
        
        for label, value in activities_summary.items():
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 12px; background: rgba(255, 255, 255, 0.05); 
                            border-radius: 10px; margin-bottom: 8px;">
                    <span style="color: white; font-size: 14px;">{label}</span>
                    <span style="color: #4ade80; font-weight: 700; font-size: 18px;">{value}</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Certifications
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>🏅 Certifications</h3>", unsafe_allow_html=True)
        
        for cert in employee_data['certifications']:
            st.markdown(f"""
                <div style="padding: 16px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); 
                            border-radius: 12px; margin-bottom: 12px; border: 1px solid rgba(102, 126, 234, 0.3);">
                    <div style="font-weight: 600; color: white; font-size: 15px;">🎓 {cert}</div>
                </div>
            """, unsafe_allow_html=True)

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
            plot_bgcolor='rgba(0,0,0,0)',
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