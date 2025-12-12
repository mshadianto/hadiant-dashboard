"""
HADIANT Tenants Page
Manage Wedding Organizer clients
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render():
    """Render tenants page"""
    
    from src.database import supabase_client
    from src.config import PLANS
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Tenants")
        st.caption("Manage semua Wedding Organizer clients")
    with col2:
        if st.button("➕ Add Tenant", type="primary", key="add_tenant_btn"):
            st.session_state.show_add_tenant_form = True
    
    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by name, phone, email...")
    with col2:
        plan_filter = st.selectbox("Plan", ["All", "Starter", "Professional", "Business"])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Trial"])
    
    st.divider()
    
    # Get tenants
    tenants_df = supabase_client.get_tenants()
    
    # Apply filters
    if not tenants_df.empty:
        if search:
            mask = (
                tenants_df['business_name'].str.contains(search, case=False, na=False) |
                tenants_df.get('phone', pd.Series()).str.contains(search, case=False, na=False) |
                tenants_df.get('email', pd.Series()).str.contains(search, case=False, na=False)
            )
            tenants_df = tenants_df[mask]
        
        if plan_filter != "All" and 'plan_name' in tenants_df.columns:
            tenants_df = tenants_df[tenants_df['plan_name'] == plan_filter]
        
        if status_filter != "All":
            tenants_df = tenants_df[tenants_df['status'] == status_filter.lower()]
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(tenants_df)
    active = len(tenants_df[tenants_df['status'] == 'active']) if not tenants_df.empty else 0
    
    col1.metric("Total", total)
    col2.metric("Active", active)
    col3.metric("Inactive", total - active)
    
    # Calculate MRR
    if not tenants_df.empty and 'plan_name' in tenants_df.columns:
        plan_prices = {"Starter": 299000, "Professional": 599000, "Business": 999000}
        mrr = sum([plan_prices.get(p, 0) for p in tenants_df[tenants_df['status'] == 'active']['plan_name']])
        col4.metric("MRR", f"Rp {mrr/1000000:.1f}Jt")
    else:
        col4.metric("MRR", "Rp 0")
    
    st.divider()
    
    # Add Tenant Form
    if st.session_state.get("show_add_tenant_form"):
        render_add_tenant_form()
    
    # Tenants List
    if tenants_df.empty:
        st.info("No tenants found. Click 'Add Tenant' to create one.")
    else:
        for idx, tenant in tenants_df.iterrows():
            render_tenant_card(tenant)

def render_add_tenant_form():
    """Render add/edit tenant form"""
    
    from src.database import supabase_client
    
    with st.expander("➕ Add New Tenant", expanded=True):
        with st.form("add_tenant_form", clear_on_submit=True):
            st.subheader("Tenant Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                business_name = st.text_input("Business Name *", placeholder="Wedding Organizer Name")
                owner_name = st.text_input("Owner Name", placeholder="Owner/PIC Name")
                email = st.text_input("Email *", placeholder="email@example.com")
                phone = st.text_input("WhatsApp Number *", placeholder="08xxxxxxxxxx")
            
            with col2:
                city = st.text_input("City", placeholder="Jakarta")
                address = st.text_area("Address", placeholder="Full address", height=68)
                plan = st.selectbox("Plan *", ["Starter", "Professional", "Business"])
                waha_session = st.text_input("WAHA Session Name", placeholder="Leave empty to auto-generate")
            
            st.subheader("AI Configuration")
            
            col1, col2 = st.columns(2)
            with col1:
                ai_name = st.text_input("AI Assistant Name", value="Sarah", placeholder="AI persona name")
            with col2:
                welcome_msg = st.text_input("Welcome Message", value="Halo! Saya Sarah, asisten virtual. Ada yang bisa dibantu?")
            
            ai_prompt = st.text_area(
                "Custom System Prompt (Optional)",
                placeholder="Additional instructions for AI behavior...",
                height=100
            )
            
            st.divider()
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                submitted = st.form_submit_button("✅ Create Tenant", type="primary")
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_add_tenant_form = False
                    st.rerun()
            
            if submitted:
                if not business_name or not email or not phone:
                    st.error("Please fill all required fields (marked with *)")
                else:
                    # Generate WAHA session name if empty
                    if not waha_session:
                        waha_session = business_name.upper().replace(" ", "_")[:20] + "_WO"
                    
                    tenant_data = {
                        "business_name": business_name,
                        "owner_name": owner_name,
                        "email": email,
                        "phone": phone,
                        "city": city,
                        "address": address,
                        "waha_session_name": waha_session,
                        "whatsapp_number": phone,
                        "ai_persona_name": ai_name,
                        "ai_welcome_message": welcome_msg,
                        "ai_system_prompt": ai_prompt,
                        "status": "trial",
                        "subscription_status": "trial"
                    }
                    
                    result = supabase_client.create_tenant(tenant_data)
                    
                    if result:
                        st.success(f"✅ Tenant '{business_name}' created successfully!")
                        st.session_state.show_add_tenant_form = False
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Failed to create tenant. Please try again.")

def render_tenant_card(tenant):
    """Render single tenant card"""
    
    # Status colors
    status_colors = {
        "active": ("🟢", "#10b981", "rgba(16, 185, 129, 0.15)"),
        "inactive": ("🟡", "#f59e0b", "rgba(245, 158, 11, 0.15)"),
        "trial": ("🔵", "#3b82f6", "rgba(59, 130, 246, 0.15)"),
        "suspended": ("🔴", "#ef4444", "rgba(239, 68, 68, 0.15)")
    }
    
    plan_colors = {
        "Starter": ("#6366f1", "rgba(99, 102, 241, 0.15)"),
        "Professional": ("#8b5cf6", "rgba(139, 92, 246, 0.15)"),
        "Business": ("#d946ef", "rgba(217, 70, 239, 0.15)")
    }
    
    status = tenant.get('status', 'inactive')
    plan_name = tenant.get('plan_name', 'Starter')
    
    status_icon, status_color, status_bg = status_colors.get(status, status_colors['inactive'])
    plan_color, plan_bg = plan_colors.get(plan_name, plan_colors['Starter'])
    
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 1.2, 1, 1, 1, 0.8])
        
        with col1:
            st.markdown(f"**{tenant.get('business_name', 'N/A')}**")
            st.caption(f"📱 {tenant.get('phone', 'N/A')} • 📧 {tenant.get('email', 'N/A')}")
        
        with col2:
            st.markdown(
                f"<span style='background:{plan_bg};color:{plan_color};padding:4px 12px;border-radius:6px;font-size:12px;font-weight:600;'>{plan_name}</span>",
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"<span style='background:{status_bg};color:{status_color};padding:4px 12px;border-radius:6px;font-size:12px;'>{status_icon} {status}</span>",
                unsafe_allow_html=True
            )
        
        with col4:
            st.caption("Chats")
            st.markdown("**--**")
        
        with col5:
            st.caption("Images")
            st.markdown("**--**")
        
        with col6:
            if st.button("⚙️", key=f"edit_{tenant.get('id', idx)}", help="Edit tenant"):
                st.session_state.editing_tenant = tenant.get('id')
                st.session_state.show_edit_modal = True
        
        st.divider()

def render_edit_tenant_modal(tenant_id: str):
    """Render edit tenant modal"""
    
    from src.database import supabase_client
    
    tenant = supabase_client.get_tenant_by_id(tenant_id)
    
    if not tenant:
        st.error("Tenant not found")
        return
    
    with st.expander(f"Edit: {tenant.get('business_name')}", expanded=True):
        with st.form("edit_tenant_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                business_name = st.text_input("Business Name", value=tenant.get('business_name', ''))
                email = st.text_input("Email", value=tenant.get('email', ''))
                phone = st.text_input("Phone", value=tenant.get('phone', ''))
            
            with col2:
                status = st.selectbox(
                    "Status",
                    ["active", "inactive", "trial", "suspended"],
                    index=["active", "inactive", "trial", "suspended"].index(tenant.get('status', 'active'))
                )
                city = st.text_input("City", value=tenant.get('city', ''))
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    success = supabase_client.update_tenant(tenant_id, {
                        "business_name": business_name,
                        "email": email,
                        "phone": phone,
                        "status": status,
                        "city": city
                    })
                    if success:
                        st.success("Tenant updated!")
                        st.session_state.show_edit_modal = False
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_edit_modal = False
                    st.rerun()
