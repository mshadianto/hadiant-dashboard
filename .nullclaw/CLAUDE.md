# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the `.nullclaw` configuration directory for **nullclaw**, a personal AI assistant framework (v0.1.0). It is not a traditional source code project — it contains workspace configuration files, persona definitions, and a SQLite memory store that together define an AI agent's behavior, identity, and runtime settings.

## Repository Structure

- `config.json` — Runtime configuration: LLM provider settings, autonomy level, memory backend, gateway/channel config, tool limits, cost controls
- `daemon_state.json` — Tracks running daemon components (gateway, channels, scheduler)
- `workspace/` — Agent workspace containing:
  - `IDENTITY.md` — Agent name and version
  - `PERSONA.md`, `SOUL.md` — Personality and communication style
  - `RULES.md` — Behavioral constraints
  - `AGENTS.md`, `TOOLS.md` — Guidelines for tool use and agent behavior
  - `USER.md`, `MEMORY.md` — User profile and persistent memory
  - `BOOTSTRAP.md` — Startup instructions
  - `HEARTBEAT.md` — Periodic task definitions
  - `memory.db` — SQLite database for conversation/memory persistence

## Architecture

nullclaw runs as a daemon with three components (see `daemon_state.json`):
1. **Gateway** — HTTP API on `127.0.0.1:3000` (configurable), requires pairing
2. **Channels** — External messaging integrations (currently Telegram)
3. **Scheduler** — Periodic task execution (tied to `HEARTBEAT.md`)

The agent uses OpenRouter as its LLM provider (model: `openai/gpt-4o-mini`) with supervised autonomy mode (max 20 actions/hour, workspace-only file access).

Memory uses SQLite with auto-save, 7-day archive, and 30-day purge cycles.

## Key Configuration Notes

- Autonomy is set to `supervised` with `workspace_only: true` — the agent should only modify files within the `workspace/` directory
- The workspace markdown files are the agent's "prompt engineering" — editing them changes how the nullclaw agent behaves
- `config.json` contains API keys and bot tokens — treat as sensitive
