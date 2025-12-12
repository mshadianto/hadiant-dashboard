"""
HADIANT - AI Wedding Platform Dashboard
Single-file version for Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="HADIANT - AI Wedding Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0f0f17 0%, #1a1a2e 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16162a 100%);
        border-right: 1px solid #2d2d3d;
    }
    
    .logo {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #1f1f2e 100%);
        border: 1px solid #2d2d3d;
        border-radius: 16px;
        padding: 20px;
    }
    
    .badge-active {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
    }
    
    .badge-inactive {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
    }
    
    .badge-starter {
        background: rgba(99, 102, 241, 0.15);
        color: #6366f1;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-professional {
        background: rgba(139, 92, 246, 0.15);
        color: #8b5cf6;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-business {
        background: rgba(217, 70, 239, 0.15);
        color: #d946ef;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 800;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1f1f2e;
        border: 1px solid #2d2d3d;
        border-radius: 10px;
        color: #9ca3af;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        border-color: transparent !important;
        color: white !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# MOCK DATA
# ============================================
@st.cache_data
def get_mock_tenants():
    return pd.DataFrame([
        {"id": 1, "business_name": "SYACRI Wedding Organizer", "phone": "085280638938", "plan": "Professional", "status": "active", "chats_today": 47, "chats_month": 892, "images": 23, "mrr": 599000},
        {"id": 2, "business_name": "Elegant Dreams WO", "phone": "081234567890", "plan": "Starter", "status": "active", "chats_today": 12, "chats_month": 234, "images": 0, "mrr": 299000},
        {"id": 3, "business_name": "Royal Wedding Planner", "phone": "087654321098", "plan": "Business", "status": "active", "chats_today": 89, "chats_month": 1567, "images": 156, "mrr": 999000},
        {"id": 4, "business_name": "Bali Wedding Expert", "phone": "082345678901", "plan": "Professional", "status": "inactive", "chats_today": 0, "chats_month": 445, "images": 34, "mrr": 599000},
        {"id": 5, "business_name": "Jakarta Wedding House", "phone": "089876543210", "plan": "Business", "status": "active", "chats_today": 56, "chats_month": 1203, "images": 89, "mrr": 999000},
        {"id": 6, "business_name": "Surabaya Wedding Co", "phone": "081122334455", "plan": "Starter", "status": "active", "chats_today": 23, "chats_month": 456, "images": 0, "mrr": 299000},
        {"id": 7, "business_name": "Bandung Wedding Studio", "phone": "082233445566", "plan": "Professional", "status": "active", "chats_today": 34, "chats_month": 678, "images": 45, "mrr": 599000},
    ])

@st.cache_data
def get_dashboard_stats():
    return {
        "total_tenants": 47,
        "active_tenants": 42,
        "chats_today": 1247,
        "chats_month": 28934,
        "images_today": 89,
        "mrr": 23850000
    }

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown('<div class="logo">✨ HADIANT</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; font-size: 12px; margin-bottom: 30px;">AI Wedding Platform</p>', unsafe_allow_html=True)
    
    st.divider()
    
    menu = st.radio(
        "Navigation",
        ["🏠 Dashboard", "👥 Tenants", "📊 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # User info
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("""
        <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#8b5cf6,#d946ef);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;">MS</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("**MS Hadianto**")
        st.caption("Super Admin")
    
    st.caption("v1.0.0")

# ============================================
# DASHBOARD PAGE
# ============================================
if "🏠 Dashboard" in menu:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Dashboard")
        st.caption("Overview performa HADIANT Platform")
    with col2:
        st.button("➕ Add Tenant", type="primary")
    
    st.divider()
    
    stats = get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tenants", stats["total_tenants"], f"{stats['active_tenants']} active")
    col2.metric("Chats Today", f"{stats['chats_today']:,}", f"{stats['chats_month']:,} bulan ini")
    col3.metric("Images Generated", f"{stats['images_today']:,}", "Today")
    col4.metric("MRR", f"Rp {stats['mrr']/1000000:.1f}Jt", "+18%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Chat Activity (7 Days)")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        values = [4200, 3800, 5100, 4700, 3200, 6800, 5900]
        fig = px.bar(x=days, y=values, color_discrete_sequence=["#8b5cf6"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d", title=""),
            yaxis=dict(gridcolor="#2d2d3d", title="Chats"),
            showlegend=False,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Revenue Growth")
        months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        revenue = [8.5, 12.3, 15.8, 18.2, 21.5, 23.85]
        fig = px.line(x=months, y=revenue, markers=True, color_discrete_sequence=["#10b981"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d", title=""),
            yaxis=dict(gridcolor="#2d2d3d", title="Revenue (Juta Rp)"),
            showlegend=False,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 Plan Distribution")
        fig = px.pie(
            values=[18, 19, 10],
            names=["Starter", "Professional", "Business"],
            color_discrete_sequence=["#6366f1", "#8b5cf6", "#d946ef"],
            hole=0.4
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#fff")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Recent Active Tenants")
        tenants = get_mock_tenants()
        display_df = tenants[["business_name", "plan", "status", "chats_today", "images"]].head(5)
        display_df.columns = ["Business", "Plan", "Status", "Chats", "Images"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ============================================
# TENANTS PAGE
# ============================================
elif "👥 Tenants" in menu:
    st.title("Tenants")
    st.caption("Manage semua Wedding Organizer clients")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search tenants...")
    with col2:
        plan_filter = st.selectbox("Plan", ["All", "Starter", "Professional", "Business"])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
    
    st.divider()
    
    tenants = get_mock_tenants()
    
    if search:
        tenants = tenants[tenants["business_name"].str.contains(search, case=False)]
    if plan_filter != "All":
        tenants = tenants[tenants["plan"] == plan_filter]
    if status_filter != "All":
        tenants = tenants[tenants["status"] == status_filter.lower()]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(tenants))
    col2.metric("Active", len(tenants[tenants["status"] == "active"]))
    col3.metric("Total Chats", f"{tenants['chats_month'].sum():,}")
    col4.metric("Total MRR", f"Rp {tenants['mrr'].sum()/1000000:.1f}Jt")
    
    st.divider()
    
    for _, tenant in tenants.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 1.2, 1, 1, 1, 0.8])
        
        with col1:
            st.markdown(f"**{tenant['business_name']}**")
            st.caption(f"📱 {tenant['phone']}")
        
        with col2:
            plan_colors = {"Starter": "#6366f1", "Professional": "#8b5cf6", "Business": "#d946ef"}
            color = plan_colors.get(tenant['plan'], "#6366f1")
            st.markdown(f"<span style='background:{color}20;color:{color};padding:4px 12px;border-radius:6px;font-size:12px;font-weight:600;'>{tenant['plan']}</span>", unsafe_allow_html=True)
        
        with col3:
            status_color = "#10b981" if tenant['status'] == "active" else "#f59e0b"
            st.markdown(f"<span style='background:{status_color}20;color:{status_color};padding:4px 12px;border-radius:6px;font-size:12px;'>● {tenant['status']}</span>", unsafe_allow_html=True)
        
        with col4:
            st.caption("Chats")
            st.markdown(f"**{tenant['chats_today']}**")
        
        with col5:
            st.caption("Images")
            st.markdown(f"**{tenant['images']}**")
        
        with col6:
            st.button("⚙️", key=f"edit_{tenant['id']}")
        
        st.divider()

# ============================================
# ANALYTICS PAGE
# ============================================
elif "📊 Analytics" in menu:
    st.title("Analytics")
    st.caption("Deep dive into platform metrics")
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📱 Chat Analytics", "🖼️ Image Analytics", "💰 Revenue"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Chats", "28,934")
        col2.metric("Daily Average", "1,247")
        col3.metric("Peak Hour", "19:00-21:00")
        col4.metric("Response Rate", "98.5%")
        
        st.divider()
        
        st.subheader("Chat Volume Trend (30 Days)")
        dates = pd.date_range(end=datetime.now(), periods=30)
        chat_data = pd.DataFrame({
            "date": dates,
            "chats": [random.randint(800, 1500) for _ in range(30)]
        })
        fig = px.area(chat_data, x="date", y="chats", color_discrete_sequence=["#8b5cf6"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Generated", "892")
        col2.metric("This Month", "234")
        col3.metric("Credits Used", "178.4")
        col4.metric("Success Rate", "99.2%")
        
        st.divider()
        
        st.subheader("Popular Decoration Styles")
        styles = pd.DataFrame({
            "Style": ["Rustic", "Modern", "Garden", "Traditional", "Luxury"],
            "Count": [234, 198, 156, 178, 126]
        })
        fig = px.bar(styles, x="Count", y="Style", orientation='h', color_discrete_sequence=["#d946ef"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            yaxis=dict(categoryorder='total ascending')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("MRR", "Rp 23.85 Jt", "+18%")
        col2.metric("ARR", "Rp 286.2 Jt")
        col3.metric("Avg/Tenant", "Rp 507K")
        col4.metric("Churn Rate", "2.3%")
        
        st.divider()
        
        st.subheader("Revenue Growth")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        revenue = [5.2, 6.8, 8.5, 10.2, 12.3, 14.5, 15.8, 17.2, 18.9, 20.5, 22.1, 23.85]
        fig = px.bar(x=months, y=revenue, color_discrete_sequence=["#10b981"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d", title="Revenue (Juta Rp)")
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# SETTINGS PAGE
# ============================================
elif "⚙️ Settings" in menu:
    st.title("Settings")
    st.caption("Platform configuration")
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "💳 Plans", "👤 Profile"])
    
    with tab1:
        st.subheader("API Configuration")
        
        with st.expander("🗄️ Supabase", expanded=True):
            st.text_input("Project URL", value="https://edcmmwadqnpwybflmgtx.supabase.co", disabled=True)
            st.text_input("API Key", value="****", type="password")
        
        with st.expander("🧠 GROQ"):
            st.text_input("API Key", value="****", type="password", key="groq")
            st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        
        with st.expander("🎨 Stability AI"):
            st.text_input("API Key", value="****", type="password", key="stability")
        
        with st.expander("📱 WAHA"):
            st.text_input("Instance URL", value="https://waha-xxx.sumopod.my.id")
            st.text_input("API Key", value="****", type="password", key="waha")
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("Settings saved!")
    
    with tab2:
        st.subheader("Subscription Plans")
        
        plans = pd.DataFrame({
            "Plan": ["Starter", "Professional", "Business"],
            "Monthly": ["Rp 299K", "Rp 599K", "Rp 999K"],
            "Chat Limit": ["500/mo", "2,000/mo", "Unlimited"],
            "Images": ["0", "50/mo", "200/mo"],
            "WA Sessions": [1, 1, 3]
        })
        st.dataframe(plans, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Admin Profile")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("""
            <div style="width:100px;height:100px;border-radius:20px;background:linear-gradient(135deg,#8b5cf6,#d946ef);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:32px;">MS</div>
            """, unsafe_allow_html=True)
        with col2:
            st.text_input("Full Name", value="MS Hadianto")
            st.text_input("Email", value="mshadianto@hadiant.ai")
        
        if st.button("Update Profile"):
            st.success("Profile updated!")

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption("© 2025 HADIANT - AI Wedding Platform by MS Hadianto")