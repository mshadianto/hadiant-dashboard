# ✨ HADIANT - AI Wedding Platform

> Platform SaaS untuk Wedding Organizer Indonesia dengan AI Chatbot dan Image Generation

![HADIANT Dashboard](https://hadiant-dashboard-id.streamlit.app)

---

## 🚀 Quick Links

- **Live Dashboard**: https://hadiant-dashboard-id.streamlit.app
- **Supabase Project**: https://supabase.com/dashboard/project/edcmmwadqnpwybflmgtx
- **Landing Page**: Deploy ke Vercel/Netlify

---

## 📁 Project Structure

```
hadiant-project/
├── app.py                          # Main Streamlit app entry point
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml.example        # Secrets template
├── src/
│   ├── __init__.py
│   ├── config.py                   # Configuration & settings
│   ├── database.py                 # Supabase client & operations
│   ├── components/
│   │   ├── __init__.py
│   │   └── sidebar.py              # Sidebar component
│   └── pages/
│       ├── __init__.py
│       ├── dashboard.py            # Dashboard page
│       ├── tenants.py              # Tenants management
│       ├── analytics.py            # Analytics & reporting
│       └── settings_page.py        # Settings & configuration
├── n8n/
│   └── hadiant-multi-tenant-workflow.json    # n8n workflow
└── landing-page/
    └── index.html                  # Marketing landing page
```

---

## 🛠️ Tech Stack

| Component | Technology | Cost |
|-----------|------------|------|
| Dashboard | Streamlit | FREE |
| Database | Supabase (PostgreSQL) | FREE (500MB) |
| Auth | Supabase Auth | FREE (50K MAU) |
| AI Chat | GROQ (LLaMA 3.3 70B) | FREE (14,400 req/day) |
| Image Gen | Stability AI | FREE (25 credits) |
| WhatsApp | WAHA (self-hosted) | FREE |
| Workflow | n8n (self-hosted) | FREE |
| Landing | Vercel/Netlify | FREE |

**Total Monthly Cost: Rp 0** (for MVP/testing)

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/mshadianto/hadiant-platform.git
cd hadiant-platform
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Secrets

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
[supabase]
url = "https://edcmmwadqnpwybflmgtx.supabase.co"
key = "your-anon-key"
service_key = "your-service-role-key"

[groq]
api_key = "gsk_xxx"

[stability]
api_key = "sk-xxx"

[waha]
url = "https://your-waha-instance.com"
api_key = "your-api-key"
```

### 4. Run Locally

```bash
streamlit run app.py
```

---

## 🗄️ Database Setup

### Supabase Tables

Database sudah di-setup dengan tables:
- `users` - Admin users
- `plans` - Subscription plans
- `tenants` - WO clients
- `conversations` - Chat sessions
- `messages` - Chat messages
- `image_generations` - Generated images log
- `usage_stats` - Daily usage metrics
- `invoices` - Billing records

### Views
- `v_dashboard_summary` - Aggregated dashboard stats
- `v_tenant_details` - Tenant with plan info

---

## 🔄 n8n Workflow Setup

### 1. Import Workflow

1. Buka n8n instance
2. Import `n8n/hadiant-multi-tenant-workflow.json`
3. Update credentials:
   - GROQ API Key
   - Stability AI Key
   - WAHA API Key
   - Supabase API Key

### 2. Configure Webhook

Set WAHA webhook ke:
```
https://your-n8n.com/webhook/hadiant-webhook
```

### 3. Workflow Features

- **Multi-tenant**: 1 workflow untuk semua WO
- **Auto-routing**: Identifikasi tenant dari session name
- **Dynamic AI**: System prompt per-tenant
- **Image generation**: Berdasarkan plan
- **Usage logging**: Track ke Supabase

---

## 💰 Pricing Tiers

| Plan | Price | Chats | Images | WhatsApp |
|------|-------|-------|--------|----------|
| Starter | Rp 299K/mo | 500 | 0 | 1 |
| Professional | Rp 599K/mo | 2,000 | 50 | 1 |
| Business | Rp 999K/mo | Unlimited | 200 | 3 |
| Enterprise | Custom | Unlimited | Unlimited | 10 |

---

## 🚀 Deployment

### Streamlit Cloud (Dashboard)

1. Push ke GitHub
2. Go to https://streamlit.io/cloud
3. Connect repo
4. Set secrets di Settings
5. Deploy!

### Vercel (Landing Page)

1. Go to https://vercel.com
2. Import `landing-page/` folder
3. Deploy!

### Cloudflare Pages (Alternative)

1. Go to https://pages.cloudflare.com
2. Connect GitHub
3. Build command: (none)
4. Output directory: `landing-page`

---

## 📊 Revenue Projections

| Tenants | Avg Plan | MRR | ARR |
|---------|----------|-----|-----|
| 10 | Mixed | ~Rp 5Jt | ~Rp 60Jt |
| 50 | Mixed | ~Rp 25Jt | ~Rp 300Jt |
| 100 | Mixed | ~Rp 50Jt | ~Rp 600Jt |
| 200 | Mixed | ~Rp 100Jt | ~Rp 1.2M |

---

## 🎯 Roadmap

### Phase 1: MVP ✅
- [x] AI Chatbot
- [x] Image Generation
- [x] Admin Dashboard
- [x] Multi-tenant Workflow
- [x] Supabase Integration
- [x] Landing Page

### Phase 2: Growth
- [ ] Tenant Self-Service Dashboard
- [ ] Payment Integration (Xendit)
- [ ] RAG Knowledge Base per-Tenant
- [ ] Voice Message Support
- [ ] CRM Integration

### Phase 3: Scale
- [ ] White-label Option
- [ ] API Access for Enterprise
- [ ] Mobile App
- [ ] Multi-language Support
- [ ] Advanced Analytics

---

## 👨‍💻 Development

### Adding New Features

1. Create new page in `src/pages/`
2. Register in `src/pages/__init__.py`
3. Add route in `app.py`

### Database Migrations

1. Write SQL in Supabase SQL Editor
2. Test in development
3. Apply to production

### Testing

```bash
# Run locally
streamlit run app.py

# Check Supabase connection
python -c "from src.database import supabase_client; print(supabase_client.is_connected)"
```

---

## 🔐 Security

- [ ] Enable Row Level Security (RLS) on all tables
- [ ] Use service_role key only on server-side
- [ ] Never expose API keys in frontend
- [ ] Enable 2FA for admin accounts
- [ ] Regular security audits

---

## 📞 Support

**Created by MS Hadianto**

- GitHub: [@mshadianto](https://github.com/mshadianto)
- Instagram: [@mshadianto](https://instagram.com/mshadianto)
- LinkedIn: [MS Hadianto](https://linkedin.com/in/mshadianto)
- Email: mshadianto@gmail.com

---

## 📄 License

MIT License - Free for commercial use

---

**© 2025 HADIANT - Illuminate Your Wedding Business** ✨
