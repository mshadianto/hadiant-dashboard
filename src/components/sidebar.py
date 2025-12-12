"""
HADIANT Sidebar Component
"""

import streamlit as st

def render_sidebar() -> str:
    """Render sidebar and return selected page"""
    
    with st.sidebar:
        # Logo
        st.markdown('<div class="logo">✨ HADIANT</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6b7280; font-size: 12px; margin-bottom: 30px;">AI Wedding Platform</p>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        menu_items = {
            "dashboard": "🏠 Dashboard",
            "tenants": "👥 Tenants", 
            "analytics": "📊 Analytics",
            "settings": "⚙️ Settings"
        }
        
        selected = st.radio(
            "Navigation",
            options=list(menu_items.keys()),
            format_func=lambda x: menu_items[x],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Connection status
        from src.database import supabase_client
        if supabase_client.is_connected:
            st.success("🟢 Database Connected", icon="✅")
        else:
            st.warning("🟡 Using Mock Data", icon="⚠️")
        
        st.divider()
        
        # User info
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("""
            <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#8b5cf6,#d946ef);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:14px;">MS</div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("**MS Hadianto**")
            st.caption("Super Admin")
        
        # Version
        st.caption("v1.0.0")
        
        return selected
