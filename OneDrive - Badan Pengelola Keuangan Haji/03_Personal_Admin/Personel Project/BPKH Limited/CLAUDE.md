# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **React-based interactive specification/blueprint** for BPKH Limited's Enterprise AI Solution - a RAG (Retrieval-Augmented Generation) Agentic AI platform designed for hajj/umrah travel services operations in Saudi Arabia. The project is a comprehensive design document presented as an interactive React dashboard, not a production application.

## Key Files

- `bpkh-limited-rag-solution.jsx` - Main React component (1,077 lines) containing the complete solution design with 6 modules
- `Transformasi_Digital_BPKH-Limited.html` - Training curriculum for implementation

## Architecture

The solution design specifies a multi-agent RAG architecture:

```
Data Sources (ERP, CRM, HRIS, Documents)
    ↓
RAG Core Engine (Vector Store, Document Processor, Hybrid Search)
    ↓
Agentic AI Layer (Orchestrator + Specialized Agents)
    ↓
Output Interfaces (WhatsApp Bot, Dashboard, Web Portal, Mobile App, API)
```

**Six Main Modules:**
1. Executive Overview - Project summary and high-level architecture
2. Bilingual Customer Service - Arabic-Indonesian WhatsApp bot with multi-agent architecture
3. Corporate Planning - Budget dashboard with real-time IDR-SAR conversion
4. Performance Monitoring - Multi-dimensional KPI framework
5. Document Intelligence - Bilingual OCR processing (Arabic-Indonesian)
6. Implementation Roadmap - 6-month phased deployment plan

## Technology Stack (Specified in Design)

- **LLM**: Groq API (Llama 3.3 70B) - free tier
- **Vector DB**: Supabase pgvector (500MB free)
- **Compute**: Cloudflare Workers (100K req/day free)
- **Orchestration**: n8n self-hosted
- **Messaging**: Meta WABA/Twilio for WhatsApp
- **UI Framework**: React 18+ with Tailwind CSS

## Domain Context

**BPKH Limited** operates hajj/umrah travel services in Saudi Arabia with four business lines:
- Hotel accommodations (Mecca & Medina)
- Bus transportation
- High-speed train tickets (Haramain Railway)
- Catering & restaurants

**Key requirements:**
- Bilingual support (Arabic + Indonesian)
- Real-time SAR-IDR currency conversion
- Arabic document OCR processing
- Performance monitoring of hajj operations

## Development Notes

This repository contains a specification document rather than runnable code. The main JSX component uses:
- Functional components with useState/useEffect hooks
- Tailwind CSS utility classes for styling
- SVG-based architecture diagrams
- Color-coded module navigation (teal/emerald, indigo, amber, red, emerald, purple)

To implement the actual solution from this blueprint, reference the architecture diagrams and technical specifications within each module section.
