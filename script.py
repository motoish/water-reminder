from slack_bolt import App
from flask import Flask
import os
from threading import Thread

# Slack app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

reminder_message = "💧 Time to drink water! Stay hydrated!"

def send_reminder():
    from datetime import datetime
    import time

    while True:
        day = datetime.now().weekday()  # 0: Monday, 6: Sunday
        if day < 5:  # Weekdays
            try:
                slack_app.client.chat_postMessage(
                    channel=os.environ.get("SLACK_CHANNEL_ID"),
                    text=reminder_message,
                )
            except Exception as e:
                print(f"Error: {e}")
        time.sleep(3600)  # 1 hour

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
