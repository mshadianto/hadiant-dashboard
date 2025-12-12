"""
HADIANT Dashboard Page
Main overview with statistics and charts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render dashboard page"""
    
    from src.database import supabase_client
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Dashboard")
        st.caption("Overview performa HADIANT Platform")
    with col2:
        if st.button("➕ Add Tenant", type="primary"):
            st.session_state.show_add_tenant = True
    
    st.divider()
    
    # Get stats
    stats = supabase_client.get_dashboard_stats()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Tenants",
            value=stats["total_tenants"],
            delta=f"{stats['active_tenants']} active"
        )
    
    with col2:
        st.metric(
            label="Chats Today",
            value=f"{stats['chats_today']:,}",
            delta=f"{stats['chats_month']:,} bulan ini"
        )
    
    with col3:
        st.metric(
            label="Images Generated",
            value=f"{stats.get('images_today', 0):,}",
            delta="Today"
        )
    
    with col4:
        mrr = stats['mrr']
        st.metric(
            label="MRR",
            value=f"Rp {mrr/1000000:.1f}Jt",
            delta="+18%"
        )
    
    st.divider()
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Chat Activity (7 Days)")
        usage_df = supabase_client.get_usage_stats(days=7)
        
        if not usage_df.empty:
            fig = px.bar(
                usage_df,
                x="date",
                y="chat_count",
                color_discrete_sequence=["#8b5cf6"]
            )
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
        else:
            # Mock data
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            values = [4200, 3800, 5100, 4700, 3200, 6800, 5900]
            fig = px.bar(x=days, y=values, color_discrete_sequence=["#8b5cf6"])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#fff",
                xaxis=dict(gridcolor="#2d2d3d", title=""),
                yaxis=dict(gridcolor="#2d2d3d", title="Chats"),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Revenue Growth")
        
        # Mock revenue data
        months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        revenue = [8.5, 12.3, 15.8, 18.2, 21.5, 23.85]
        
        fig = px.line(
            x=months, y=revenue,
            markers=True,
            color_discrete_sequence=["#10b981"]
        )
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
    
    # Second Row
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 Plan Distribution")
        
        tenants_df = supabase_client.get_tenants()
        if not tenants_df.empty and 'plan_name' in tenants_df.columns:
            plan_counts = tenants_df['plan_name'].value_counts()
            fig = px.pie(
                values=plan_counts.values,
                names=plan_counts.index,
                color_discrete_sequence=["#6366f1", "#8b5cf6", "#d946ef"],
                hole=0.4
            )
        else:
            # Mock
            fig = px.pie(
                values=[18, 19, 10],
                names=["Starter", "Professional", "Business"],
                color_discrete_sequence=["#6366f1", "#8b5cf6", "#d946ef"],
                hole=0.4
            )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#fff",
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Recent Active Tenants")
        
        tenants_df = supabase_client.get_tenants()
        
        if not tenants_df.empty:
            display_cols = ["business_name", "plan_name", "status", "phone"]
            available_cols = [c for c in display_cols if c in tenants_df.columns]
            
            if available_cols:
                display_df = tenants_df[available_cols].head(5)
                display_df.columns = [c.replace("_", " ").title() for c in available_cols]
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("No tenant data available")
        else:
            st.info("No tenants found")
    
    # Add Tenant Modal
    if st.session_state.get("show_add_tenant"):
        render_add_tenant_modal()

def render_add_tenant_modal():
    """Render add tenant modal/form"""
    
    with st.expander("➕ Add New Tenant", expanded=True):
        with st.form("add_tenant_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                business_name = st.text_input("Business Name *")
                owner_name = st.text_input("Owner Name")
                email = st.text_input("Email *")
            
            with col2:
                phone = st.text_input("WhatsApp Number *")
                city = st.text_input("City")
                plan = st.selectbox("Plan", ["Starter", "Professional", "Business"])
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submitted = st.form_submit_button("Create Tenant", type="primary")
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_add_tenant = False
                    st.rerun()
            
            if submitted:
                if business_name and email and phone:
                    from src.database import supabase_client
                    
                    result = supabase_client.create_tenant({
                        "business_name": business_name,
                        "owner_name": owner_name,
                        "email": email,
                        "phone": phone,
                        "city": city,
                        "status": "active"
                    })
                    
                    if result:
                        st.success(f"✅ Tenant '{business_name}' created!")
                        st.session_state.show_add_tenant = False
                        st.rerun()
                    else:
                        st.error("Failed to create tenant")
                else:
                    st.error("Please fill required fields")
