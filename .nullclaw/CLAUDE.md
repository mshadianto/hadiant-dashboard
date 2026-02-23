# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the `.nullclaw` configuration directory for **nullclaw** (v0.1.0), a personal AI assistant. It contains two things: (1) a Telegram bot (`bot.py`) that runs as the "Moni" assistant with GitHub monitoring, and (2) workspace configuration files that define the agent's persona, rules, and memory.

## Running the Bot

```bash
python bot.py
```

Requires `gh` CLI authenticated and on PATH (used for GitHub API calls). Python dependencies: `python-telegram-bot`, `google-genai`, `groq`.

## Architecture

`bot.py` is the sole executable. It runs a Telegram bot with two functions:

1. **GitHub Monitor** — Polls `mshadianto/bayan_ai` and `mshadianto/labbaik-v7.1` every 30 minutes (08:00–22:00 WIB) via `gh api` subprocess calls. Tracks commits, PRs, issues, and workflow runs in SQLite (`workspace/memory.db`). Sends Telegram notifications on new activity.

2. **LLM Chat** — Responds to Telegram messages using a provider fallback chain. Default provider is Groq (model: `llama-3.3-70b-versatile`), fallback is Gemini (model: `gemini-2.0-flash`). The system prompt is embedded in `config.json` under `agents.defaults.system_prompt`. Conversation history is kept in-memory per chat (max 20 messages).

The bot is whitelisted to `allow_from` usernames in config. Commands: `/start`, `/status`, `/check`.

## Key Files

- `config.json` — All runtime config: API keys (Gemini, Groq, Anthropic), bot token, LLM model/provider settings, system prompt, autonomy limits, cost controls. **Sensitive — never commit plaintext keys.**
- `bot.py` — Telegram bot: GitHub monitoring + multi-provider LLM chat
- `workspace/` — Markdown files that define the nullclaw agent's behavior (persona, rules, identity). Editing these files changes how the agent behaves. `memory.db` inside workspace stores GitHub monitoring state.
- `daemon_state.json` — Tracks daemon component status (gateway, channels, scheduler)

## Configuration Notes

- Autonomy: `supervised`, `workspace_only: true`, max 50 actions/hour
- Memory: SQLite with auto-save, 30-day archive, 90-day purge, 90-day conversation retention
- Cost limits: $5/day, $50/month
- The `.gitignore` allowlists specific files — most of the home directory is ignored. `memory.db` and its WAL files are gitignored.
