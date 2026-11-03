import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from signal_engine import generate_signal

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Set TELEGRAM_BOT_TOKEN in your environment before starting the bot.")

INTERVAL_SECONDS = 30 * 60  # opted-in signals every 30 minutes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 GOLDEN MINES AI\n\n"
        "Commands:\n"
        "/signal 5 — generate one suggestion (3–10 mines)\n"
        "/auto 5 — opt in to suggestions every 30 minutes\n"
        "/stop — stop automatic suggestions\n\n"
        "Important: suggestions are random and cannot predict actual safe tiles."
    )

async def send_signal(chat_id: int, mines: int, context: ContextTypes.DEFAULT_TYPE):
    result = generate_signal(mines, 5)
    tiles = ", ".join(map(str, result["tiles"]))
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"✨ GOLDEN MINES AI — RANDOM SUGGESTION\n"
            f"💣 Mines: {mines}\n"
            f"⭐ Suggested tiles: {tiles}\n\n"
            "These are random suggestions, NOT verified safe tiles. "
            "The game may place a mine on any tile. No guarantee of winning."
        ),
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mines = int(context.args[0]) if context.args else 5
        if not 3 <= mines <= 10:
            raise ValueError
        await send_signal(update.effective_chat.id, mines, context)
    except (ValueError, IndexError):
        await update.message.reply_text("Usage: /signal 5  (choose 3–10 mines)")

async def auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mines = int(context.args[0]) if context.args else 5
        if not 3 <= mines <= 10:
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text("Usage: /auto 5  (choose 3–10 mines)")
        return

    chat_id = update.effective_chat.id
    job_name = f"auto_signal_{chat_id}"
    existing = context.job_queue.get_jobs_by_name(job_name)
    for job in existing:
        job.schedule_removal()

    context.job_queue.run_repeating(
        auto_job,
        interval=INTERVAL_SECONDS,
        first=INTERVAL_SECONDS,
        name=job_name,
        chat_id=chat_id,
        data={"mines": mines},
    )
    await update.message.reply_text(
        f"✅ Automatic suggestions enabled for this chat every 30 minutes with {mines} mines.\n"
        "Send /stop to turn them off. Suggestions are random, not predictions."
    )

async def auto_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await send_signal(job.chat_id, job.data["mines"], context)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job_name = f"auto_signal_{update.effective_chat.id}"
    jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in jobs:
        job.schedule_removal()
    if jobs:
        await update.message.reply_text("🛑 Automatic suggestions stopped.")
    else:
        await update.message.reply_text("No automatic suggestions are running. Use /auto 5 to opt in.")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("auto", auto))
    app.add_handler(CommandHandler("stop", stop))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
