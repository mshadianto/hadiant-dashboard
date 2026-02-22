"""
Moni — nullclaw Telegram Bot
GitHub repo monitor + multi-provider LLM chat assistant.
Run: python bot.py
"""

import json
import sqlite3
import asyncio
import shutil
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import google.generativeai as genai
from groq import AsyncGroq

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
DB_PATH = BASE_DIR / "workspace" / "memory.db"

with open(CONFIG_PATH, "r", encoding="utf-8") as _f:
    cfg = json.load(_f)

BOT_TOKEN = cfg["channels"]["telegram"]["accounts"]["main"]["bot_token"]
ALLOWED_USERS = set(cfg["channels"]["telegram"]["accounts"]["main"]["allow_from"])
DEFAULT_PROVIDER = cfg.get("default_provider", "groq")
MODEL_PRIMARY = cfg["agents"]["defaults"]["model"]["primary"]
MODEL_FALLBACK = cfg["agents"]["defaults"]["model"]["fallback"]
SYSTEM_PROMPT = cfg["agents"]["defaults"]["system_prompt"]
TEMPERATURE = cfg.get("default_temperature", 0.7)

# Provider clients
GEMINI_API_KEY = cfg["models"]["providers"].get("gemini", {}).get("api_key")
GROQ_API_KEY = cfg["models"]["providers"].get("groq", {}).get("api_key")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

groq_client = AsyncGroq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

REPOS = ["mshadianto/bayan_ai", "mshadianto/labbaik-v7.1"]
CHECK_INTERVAL_SECONDS = 1800  # 30 minutes
ACTIVE_HOUR_START = 8
ACTIVE_HOUR_END = 22
WIB = timezone(timedelta(hours=7))

conversations: dict[int, list[dict]] = {}
MAX_HISTORY = 20

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------


class Database:
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        stmts = [
            """CREATE TABLE IF NOT EXISTS kv (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS gh_commits (
                repo    TEXT NOT NULL,
                sha     TEXT NOT NULL,
                message TEXT,
                author  TEXT,
                date    TEXT,
                PRIMARY KEY (repo, sha)
            )""",
            """CREATE TABLE IF NOT EXISTS gh_pulls (
                repo       TEXT NOT NULL,
                number     INTEGER NOT NULL,
                title      TEXT,
                state      TEXT,
                merged     INTEGER DEFAULT 0,
                updated_at TEXT,
                PRIMARY KEY (repo, number)
            )""",
            """CREATE TABLE IF NOT EXISTS gh_issues (
                repo       TEXT NOT NULL,
                number     INTEGER NOT NULL,
                title      TEXT,
                state      TEXT,
                updated_at TEXT,
                PRIMARY KEY (repo, number)
            )""",
            """CREATE TABLE IF NOT EXISTS gh_runs (
                repo       TEXT NOT NULL,
                run_id     INTEGER NOT NULL,
                name       TEXT,
                status     TEXT,
                conclusion TEXT,
                html_url   TEXT,
                PRIMARY KEY (repo, run_id)
            )""",
        ]
        for s in stmts:
            self.conn.execute(s)
        self.conn.commit()

    # -- kv helpers --

    def get_kv(self, key: str) -> str | None:
        row = self.conn.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
        return row["value"] if row else None

    def set_kv(self, key: str, value: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)", (key, value)
        )
        self.conn.commit()

    # -- commits --

    def get_known_shas(self, repo: str) -> set[str]:
        rows = self.conn.execute(
            "SELECT sha FROM gh_commits WHERE repo=?", (repo,)
        ).fetchall()
        return {r["sha"] for r in rows}

    def insert_commit(self, repo, sha, message, author, date):
        self.conn.execute(
            "INSERT OR IGNORE INTO gh_commits (repo,sha,message,author,date) VALUES (?,?,?,?,?)",
            (repo, sha, message, author, date),
        )
        self.conn.commit()

    # -- pulls --

    def get_known_prs(self, repo: str) -> dict[int, dict]:
        rows = self.conn.execute(
            "SELECT number, state, merged FROM gh_pulls WHERE repo=?", (repo,)
        ).fetchall()
        return {r["number"]: {"state": r["state"], "merged": r["merged"]} for r in rows}

    def upsert_pr(self, repo, number, title, state, merged, updated_at):
        self.conn.execute(
            """INSERT INTO gh_pulls (repo,number,title,state,merged,updated_at)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(repo,number) DO UPDATE SET
                 title=excluded.title, state=excluded.state,
                 merged=excluded.merged, updated_at=excluded.updated_at""",
            (repo, number, title, state, merged, updated_at),
        )
        self.conn.commit()

    # -- issues --

    def get_known_issues(self, repo: str) -> dict[int, dict]:
        rows = self.conn.execute(
            "SELECT number, state FROM gh_issues WHERE repo=?", (repo,)
        ).fetchall()
        return {r["number"]: {"state": r["state"]} for r in rows}

    def upsert_issue(self, repo, number, title, state, updated_at):
        self.conn.execute(
            """INSERT INTO gh_issues (repo,number,title,state,updated_at)
               VALUES (?,?,?,?,?)
               ON CONFLICT(repo,number) DO UPDATE SET
                 title=excluded.title, state=excluded.state,
                 updated_at=excluded.updated_at""",
            (repo, number, title, state, updated_at),
        )
        self.conn.commit()

    # -- workflow runs --

    def get_known_runs(self, repo: str) -> dict[int, dict]:
        rows = self.conn.execute(
            "SELECT run_id, status, conclusion FROM gh_runs WHERE repo=?", (repo,)
        ).fetchall()
        return {
            r["run_id"]: {"status": r["status"], "conclusion": r["conclusion"]}
            for r in rows
        }

    def upsert_run(self, repo, run_id, name, status, conclusion, html_url):
        self.conn.execute(
            """INSERT INTO gh_runs (repo,run_id,name,status,conclusion,html_url)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(repo,run_id) DO UPDATE SET
                 status=excluded.status, conclusion=excluded.conclusion""",
            (repo, run_id, name, status, conclusion, html_url),
        )
        self.conn.commit()


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------


async def gh_api(endpoint: str, jq_filter: str = ".") -> list | dict:
    proc = await asyncio.create_subprocess_exec(
        "gh", "api", endpoint, "--jq", jq_filter,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        logging.error("gh api %s failed: %s", endpoint, stderr.decode().strip())
        return []
    text = stdout.decode().strip()
    if not text:
        return []
    return json.loads(text)


async def check_commits(db: Database, repo: str) -> list[str]:
    data = await gh_api(
        f"repos/{repo}/commits?per_page=10",
        '[.[] | {sha: .sha, msg: .commit.message, author: .commit.author.name, date: .commit.author.date}]',
    )
    known = db.get_known_shas(repo)
    first_run = len(known) == 0
    notes = []
    for c in data:
        if c["sha"] not in known:
            db.insert_commit(repo, c["sha"], c["msg"], c["author"], c["date"])
            if not first_run:
                short = c["sha"][:7]
                line = c["msg"].split("\n")[0][:80]
                notes.append(
                    f"\U0001f4e6 *Commit baru* di `{repo}`\n"
                    f"`{short}` — {line}\n"
                    f"oleh {c['author']}\n"
                    f"https://github.com/{repo}/commit/{c['sha']}"
                )
    return notes


async def check_pulls(db: Database, repo: str) -> list[str]:
    data = await gh_api(
        f"repos/{repo}/pulls?state=all&per_page=10&sort=updated&direction=desc",
        '[.[] | {number: .number, title: .title, state: .state, merged_at: .merged_at, updated_at: .updated_at, url: .html_url}]',
    )
    known = db.get_known_prs(repo)
    first_run = len(known) == 0
    notes = []
    for pr in data:
        num = pr["number"]
        merged = 1 if pr.get("merged_at") else 0
        prev = known.get(num)
        if prev is None and not first_run:
            label = "merged" if merged else pr["state"]
            notes.append(
                f"\U0001f500 *PR #{num}* [{label}] di `{repo}`\n"
                f"{pr['title']}\n{pr.get('url', '')}"
            )
        elif prev and (prev["state"] != pr["state"] or prev["merged"] != merged):
            if merged and not prev["merged"]:
                action = "merged \u2705"
            elif pr["state"] == "closed":
                action = "closed \u274c"
            else:
                action = "reopened \U0001f504"
            notes.append(
                f"\U0001f500 *PR #{num}* {action} di `{repo}`\n"
                f"{pr['title']}\n{pr.get('url', '')}"
            )
        db.upsert_pr(repo, num, pr["title"], pr["state"], merged, pr["updated_at"])
    return notes


async def check_issues(db: Database, repo: str) -> list[str]:
    data = await gh_api(
        f"repos/{repo}/issues?state=all&per_page=10&sort=updated&direction=desc",
        '[.[] | select(.pull_request == null) | {number: .number, title: .title, state: .state, updated_at: .updated_at, url: .html_url}]',
    )
    known = db.get_known_issues(repo)
    first_run = len(known) == 0
    notes = []
    for iss in data:
        num = iss["number"]
        prev = known.get(num)
        if prev is None and not first_run:
            notes.append(
                f"\U0001f4cb *Issue #{num}* [{iss['state']}] di `{repo}`\n"
                f"{iss['title']}\n{iss.get('url', '')}"
            )
        elif prev and prev["state"] != iss["state"]:
            action = "closed \u2705" if iss["state"] == "closed" else "reopened \U0001f504"
            notes.append(
                f"\U0001f4cb *Issue #{num}* {action} di `{repo}`\n"
                f"{iss['title']}\n{iss.get('url', '')}"
            )
        db.upsert_issue(repo, num, iss["title"], iss["state"], iss["updated_at"])
    return notes


async def check_runs(db: Database, repo: str) -> list[str]:
    data = await gh_api(
        f"repos/{repo}/actions/runs?per_page=10",
        '[.workflow_runs[]? | {id: .id, name: .name, status: .status, conclusion: .conclusion, url: .html_url}]',
    )
    known = db.get_known_runs(repo)
    first_run = len(known) == 0
    notes = []
    for run in data:
        rid = run["id"]
        prev = known.get(rid)
        if prev is None:
            db.upsert_run(repo, rid, run["name"], run["status"], run["conclusion"], run["url"])
            if not first_run and run["conclusion"]:
                emoji = "\u2705" if run["conclusion"] == "success" else "\u274c"
                notes.append(
                    f"{emoji} *Workflow* `{run['name']}` {run['conclusion']} di `{repo}`\n"
                    f"{run['url']}"
                )
        elif prev["conclusion"] != run["conclusion"] and run["conclusion"]:
            emoji = "\u2705" if run["conclusion"] == "success" else "\u274c"
            notes.append(
                f"{emoji} *Workflow* `{run['name']}` {run['conclusion']} di `{repo}`\n"
                f"{run['url']}"
            )
            db.upsert_run(repo, rid, run["name"], run["status"], run["conclusion"], run["url"])
    return notes


async def check_all_repos(db: Database) -> list[str]:
    all_notes = []
    for repo in REPOS:
        for fn in [check_commits, check_pulls, check_issues, check_runs]:
            try:
                all_notes.extend(await fn(db, repo))
            except Exception as e:
                logging.error("Error in %s for %s: %s", fn.__name__, repo, e)
    return all_notes


# ---------------------------------------------------------------------------
# Active hours
# ---------------------------------------------------------------------------


def is_active_hours() -> bool:
    now = datetime.now(WIB)
    return ACTIVE_HOUR_START <= now.hour < ACTIVE_HOUR_END


# ---------------------------------------------------------------------------
# Whitelist
# ---------------------------------------------------------------------------


def is_allowed(update: Update) -> bool:
    user = update.effective_user
    return user is not None and user.username in ALLOWED_USERS


# ---------------------------------------------------------------------------
# Scheduled job
# ---------------------------------------------------------------------------


async def scheduled_check(context: ContextTypes.DEFAULT_TYPE):
    if not is_active_hours():
        return
    db: Database = context.bot_data["db"]
    chat_id = db.get_kv("telegram_chat_id")
    if not chat_id:
        return

    notes = await check_all_repos(db)
    if not notes:
        return

    header = "\U0001f514 *GitHub Monitor Update*\n" + "=" * 30 + "\n\n"
    msg = header
    for note in notes:
        if len(msg) + len(note) + 3 > 4000:
            await context.bot.send_message(
                chat_id=int(chat_id), text=msg, parse_mode="Markdown"
            )
            msg = ""
        msg += note + "\n\n"
    if msg.strip():
        await context.bot.send_message(
            chat_id=int(chat_id), text=msg, parse_mode="Markdown"
        )

    db.set_kv("last_check_time", datetime.now(WIB).isoformat())


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    db: Database = context.bot_data["db"]
    db.set_kv("telegram_chat_id", str(update.effective_chat.id))
    await update.message.reply_text(
        "Halo! Saya *Moni*, asisten AI pribadi MS \U0001f44b\n\n"
        "*Perintah:*\n"
        "/start — Mulai & daftarkan chat untuk notifikasi\n"
        "/status — Status terakhir repo GitHub\n"
        "/check — Paksa cek repo sekarang\n\n"
        "Atau kirim pesan biasa untuk ngobrol \U0001f4ac",
        parse_mode="Markdown",
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    db: Database = context.bot_data["db"]
    last_check = db.get_kv("last_check_time") or "Belum pernah"
    lines = [f"*Status Monitor GitHub*\nTerakhir dicek: {last_check}\n"]
    for repo in REPOS:
        row = db.conn.execute(
            "SELECT sha, message, date FROM gh_commits WHERE repo=? ORDER BY date DESC LIMIT 1",
            (repo,),
        ).fetchone()
        if row:
            lines.append(
                f"\n*{repo}*\n"
                f"Commit: `{row['sha'][:7]}` — {row['message'].split(chr(10))[0][:60]}\n"
                f"Tanggal: {row['date']}"
            )
        else:
            lines.append(f"\n*{repo}*\nBelum ada data.")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    db: Database = context.bot_data["db"]
    await update.message.reply_text("Mengecek repo... \u23F3")
    notes = await check_all_repos(db)
    if notes:
        for note in notes:
            await update.message.reply_text(
                f"\U0001f514 {note}", parse_mode="Markdown"
            )
    else:
        await update.message.reply_text("Tidak ada aktivitas baru. \u2705")
    db.set_kv("last_check_time", datetime.now(WIB).isoformat())


# ---------------------------------------------------------------------------
# LLM chat handler
# ---------------------------------------------------------------------------


async def _chat_gemini(messages: list[dict], model: str) -> str | None:
    """Call Gemini API. Converts openai-style messages to Gemini format."""
    gemini_history = []
    for m in messages:
        if m["role"] == "system":
            continue  # system prompt passed via system_instruction
        role = "user" if m["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [m["content"]]})

    gm = genai.GenerativeModel(
        model_name=model,
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.GenerationConfig(
            temperature=TEMPERATURE,
            max_output_tokens=1024,
        ),
    )
    resp = await asyncio.to_thread(
        lambda: gm.generate_content(gemini_history)
    )
    return resp.text


async def _chat_groq(messages: list[dict], model: str) -> str | None:
    """Call Groq API."""
    if not groq_client:
        return None
    resp = await groq_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=1024,
    )
    return resp.choices[0].message.content


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_text = update.message.text

    if chat_id not in conversations:
        conversations[chat_id] = []
    conversations[chat_id].append({"role": "user", "content": user_text})
    if len(conversations[chat_id]) > MAX_HISTORY:
        conversations[chat_id] = conversations[chat_id][-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversations[chat_id]

    # Build provider chain: primary model first, then fallback
    attempts = []
    if DEFAULT_PROVIDER == "gemini":
        attempts.append(("gemini", MODEL_PRIMARY, _chat_gemini))
        attempts.append(("groq", MODEL_FALLBACK, _chat_groq))
    else:
        attempts.append(("groq", MODEL_PRIMARY, _chat_groq))
        attempts.append(("gemini", MODEL_FALLBACK, _chat_gemini))

    reply = None
    for provider, model, chat_fn in attempts:
        try:
            reply = await chat_fn(messages, model)
            if reply:
                break
        except Exception as e:
            logging.error("%s %s error: %s", provider, model, e)

    if not reply:
        reply = "Maaf, saya sedang mengalami gangguan. Coba lagi nanti ya."

    conversations[chat_id].append({"role": "assistant", "content": reply})

    if len(reply) > 4000:
        for i in range(0, len(reply), 4000):
            await update.message.reply_text(reply[i : i + 4000])
    else:
        await update.message.reply_text(reply)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    if not shutil.which("gh"):
        logging.fatal("gh CLI not found on PATH. Install: https://cli.github.com/")
        return

    db = Database(DB_PATH)
    app = Application.builder().token(BOT_TOKEN).build()
    app.bot_data["db"] = db

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("check", cmd_check))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.job_queue.run_repeating(
        callback=scheduled_check,
        interval=CHECK_INTERVAL_SECONDS,
        first=10,
        name="github_monitor",
    )

    logging.info("Moni bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
