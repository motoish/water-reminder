from slack_bolt import App
from pytz import timezone
from datetime import datetime
import os
import time
from threading import Thread
from flask import Flask

# Slack app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

reminder_message = "💧 Time to drink water! Stay hydrated!"

def send_reminder():
    jst = timezone('Asia/Tokyo')  # Define JST timezone

    while True:
        now = datetime.now(jst)
        day = now.weekday()  # 0: Monday, 6: Sunday
        hour = now.hour  # JST hour
        
        if day < 5 and 9 <= hour <= 17:  # Weekdays, between 9 AM and 5 PM
            try:
                slack_app.client.chat_postMessage(
                    channel=os.environ.get("SLACK_CHANNEL_ID"),
                    text=reminder_message,
                )
            except Exception as e:
                print(f"Error: {e}")
        time.sleep(3600)  # Wait for 1 hour

# Start the reminder thread
reminder_thread = Thread(target=send_reminder, daemon=True)
reminder_thread.start()

# Flask app for Render's port binding
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Slack bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)
