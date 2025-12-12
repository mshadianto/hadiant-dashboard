"""
HADIANT Database Module
Supabase client and database operations
"""

import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import pandas as pd

# Try to import supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

class SupabaseClient:
    """Supabase database client wrapper"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Supabase client"""
        if not SUPABASE_AVAILABLE:
            return
            
        try:
            url = st.secrets.get("supabase", {}).get("url", "")
            key = st.secrets.get("supabase", {}).get("key", "")
            
            if url and key:
                self.client = create_client(url, key)
        except Exception as e:
            st.warning(f"Could not connect to Supabase: {e}")
    
    @property
    def is_connected(self) -> bool:
        return self.client is not None
    
    # ============================================
    # TENANTS
    # ============================================
    
    def get_tenants(self, status: Optional[str] = None, plan: Optional[str] = None) -> pd.DataFrame:
        """Get all tenants with optional filters"""
        if not self.is_connected:
            return self._get_mock_tenants()
        
        try:
            query = self.client.table("tenants").select("*, plans(name, price_monthly)")
            
            if status and status != "all":
                query = query.eq("status", status)
            
            response = query.execute()
            
            if response.data:
                df = pd.DataFrame(response.data)
                # Extract plan name
                if 'plans' in df.columns:
                    df['plan_name'] = df['plans'].apply(lambda x: x.get('name') if x else None)
                    df['plan_price'] = df['plans'].apply(lambda x: x.get('price_monthly') if x else 0)
                return df
            return pd.DataFrame()
            
        except Exception as e:
            st.error(f"Error fetching tenants: {e}")
            return self._get_mock_tenants()
    
    def get_tenant_by_id(self, tenant_id: str) -> Optional[Dict]:
        """Get single tenant by ID"""
        if not self.is_connected:
            return None
            
        try:
            response = self.client.table("tenants")\
                .select("*, plans(*)")\
                .eq("id", tenant_id)\
                .single()\
                .execute()
            return response.data
        except Exception:
            return None
    
    def create_tenant(self, data: Dict) -> Optional[Dict]:
        """Create new tenant"""
        if not self.is_connected:
            return None
            
        try:
            response = self.client.table("tenants").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating tenant: {e}")
            return None
    
    def update_tenant(self, tenant_id: str, data: Dict) -> bool:
        """Update tenant"""
        if not self.is_connected:
            return False
            
        try:
            self.client.table("tenants").update(data).eq("id", tenant_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating tenant: {e}")
            return False
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """Delete tenant (soft delete by setting status)"""
        return self.update_tenant(tenant_id, {"status": "deleted", "is_active": False})
    
    # ============================================
    # PLANS
    # ============================================
    
    def get_plans(self) -> pd.DataFrame:
        """Get all subscription plans"""
        if not self.is_connected:
            return self._get_mock_plans()
            
        try:
            response = self.client.table("plans").select("*").eq("is_active", True).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception:
            return self._get_mock_plans()
    
    # ============================================
    # CONVERSATIONS & MESSAGES
    # ============================================
    
    def get_conversations(self, tenant_id: Optional[str] = None, limit: int = 100) -> pd.DataFrame:
        """Get conversations"""
        if not self.is_connected:
            return pd.DataFrame()
            
        try:
            query = self.client.table("conversations").select("*").limit(limit)
            if tenant_id:
                query = query.eq("tenant_id", tenant_id)
            response = query.order("created_at", desc=True).execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception:
            return pd.DataFrame()
    
    def get_messages(self, conversation_id: str) -> pd.DataFrame:
        """Get messages for a conversation"""
        if not self.is_connected:
            return pd.DataFrame()
            
        try:
            response = self.client.table("messages")\
                .select("*")\
                .eq("conversation_id", conversation_id)\
                .order("created_at")\
                .execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception:
            return pd.DataFrame()
    
    def log_message(self, data: Dict) -> bool:
        """Log a message"""
        if not self.is_connected:
            return False
            
        try:
            self.client.table("messages").insert(data).execute()
            return True
        except Exception:
            return False
    
    # ============================================
    # USAGE STATS
    # ============================================
    
    def get_usage_stats(self, tenant_id: Optional[str] = None, days: int = 30) -> pd.DataFrame:
        """Get usage statistics"""
        if not self.is_connected:
            return self._get_mock_usage_stats()
            
        try:
            from_date = (datetime.now() - pd.Timedelta(days=days)).strftime("%Y-%m-%d")
            
            query = self.client.table("usage_stats")\
                .select("*")\
                .gte("date", from_date)
            
            if tenant_id:
                query = query.eq("tenant_id", tenant_id)
            
            response = query.order("date").execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception:
            return self._get_mock_usage_stats()
    
    def increment_usage(self, tenant_id: str, chat_count: int = 0, image_count: int = 0) -> bool:
        """Increment usage stats for today"""
        if not self.is_connected:
            return False
            
        try:
            today = date.today().isoformat()
            
            # Try upsert
            self.client.rpc("increment_usage_stat", {
                "p_tenant_id": tenant_id,
                "p_date": today,
                "p_chat_count": chat_count,
                "p_message_count": 0,
                "p_image_count": image_count
            }).execute()
            return True
        except Exception:
            return False
    
    # ============================================
    # DASHBOARD STATS
    # ============================================
    
    def get_dashboard_stats(self) -> Dict:
        """Get aggregated dashboard statistics"""
        if not self.is_connected:
            return self._get_mock_dashboard_stats()
            
        try:
            # Get tenant counts
            tenants = self.get_tenants()
            total_tenants = len(tenants)
            active_tenants = len(tenants[tenants['status'] == 'active']) if not tenants.empty else 0
            
            # Get today's usage
            today = date.today().isoformat()
            usage_today = self.client.table("usage_stats")\
                .select("chat_count, image_count")\
                .eq("date", today)\
                .execute()
            
            chats_today = sum([u.get('chat_count', 0) for u in (usage_today.data or [])])
            images_today = sum([u.get('image_count', 0) for u in (usage_today.data or [])])
            
            # Get this month's usage
            month_start = date.today().replace(day=1).isoformat()
            usage_month = self.client.table("usage_stats")\
                .select("chat_count, image_count")\
                .gte("date", month_start)\
                .execute()
            
            chats_month = sum([u.get('chat_count', 0) for u in (usage_month.data or [])])
            
            # Calculate MRR
            mrr = tenants['plan_price'].sum() if 'plan_price' in tenants.columns else 0
            
            return {
                "total_tenants": total_tenants,
                "active_tenants": active_tenants,
                "chats_today": chats_today,
                "chats_month": chats_month,
                "images_today": images_today,
                "mrr": mrr
            }
            
        except Exception as e:
            st.warning(f"Using mock data: {e}")
            return self._get_mock_dashboard_stats()
    
    # ============================================
    # MOCK DATA (Fallback)
    # ============================================
    
    def _get_mock_tenants(self) -> pd.DataFrame:
        """Mock tenant data for development"""
        return pd.DataFrame([
            {"id": "1", "business_name": "SYACRI Wedding Organizer", "phone": "085280638938", "plan_name": "Professional", "status": "active", "email": "syacri@example.com"},
            {"id": "2", "business_name": "Elegant Dreams WO", "phone": "081234567890", "plan_name": "Starter", "status": "active", "email": "elegant@example.com"},
            {"id": "3", "business_name": "Royal Wedding Planner", "phone": "087654321098", "plan_name": "Business", "status": "active", "email": "royal@example.com"},
            {"id": "4", "business_name": "Bali Wedding Expert", "phone": "082345678901", "plan_name": "Professional", "status": "inactive", "email": "bali@example.com"},
            {"id": "5", "business_name": "Jakarta Wedding House", "phone": "089876543210", "plan_name": "Business", "status": "active", "email": "jakarta@example.com"},
        ])
    
    def _get_mock_plans(self) -> pd.DataFrame:
        """Mock plans data"""
        return pd.DataFrame([
            {"id": "1", "name": "Starter", "price_monthly": 299000, "chat_limit_monthly": 500, "image_limit_monthly": 0},
            {"id": "2", "name": "Professional", "price_monthly": 599000, "chat_limit_monthly": 2000, "image_limit_monthly": 50},
            {"id": "3", "name": "Business", "price_monthly": 999000, "chat_limit_monthly": None, "image_limit_monthly": 200},
        ])
    
    def _get_mock_usage_stats(self) -> pd.DataFrame:
        """Mock usage stats"""
        import random
        dates = pd.date_range(end=datetime.now(), periods=30)
        return pd.DataFrame({
            "date": dates,
            "chat_count": [random.randint(800, 1500) for _ in range(30)],
            "image_count": [random.randint(10, 50) for _ in range(30)]
        })
    
    def _get_mock_dashboard_stats(self) -> Dict:
        """Mock dashboard stats"""
        return {
            "total_tenants": 47,
            "active_tenants": 42,
            "chats_today": 1247,
            "chats_month": 28934,
            "images_today": 89,
            "mrr": 23850000
        }

# Singleton instance
supabase_client = SupabaseClient()
