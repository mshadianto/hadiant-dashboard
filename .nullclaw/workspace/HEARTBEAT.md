# Heartbeat

Periodic tasks and reminders. Add items below to be checked regularly.

## GitHub Repository Monitor

Monitor the following repositories for all activity and send updates via Telegram to @mshadianto.

### Repositories

| Repo | Branch | Owner |
|------|--------|-------|
| `mshadianto/bayan_ai` | main | mshadianto |
| `mshadianto/labbaik-v7.1` | main | mshadianto |

### What to Monitor

#### Commits & PRs
- New commits pushed to `main`
- Pull requests opened, merged, or closed
- Branch created or deleted

#### Issues & Discussions
- New issues opened
- Issue comments and status changes (closed/reopened)
- New discussions or replies

#### CI/CD & Health
- GitHub Actions workflow runs (success/failure)
- Build failures or errors
- Release tags published

### Schedule
- **Frequency**: Every 30 minutes during active hours (08:00–22:00 WIB / UTC+7)
- **Method**: Use `gh` CLI to fetch recent events
- **Notification**: Send summary to Telegram via nullclaw channel

### Check Commands
```bash
# Recent commits
gh api repos/mshadianto/bayan_ai/commits?per_page=5
gh api repos/mshadianto/labbaik-v7.1/commits?per_page=5

# Open PRs
gh pr list --repo mshadianto/bayan_ai --state open
gh pr list --repo mshadianto/labbaik-v7.1 --state open

# Recent issues
gh issue list --repo mshadianto/bayan_ai --state all --limit 5
gh issue list --repo mshadianto/labbaik-v7.1 --state all --limit 5

# Workflow runs
gh run list --repo mshadianto/bayan_ai --limit 5
gh run list --repo mshadianto/labbaik-v7.1 --limit 5

# Repo events (catches everything)
gh api repos/mshadianto/bayan_ai/events?per_page=10
gh api repos/mshadianto/labbaik-v7.1/events?per_page=10
```

### Notification Format
```
🔔 [repo_name] — [event_type]
[summary of what happened]
[link to commit/PR/issue]
```
