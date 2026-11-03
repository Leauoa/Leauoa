# GOLDEN MINES AI — starter project

This starter includes:
- Telegram bot (`bot.py`) with `/start` and `/signal 5`
- Web dashboard (`web.py`) with a 5×5 board
- 3–10 mine selection
- Five randomly selected suggested tiles

## Important limitation
The suggestions are random coordinates, not predictions. This project does not connect to 1win, inspect its private game state, or know where mines are. A fair/random game cannot be reliably predicted from previous rounds. Do not treat highlighted tiles as safe or guaranteed.

## Setup
Use Python 3.10 or newer.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the website
```bash
python web.py
```
Open http://127.0.0.1:5000

## Run the Telegram bot
1. Create a bot with Telegram's official @BotFather.
2. Copy its token privately; do not share it in chat or publish it.
3. Set the environment variable `TELEGRAM_BOT_TOKEN`.

Windows PowerShell:
```powershell
$env:TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
python bot.py
```

macOS/Linux:
```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
python bot.py
```

## About automatic signals
Automatic broadcast is not enabled in this starter. Before enabling it, add an explicit opt-in subscription, an adjustable interval, a stop command, and rate limits. Unsolicited signal spam is not enabled by default.


## Deploy online with Render
1. Upload this project to a private GitHub repository.
2. In Render, choose New > Blueprint and connect that repository.
3. Render reads `render.yaml` and proposes two services: a free web service and a paid background worker for Telegram.
4. When prompted, enter `TELEGRAM_BOT_TOKEN` as a secret environment variable for the worker. Never commit your token to GitHub.
5. Review costs and confirm before creating the worker. Render's free plan does not support background workers, so the Telegram bot worker is configured on a paid starter tier; the website may be hosted free with idle-sleep limitations.

Official Render docs:
- https://render.com/docs/infrastructure-as-code
- https://render.com/docs/free
