"""
==============================================================================
HR REWARDS & ENGAGEMENT PLATFORM - COMPLETE SYSTEM
==============================================================================
Single-file Streamlit application implementing comprehensive rewards system
with gamification, admin management, and analytics.

Author: Alkhorayef HR Digital Team
Version: 2.0
==============================================================================
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import random

# ==============================================================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ==============================================================================

# Page Configuration
st.set_page_config(
    page_title="HR Rewards Platform",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
        
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        .main { background-color: #0f1425; }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(30, 41, 59, 0.5);
            padding: 8px;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 600;
        }
        
        .metric-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
            border-color: rgba(148, 163, 184, 0.4);
        }
        
        .success-message {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
            color: white;
            padding: 16px;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .warning-message {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: white;
            padding: 16px;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .error-message {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 16px;
            border-radius: 12px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

# Leaderboard Levels Configuration
LEVELS = [
    {"id": 1, "name": "Bronze", "icon": "🥉", "points_min": 0, "points_max": 499, "color": "#cd7f32"},
    {"id": 2, "name": "Silver", "icon": "🥈", "points_min": 500, "points_max": 999, "color": "#c0c0c0"},
    {"id": 3, "name": "Gold", "icon": "🥇", "points_min": 1000, "points_max": 2999, "color": "#ffd700"},
    {"id": 4, "name": "Platinum", "icon": "💎", "points_min": 3000, "points_max": 4999, "color": "#e5e4e2"},
    {"id": 5, "name": "Champion", "icon": "🏅", "points_min": 5000, "points_max": 7999, "color": "#4169e1"},
    {"id": 6, "name": "Grand Master", "icon": "👑", "points_min": 8000, "points_max": 999999, "color": "#9966cc"}
]

# Badges Configuration
BADGES = [
    {"id": 1, "name": "Survey Champion", "icon": "📊", "criteria": "Complete 50 surveys", "points_threshold": 50, "category": "surveys"},
    {"id": 2, "name": "Training Master", "icon": "📚", "criteria": "Complete 100 training hours", "points_threshold": 100, "category": "training"},
    {"id": 3, "name": "Innovation Star", "icon": "💡", "criteria": "Submit 10 ideas", "points_threshold": 10, "category": "innovation"},
    {"id": 4, "name": "Perfect Attendee", "icon": "⭐", "criteria": "3 months perfect attendance", "points_threshold": 3, "category": "attendance"},
    {"id": 5, "name": "Team Player", "icon": "🤝", "criteria": "Attend 20 events", "points_threshold": 20, "category": "events"},
    {"id": 6, "name": "Certificate Collector", "icon": "🎓", "criteria": "Earn 5 certifications", "points_threshold": 5, "category": "certifications"},
    {"id": 7, "name": "Wellness Warrior", "icon": "🏋️", "criteria": "Attend 15 wellness sessions", "points_threshold": 15, "category": "wellness"},
    {"id": 8, "name": "KPI Crusher", "icon": "🎯", "criteria": "Achieve 10 KPI targets", "points_threshold": 10, "category": "performance"}
]

# Scoring Rules - Central Source of Truth
SCORING_RULES = {
    # Surveys
    "survey_per_question": 10,
    "survey_short": 50,      # 5-10 min surveys
    "survey_medium": 80,     # 10-15 min surveys
    "survey_long": 100,      # 15-20 min surveys
    
    # Training
    "training_per_hour": 20,
    "training_full_day": 200,    # 8 hours
    "training_half_day": 100,    # 4 hours
    "training_mandatory": 30,    # per hour for mandatory
    "training_elective": 20,     # per hour for elective
    
    # Certifications
    "certification_basic": 250,
    "certification_advanced": 500,
    "certification_professional": 750,
    
    # Initiatives
    "initiative_qudwa": 500,
    "initiative_digital_champion": 1000,
    "initiative_alkhorayef_champion": 1000,
    "initiative_thank_you_card": 50,
    "initiative_idea_submission": 60,
    "initiative_idea_accepted": 1000,
    
    # Events
    "event_corporate": 80,
    "event_csr": 100,
    "event_wellness": 45,
    
    # Performance
    "kpi_target_achieved": 200,
    "kpi_exceed_target": 300,
    "extra_milestone": 150,
    
    # Attendance
    "perfect_attendance_month": 300,
    "perfect_attendance_quarter": 1000,
    
    # Other
    "compliance_module": 30,
    "safety_training_hour": 25,
    "hr_session": 10,
    "town_hall": 10
}

# Earn Types (Goals) Configuration
EARN_TYPES = [
    {"id": 1, "name": "Employee Survey", "category": "surveys", "points": "Variable", "description": "Complete employee satisfaction surveys"},
    {"id": 2, "name": "Training Course", "category": "training", "points": "Variable", "description": "Attend and complete training courses"},
    {"id": 3, "name": "Professional Certification", "category": "certifications", "points": "250-750", "description": "Earn professional certifications"},
    {"id": 4, "name": "Innovation Idea", "category": "innovation", "points": "60-1000", "description": "Submit innovative ideas"},
    {"id": 5, "name": "Corporate Event", "category": "events", "points": "80", "description": "Attend corporate events"},
    {"id": 6, "name": "CSR Activity", "category": "events", "points": "100", "description": "Participate in CSR activities"},
    {"id": 7, "name": "KPI Achievement", "category": "performance", "points": "200-300", "description": "Achieve KPI targets"},
    {"id": 8, "name": "Perfect Attendance", "category": "attendance", "points": "300-1000", "description": "Maintain perfect attendance"},
    {"id": 9, "name": "Qudwa Program", "category": "innovation", "points": "500", "description": "Complete Qudwa leadership program"},
    {"id": 10, "name": "Wellness Session", "category": "events", "points": "45", "description": "Attend wellness sessions"}
]

# Redemption Options Configuration
REDEMPTION_OPTIONS = [
    {"id": 1, "name": "Vacation Days", "points": 4000, "value": "2 Days", "icon": "🏖️", "category": "Time Off", "description": "2 additional vacation days"},
    {"id": 2, "name": "Shopping Voucher", "points": 5000, "value": "500 SAR", "icon": "🛍️", "category": "Vouchers", "description": "Shopping voucher worth 500 SAR"},
    {"id": 3, "name": "Cash Reward", "points": 1500, "value": "150 SAR", "icon": "💵", "category": "Cash", "description": "Direct cash reward"},
    {"id": 4, "name": "Gym Membership", "points": 3000, "value": "3 Months", "icon": "🏋️", "category": "Wellness", "description": "3-month gym membership"},
    {"id": 5, "name": "Training Course", "points": 2500, "value": "Course Credit", "icon": "📚", "category": "Learning", "description": "Credit for external training"},
    {"id": 6, "name": "Tech Gadget", "points": 8000, "value": "800 SAR", "icon": "📱", "category": "Electronics", "description": "Tech gadget voucher"},
    {"id": 7, "name": "Dining Voucher", "points": 2000, "value": "200 SAR", "icon": "🍽️", "category": "Dining", "description": "Restaurant voucher"},
    {"id": 8, "name": "Spa Package", "points": 3500, "value": "350 SAR", "icon": "💆", "category": "Wellness", "description": "Spa and wellness package"},
    {"id": 9, "name": "Books/Learning", "points": 1000, "value": "100 SAR", "icon": "📖", "category": "Learning", "description": "Books or e-learning credit"},
    {"id": 10, "name": "Travel Voucher", "points": 10000, "value": "1000 SAR", "icon": "✈️", "category": "Travel", "description": "Travel booking voucher"}
]

# ==============================================================================
# SECTION 2: DATA STRUCTURES (In-Memory Database Simulation)
# ==============================================================================

# Initialize session state for data persistence
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # Users database
    st.session_state.users = [
        {"id": 1, "name": "Ahmed Al-Saud", "email": "ahmed@alkhorayef.com", "department": "Engineering", "role": "user", "join_date": "2023-01-15"},
        {"id": 2, "name": "Mahmoud Hamidah", "email": "mahmoud.hamidah@alkhorayef.com", "department": "HR", "role": "admin", "join_date": "2022-06-10"},
        {"id": 3, "name": "Renier Annandale", "email": "renier@alkhorayef.com", "department": "IT", "title": "Digital Transformation Director", "role": "user", "join_date": "2023-06-20"},
        {"id": 4, "name": "Sara Al-Mutairi", "email": "sara@alkhorayef.com", "department": "Finance", "role": "user", "join_date": "2022-03-05"},
        {"id": 5, "name": "Mohammed Al-Qahtani", "email": "mohammed@alkhorayef.com", "department": "Operations", "role": "user", "join_date": "2021-11-12"}
    ]
    
    # Current user (for demo purposes - in production, this would be from authentication)
    st.session_state.current_user_id = 3  # Renier
    
    # Points ledger (all point transactions)
    st.session_state.points_ledger = [
        {"id": 1, "user_id": 3, "points": 840, "category": "training", "description": "Mandatory training - 42 hours", "date": "2024-11-15", "status": "approved", "approved_by": 2, "approved_date": "2024-11-15"},
        {"id": 2, "user_id": 3, "points": 480, "category": "training", "description": "Elective training - 24 hours", "date": "2024-11-20", "status": "approved", "approved_by": 2, "approved_date": "2024-11-20"},
        {"id": 3, "user_id": 3, "points": 500, "category": "certifications", "description": "Azure Fundamentals", "date": "2024-10-05", "status": "approved", "approved_by": 2, "approved_date": "2024-10-05"},
        {"id": 4, "user_id": 3, "points": 1000, "category": "innovation", "description": "Digital Champion - Idea Accepted", "date": "2024-12-01", "status": "approved", "approved_by": 2, "approved_date": "2024-12-01"},
        {"id": 5, "user_id": 3, "points": 80, "category": "events", "description": "Corporate Town Hall", "date": "2024-11-25", "status": "approved", "approved_by": 2, "approved_date": "2024-11-25"},
        {"id": 6, "user_id": 1, "points": 300, "category": "performance", "description": "KPI Target Achieved Q3", "date": "2024-10-01", "status": "approved", "approved_by": 2, "approved_date": "2024-10-01"},
        {"id": 7, "user_id": 4, "points": 1000, "category": "attendance", "description": "Perfect Attendance Q4", "date": "2024-12-01", "status": "approved", "approved_by": 2, "approved_date": "2024-12-01"}
    ]
    
    # Reward requests (pending/approved/rejected point claims)
    st.session_state.reward_requests = [
        {"id": 1, "user_id": 3, "earn_type": "Training Course", "category": "training", "points_requested": 200, "description": "Completed Advanced Leadership Training", "date_submitted": "2024-12-08", "status": "pending", "justification": "8-hour leadership course with certificate", "attachment_desc": "Certificate_Leadership.pdf"},
        {"id": 2, "user_id": 1, "earn_type": "Innovation Idea", "category": "innovation", "points_requested": 60, "description": "Submitted process improvement idea", "date_submitted": "2024-12-09", "status": "pending", "justification": "Idea to streamline approval workflows", "attachment_desc": "Idea_Workflow.docx"}
    ]
    
    # Redemption requests
    st.session_state.redemption_requests = [
        {"id": 1, "user_id": 3, "redemption_name": "Cash Reward", "points_cost": 1500, "date_submitted": "2024-12-05", "status": "approved", "approved_by": 2, "approved_date": "2024-12-06", "fulfillment_status": "completed"},
        {"id": 2, "user_id": 4, "redemption_name": "Gym Membership", "points_cost": 3000, "date_submitted": "2024-12-07", "status": "pending", "fulfillment_status": "pending"}
    ]
    
    # User badges (earned badges)
    st.session_state.user_badges = [
        {"user_id": 3, "badge_id": 2, "earned_date": "2024-11-20"},
        {"user_id": 3, "badge_id": 3, "earned_date": "2024-12-01"},
        {"user_id": 1, "badge_id": 8, "earned_date": "2024-10-01"}
    ]
    
    # Notifications
    st.session_state.notifications = [
        {"id": 1, "user_id": 3, "type": "points_earned", "message": "You earned 200 points for Advanced Leadership Training!", "date": "2024-11-20", "read": False},
        {"id": 2, "user_id": 3, "type": "level_up", "message": "Congratulations! You've reached Gold level!", "date": "2024-12-01", "read": False},
        {"id": 3, "user_id": 2, "type": "admin_request", "message": "New reward point request from Ahmed Al-Saud", "date": "2024-12-09", "read": False},
        {"id": 4, "user_id": 2, "type": "admin_redemption", "message": "New redemption request from Sara Al-Mutairi", "date": "2024-12-07", "read": False}
    ]
    
    # Audit log
    st.session_state.audit_log = [
        {"id": 1, "user_id": 2, "action": "approved_reward_request", "details": "Approved 840 points for Renier Annandale - Training", "date": "2024-11-15 14:30"},
        {"id": 2, "user_id": 2, "action": "approved_redemption", "details": "Approved Cash Reward redemption for Renier Annandale", "date": "2024-12-06 10:15"},
        {"id": 3, "user_id": 3, "action": "submitted_reward_request", "details": "Submitted request for 200 points - Training", "date": "2024-12-08 09:20"},
        {"id": 4, "user_id": 4, "action": "submitted_redemption", "details": "Requested Gym Membership redemption", "date": "2024-12-07 16:45"}
    ]
    
    # Next IDs for new records
    st.session_state.next_points_id = max([p["id"] for p in st.session_state.points_ledger], default=0) + 1
    st.session_state.next_request_id = max([r["id"] for r in st.session_state.reward_requests], default=0) + 1
    st.session_state.next_redemption_id = max([r["id"] for r in st.session_state.redemption_requests], default=0) + 1
    st.session_state.next_notification_id = max([n["id"] for n in st.session_state.notifications], default=0) + 1
    st.session_state.next_audit_id = max([a["id"] for a in st.session_state.audit_log], default=0) + 1

# ==============================================================================
# SECTION 3: HELPER FUNCTIONS - SCORING & CALCULATIONS
# ==============================================================================

def calculate_points_for_survey(num_questions: int, survey_type: str = "medium") -> int:
    """Calculate points for survey completion"""
    if survey_type == "short":
        return SCORING_RULES["survey_short"]
    elif survey_type == "medium":
        return SCORING_RULES["survey_medium"]
    elif survey_type == "long":
        return SCORING_RULES["survey_long"]
    else:
        return num_questions * SCORING_RULES["survey_per_question"]

def calculate_points_for_training(hours: float, training_type: str = "mandatory") -> int:
    """Calculate points for training completion"""
    if hours >= 8:
        return SCORING_RULES["training_full_day"]
    elif hours >= 4:
        return SCORING_RULES["training_half_day"]
    else:
        rate = SCORING_RULES["training_mandatory"] if training_type == "mandatory" else SCORING_RULES["training_elective"]
        return int(hours * rate)

def calculate_points_for_certification(cert_level: str = "basic") -> int:
    """Calculate points for certification"""
    if cert_level == "professional":
        return SCORING_RULES["certification_professional"]
    elif cert_level == "advanced":
        return SCORING_RULES["certification_advanced"]
    else:
        return SCORING_RULES["certification_basic"]

def calculate_points_for_initiative(initiative_type: str) -> int:
    """Calculate points for initiative participation"""
    key = f"initiative_{initiative_type.lower().replace(' ', '_')}"
    return SCORING_RULES.get(key, 50)

def calculate_points_for_event(event_type: str) -> int:
    """Calculate points for event attendance"""
    key = f"event_{event_type.lower()}"
    return SCORING_RULES.get(key, 50)

def get_user_total_points(user_id: int) -> int:
    """Get total approved points for a user"""
    earned = sum(p["points"] for p in st.session_state.points_ledger 
                 if p["user_id"] == user_id and p["status"] == "approved")
    redeemed = sum(r["points_cost"] for r in st.session_state.redemption_requests 
                   if r["user_id"] == user_id and r["status"] == "approved")
    return earned - redeemed

def get_user_level(total_points: int) -> Dict:
    """Determine user's level based on total points"""
    for level in reversed(LEVELS):
        if total_points >= level["points_min"]:
            return level
    return LEVELS[0]

def get_points_by_category(user_id: int) -> Dict[str, int]:
    """Get points breakdown by category for a user"""
    categories = {}
    for point in st.session_state.points_ledger:
        if point["user_id"] == user_id and point["status"] == "approved":
            cat = point["category"]
            categories[cat] = categories.get(cat, 0) + point["points"]
    return categories

def check_and_award_badges(user_id: int):
    """Check if user qualifies for any new badges and award them"""
    user_points_by_cat = get_points_by_category(user_id)
    current_badges = [b["badge_id"] for b in st.session_state.user_badges if b["user_id"] == user_id]
    
    for badge in BADGES:
        if badge["id"] not in current_badges:
            # Count activities in badge category
            count = 0
            for point in st.session_state.points_ledger:
                if point["user_id"] == user_id and point["category"] == badge["category"]:
                    count += 1
            
            if count >= badge["points_threshold"]:
                st.session_state.user_badges.append({
                    "user_id": user_id,
                    "badge_id": badge["id"],
                    "earned_date": datetime.now().strftime("%Y-%m-%d")
                })
                # Create notification
                add_notification(user_id, "badge_earned", f"🎉 You've earned the {badge['name']} badge!")

def check_duplicate_claim(user_id: int, category: str, description: str, date: str) -> bool:
    """Check if a similar claim already exists (anti-abuse)"""
    for point in st.session_state.points_ledger:
        if (point["user_id"] == user_id and 
            point["category"] == category and 
            point["description"] == description and 
            point["date"] == date):
            return True
    return False

def add_notification(user_id: int, notif_type: str, message: str):
    """Add a notification for a user"""
    st.session_state.notifications.append({
        "id": st.session_state.next_notification_id,
        "user_id": user_id,
        "type": notif_type,
        "message": message,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False
    })
    st.session_state.next_notification_id += 1

def add_audit_log(user_id: int, action: str, details: str):
    """Add entry to audit log"""
    st.session_state.audit_log.append({
        "id": st.session_state.next_audit_id,
        "user_id": user_id,
        "action": action,
        "details": details,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    st.session_state.next_audit_id += 1

def generate_leaderboard() -> pd.DataFrame:
    """Generate leaderboard with all users ranked by points"""
    leaderboard = []
    for user in st.session_state.users:
        if user["role"] == "user":  # Exclude admins from leaderboard
            total_points = get_user_total_points(user["id"])
            level = get_user_level(total_points)
            leaderboard.append({
                "Rank": 0,
                "Name": user["name"],
                "Department": user["department"],
                "Points": total_points,
                "Level": f"{level['icon']} {level['name']}",
                "level_id": level["id"]
            })
    
    # Sort by points and assign ranks
    leaderboard.sort(key=lambda x: x["Points"], reverse=True)
    for i, entry in enumerate(leaderboard, 1):
        entry["Rank"] = i
    
    return pd.DataFrame(leaderboard)

# ==============================================================================
# SECTION 4: UI RENDERING FUNCTIONS - EMPLOYEE DASHBOARD
# ==============================================================================

def render_employee_dashboard():
    """Render employee dashboard with profile, points, activities, and redemption"""
    load_css()
    
    current_user = next(u for u in st.session_state.users if u["id"] == st.session_state.current_user_id)
    total_points = get_user_total_points(st.session_state.current_user_id)
    current_level = get_user_level(total_points)
    points_by_category = get_points_by_category(st.session_state.current_user_id)
    
    # Next level calculation
    next_level = None
    points_to_next = 0
    if current_level["id"] < len(LEVELS):
        next_level = LEVELS[current_level["id"]]
        points_to_next = next_level["points_min"] - total_points
    
    # Profile Header
    # Profile header - get title if it exists
    user_title = current_user.get('title', '')
    dept_display = f"{user_title}<br>{current_user['department']}" if user_title else current_user['department']
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 24px; padding: 40px; margin-bottom: 40px;
                    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);">
            <div style="display: grid; grid-template-columns: 1fr auto; gap: 40px; align-items: center;">
                <div>
                    <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 12px; color: white;'>{current_user['name']}</h1>
                    <p style='font-size: 20px; opacity: 0.95; margin-bottom: 24px; color: white; line-height: 1.4;'>
                        {dept_display}
                    </p>
                    <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;">
                        <span style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); 
                                     border-radius: 12px; padding: 10px 20px; font-weight: 600; 
                                     font-size: 15px; color: white; border: 1px solid rgba(255,255,255,0.3);">
                            {current_level['icon']} {current_level['name']} Level
                        </span>
                        <span style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); 
                                     border-radius: 12px; padding: 10px 20px; font-weight: 600; 
                                     font-size: 15px; color: white; border: 1px solid rgba(255,255,255,0.3);">
                            💰 {total_points:,} Points
                        </span>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.15); padding: 16px; border-radius: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="font-size: 14px; font-weight: 600; color: white;">Progress to Next Level</span>
                            <span style="font-size: 14px; font-weight: 600; color: white;">{total_points:,} / {next_level['points_min'] if next_level else 'MAX':,} pts</span>
                        </div>
                        <div style="height: 12px; background: rgba(255, 255, 255, 0.2); border-radius: 6px; overflow: hidden;">
                            <div style="width: {min(100, (total_points / next_level['points_min'] * 100) if next_level else 100)}%; 
                                        height: 100%; background: linear-gradient(90deg, #4ade80 0%, #10b981 100%); 
                                        transition: width 1s ease;"></div>
                        </div>
                        <div style="font-size: 12px; margin-top: 6px; color: white; opacity: 0.9;">
                            {points_to_next:,} points to {next_level['name'] if next_level else 'Grand Master'} level
                        </div>
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="width: 200px; height: 200px; border-radius: 50%; 
                                background: linear-gradient(135deg, {current_level['color']} 0%, rgba(255,255,255,0.3) 100%);
                                display: flex; align-items: center; justify-content: center;
                                position: relative; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);">
                        <div style="width: 175px; height: 175px; border-radius: 50%; 
                                    background: rgba(30, 41, 59, 0.95); display: flex; flex-direction: column; 
                                    align-items: center; justify-content: center;">
                            <div style="font-size: 64px; margin-bottom: 8px;">{current_level['icon']}</div>
                            <div style="font-size: 24px; font-weight: 800; color: {current_level['color']};">
                                {current_level['name']}
                            </div>
                            <div style="font-size: 14px; color: #94a3b8; margin-top: 4px;">
                                Level {current_level['id']}/6
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tabs = st.tabs(["📊 Overview", "🎯 Submit Request", "📜 My History", "🎁 Redeem Points", "🏆 My Badges"])
    
    with tabs[0]:  # Overview
        render_employee_overview(points_by_category, total_points)
    
    with tabs[1]:  # Submit Request
        render_submit_reward_request()
    
    with tabs[2]:  # History
        render_employee_history()
    
    with tabs[3]:  # Redemption
        render_redemption_section(total_points)
    
    with tabs[4]:  # Badges
        render_employee_badges()

def render_employee_overview(points_by_category: Dict, total_points: int):
    """Render employee overview with charts and metrics"""
    st.markdown("### 📊 Points Breakdown")
    
    # Category breakdown cards
    cols = st.columns(4)
    categories_display = [
        ("training", "📚 Training", "#3b82f6"),
        ("innovation", "💡 Innovation", "#a78bfa"),
        ("events", "🎪 Events", "#ec4899"),
        ("performance", "🎯 Performance", "#4ade80")
    ]
    
    for i, (cat, label, color) in enumerate(categories_display):
        with cols[i]:
            points = points_by_category.get(cat, 0)
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px);
                            border-radius: 16px; padding: 24px; border: 1px solid rgba(148, 163, 184, 0.2);
                            transition: all 0.3s ease; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 8px;">{label.split()[0]}</div>
                    <div style="font-size: 28px; font-weight: 700; color: {color}; margin-bottom: 4px;">
                        {points:,}
                    </div>
                    <div style="font-size: 13px; color: #94a3b8;">{label.split()[1]}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart of points by category
        if points_by_category and len(points_by_category) > 0:
            try:
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(points_by_category.keys()),
                    values=list(points_by_category.values()),
                    hole=0.4,
                    marker=dict(colors=['#3b82f6', '#a78bfa', '#ec4899', '#4ade80', '#fbbf24', '#ef4444'])
                )])
                fig_pie.update_layout(
                    title=dict(text="Points Distribution by Category"),
                    paper_bgcolor='transparent',
                    plot_bgcolor='transparent',
                    font=dict(color='white', family='Outfit'),
                    height=350,
                    showlegend=True
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            except Exception as e:
                st.info("No points data available for chart")
        else:
            st.info("No points earned yet. Start submitting requests!")
    
    with col2:
        # Bar chart of recent activities
        recent_activities = [p for p in st.session_state.points_ledger 
                           if p["user_id"] == st.session_state.current_user_id and p["status"] == "approved"]
        recent_activities.sort(key=lambda x: x["date"], reverse=True)
        recent_activities = recent_activities[:10]
        
        if recent_activities and len(recent_activities) > 0:
            try:
                df_activities = pd.DataFrame(recent_activities)
                fig_bar = px.bar(df_activities, x='date', y='points', color='category',
                               title="Recent Points Earned")
                fig_bar.update_layout(
                    paper_bgcolor='transparent',
                    plot_bgcolor='transparent',
                    font=dict(color='white', family='Outfit'),
                    height=350,
                    xaxis=dict(title="Date"),
                    yaxis=dict(title="Points")
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            except Exception as e:
                st.info("No activity data available for chart")
        else:
            st.info("No recent activities to display")

def render_submit_reward_request():
    """Render form to submit new reward point request"""
    st.markdown("### 🎯 Submit Points Request")
    st.markdown("Submit a request to earn points for your activities and achievements.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        earn_type = st.selectbox(
            "Activity Type",
            options=[et["name"] for et in EARN_TYPES],
            help="Select the type of activity you completed"
        )
        
        selected_earn = next(et for et in EARN_TYPES if et["name"] == earn_type)
        category = selected_earn["category"]
        
        # Dynamic points calculation based on type
        if category == "training":
            hours = st.number_input("Training Hours", min_value=0.5, max_value=40.0, value=1.0, step=0.5)
            training_type = st.selectbox("Training Type", ["mandatory", "elective"])
            calculated_points = calculate_points_for_training(hours, training_type)
        elif category == "surveys":
            survey_type = st.selectbox("Survey Type", ["short", "medium", "long"])
            num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
            calculated_points = calculate_points_for_survey(num_questions, survey_type)
        elif category == "certifications":
            cert_level = st.selectbox("Certification Level", ["basic", "advanced", "professional"])
            calculated_points = calculate_points_for_certification(cert_level)
        elif category == "innovation":
            if "idea" in earn_type.lower():
                idea_status = st.selectbox("Idea Status", ["submitted", "accepted"])
                calculated_points = SCORING_RULES["initiative_idea_accepted"] if idea_status == "accepted" else SCORING_RULES["initiative_idea_submission"]
            else:
                calculated_points = calculate_points_for_initiative(earn_type)
        else:
            calculated_points = st.number_input("Points Requested", min_value=10, max_value=1000, value=100, step=10)
        
        st.info(f"💰 Calculated Points: **{calculated_points:,}**")
    
    with col2:
        description = st.text_area(
            "Activity Description",
            placeholder="Provide details about the activity...",
            help="Describe what you did and when"
        )
        
        justification = st.text_area(
            "Justification (Required)",
            placeholder="Explain why you should receive these points...",
            help="Required for audit purposes"
        )
        
        attachment_desc = st.text_input(
            "Attachment/Evidence",
            placeholder="Certificate.pdf, Screenshot.jpg, etc.",
            help="Describe any supporting documents"
        )
    
    if st.button("Submit Request", type="primary", use_container_width=True):
        if not description or not justification:
            st.error("Please provide both description and justification.")
        else:
            # Check for duplicates
            date_today = datetime.now().strftime("%Y-%m-%d")
            if check_duplicate_claim(st.session_state.current_user_id, category, description, date_today):
                st.error("❌ Duplicate claim detected! You already have a similar request for today.")
            else:
                # Create new request
                new_request = {
                    "id": st.session_state.next_request_id,
                    "user_id": st.session_state.current_user_id,
                    "earn_type": earn_type,
                    "category": category,
                    "points_requested": calculated_points,
                    "description": description,
                    "date_submitted": date_today,
                    "status": "pending",
                    "justification": justification,
                    "attachment_desc": attachment_desc
                }
                st.session_state.reward_requests.append(new_request)
                st.session_state.next_request_id += 1
                
                # Add audit log
                add_audit_log(st.session_state.current_user_id, "submitted_reward_request", 
                            f"Submitted request for {calculated_points} points - {earn_type}")
                
                # Notify admins
                for user in st.session_state.users:
                    if user["role"] == "admin":
                        add_notification(user["id"], "admin_request", 
                                       f"New reward request from {st.session_state.users[st.session_state.current_user_id-1]['name']}")
                
                st.success("✅ Request submitted successfully! It will be reviewed by HR.")
                st.balloons()

def render_employee_history():
    """Render employee's reward request and redemption history"""
    st.markdown("### 📜 My Points History")
    
    # Points earned history
    st.markdown("#### 💰 Points Earned")
    user_points = [p for p in st.session_state.points_ledger 
                   if p["user_id"] == st.session_state.current_user_id]
    
    if user_points:
        df_points = pd.DataFrame(user_points)
        df_points = df_points.sort_values('date', ascending=False)
        df_points['status'] = df_points['status'].apply(
            lambda x: f"✅ {x.upper()}" if x == "approved" else f"⏳ {x.upper()}"
        )
        st.dataframe(
            df_points[['date', 'category', 'description', 'points', 'status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No points earned yet. Start submitting requests!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Pending requests
    st.markdown("#### ⏳ Pending Requests")
    pending_requests = [r for r in st.session_state.reward_requests 
                       if r["user_id"] == st.session_state.current_user_id and r["status"] == "pending"]
    
    if pending_requests:
        df_pending = pd.DataFrame(pending_requests)
        st.dataframe(
            df_pending[['date_submitted', 'earn_type', 'points_requested', 'description', 'status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No pending requests")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Redemption history
    st.markdown("#### 🎁 Redemption History")
    user_redemptions = [r for r in st.session_state.redemption_requests 
                       if r["user_id"] == st.session_state.current_user_id]
    
    if user_redemptions:
        df_redemptions = pd.DataFrame(user_redemptions)
        df_redemptions = df_redemptions.sort_values('date_submitted', ascending=False)
        st.dataframe(
            df_redemptions[['date_submitted', 'redemption_name', 'points_cost', 'status', 'fulfillment_status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No redemptions yet")

def render_redemption_section(available_points: int):
    """Render redemption catalog and request form"""
    st.markdown("### 🎁 Redeem Your Points")
    st.markdown(f"**Available Points:** {available_points:,} 💰")
    
    # Redemption catalog
    st.markdown("#### Available Rewards")
    
    cols = st.columns(3)
    for i, option in enumerate(REDEMPTION_OPTIONS):
        with cols[i % 3]:
            can_afford = available_points >= option["points"]
            border_color = "#4ade80" if can_afford else "#64748b"
            
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px);
                            border-radius: 16px; padding: 20px; border: 2px solid {border_color};
                            margin-bottom: 16px; text-align: center; min-height: 220px;">
                    <div style="font-size: 48px; margin-bottom: 12px;">{option['icon']}</div>
                    <div style="font-size: 18px; font-weight: 700; color: white; margin-bottom: 8px;">
                        {option['name']}
                    </div>
                    <div style="font-size: 14px; color: #94a3b8; margin-bottom: 12px;">
                        {option['description']}
                    </div>
                    <div style="font-size: 24px; font-weight: 700; color: #3b82f6; margin-bottom: 8px;">
                        {option['points']:,} pts
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; margin-bottom: 12px;">
                        Value: {option['value']}
                    </div>
                    <div style="padding: 8px 16px; background: {'#4ade80' if can_afford else '#64748b'}; 
                                border-radius: 8px; font-size: 12px; font-weight: 600; color: white;">
                        {'✓ AVAILABLE' if can_afford else '🔒 LOCKED'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Redemption request form
    st.markdown("#### Submit Redemption Request")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        affordable_options = [opt for opt in REDEMPTION_OPTIONS if available_points >= opt["points"]]
        
        if affordable_options:
            selected_redemption = st.selectbox(
                "Choose Reward",
                options=[opt["name"] for opt in affordable_options]
            )
            
            selected_opt = next(opt for opt in REDEMPTION_OPTIONS if opt["name"] == selected_redemption)
            
            st.info(f"💰 Cost: **{selected_opt['points']:,} points** | Value: **{selected_opt['value']}**")
            
            notes = st.text_area(
                "Delivery Notes (Optional)",
                placeholder="Any special instructions for delivery/fulfillment..."
            )
            
            if st.button("Submit Redemption Request", type="primary", use_container_width=True):
                # Create redemption request
                new_redemption = {
                    "id": st.session_state.next_redemption_id,
                    "user_id": st.session_state.current_user_id,
                    "redemption_name": selected_redemption,
                    "points_cost": selected_opt["points"],
                    "date_submitted": datetime.now().strftime("%Y-%m-%d"),
                    "status": "pending",
                    "fulfillment_status": "pending",
                    "notes": notes
                }
                st.session_state.redemption_requests.append(new_redemption)
                st.session_state.next_redemption_id += 1
                
                # Add audit log
                add_audit_log(st.session_state.current_user_id, "submitted_redemption",
                            f"Requested {selected_redemption} redemption")
                
                # Notify admins
                for user in st.session_state.users:
                    if user["role"] == "admin":
                        add_notification(user["id"], "admin_redemption",
                                       f"New redemption request from {st.session_state.users[st.session_state.current_user_id-1]['name']}")
                
                st.success("✅ Redemption request submitted! HR will process it soon.")
                st.balloons()
        else:
            st.warning("❌ You don't have enough points for any rewards yet. Keep earning!")
    
    with col2:
        st.markdown("#### 💡 Tips")
        st.markdown("""
            - Points expire after 2 years
            - Redemptions are processed within 5 business days
            - Check fulfillment status in History
            - Contact HR for special requests
        """)

def render_employee_badges():
    """Render earned badges for employee"""
    st.markdown("### 🏆 My Badges")
    
    user_badge_ids = [b["badge_id"] for b in st.session_state.user_badges 
                     if b["user_id"] == st.session_state.current_user_id]
    
    earned_badges = [b for b in BADGES if b["id"] in user_badge_ids]
    locked_badges = [b for b in BADGES if b["id"] not in user_badge_ids]
    
    if earned_badges:
        st.markdown("#### ✅ Earned Badges")
        cols = st.columns(4)
        for i, badge in enumerate(earned_badges):
            with cols[i % 4]:
                st.markdown(f"""
                    <div style="background: rgba(74, 222, 128, 0.2); border: 2px solid #4ade80;
                                border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 16px;">
                        <div style="font-size: 48px; margin-bottom: 8px;">{badge['icon']}</div>
                        <div style="font-size: 16px; font-weight: 700; color: white;">
                            {badge['name']}
                        </div>
                        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">
                            {badge['criteria']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No badges earned yet. Complete activities to unlock badges!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if locked_badges:
        st.markdown("#### 🔒 Locked Badges")
        cols = st.columns(4)
        for i, badge in enumerate(locked_badges):
            with cols[i % 4]:
                st.markdown(f"""
                    <div style="background: rgba(100, 116, 139, 0.2); border: 2px solid #64748b;
                                border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 16px;
                                opacity: 0.6;">
                        <div style="font-size: 48px; margin-bottom: 8px; filter: grayscale(100%);">{badge['icon']}</div>
                        <div style="font-size: 16px; font-weight: 700; color: #94a3b8;">
                            {badge['name']}
                        </div>
                        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">
                            {badge['criteria']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# SECTION 5: UI RENDERING FUNCTIONS - ORGANIZATION DASHBOARD
# ==============================================================================

def render_organization_dashboard():
    """Render organization-level analytics and insights"""
    load_css()
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    border-radius: 24px; padding: 40px; margin-bottom: 40px;">
            <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 12px; color: white;'>
                📊 Organization Dashboard
            </h1>
            <p style='font-size: 20px; opacity: 0.95; color: white;'>
                Company-wide analytics, engagement metrics, and performance insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if user is admin
    current_user = next(u for u in st.session_state.users if u["id"] == st.session_state.current_user_id)
    is_admin = current_user["role"] == "admin"
    
    # Tabs
    if is_admin:
        tabs = st.tabs(["📈 Analytics", "🏆 Leaderboard", "⚙️ Activity Management"])
    else:
        tabs = st.tabs(["📈 Analytics", "🏆 Leaderboard"])
    
    with tabs[0]:  # Analytics
        render_org_analytics()
    
    with tabs[1]:  # Leaderboard
        render_org_leaderboard()
    
    if is_admin and len(tabs) > 2:
        with tabs[2]:  # Activity Management
            render_activity_management()

def render_org_analytics():
    """Render organization analytics section"""
    # Key metrics
    total_users = len([u for u in st.session_state.users if u["role"] == "user"])
    total_points_distributed = sum(p["points"] for p in st.session_state.points_ledger if p["status"] == "approved")
    total_redemptions = len([r for r in st.session_state.redemption_requests if r["status"] == "approved"])
    avg_points_per_user = total_points_distributed / total_users if total_users > 0 else 0
    
    cols = st.columns(4)
    metrics = [
        ("👥 Total Employees", total_users, "#3b82f6"),
        ("💰 Points Distributed", f"{total_points_distributed:,}", "#4ade80"),
        ("🎁 Redemptions", total_redemptions, "#ec4899"),
        ("📊 Avg Points/User", f"{avg_points_per_user:,.0f}", "#fbbf24")
    ]
    
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div style="background: white; border-radius: 16px; padding: 24px; text-align: center;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <div style="font-size: 14px; color: #64748b; margin-bottom: 8px; font-weight: 600;">
                        {label}
                    </div>
                    <div style="font-size: 32px; font-weight: 800; color: {color};">
                        {value}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Points by department
        dept_points = {}
        for user in st.session_state.users:
            if user["role"] == "user":
                points = get_user_total_points(user["id"])
                dept = user["department"]
                dept_points[dept] = dept_points.get(dept, 0) + points
        
        if dept_points and len(dept_points) > 0:
            try:
                fig_dept = go.Figure(data=[go.Bar(
                    x=list(dept_points.keys()),
                    y=list(dept_points.values()),
                    marker=dict(color='#3b82f6')
                )])
                fig_dept.update_layout(
                    title=dict(text="Points by Department"),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=dict(color='#1e293b', family='Outfit'),
                    height=350,
                    xaxis=dict(title="Department"),
                    yaxis=dict(title="Total Points")
                )
                st.plotly_chart(fig_dept, use_container_width=True)
            except Exception as e:
                st.info("Unable to display department chart")
        else:
            st.info("No department data available")
    
    with col2:
        # Level distribution
        level_dist = {}
        for user in st.session_state.users:
            if user["role"] == "user":
                points = get_user_total_points(user["id"])
                level = get_user_level(points)
                level_name = level["name"]
                level_dist[level_name] = level_dist.get(level_name, 0) + 1
        
        if level_dist and len(level_dist) > 0:
            try:
                fig_levels = go.Figure(data=[go.Pie(
                    labels=list(level_dist.keys()),
                    values=list(level_dist.values()),
                    hole=0.4,
                    marker=dict(colors=['#cd7f32', '#c0c0c0', '#ffd700', '#e5e4e2', '#4169e1', '#9966cc'])
                )])
                fig_levels.update_layout(
                    title=dict(text="Employee Level Distribution"),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=dict(color='#1e293b', family='Outfit'),
                    height=350,
                    showlegend=True
                )
                st.plotly_chart(fig_levels, use_container_width=True)
            except Exception as e:
                st.info("Unable to display level distribution chart")
        else:
            st.info("No level data available")

def render_org_leaderboard():
    """Render organization leaderboard"""
    st.markdown("### 🏆 Company Leaderboard")
    leaderboard_df = generate_leaderboard()
    
    # Style the dataframe
    st.dataframe(
        leaderboard_df[['Rank', 'Name', 'Department', 'Level', 'Points']],
        use_container_width=True,
        hide_index=True,
        height=400
    )

def render_activity_management():
    """Render activity and scoring management for HR"""
    st.markdown("### ⚙️ Activity & Scoring Management")
    st.markdown("Manage activity types, point values, and scoring rules")
    
    # Initialize custom activities in session state if not exists
    if 'custom_earn_types' not in st.session_state:
        st.session_state.custom_earn_types = []
    
    if 'custom_scoring_rules' not in st.session_state:
        st.session_state.custom_scoring_rules = {}
    
    # Sub-tabs for different management areas
    mgmt_tabs = st.tabs(["📋 Current Activities", "➕ Add New Activity", "💰 Scoring Rules"])
    
    with mgmt_tabs[0]:  # Current Activities
        st.markdown("#### 📋 All Submittable Activities")
        st.info("💡 **These are ALL the activities employees can submit for points.** Manage what's available, update descriptions, or remove custom activities.")
        
        # Display statistics
        all_earn_types = EARN_TYPES + st.session_state.custom_earn_types
        active_activities = [et for et in all_earn_types if et.get('is_active', True)]
        custom_count = len(st.session_state.custom_earn_types)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Activities", len(all_earn_types))
        with col2:
            st.metric("Active", len(active_activities))
        with col3:
            st.metric("Custom Added", custom_count)
        
        st.markdown("---")
        
        # Group by category
        categories = {}
        for earn_type in all_earn_types:
            cat = earn_type['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(earn_type)
        
        # Display by category
        for category_name, activities in sorted(categories.items()):
            with st.expander(f"📂 {category_name.upper()} ({len(activities)} activities)", expanded=False):
                for earn_type in activities:
                    is_custom = earn_type.get('id', 0) > 10
                    is_active = earn_type.get('is_active', True)
                    
                    # Activity card
                    status_badge = "✅ Active" if is_active else "⏸️ Inactive"
                    custom_badge = " 🔧 Custom" if is_custom else " 📌 System"
                    
                    st.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.3); padding: 16px; border-radius: 12px; 
                                    margin-bottom: 12px; border-left: 4px solid {'#4ade80' if is_active else '#64748b'};">
                            <div style="font-size: 18px; font-weight: 700; color: white; margin-bottom: 8px;">
                                {earn_type['name']} {custom_badge}
                            </div>
                            <div style="font-size: 14px; color: #94a3b8; margin-bottom: 8px;">
                                {earn_type['description']}
                            </div>
                            <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                                <span style="font-size: 13px; color: #a78bfa;">💰 Points: {earn_type['points']}</span>
                                <span style="font-size: 13px; color: #60a5fa;">📂 Category: {earn_type['category']}</span>
                                <span style="font-size: 13px; color: {'#4ade80' if is_active else '#64748b'};">{status_badge}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Delete button for custom activities
                    if is_custom:
                        activity_index = st.session_state.custom_earn_types.index(earn_type)
                        if st.button(f"🗑️ Delete {earn_type['name']}", key=f"del_{earn_type['id']}", use_container_width=True):
                            st.session_state.custom_earn_types.pop(activity_index)
                            add_audit_log(
                                st.session_state.current_user_id,
                                "deleted_activity_type",
                                f"Deleted activity: {earn_type['name']}"
                            )
                            st.success(f"✅ Deleted {earn_type['name']}")
                            st.rerun()
        
        if not all_earn_types:
            st.info("No activities configured yet")
    
    with mgmt_tabs[1]:  # Add New Activity
        st.markdown("#### ➕ Add New Activity Type")
        
        with st.form("add_activity_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_name = st.text_input("Activity Name", placeholder="e.g., Team Building Event")
                
                category = st.selectbox(
                    "Category",
                    ["training", "surveys", "certifications", "innovation", "events", "performance", "attendance", "other"]
                )
                
                points_type = st.selectbox(
                    "Points Type",
                    ["Fixed", "Variable", "Range"]
                )
                
                if points_type == "Fixed":
                    points_value = st.number_input("Points", min_value=1, max_value=5000, value=100)
                    points_display = str(points_value)
                elif points_type == "Range":
                    col_min, col_max = st.columns(2)
                    with col_min:
                        points_min = st.number_input("Min Points", min_value=1, max_value=5000, value=50)
                    with col_max:
                        points_max = st.number_input("Max Points", min_value=1, max_value=5000, value=200)
                    points_display = f"{points_min}-{points_max}"
                    points_value = points_max
                else:  # Variable
                    points_display = "Variable"
                    points_value = 0
            
            with col2:
                description = st.text_area(
                    "Description",
                    placeholder="Describe what this activity involves...",
                    height=100
                )
                
                requires_approval = st.checkbox("Requires Admin Approval", value=True)
                
                requires_evidence = st.checkbox("Requires Evidence/Attachment", value=False)
                
                is_active = st.checkbox("Active", value=True)
            
            submitted = st.form_submit_button("➕ Add Activity", type="primary", use_container_width=True)
            
            if submitted:
                if not activity_name or not description:
                    st.error("Please fill in all required fields")
                else:
                    # Add to custom earn types
                    new_activity = {
                        "id": len(EARN_TYPES) + len(st.session_state.custom_earn_types) + 1,
                        "name": activity_name,
                        "category": category,
                        "points": points_display,
                        "description": description,
                        "requires_approval": requires_approval,
                        "requires_evidence": requires_evidence,
                        "is_active": is_active,
                        "points_value": points_value
                    }
                    
                    st.session_state.custom_earn_types.append(new_activity)
                    
                    # Add to custom scoring rules
                    scoring_key = f"custom_{activity_name.lower().replace(' ', '_')}"
                    st.session_state.custom_scoring_rules[scoring_key] = points_value
                    
                    # Add audit log
                    add_audit_log(
                        st.session_state.current_user_id,
                        "added_activity_type",
                        f"Added new activity type: {activity_name} ({points_display} points)"
                    )
                    
                    st.success(f"✅ Activity '{activity_name}' added successfully!")
                    st.balloons()
                    st.rerun()
    
    with mgmt_tabs[2]:  # Scoring Rules
        st.markdown("#### 💰 Scoring Rules Configuration")
        st.markdown("Modify point values for different activity types")
        
        # Organize scoring rules by category
        categories_scoring = {
            "Surveys": ["survey_per_question", "survey_short", "survey_medium", "survey_long"],
            "Training": ["training_per_hour", "training_full_day", "training_half_day", "training_mandatory", "training_elective"],
            "Certifications": ["certification_basic", "certification_advanced", "certification_professional"],
            "Initiatives": ["initiative_qudwa", "initiative_digital_champion", "initiative_alkhorayef_champion", 
                            "initiative_thank_you_card", "initiative_idea_submission", "initiative_idea_accepted"],
            "Events": ["event_corporate", "event_csr", "event_wellness"],
            "Performance": ["kpi_target_achieved", "kpi_exceed_target", "extra_milestone"],
            "Attendance": ["perfect_attendance_month", "perfect_attendance_quarter"]
        }
        
        st.info("💡 Changes to scoring rules will apply to all future point calculations. Existing awarded points are not affected.")
        
        for cat_name, rules in categories_scoring.items():
            with st.expander(f"📌 {cat_name}", expanded=False):
                for rule in rules:
                    if rule in SCORING_RULES:
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            st.write(f"**{rule.replace('_', ' ').title()}**")
                        
                        with col2:
                            # Get current value
                            current_value = st.session_state.custom_scoring_rules.get(rule, SCORING_RULES[rule])
                            
                            new_value = st.number_input(
                                "Points",
                                min_value=1,
                                max_value=5000,
                                value=int(current_value),
                                key=f"score_{rule}",
                                label_visibility="collapsed"
                            )
                        
                        with col3:
                            if st.button("Update", key=f"update_{rule}", use_container_width=True):
                                st.session_state.custom_scoring_rules[rule] = new_value
                                
                                # Add audit log
                                add_audit_log(
                                    st.session_state.current_user_id,
                                    "updated_scoring_rule",
                                    f"Updated {rule}: {SCORING_RULES[rule]} → {new_value} points"
                                )
                                
                                st.success(f"✅ Updated {rule} to {new_value} points")
                                st.rerun()
        
        # Custom activities scoring
        if st.session_state.custom_scoring_rules:
            st.markdown("---")
            st.markdown("#### Custom Activity Scoring")
            
            for key, value in st.session_state.custom_scoring_rules.items():
                if key.startswith("custom_"):
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.write(f"**{key.replace('custom_', '').replace('_', ' ').title()}**")
                    
                    with col2:
                        new_value = st.number_input(
                            "Points",
                            min_value=1,
                            max_value=5000,
                            value=int(value),
                            key=f"custom_score_{key}",
                            label_visibility="collapsed"
                        )
                    
                    with col3:
                        if st.button("Update", key=f"update_custom_{key}", use_container_width=True):
                            st.session_state.custom_scoring_rules[key] = new_value
                            st.success(f"✅ Updated to {new_value} points")
                            st.rerun()

# Keep the rest of organization dashboard
    st.markdown("### 📈 Recent Activity")
    recent_points = sorted(st.session_state.points_ledger, key=lambda x: x["date"], reverse=True)[:20]
    
    if recent_points:
        activity_data = []
        for point in recent_points:
            user = next(u for u in st.session_state.users if u["id"] == point["user_id"])
            activity_data.append({
                "Date": point["date"],
                "Employee": user["name"],
                "Department": user["department"],
                "Activity": point["description"],
                "Points": point["points"],
                "Status": point["status"]
            })
        
        df_activity = pd.DataFrame(activity_data)
        st.dataframe(df_activity, use_container_width=True, hide_index=True)

# ==============================================================================
# SECTION 6: UI RENDERING FUNCTIONS - ADMIN DASHBOARD
# ==============================================================================

def render_admin_dashboard():
    """Render admin dashboard with management capabilities"""
    load_css()
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    border-radius: 24px; padding: 40px; margin-bottom: 40px;">
            <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 12px; color: white;'>
                🔧 Admin Dashboard
            </h1>
            <p style='font-size: 20px; opacity: 0.95; color: white;'>
                Manage requests, add points, and oversee the rewards system
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["🔔 Pending Requests", "👥 All Employees", "➕ Add Points", "⚙️ Manage Items", "📋 Audit Log"])
    
    with tabs[0]:  # Pending Requests
        render_admin_pending_requests()
    
    with tabs[1]:  # All Employees
        render_admin_all_employees()
    
    with tabs[2]:  # Add Points
        render_admin_add_points()
    
    with tabs[3]:  # Manage Items
        render_admin_manage_items()
    
    with tabs[4]:  # Audit Log
        render_admin_audit_log()

def render_admin_manage_items():
    """Comprehensive admin interface to manage all system items"""
    st.markdown("### ⚙️ Manage System Items")
    st.info("🎯 **Central hub to manage ALL items in the rewards system** - activities, scoring, redemptions, levels, and badges")
    
    # Initialize custom items if needed
    if 'custom_earn_types' not in st.session_state:
        st.session_state.custom_earn_types = []
    if 'custom_scoring_rules' not in st.session_state:
        st.session_state.custom_scoring_rules = {}
    
    # Sub-tabs for different item types
    item_tabs = st.tabs(["📋 Activities", "💰 Scoring Rules", "🎁 Redemptions", "⭐ Levels", "🏆 Badges"])
    
    with item_tabs[0]:  # Activities Management
        st.markdown("#### 📋 All Submittable Activities")
        st.markdown("**These are ALL the activities employees can submit for points.**")
        
        # Statistics
        all_activities = EARN_TYPES + st.session_state.custom_earn_types
        active_count = len([a for a in all_activities if a.get('is_active', True)])
        custom_count = len(st.session_state.custom_earn_types)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Activities", len(all_activities))
        with col2:
            st.metric("System Activities", len(EARN_TYPES))
        with col3:
            st.metric("Custom Activities", custom_count)
        with col4:
            st.metric("Active", active_count)
        
        st.markdown("---")
        
        # Group by category
        categories = {}
        for activity in all_activities:
            cat = activity['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(activity)
        
        # Display grouped activities
        for cat_name in sorted(categories.keys()):
            activities = categories[cat_name]
            with st.expander(f"📂 **{cat_name.upper()}** ({len(activities)} activities)", expanded=False):
                for activity in activities:
                    is_custom = activity.get('id', 0) > 10
                    is_active = activity.get('is_active', True)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        status_icon = "✅" if is_active else "⏸️"
                        type_badge = "🔧 Custom" if is_custom else "📌 System"
                        
                        st.markdown(f"""
                            <div style="padding: 12px; background: rgba(30,41,59,0.3); border-radius: 8px; 
                                        border-left: 4px solid {'#4ade80' if is_active else '#94a3b8'};">
                                <div style="font-size: 16px; font-weight: 700; color: white; margin-bottom: 6px;">
                                    {status_icon} {activity['name']} {type_badge}
                                </div>
                                <div style="font-size: 13px; color: #94a3b8; margin-bottom: 8px;">
                                    {activity['description']}
                                </div>
                                <div style="font-size: 12px; color: #60a5fa;">
                                    💰 Points: {activity['points']} | 📂 Category: {activity['category']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if is_custom:
                            edit_key = f"edit_act_{activity['id']}"
                            if st.button("✏️ Edit", key=edit_key, use_container_width=True):
                                # Store activity being edited
                                st.session_state[f'editing_{activity["id"]}'] = True
                            
                            # Show edit form if this activity is being edited
                            if st.session_state.get(f'editing_{activity["id"]}', False):
                                with st.form(key=f"form_edit_{activity['id']}"):
                                    st.markdown("**Edit Activity**")
                                    
                                    new_name = st.text_input("Name", value=activity['name'])
                                    new_desc = st.text_area("Description", value=activity['description'])
                                    new_points = st.number_input("Points", value=int(activity.get('points_value', 100)), min_value=1, max_value=10000)
                                    new_category = st.selectbox("Category", 
                                        ["training", "surveys", "certifications", "innovation", "events", "performance", "attendance", "other"],
                                        index=["training", "surveys", "certifications", "innovation", "events", "performance", "attendance", "other"].index(activity['category']))
                                    new_active = st.checkbox("Active", value=activity.get('is_active', True))
                                    
                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        if st.form_submit_button("💾 Save", use_container_width=True):
                                            # Update activity
                                            activity['name'] = new_name
                                            activity['description'] = new_desc
                                            activity['points'] = str(new_points)
                                            activity['points_value'] = new_points
                                            activity['category'] = new_category
                                            activity['is_active'] = new_active
                                            
                                            add_audit_log(
                                                st.session_state.current_user_id,
                                                "updated_activity",
                                                f"Updated activity: {new_name}"
                                            )
                                            st.session_state[f'editing_{activity["id"]}'] = False
                                            st.success(f"✅ Updated {new_name}")
                                            st.rerun()
                                    
                                    with col_cancel:
                                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                                            st.session_state[f'editing_{activity["id"]}'] = False
                                            st.rerun()
                    
                    with col3:
                        if is_custom:
                            if st.button("🗑️ Delete", key=f"del_act_{activity['id']}", use_container_width=True):
                                activity_index = st.session_state.custom_earn_types.index(activity)
                                st.session_state.custom_earn_types.pop(activity_index)
                                add_audit_log(
                                    st.session_state.current_user_id,
                                    "deleted_activity",
                                    f"Deleted activity: {activity['name']}"
                                )
                                st.success(f"✅ Deleted {activity['name']}")
                                st.rerun()
        
        # Add new activity button
        st.markdown("---")
        if st.button("➕ Add New Activity", type="primary", use_container_width=True):
            st.info("💡 Go to Organization → Activity Management to add new activities")
    
    with item_tabs[1]:  # Scoring Rules
        st.markdown("#### 💰 All Scoring Rules")
        st.markdown("**Manage point values for all activity types**")
        
        # Group scoring rules by category
        scoring_categories = {
            "📊 Surveys": ["survey_per_question", "survey_short", "survey_medium", "survey_long"],
            "📚 Training": ["training_per_hour", "training_full_day", "training_half_day", "training_mandatory", "training_elective"],
            "🎓 Certifications": ["certification_basic", "certification_advanced", "certification_professional"],
            "💡 Initiatives": ["initiative_qudwa", "initiative_digital_champion", "initiative_alkhorayef_champion", 
                              "initiative_thank_you_card", "initiative_idea_submission", "initiative_idea_accepted"],
            "🎪 Events": ["event_corporate", "event_csr", "event_wellness"],
            "🎯 Performance": ["kpi_target_achieved", "kpi_exceed_target", "extra_milestone"],
            "⭐ Attendance": ["perfect_attendance_month", "perfect_attendance_quarter"]
        }
        
        st.info("💡 Changes apply to all future point calculations. Existing awarded points are not affected.")
        
        for cat_name, rules in scoring_categories.items():
            with st.expander(f"{cat_name} ({len(rules)} rules)", expanded=False):
                for rule in rules:
                    if rule in SCORING_RULES:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**{rule.replace('_', ' ').title()}**")
                        
                        with col2:
                            current_value = st.session_state.custom_scoring_rules.get(rule, SCORING_RULES[rule])
                            new_value = st.number_input(
                                "Points",
                                min_value=1,
                                max_value=10000,
                                value=int(current_value),
                                key=f"admin_score_{rule}",
                                label_visibility="collapsed"
                            )
                        
                        with col3:
                            if st.button("💾 Update", key=f"admin_upd_{rule}", use_container_width=True):
                                st.session_state.custom_scoring_rules[rule] = new_value
                                add_audit_log(
                                    st.session_state.current_user_id,
                                    "updated_scoring",
                                    f"Updated {rule}: {SCORING_RULES[rule]} → {new_value} pts"
                                )
                                st.success(f"✅ Updated to {new_value} points")
                                st.rerun()
    
    with item_tabs[2]:  # Redemptions
        st.markdown("#### 🎁 Redemption Options")
        st.markdown("**All rewards employees can redeem their points for**")
        
        # Display redemption options
        redemption_categories = {}
        for redemption in REDEMPTION_OPTIONS:
            cat = redemption.get('category', 'Other')
            if cat not in redemption_categories:
                redemption_categories[cat] = []
            redemption_categories[cat].append(redemption)
        
        for cat_name in sorted(redemption_categories.keys()):
            items = redemption_categories[cat_name]
            with st.expander(f"🎁 **{cat_name}** ({len(items)} items)", expanded=False):
                for item in items:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                            <div style="padding: 12px; background: rgba(30,41,59,0.3); border-radius: 8px;">
                                <div style="font-size: 16px; font-weight: 700; color: white; margin-bottom: 6px;">
                                    {item['icon']} {item['name']}
                                </div>
                                <div style="font-size: 13px; color: #94a3b8; margin-bottom: 8px;">
                                    {item['description']}
                                </div>
                                <div style="font-size: 12px; color: #fbbf24;">
                                    💰 {item['points']:,} points | 💵 Value: {item['value']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        edit_red_key = f"edit_red_{item['id']}"
                        if st.button("✏️ Edit", key=edit_red_key, use_container_width=True):
                            st.session_state[f'editing_red_{item["id"]}'] = True
                        
                        # Show edit form if this item is being edited
                        if st.session_state.get(f'editing_red_{item["id"]}', False):
                            with st.form(key=f"form_red_{item['id']}"):
                                st.markdown("**Edit Redemption**")
                                
                                new_name = st.text_input("Name", value=item['name'])
                                new_desc = st.text_area("Description", value=item['description'])
                                new_points = st.number_input("Points Cost", value=item['points'], min_value=100, max_value=100000, step=100)
                                new_value = st.text_input("Value", value=item['value'])
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Save", use_container_width=True):
                                        # Update redemption item
                                        item['name'] = new_name
                                        item['description'] = new_desc
                                        item['points'] = new_points
                                        item['value'] = new_value
                                        
                                        add_audit_log(
                                            st.session_state.current_user_id,
                                            "updated_redemption",
                                            f"Updated redemption: {new_name} - {new_points:,} pts"
                                        )
                                        st.session_state[f'editing_red_{item["id"]}'] = False
                                        st.success(f"✅ Updated {new_name}")
                                        st.rerun()
                                
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                                        st.session_state[f'editing_red_{item["id"]}'] = False
                                        st.rerun()
                    
                    with col3:
                        pass  # Keep for future delete functionality if needed
        
        st.markdown("---")
        st.info("💡 To add custom redemption options, contact system administrator")
    
    with item_tabs[3]:  # Levels
        st.markdown("#### ⭐ Level Definitions")
        st.markdown("**All achievement levels in the system**")
        
        for level in LEVELS:
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
            
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 48px;'>{level['icon']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="padding: 12px;">
                        <div style="font-size: 18px; font-weight: 700; color: white;">{level['name']}</div>
                        <div style="font-size: 13px; color: #94a3b8;">Level {level['id']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style="padding: 12px;">
                        <div style="font-size: 14px; color: #60a5fa;">Min Points</div>
                        <div style="font-size: 16px; font-weight: 700; color: white;">{level['points_min']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                max_pts = level['points_max'] if level['points_max'] < 999999 else "∞"
                st.markdown(f"""
                    <div style="padding: 12px;">
                        <div style="font-size: 14px; color: #60a5fa;">Max Points</div>
                        <div style="font-size: 16px; font-weight: 700; color: white;">{max_pts if isinstance(max_pts, str) else f'{max_pts:,}'}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col5:
                edit_level_key = f"edit_level_{level['id']}"
                if st.button("✏️", key=edit_level_key, use_container_width=True, help="Edit level thresholds"):
                    st.session_state[f'editing_level_{level["id"]}'] = True
            
            # Show edit form if this level is being edited
            if st.session_state.get(f'editing_level_{level["id"]}', False):
                with st.form(key=f"form_level_{level['id']}"):
                    st.markdown(f"**Edit {level['name']} Level**")
                    
                    col_form1, col_form2 = st.columns(2)
                    with col_form1:
                        new_min = st.number_input("Min Points", value=level['points_min'], min_value=0, max_value=1000000, step=100)
                    with col_form2:
                        new_max = st.number_input("Max Points", value=level['points_max'], min_value=0, max_value=1000000, step=100)
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Save", use_container_width=True):
                            level['points_min'] = new_min
                            level['points_max'] = new_max
                            
                            add_audit_log(
                                st.session_state.current_user_id,
                                "updated_level",
                                f"Updated {level['name']} level: {new_min:,} - {new_max:,} pts"
                            )
                            st.session_state[f'editing_level_{level["id"]}'] = False
                            st.success(f"✅ Updated {level['name']} level")
                            st.rerun()
                    
                    with col_cancel:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            st.session_state[f'editing_level_{level["id"]}'] = False
                            st.rerun()
            
            st.markdown("---")
    
    with item_tabs[4]:  # Badges
        st.markdown("#### 🏆 Badge Definitions")
        st.markdown("**All achievement badges employees can earn**")
        
        for badge in BADGES:
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
            
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 48px;'>{badge['icon']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="padding: 12px;">
                        <div style="font-size: 18px; font-weight: 700; color: white;">{badge['name']}</div>
                        <div style="font-size: 13px; color: #94a3b8;">{badge['category']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style="padding: 12px;">
                        <div style="font-size: 14px; color: #94a3b8;">Criteria</div>
                        <div style="font-size: 13px; color: white;">{badge['criteria']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                threshold = badge.get('points_threshold', badge.get('count_threshold', 'N/A'))
                st.markdown(f"""
                    <div style="padding: 12px;">
                        <div style="font-size: 14px; color: #fbbf24;">Threshold</div>
                        <div style="font-size: 16px; font-weight: 700; color: white;">{threshold}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col5:
                edit_badge_key = f"edit_badge_{badge['id']}"
                if st.button("✏️", key=edit_badge_key, use_container_width=True, help="Edit badge criteria"):
                    st.session_state[f'editing_badge_{badge["id"]}'] = True
            
            # Show edit form if this badge is being edited
            if st.session_state.get(f'editing_badge_{badge["id"]}', False):
                with st.form(key=f"form_badge_{badge['id']}"):
                    st.markdown(f"**Edit {badge['name']} Badge**")
                    
                    new_criteria = st.text_input("Criteria", value=badge['criteria'])
                    new_threshold = st.number_input("Threshold", value=int(threshold), min_value=1, max_value=1000, step=1)
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Save", use_container_width=True):
                            badge['criteria'] = new_criteria
                            if 'points_threshold' in badge:
                                badge['points_threshold'] = new_threshold
                            else:
                                badge['count_threshold'] = new_threshold
                            
                            add_audit_log(
                                st.session_state.current_user_id,
                                "updated_badge",
                                f"Updated {badge['name']} badge: {new_criteria} (threshold: {new_threshold})"
                            )
                            st.session_state[f'editing_badge_{badge["id"]}'] = False
                            st.success(f"✅ Updated {badge['name']} badge")
                            st.rerun()
                    
                    with col_cancel:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            st.session_state[f'editing_badge_{badge["id"]}'] = False
                            st.rerun()
            
            st.markdown("---")

def render_admin_pending_requests():
    """Render pending reward and redemption requests with approve/reject actions"""
    st.markdown("### 🔔 Pending Requests")
    
    # Reward requests
    st.markdown("#### 💰 Reward Point Requests")
    pending_rewards = [r for r in st.session_state.reward_requests if r["status"] == "pending"]
    
    if pending_rewards:
        for req in pending_rewards:
            user = next(u for u in st.session_state.users if u["id"] == req["user_id"])
            
            with st.expander(f"Request #{req['id']} - {user['name']} - {req['points_requested']} pts"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Employee:** {user['name']} ({user['department']})")
                    st.write(f"**Activity:** {req['earn_type']}")
                    st.write(f"**Category:** {req['category']}")
                    st.write(f"**Points Requested:** {req['points_requested']:,}")
                
                with col2:
                    st.write(f"**Description:** {req['description']}")
                    st.write(f"**Justification:** {req['justification']}")
                    st.write(f"**Evidence:** {req.get('attachment_desc', 'N/A')}")
                    st.write(f"**Submitted:** {req['date_submitted']}")
                
                with col3:
                    if st.button(f"✅ Approve", key=f"approve_reward_{req['id']}", type="primary", use_container_width=True):
                        # Approve request
                        req["status"] = "approved"
                        req["approved_by"] = st.session_state.current_user_id
                        req["approved_date"] = datetime.now().strftime("%Y-%m-%d")
                        
                        # Add points to ledger
                        new_points = {
                            "id": st.session_state.next_points_id,
                            "user_id": req["user_id"],
                            "points": req["points_requested"],
                            "category": req["category"],
                            "description": req["description"],
                            "date": req["date_submitted"],
                            "status": "approved",
                            "approved_by": st.session_state.current_user_id,
                            "approved_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.points_ledger.append(new_points)
                        st.session_state.next_points_id += 1
                        
                        # Check and award badges
                        check_and_award_badges(req["user_id"])
                        
                        # Check level up
                        old_level = get_user_level(get_user_total_points(req["user_id"]) - req["points_requested"])
                        new_level = get_user_level(get_user_total_points(req["user_id"]))
                        if new_level["id"] > old_level["id"]:
                            add_notification(req["user_id"], "level_up", 
                                           f"🎉 Congratulations! You've reached {new_level['name']} level!")
                        
                        # Notify user
                        add_notification(req["user_id"], "points_earned",
                                       f"✅ Your request for {req['points_requested']} points has been approved!")
                        
                        # Audit log
                        add_audit_log(st.session_state.current_user_id, "approved_reward_request",
                                    f"Approved {req['points_requested']} points for {user['name']}")
                        
                        st.success(f"✅ Approved {req['points_requested']} points for {user['name']}")
                        st.rerun()
                    
                    if st.button(f"❌ Reject", key=f"reject_reward_{req['id']}", use_container_width=True):
                        req["status"] = "rejected"
                        req["reviewed_by"] = st.session_state.current_user_id
                        req["reviewed_date"] = datetime.now().strftime("%Y-%m-%d")
                        
                        # Notify user
                        add_notification(req["user_id"], "request_rejected",
                                       f"❌ Your request for {req['points_requested']} points has been rejected. Contact HR for details.")
                        
                        # Audit log
                        add_audit_log(st.session_state.current_user_id, "rejected_reward_request",
                                    f"Rejected request from {user['name']}")
                        
                        st.warning(f"Request rejected")
                        st.rerun()
    else:
        st.info("No pending reward requests")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Redemption requests
    st.markdown("#### 🎁 Redemption Requests")
    pending_redemptions = [r for r in st.session_state.redemption_requests if r["status"] == "pending"]
    
    if pending_redemptions:
        for req in pending_redemptions:
            user = next(u for u in st.session_state.users if u["id"] == req["user_id"])
            user_points = get_user_total_points(req["user_id"])
            can_afford = user_points >= req["points_cost"]
            
            with st.expander(f"Redemption #{req['id']} - {user['name']} - {req['redemption_name']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Employee:** {user['name']} ({user['department']})")
                    st.write(f"**Reward:** {req['redemption_name']}")
                    st.write(f"**Points Cost:** {req['points_cost']:,}")
                    st.write(f"**Available Points:** {user_points:,}")
                
                with col2:
                    st.write(f"**Submitted:** {req['date_submitted']}")
                    st.write(f"**Notes:** {req.get('notes', 'N/A')}")
                    if not can_afford:
                        st.error(f"⚠️ Insufficient points! Needs {req['points_cost'] - user_points:,} more")
                
                with col3:
                    if can_afford:
                        if st.button(f"✅ Approve", key=f"approve_redemption_{req['id']}", type="primary", use_container_width=True):
                            req["status"] = "approved"
                            req["approved_by"] = st.session_state.current_user_id
                            req["approved_date"] = datetime.now().strftime("%Y-%m-%d")
                            req["fulfillment_status"] = "processing"
                            
                            # Notify user
                            add_notification(req["user_id"], "redemption_approved",
                                           f"✅ Your redemption of {req['redemption_name']} has been approved!")
                            
                            # Audit log
                            add_audit_log(st.session_state.current_user_id, "approved_redemption",
                                        f"Approved {req['redemption_name']} redemption for {user['name']}")
                            
                            st.success(f"✅ Approved redemption for {user['name']}")
                            st.rerun()
                        
                        if st.button(f"❌ Reject", key=f"reject_redemption_{req['id']}", use_container_width=True):
                            req["status"] = "rejected"
                            req["reviewed_by"] = st.session_state.current_user_id
                            req["reviewed_date"] = datetime.now().strftime("%Y-%m-%d")
                            
                            # Notify user
                            add_notification(req["user_id"], "redemption_rejected",
                                           f"❌ Your redemption request has been rejected. Contact HR for details.")
                            
                            # Audit log
                            add_audit_log(st.session_state.current_user_id, "rejected_redemption",
                                        f"Rejected redemption from {user['name']}")
                            
                            st.warning("Request rejected")
                            st.rerun()
                    else:
                        st.error("Cannot approve - insufficient points")
    else:
        st.info("No pending redemption requests")

def render_admin_all_employees():
    """Render view of all employees with their points"""
    st.markdown("### 👥 All Employees")
    
    employees_data = []
    for user in st.session_state.users:
        if user["role"] == "user":
            total_points = get_user_total_points(user["id"])
            level = get_user_level(total_points)
            points_by_cat = get_points_by_category(user["id"])
            
            employees_data.append({
                "ID": user["id"],
                "Name": user["name"],
                "Department": user["department"],
                "Total Points": total_points,
                "Level": f"{level['icon']} {level['name']}",
                "Training": points_by_cat.get("training", 0),
                "Innovation": points_by_cat.get("innovation", 0),
                "Events": points_by_cat.get("events", 0),
                "Performance": points_by_cat.get("performance", 0)
            })
    
    df_employees = pd.DataFrame(employees_data)
    st.dataframe(df_employees, use_container_width=True, hide_index=True, height=500)
    
    # Export option
    if st.button("📥 Export to CSV"):
        csv = df_employees.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"employees_points_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def render_admin_add_points():
    """Render form for admin to manually add points"""
    st.markdown("### ➕ Manually Add Points")
    st.markdown("Award points directly to employees for special achievements or corrections.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_names = [u["name"] for u in st.session_state.users if u["role"] == "user"]
        selected_user_name = st.selectbox("Select Employee", user_names)
        selected_user = next(u for u in st.session_state.users if u["name"] == selected_user_name)
        
        points_to_add = st.number_input("Points to Award", min_value=10, max_value=5000, value=100, step=10)
        
        category = st.selectbox("Category", ["training", "innovation", "events", "performance", "attendance", "other"])
    
    with col2:
        reason = st.text_area(
            "Reason for Manual Points",
            placeholder="Explain why these points are being awarded...",
            help="This will appear in the audit log"
        )
        
        date_awarded = st.date_input("Date", datetime.now())
    
    if st.button("Award Points", type="primary", use_container_width=True):
        if not reason:
            st.error("Please provide a reason for awarding points")
        else:
            # Add to points ledger
            new_points = {
                "id": st.session_state.next_points_id,
                "user_id": selected_user["id"],
                "points": points_to_add,
                "category": category,
                "description": f"Manual award: {reason}",
                "date": date_awarded.strftime("%Y-%m-%d"),
                "status": "approved",
                "approved_by": st.session_state.current_user_id,
                "approved_date": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.points_ledger.append(new_points)
            st.session_state.next_points_id += 1
            
            # Check badges
            check_and_award_badges(selected_user["id"])
            
            # Check level up
            total_points = get_user_total_points(selected_user["id"])
            level = get_user_level(total_points)
            add_notification(selected_user["id"], "level_up",
                           f"🎉 Admin awarded you {points_to_add} points! Current level: {level['name']}")
            
            # Audit log
            add_audit_log(st.session_state.current_user_id, "manual_points_added",
                        f"Added {points_to_add} points to {selected_user['name']} - {reason}")
            
            st.success(f"✅ Successfully awarded {points_to_add} points to {selected_user['name']}")
            st.balloons()

def render_admin_audit_log():
    """Render audit log of all system actions"""
    st.markdown("### 📋 Audit Log")
    st.markdown("Complete history of all admin actions and system events")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_action = st.selectbox("Filter by Action", 
                                     ["All"] + list(set([a["action"] for a in st.session_state.audit_log])))
    with col2:
        filter_user = st.selectbox("Filter by User",
                                   ["All"] + [u["name"] for u in st.session_state.users])
    with col3:
        days_back = st.number_input("Days Back", min_value=1, max_value=90, value=30)
    
    # Filter audit log
    filtered_log = st.session_state.audit_log.copy()
    
    if filter_action != "All":
        filtered_log = [a for a in filtered_log if a["action"] == filter_action]
    
    if filter_user != "All":
        user_id = next(u["id"] for u in st.session_state.users if u["name"] == filter_user)
        filtered_log = [a for a in filtered_log if a["user_id"] == user_id]
    
    # Convert to dataframe
    if filtered_log:
        audit_data = []
        for entry in sorted(filtered_log, key=lambda x: x["date"], reverse=True):
            user = next(u for u in st.session_state.users if u["id"] == entry["user_id"])
            audit_data.append({
                "Date": entry["date"],
                "User": user["name"],
                "Action": entry["action"].replace("_", " ").title(),
                "Details": entry["details"]
            })
        
        df_audit = pd.DataFrame(audit_data)
        st.dataframe(df_audit, use_container_width=True, hide_index=True, height=500)
        
        # Export option
        if st.button("📥 Export Audit Log"):
            csv = df_audit.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"audit_log_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No audit entries match the filters")

# ==============================================================================
# SECTION 7: UI RENDERING FUNCTIONS - SETTINGS & DEFINITIONS
# ==============================================================================

def render_definitions_settings():
    """Render settings and definitions management"""
    load_css()
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
                    border-radius: 24px; padding: 40px; margin-bottom: 40px;">
            <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 12px; color: white;'>
                ⚙️ Settings & Definitions
            </h1>
            <p style='font-size: 20px; opacity: 0.95; color: white;'>
                Configure levels, badges, earn types, and redemption options
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["🏆 Levels", "🎖️ Badges", "🎯 Earn Types", "🎁 Redemptions", "📊 Scoring Rules"])
    
    with tabs[0]:  # Levels
        render_levels_management()
    
    with tabs[1]:  # Badges
        render_badges_management()
    
    with tabs[2]:  # Earn Types
        render_earn_types_management()
    
    with tabs[3]:  # Redemptions
        render_redemptions_management()
    
    with tabs[4]:  # Scoring Rules
        render_scoring_rules()

def render_levels_management():
    """Render level definitions and management"""
    st.markdown("### 🏆 Leaderboard Levels")
    
    # Display current levels
    for level in LEVELS:
        with st.expander(f"{level['icon']} {level['name']} - Level {level['id']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Points Range:** {level['points_min']:,} - {level['points_max']:,}")
            with col2:
                st.write(f"**Color:** {level['color']}")
                st.markdown(f"<div style='width: 50px; height: 50px; background: {level['color']}; border-radius: 8px;'></div>", unsafe_allow_html=True)
            with col3:
                st.write(f"**Icon:** {level['icon']}")
    
    st.info("ℹ️ Level definitions are configured in the system constants. Contact system admin to modify.")

def render_badges_management():
    """Render badge definitions and management"""
    st.markdown("### 🎖️ Badge Definitions")
    
    # Display badges in a grid
    cols = st.columns(3)
    for i, badge in enumerate(BADGES):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.6); border-radius: 16px; padding: 20px;
                            border: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 16px;">
                    <div style="font-size: 48px; text-align: center; margin-bottom: 12px;">{badge['icon']}</div>
                    <div style="font-size: 18px; font-weight: 700; color: white; text-align: center; margin-bottom: 8px;">
                        {badge['name']}
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; text-align: center; margin-bottom: 12px;">
                        {badge['criteria']}
                    </div>
                    <div style="font-size: 12px; color: #64748b; text-align: center;">
                        Category: {badge['category']} | Threshold: {badge['points_threshold']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.info("ℹ️ Badge definitions are configured in the system constants. Contact system admin to modify.")

def render_earn_types_management():
    """Render earn types (goals) definitions"""
    st.markdown("### 🎯 Earn Types / Goals")
    
    # Display earn types in table
    earn_types_data = []
    for et in EARN_TYPES:
        earn_types_data.append({
            "ID": et["id"],
            "Name": et["name"],
            "Category": et["category"],
            "Points": et["points"],
            "Description": et["description"]
        })
    
    df_earn_types = pd.DataFrame(earn_types_data)
    st.dataframe(df_earn_types, use_container_width=True, hide_index=True)
    
    st.info("ℹ️ Earn types are configured in the system constants. Contact system admin to modify.")

def render_redemptions_management():
    """Render redemption options management"""
    st.markdown("### 🎁 Redemption Options")
    
    # Display redemption options
    cols = st.columns(3)
    for i, option in enumerate(REDEMPTION_OPTIONS):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.6); border-radius: 16px; padding: 20px;
                            border: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 16px;">
                    <div style="font-size: 48px; text-align: center; margin-bottom: 12px;">{option['icon']}</div>
                    <div style="font-size: 18px; font-weight: 700; color: white; text-align: center; margin-bottom: 8px;">
                        {option['name']}
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; text-align: center; margin-bottom: 12px;">
                        {option['description']}
                    </div>
                    <div style="font-size: 14px; color: #3b82f6; text-align: center; margin-bottom: 4px; font-weight: 700;">
                        {option['points']:,} points
                    </div>
                    <div style="font-size: 12px; color: #64748b; text-align: center;">
                        Value: {option['value']} | {option['category']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.info("ℹ️ Redemption options are configured in the system constants. Contact system admin to modify.")

def render_scoring_rules():
    """Render scoring rules reference"""
    st.markdown("### 📊 Scoring Rules - Central Configuration")
    
    st.markdown("All point calculations are based on these rules:")
    
    # Display scoring rules by category
    categories = {
        "Surveys": ["survey_per_question", "survey_short", "survey_medium", "survey_long"],
        "Training": ["training_per_hour", "training_full_day", "training_half_day", "training_mandatory", "training_elective"],
        "Certifications": ["certification_basic", "certification_advanced", "certification_professional"],
        "Initiatives": ["initiative_qudwa", "initiative_digital_champion", "initiative_alkhorayef_champion", 
                        "initiative_thank_you_card", "initiative_idea_submission", "initiative_idea_accepted"],
        "Events": ["event_corporate", "event_csr", "event_wellness"],
        "Performance": ["kpi_target_achieved", "kpi_exceed_target", "extra_milestone"],
        "Attendance": ["perfect_attendance_month", "perfect_attendance_quarter"],
        "Other": ["compliance_module", "safety_training_hour", "hr_session", "town_hall"]
    }
    
    for category, rules in categories.items():
        with st.expander(f"📌 {category}"):
            for rule in rules:
                if rule in SCORING_RULES:
                    st.write(f"**{rule.replace('_', ' ').title()}:** {SCORING_RULES[rule]} points")
    
    st.info("ℹ️ Scoring rules are configured in SCORING_RULES constant at the top of the code.")

# ==============================================================================
# SECTION 8: MAIN APPLICATION
# ==============================================================================

# ==============================================================================
# SECTION 8: UI RENDERING FUNCTIONS - LEADERBOARDS PAGE
# ==============================================================================

def render_leaderboards_page():
    """Render comprehensive leaderboards page with time filters"""
    load_css()
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                    border-radius: 24px; padding: 40px; margin-bottom: 40px;">
            <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 12px; color: white;'>
                🏆 Leaderboards
            </h1>
            <p style='font-size: 20px; opacity: 0.95; color: white;'>
                Company rankings across different time periods - compete and climb to the top!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Time period selector
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        time_period = st.selectbox(
            "📅 Time Period",
            ["Today", "This Month", "Last 3 Months", "This Year", "All Time"],
            index=4  # Default to All Time
        )
    
    with col2:
        department_filter = st.selectbox(
            "🏢 Department",
            ["All Departments"] + list(set([u["department"] for u in st.session_state.users if u["role"] == "user"]))
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_stats = st.checkbox("Show Stats", value=True)
    
    # Calculate date range based on time period
    from datetime import datetime, timedelta
    today = datetime.now()
    
    if time_period == "Today":
        start_date = today.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        period_label = "Today"
    elif time_period == "This Month":
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        period_label = f"{today.strftime('%B %Y')}"
    elif time_period == "Last 3 Months":
        start_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        period_label = "Last 3 Months"
    elif time_period == "This Year":
        start_date = f"{today.year}-01-01"
        end_date = today.strftime("%Y-%m-%d")
        period_label = f"Year {today.year}"
    else:  # All Time
        start_date = "2000-01-01"
        end_date = "2099-12-31"
        period_label = "All Time"
    
    # Generate leaderboard with filters
    leaderboard_data = []
    
    for user in st.session_state.users:
        if user["role"] == "user":
            # Apply department filter
            if department_filter != "All Departments" and user["department"] != department_filter:
                continue
            
            # Calculate points for time period
            period_points = 0
            for point in st.session_state.points_ledger:
                if (point["user_id"] == user["id"] and 
                    point["status"] == "approved" and 
                    start_date <= point["date"] <= end_date):
                    period_points += point["points"]
            
            # Get total points (all time)
            total_points = get_user_total_points(user["id"])
            level = get_user_level(total_points)
            
            # Get category breakdown for period
            category_points = {}
            for point in st.session_state.points_ledger:
                if (point["user_id"] == user["id"] and 
                    point["status"] == "approved" and 
                    start_date <= point["date"] <= end_date):
                    cat = point["category"]
                    category_points[cat] = category_points.get(cat, 0) + point["points"]
            
            leaderboard_data.append({
                "user_id": user["id"],
                "name": user["name"],
                "department": user["department"],
                "title": user.get("title", ""),
                "period_points": period_points,
                "total_points": total_points,
                "level": level,
                "category_breakdown": category_points
            })
    
    # Sort by period points
    leaderboard_data.sort(key=lambda x: x["period_points"], reverse=True)
    
    # Assign ranks
    for i, entry in enumerate(leaderboard_data, 1):
        entry["rank"] = i
    
    # Display top 3 podium
    if len(leaderboard_data) >= 3 and leaderboard_data[0]["period_points"] > 0:
        st.markdown(f"### 🏆 Top 3 Champions - {period_label}")
        
        cols = st.columns([1, 2, 1])
        
        # 2nd Place
        with cols[0]:
            second = leaderboard_data[1]
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #c0c0c0 0%, #a8a8a8 100%);
                            border-radius: 20px; padding: 30px; text-align: center;
                            margin-top: 40px; border: 3px solid #e0e0e0;
                            box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
                    <div style="font-size: 60px; margin-bottom: 12px;">🥈</div>
                    <div style="font-size: 20px; font-weight: 800; color: white; margin-bottom: 8px;">
                        {second['name']}
                    </div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.9); margin-bottom: 12px;">
                        {second['title'] if second['title'] else second['department']}
                    </div>
                    <div style="font-size: 32px; font-weight: 800; color: white;">
                        {second['period_points']:,}
                    </div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.9);">points</div>
                </div>
            """, unsafe_allow_html=True)
        
        # 1st Place
        with cols[1]:
            first = leaderboard_data[0]
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
                            border-radius: 24px; padding: 40px; text-align: center;
                            border: 4px solid #ffed4e; margin-top: 0px;
                            box-shadow: 0 12px 32px rgba(255, 215, 0, 0.4);
                            animation: pulse 2s infinite;">
                    <div style="font-size: 80px; margin-bottom: 16px;">👑</div>
                    <div style="font-size: 24px; font-weight: 800; color: #1e293b; margin-bottom: 8px;">
                        {first['name']}
                    </div>
                    <div style="font-size: 16px; color: #64748b; margin-bottom: 16px;">
                        {first['title'] if first['title'] else first['department']}
                    </div>
                    <div style="font-size: 48px; font-weight: 800; color: #1e293b;">
                        {first['period_points']:,}
                    </div>
                    <div style="font-size: 16px; color: #64748b; margin-bottom: 16px;">points</div>
                    <div style="font-size: 14px; padding: 8px 16px; background: rgba(30, 41, 59, 0.1);
                                border-radius: 8px; display: inline-block;">
                        {first['level']['icon']} {first['level']['name']} Level
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 3rd Place
        with cols[2]:
            third = leaderboard_data[2]
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
                            border-radius: 20px; padding: 30px; text-align: center;
                            margin-top: 40px; border: 3px solid #d4a574;
                            box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
                    <div style="font-size: 60px; margin-bottom: 12px;">🥉</div>
                    <div style="font-size: 20px; font-weight: 800; color: white; margin-bottom: 8px;">
                        {third['name']}
                    </div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.9); margin-bottom: 12px;">
                        {third['title'] if third['title'] else third['department']}
                    </div>
                    <div style="font-size: 32px; font-weight: 800; color: white;">
                        {third['period_points']:,}
                    </div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.9);">points</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Full leaderboard table
    st.markdown(f"### 📊 Complete Rankings - {period_label}")
    
    if department_filter != "All Departments":
        st.info(f"Showing results for: **{department_filter}** department")
    
    if leaderboard_data:
        # Prepare dataframe
        leaderboard_display = []
        for entry in leaderboard_data:
            display_entry = {
                "🏅 Rank": entry["rank"],
                "👤 Name": entry["name"],
                "🏢 Department": entry["department"],
                f"💰 Points ({period_label})": f"{entry['period_points']:,}",
                "📊 Total Points": f"{entry['total_points']:,}",
                "⭐ Level": f"{entry['level']['icon']} {entry['level']['name']}"
            }
            
            if show_stats and entry["category_breakdown"]:
                # Add top category
                top_cat = max(entry["category_breakdown"].items(), key=lambda x: x[1])
                display_entry["🎯 Top Category"] = f"{top_cat[0].title()} ({top_cat[1]} pts)"
            
            leaderboard_display.append(display_entry)
        
        df_leaderboard = pd.DataFrame(leaderboard_display)
        
        # Highlight current user
        current_user = next(u for u in st.session_state.users if u["id"] == st.session_state.current_user_id)
        
        st.dataframe(
            df_leaderboard,
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        # Show current user's position
        user_entry = next((e for e in leaderboard_data if e["user_id"] == st.session_state.current_user_id), None)
        
        if user_entry and user_entry["period_points"] > 0:
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Your Rank", f"#{user_entry['rank']}", help="Your position in this leaderboard")
            
            with col2:
                st.metric(f"Your Points ({period_label})", f"{user_entry['period_points']:,}", help="Points earned in this period")
            
            with col3:
                if user_entry["rank"] > 1:
                    gap = leaderboard_data[user_entry["rank"]-2]["period_points"] - user_entry["period_points"]
                    st.metric("Points to Next Rank", f"{gap:,}", help="Points needed to move up one position")
                else:
                    st.metric("Status", "🏆 #1", help="You're at the top!")
            
            with col4:
                if user_entry["rank"] <= 10:
                    st.metric("Status", "🌟 Top 10!", help="You're in the top 10")
                elif user_entry["rank"] <= 25:
                    st.metric("Status", "⭐ Top 25", help="You're in the top 25")
                else:
                    st.metric("Status", "Keep Going!", help="Keep earning points to climb")
    else:
        st.info("No data available for the selected time period and filters")
    
    # Statistics section
    if show_stats and leaderboard_data:
        st.markdown("---")
        st.markdown(f"### 📈 Period Statistics - {period_label}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_points_period = sum(e["period_points"] for e in leaderboard_data)
        avg_points = total_points_period / len(leaderboard_data) if leaderboard_data else 0
        max_points = max([e["period_points"] for e in leaderboard_data], default=0)
        active_users = len([e for e in leaderboard_data if e["period_points"] > 0])
        
        with col1:
            st.metric("Total Points Awarded", f"{total_points_period:,}")
        
        with col2:
            st.metric("Average Points", f"{avg_points:,.0f}")
        
        with col3:
            st.metric("Highest Score", f"{max_points:,}")
        
        with col4:
            st.metric("Active Employees", f"{active_users}/{len(leaderboard_data)}")

# ==============================================================================
# SECTION 9: MAIN APPLICATION
# ==============================================================================

def main():
    """Main application logic with navigation"""
    load_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 16px; margin-bottom: 20px;">
                <h1 style="color: white; font-size: 32px; margin: 0;">🏆</h1>
                <h2 style="color: white; font-size: 20px; margin: 10px 0 0 0;">Rewards Platform</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # User switcher (for demo purposes)
        st.markdown("### 👤 Switch User")
        user_options = {f"{u['name']} ({u['role'].upper()})": u['id'] for u in st.session_state.users}
        
        current_user_name = next(u['name'] for u in st.session_state.users if u["id"] == st.session_state.current_user_id)
        current_display = f"{current_user_name} ({next(u['role'].upper() for u in st.session_state.users if u['id'] == st.session_state.current_user_id)})"
        
        selected_user = st.selectbox(
            "Select User",
            options=list(user_options.keys()),
            index=list(user_options.keys()).index(current_display) if current_display in user_options.keys() else 0,
            label_visibility="collapsed"
        )
        
        if user_options[selected_user] != st.session_state.current_user_id:
            st.session_state.current_user_id = user_options[selected_user]
            st.rerun()
        
        st.markdown("---")
        
        # Get current user
        current_user = next(u for u in st.session_state.users if u["id"] == st.session_state.current_user_id)
        
        # Format display with title if exists
        user_title = current_user.get('title', '')
        role_display = f'<div style="font-size: 14px; font-weight: 600; color: #a78bfa; margin-bottom: 2px;">{user_title}</div>' if user_title else ''
        
        st.markdown(f"""
            <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; margin-bottom: 20px;">
                <div style="font-size: 14px; color: #94a3b8; margin-bottom: 4px;">Currently viewing as</div>
                <div style="font-size: 16px; font-weight: 700; color: white;">{current_user['name']}</div>
                {role_display}
                <div style="font-size: 13px; color: #94a3b8;">{current_user['department']}</div>
                <div style="font-size: 12px; color: #fbbf24; margin-top: 6px; font-weight: 600;">
                    🔑 Role: {current_user['role'].upper()}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("### 🧭 Navigation")
        
        if current_user["role"] == "admin":
            page = st.radio(
                "Select Page",
                ["👤 Employee View", "🏆 Leaderboards", "📊 Organization", "🔧 Admin", "⚙️ Settings"],
                label_visibility="collapsed"
            )
        else:
            page = st.radio(
                "Select Page",
                ["👤 My Dashboard", "🏆 Leaderboards"],
                label_visibility="collapsed"
            )
        
        # Notifications panel
        st.markdown("---")
        st.markdown("### 🔔 Notifications")
        user_notifications = [n for n in st.session_state.notifications 
                            if n["user_id"] == st.session_state.current_user_id and not n["read"]]
        
        if user_notifications:
            st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; 
                            border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                    <div style="font-size: 14px; font-weight: 600; color: white;">
                        {len(user_notifications)} New Notifications
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for notif in user_notifications[:3]:
                st.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.6); border-radius: 8px; 
                                padding: 12px; margin-bottom: 8px; font-size: 12px; color: #94a3b8;">
                        {notif['message']}
                    </div>
                """, unsafe_allow_html=True)
            
            if st.button("Mark All Read", use_container_width=True):
                for notif in user_notifications:
                    notif["read"] = True
                st.rerun()
        else:
            st.info("No new notifications")
        
        # Quick stats
        if current_user["role"] == "user":
            st.markdown("---")
            st.markdown("### 📊 Quick Stats")
            total_points = get_user_total_points(st.session_state.current_user_id)
            level = get_user_level(total_points)
            
            st.metric("Total Points", f"{total_points:,}")
            st.metric("Current Level", f"{level['icon']} {level['name']}")
    
    # Main content area - route to appropriate page
    if current_user["role"] == "admin":
        if page == "👤 Employee View":
            render_employee_dashboard()
        elif page == "🏆 Leaderboards":
            render_leaderboards_page()
        elif page == "📊 Organization":
            render_organization_dashboard()
        elif page == "🔧 Admin":
            render_admin_dashboard()
        elif page == "⚙️ Settings":
            render_definitions_settings()
    else:
        if page == "👤 My Dashboard":
            render_employee_dashboard()
        elif page == "🏆 Leaderboards":
            render_leaderboards_page()
        elif page == "📊 Organization":
            render_organization_dashboard()

# ==============================================================================
# SECTION 9: APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    main()
