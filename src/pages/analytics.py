"""
HADIANT Analytics Page
Detailed analytics and reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def render():
    """Render analytics page"""
    
    from src.database import supabase_client
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Analytics")
        st.caption("Deep dive into platform metrics")
    with col2:
        period = st.selectbox(
            "Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year"],
            label_visibility="collapsed"
        )
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📱 Chat Analytics", "🖼️ Image Analytics", "💰 Revenue", "👥 Tenant Performance"])
    
    with tab1:
        render_chat_analytics(period)
    
    with tab2:
        render_image_analytics(period)
    
    with tab3:
        render_revenue_analytics(period)
    
    with tab4:
        render_tenant_performance()

def render_chat_analytics(period: str):
    """Chat analytics tab"""
    
    st.subheader("Chat Volume Trend")
    
    # Generate mock data based on period
    days = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90, "This Year": 365}
    num_days = days.get(period, 30)
    
    dates = pd.date_range(end=datetime.now(), periods=num_days)
    chat_data = pd.DataFrame({
        "date": dates,
        "chats": [random.randint(800, 2000) for _ in range(num_days)],
        "responses": [random.randint(750, 1900) for _ in range(num_days)]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chat_data['date'], y=chat_data['chats'],
        mode='lines', name='Incoming',
        line=dict(color='#8b5cf6', width=2),
        fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=chat_data['date'], y=chat_data['responses'],
        mode='lines', name='AI Responses',
        line=dict(color='#10b981', width=2)
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#fff",
        xaxis=dict(gridcolor="#2d2d3d"),
        yaxis=dict(gridcolor="#2d2d3d"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=0, r=0, t=40, b=0),
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Chats", f"{chat_data['chats'].sum():,}")
    col2.metric("Daily Average", f"{int(chat_data['chats'].mean()):,}")
    col3.metric("Peak Day", f"{chat_data['chats'].max():,}")
    col4.metric("Response Rate", "98.5%")
    
    st.divider()
    
    # Hourly distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Hourly Distribution")
        hours = list(range(24))
        hourly_data = [random.randint(20, 150) if 8 <= h <= 22 else random.randint(5, 30) for h in hours]
        
        fig = px.bar(
            x=hours, y=hourly_data,
            labels={'x': 'Hour', 'y': 'Chats'},
            color_discrete_sequence=['#8b5cf6']
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d", dtick=2),
            yaxis=dict(gridcolor="#2d2d3d"),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔥 Peak hours: 19:00 - 21:00")
    
    with col2:
        st.subheader("📈 Response Time")
        response_times = ["< 1s", "1-3s", "3-5s", "5-10s", "> 10s"]
        response_dist = [45, 35, 12, 6, 2]
        
        fig = px.pie(
            values=response_dist,
            names=response_times,
            color_discrete_sequence=["#10b981", "#22c55e", "#84cc16", "#eab308", "#ef4444"],
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("⚡ Avg response time: 2.3 seconds")

def render_image_analytics(period: str):
    """Image generation analytics tab"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Generated", "892")
    col2.metric("This Month", "234")
    col3.metric("Credits Used", "178.4")
    col4.metric("Success Rate", "99.2%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Popular Decoration Styles")
        styles = pd.DataFrame({
            "Style": ["Rustic", "Modern", "Garden", "Traditional", "Luxury", "Intimate", "Boho"],
            "Count": [234, 198, 156, 178, 126, 98, 67]
        })
        
        fig = px.bar(
            styles, x="Count", y="Style",
            orientation='h',
            color_discrete_sequence=["#d946ef"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d", categoryorder='total ascending'),
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Daily Generation Trend")
        days = pd.date_range(end=datetime.now(), periods=14)
        daily_images = [random.randint(15, 45) for _ in range(14)]
        
        fig = px.line(
            x=days, y=daily_images,
            markers=True,
            color_discrete_sequence=["#d946ef"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d", title="Images"),
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("🏆 Top Image Generators")
    top_users = pd.DataFrame({
        "Tenant": ["Royal Wedding Planner", "Jakarta Wedding House", "SYACRI Wedding", "Bali Wedding Expert", "Elegant Dreams WO"],
        "Images": [156, 89, 67, 45, 34],
        "Plan": ["Business", "Business", "Professional", "Professional", "Starter"]
    })
    st.dataframe(top_users, use_container_width=True, hide_index=True)

def render_revenue_analytics(period: str):
    """Revenue analytics tab"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("MRR", "Rp 23.85 Jt", "+18%")
    col2.metric("ARR", "Rp 286.2 Jt")
    col3.metric("Avg Revenue/Tenant", "Rp 507K")
    col4.metric("Churn Rate", "2.3%", "-0.5%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue Growth")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        revenue = [5.2, 6.8, 8.5, 10.2, 12.3, 14.5, 15.8, 17.2, 18.9, 20.5, 22.1, 23.85]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months, y=revenue,
            marker_color='#10b981',
            name='Revenue'
        ))
        fig.add_trace(go.Scatter(
            x=months, y=revenue,
            mode='lines+markers',
            line=dict(color='#fff', width=2),
            name='Trend'
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d", title="Revenue (Juta Rp)"),
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Revenue by Plan")
        plan_revenue = pd.DataFrame({
            "Plan": ["Starter", "Professional", "Business"],
            "Tenants": [18, 19, 10],
            "Revenue": [5.382, 11.381, 9.99]
        })
        
        fig = px.pie(
            plan_revenue,
            values="Revenue",
            names="Plan",
            color_discrete_sequence=["#6366f1", "#8b5cf6", "#d946ef"],
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("📈 Projected Revenue")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Next Month", "Rp 26.2 Jt", "+10%")
    col2.metric("Q1 2026", "Rp 85 Jt")
    col3.metric("End of 2026", "Rp 150 Jt", "Target")

def render_tenant_performance():
    """Tenant performance analytics"""
    
    st.subheader("🏆 Tenant Leaderboard")
    
    performance_data = pd.DataFrame({
        "Rank": ["🥇", "🥈", "🥉", "4", "5"],
        "Tenant": ["Royal Wedding Planner", "Jakarta Wedding House", "SYACRI Wedding", "Bandung Wedding Studio", "Surabaya Wedding Co"],
        "Plan": ["Business", "Business", "Professional", "Professional", "Starter"],
        "Chats/Month": [1567, 1203, 892, 678, 456],
        "Images": [156, 89, 67, 45, 12],
        "Lead Conversion": ["34%", "28%", "31%", "25%", "22%"],
        "Status": ["🟢 Active", "🟢 Active", "🟢 Active", "🟢 Active", "🟢 Active"]
    })
    
    st.dataframe(performance_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Usage Distribution")
        
        # Scatter plot of chats vs images
        scatter_data = pd.DataFrame({
            "Tenant": ["Royal", "Jakarta", "SYACRI", "Bandung", "Surabaya", "Bali", "Elegant"],
            "Chats": [1567, 1203, 892, 678, 456, 445, 234],
            "Images": [156, 89, 67, 45, 12, 34, 5],
            "Plan": ["Business", "Business", "Professional", "Professional", "Starter", "Professional", "Starter"]
        })
        
        fig = px.scatter(
            scatter_data,
            x="Chats", y="Images",
            size="Chats",
            color="Plan",
            hover_name="Tenant",
            color_discrete_map={
                "Starter": "#6366f1",
                "Professional": "#8b5cf6",
                "Business": "#d946ef"
            }
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d"),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ At-Risk Tenants")
        
        at_risk = pd.DataFrame({
            "Tenant": ["Bali Wedding Expert", "Elegant Dreams WO"],
            "Last Active": ["2 days ago", "5 hours ago"],
            "Issue": ["Low activity", "Approaching limit"],
            "Action": ["Reach out", "Upgrade offer"]
        })
        
        st.dataframe(at_risk, use_container_width=True, hide_index=True)
        
        st.warning("2 tenants need attention")
