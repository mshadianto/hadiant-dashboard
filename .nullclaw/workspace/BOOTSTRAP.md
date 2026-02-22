# Bootstrap

Startup instructions executed when the agent initializes.

## On Start
- Load workspace context
- Check for pending tasks
- Start GitHub repo monitor (see HEARTBEAT.md)
  - Fetch latest events from `mshadianto/bayan_ai` and `mshadianto/labbaik-v7.1`
  - Compare with last known state in memory
  - Send Telegram notification if new activity detected
