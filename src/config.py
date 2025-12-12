"""
HADIANT Configuration
Environment variables and settings
"""

import os
from dataclasses import dataclass
from typing import Optional
import streamlit as st

@dataclass
class Settings:
    """Application settings from environment/secrets"""
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""
    
    # GROQ
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Stability AI
    stability_api_key: str = ""
    stability_api_key_backup: str = ""
    
    # WAHA
    waha_url: str = ""
    waha_api_key: str = ""
    
    # App
    app_name: str = "HADIANT"
    app_version: str = "1.0.0"
    debug: bool = False
    
    def __post_init__(self):
        """Load from Streamlit secrets or environment"""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets'):
                self.supabase_url = st.secrets.get("supabase", {}).get("url", "")
                self.supabase_key = st.secrets.get("supabase", {}).get("key", "")
                self.supabase_service_key = st.secrets.get("supabase", {}).get("service_key", "")
                
                self.groq_api_key = st.secrets.get("groq", {}).get("api_key", "")
                
                self.stability_api_key = st.secrets.get("stability", {}).get("api_key", "")
                self.stability_api_key_backup = st.secrets.get("stability", {}).get("api_key_backup", "")
                
                self.waha_url = st.secrets.get("waha", {}).get("url", "")
                self.waha_api_key = st.secrets.get("waha", {}).get("api_key", "")
        except Exception:
            pass
        
        # Fallback to environment variables
        self.supabase_url = self.supabase_url or os.getenv("SUPABASE_URL", "")
        self.supabase_key = self.supabase_key or os.getenv("SUPABASE_KEY", "")
        self.supabase_service_key = self.supabase_service_key or os.getenv("SUPABASE_SERVICE_KEY", "")
        
        self.groq_api_key = self.groq_api_key or os.getenv("GROQ_API_KEY", "")
        
        self.stability_api_key = self.stability_api_key or os.getenv("STABILITY_API_KEY", "")
        
        self.waha_url = self.waha_url or os.getenv("WAHA_URL", "")
        self.waha_api_key = self.waha_api_key or os.getenv("WAHA_API_KEY", "")
        
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

# Singleton instance
settings = Settings()

# Plan configurations
PLANS = {
    "starter": {
        "name": "Starter",
        "price_monthly": 299000,
        "price_yearly": 2990000,
        "chat_limit": 500,
        "image_limit": 0,
        "whatsapp_sessions": 1,
        "features": ["AI Chat", "Lead Qualification", "Basic Analytics"],
        "color": "#6366f1"
    },
    "professional": {
        "name": "Professional", 
        "price_monthly": 599000,
        "price_yearly": 5990000,
        "chat_limit": 2000,
        "image_limit": 50,
        "whatsapp_sessions": 1,
        "features": ["AI Chat", "Lead Qualification", "Image Generation", "Advanced Analytics", "Priority Support"],
        "color": "#8b5cf6"
    },
    "business": {
        "name": "Business",
        "price_monthly": 999000,
        "price_yearly": 9990000,
        "chat_limit": None,  # Unlimited
        "image_limit": 200,
        "whatsapp_sessions": 3,
        "features": ["AI Chat", "Lead Qualification", "Image Generation", "Advanced Analytics", "Priority Support", "Multi WhatsApp", "API Access"],
        "color": "#d946ef"
    },
    "enterprise": {
        "name": "Enterprise",
        "price_monthly": 0,  # Custom
        "price_yearly": 0,
        "chat_limit": None,
        "image_limit": None,
        "whatsapp_sessions": 10,
        "features": ["Everything", "White Label", "Dedicated Support", "Custom Integration"],
        "color": "#f59e0b"
    }
}
