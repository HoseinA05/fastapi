from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import logging

app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/api/telegram_webhook")
async def telegram_webhook(request: Request):
    try:
        import telebot
        from bot.bot import get_bot

        bot = get_bot()
        json_data = await request.json()

        logger.info(f"Received update: {json_data}")

        update = telebot.types.Update.de_json(json_data)

        # Process ALL types of updates (messages, callback queries, etc.)
        try:
            bot.process_new_updates([update])
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            # Still return 200 to Telegram to acknowledge receipt
            return JSONResponse(content={"ok": True}, status_code=200)

        return JSONResponse(content={"ok": True}, status_code=200)

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        # Return 200 even on error to prevent Telegram from retrying
        return JSONResponse(content={"ok": True}, status_code=200)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """<!DOCTYPE html>
    <html>
    <head><title>Vercel + FastAPI</title></head>
    <body><h1>Vercel + FastAPI</h1></body>
    </html>"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
