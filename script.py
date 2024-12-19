from slack_bolt import App
from datetime import datetime
import time
import os

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

reminder_message = "💧 Time to drink water! Stay hydrated!"

def send_reminder():
    day = datetime.now().weekday()  # 0: Monday, 6: Sunday
    if day < 5:  # Weekdays
        try:
            app.client.chat_postMessage(
                channel=os.environ.get("SLACK_CHANNEL_ID"),
                text=reminder_message
            )
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        send_reminder()
        time.sleep(3600)  # Wait for 1 hour
