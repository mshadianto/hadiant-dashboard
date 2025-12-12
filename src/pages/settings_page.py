"""
HADIANT Settings Page
Platform configuration and admin settings
"""

import streamlit as st
import pandas as pd

def render():
    """Render settings page"""
    
    st.title("Settings")
    st.caption("Platform configuration and admin settings")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔑 API Keys",
        "💳 Plans & Billing", 
        "🤖 AI Configuration",
        "📱 WhatsApp (WAHA)",
        "👤 Admin Profile"
    ])
    
    with tab1:
        render_api_settings()
    
    with tab2:
        render_billing_settings()
    
    with tab3:
        render_ai_settings()
    
    with tab4:
        render_waha_settings()
    
    with tab5:
        render_profile_settings()

def render_api_settings():
    """API keys configuration"""
    
    st.subheader("API Configuration")
    st.caption("Manage API keys for external services")
    
    # Supabase
    with st.expander("🗄️ Supabase (Database)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Project URL", value="https://edcmmwadqnpwybflmgtx.supabase.co", disabled=True)
        with col2:
            st.text_input("Anon Key", value="eyJhbG***", type="password")
        
        st.text_input("Service Role Key", value="eyJhbG***", type="password", help="Only for server-side operations")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Test Connection", key="test_supabase"):
                st.success("✅ Connected to Supabase!")
    
    # GROQ
    with st.expander("🧠 GROQ (AI Model)"):
        st.text_input("API Key", value="gsk_****", type="password", key="groq_key")
        st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"])
        st.slider("Temperature", 0.0, 1.0, 0.7)
        st.number_input("Max Tokens", 100, 4096, 1024)
    
    # Stability AI
    with st.expander("🎨 Stability AI (Image Generation)"):
        st.text_input("API Key (Primary)", value="sk-****", type="password", key="stability_key_1")
        st.text_input("API Key (Backup)", value="sk-****", type="password", key="stability_key_2")
        st.selectbox("Model", ["stable-diffusion-xl-1024-v1-0", "stable-diffusion-v1-6"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Steps", 10, 50, 30)
        with col2:
            st.number_input("CFG Scale", 1, 20, 7)
    
    st.divider()
    
    if st.button("💾 Save API Settings", type="primary"):
        st.success("Settings saved successfully!")

def render_billing_settings():
    """Plans and billing configuration"""
    
    st.subheader("Subscription Plans")
    
    plans_data = pd.DataFrame({
        "Plan": ["Starter", "Professional", "Business", "Enterprise"],
        "Monthly": ["Rp 299K", "Rp 599K", "Rp 999K", "Custom"],
        "Yearly": ["Rp 2.99Jt", "Rp 5.99Jt", "Rp 9.99Jt", "Custom"],
        "Chat Limit": ["500/mo", "2,000/mo", "Unlimited", "Unlimited"],
        "Images": ["0", "50/mo", "200/mo", "Unlimited"],
        "WA Sessions": ["1", "1", "3", "10"],
        "Active Tenants": ["18", "19", "10", "0"]
    })
    
    st.dataframe(plans_data, use_container_width=True, hide_index=True)
    
    with st.expander("✏️ Edit Plans"):
        plan_to_edit = st.selectbox("Select Plan", ["Starter", "Professional", "Business"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Monthly Price (Rp)", value=299000 if plan_to_edit == "Starter" else 599000)
            st.number_input("Chat Limit", value=500 if plan_to_edit == "Starter" else 2000)
        with col2:
            st.number_input("Yearly Price (Rp)", value=2990000 if plan_to_edit == "Starter" else 5990000)
            st.number_input("Image Limit", value=0 if plan_to_edit == "Starter" else 50)
        
        if st.button("Update Plan"):
            st.success(f"{plan_to_edit} plan updated!")
    
    st.divider()
    
    st.subheader("Payment Configuration")
    
    with st.expander("💳 Payment Gateway (Coming Soon)"):
        st.selectbox("Provider", ["Xendit", "Midtrans", "Stripe"], disabled=True)
        st.text_input("API Key", disabled=True, placeholder="Coming soon...")
        st.info("Payment integration akan tersedia di versi mendatang")

def render_ai_settings():
    """AI configuration"""
    
    st.subheader("Default AI Configuration")
    st.caption("Settings ini akan digunakan sebagai default untuk tenant baru")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Default AI Name", value="Sarah")
        st.text_input("Default Welcome Message", value="Halo! Saya Sarah, asisten virtual. Ada yang bisa dibantu?")
    
    with col2:
        st.selectbox("Default Language", ["Bahasa Indonesia", "English", "Both"])
        st.selectbox("Personality", ["Friendly & Professional", "Formal", "Casual"])
    
    st.text_area(
        "Default System Prompt",
        value="""Kamu adalah Sarah, asisten virtual Wedding Organizer yang ramah dan profesional.

TUGAS UTAMA:
1. Menjawab pertanyaan tentang paket wedding
2. Membantu calon pengantin merencanakan pernikahan
3. Mengumpulkan informasi leads (nama, tanggal, budget, jumlah tamu)
4. Memberikan rekomendasi yang personal

GAYA KOMUNIKASI:
- Ramah dan hangat
- Gunakan bahasa Indonesia yang santai tapi sopan
- Panggil user dengan "Kak"
- Gunakan emoji secukupnya ✨💐""",
        height=250
    )
    
    st.divider()
    
    st.subheader("Image Generation Prompts")
    
    decoration_styles = st.text_area(
        "Decoration Style Mappings",
        value="""rustic: rustic wooden wedding decoration with flowers and fairy lights
modern: modern minimalist wedding decoration with clean lines
garden: outdoor garden wedding with natural greenery
traditional: traditional Javanese wedding pelaminan
luxury: grand ballroom wedding with crystal chandeliers""",
        height=150
    )
    
    if st.button("💾 Save AI Settings", type="primary"):
        st.success("AI settings saved!")

def render_waha_settings():
    """WAHA configuration"""
    
    st.subheader("WAHA Configuration")
    st.caption("WhatsApp HTTP API settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("WAHA Instance URL", value="https://waha-qikiufjwa2nh.cgk-max.sumopod.my.id")
        st.text_input("API Key", value="****", type="password")
    
    with col2:
        st.text_input("Webhook Base URL", value="https://your-n8n.com/webhook")
        st.number_input("Session Timeout (hours)", value=24)
    
    st.divider()
    
    st.subheader("Active Sessions")
    
    sessions_data = pd.DataFrame({
        "Session": ["SYACRI_WO", "ELEGANT_WO", "ROYAL_WO"],
        "Tenant": ["SYACRI Wedding", "Elegant Dreams WO", "Royal Wedding Planner"],
        "Phone": ["085280638938", "081234567890", "087654321098"],
        "Status": ["🟢 Connected", "🟢 Connected", "🟡 Reconnecting"],
        "Last Activity": ["2 min ago", "5 min ago", "10 min ago"]
    })
    
    st.dataframe(sessions_data, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Refresh All Sessions"):
            st.info("Refreshing sessions...")
    with col2:
        if st.button("📊 View Logs"):
            st.info("Opening logs...")
    with col3:
        if st.button("➕ New Session"):
            st.info("Create session from Tenants page")

def render_profile_settings():
    """Admin profile settings"""
    
    st.subheader("Admin Profile")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div style="width:120px;height:120px;border-radius:20px;background:linear-gradient(135deg,#8b5cf6,#d946ef);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:40px;">MS</div>
        """, unsafe_allow_html=True)
        st.button("📷 Change Photo", disabled=True)
    
    with col2:
        st.text_input("Full Name", value="MS Hadianto")
        st.text_input("Email", value="mshadianto@hadiant.ai")
        st.text_input("Phone", value="081596588833")
    
    st.divider()
    
    st.subheader("Security")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Current Password", type="password")
        st.text_input("New Password", type="password")
        st.text_input("Confirm Password", type="password")
    
    with col2:
        st.checkbox("Enable 2FA", value=False)
        st.selectbox("Session Timeout", ["1 hour", "4 hours", "8 hours", "24 hours"])
    
    st.divider()
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("💾 Save Profile", type="primary"):
            st.success("Profile updated!")
    with col2:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.rerun()
