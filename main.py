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
        from bot import get_bot
        
        bot = get_bot()
        json_data = await request.json()
        
        logger.info(f"Received update: {json_data}")
        
        update = telebot.types.Update.de_json(json_data)
        
        # Process the update directly instead of using process_new_updates
        if update.message:
            try:
                # Call your message handlers directly
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


@app.post("/api/test")
async def test():
    return {"message": "Test successful"}


@app.get("/api/data")
def get_sample_data():
    return {
        "data": [
            {"id": 1, "name": "Sample Item 1", "value": 100},
            {"id": 2, "name": "Sample Item 2", "value": 200},
            {"id": 3, "name": "Sample Item 3", "value": 300}
        ],
        "total": 3,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    return {
        "item": {
            "id": item_id,
            "name": "Sample Item " + str(item_id),
            "value": item_id * 100
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }


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