import datetime as dt
import os

from pytz import timezone
from slack_bolt import App

# Initialize the Slack app using environment variables
slack_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)

# Reminder message and channel ID
reminder_message = "💧 Time to drink water! Stay hydrated!"
channel_id = os.getenv("SLACK_CHANNEL_ID")


def send_reminder():
    """
    Sends a reminder message if the current time is during JST working hours (9 AM - 5 PM)
    on weekdays (Monday - Friday).
    """
    jst = dt.timezone(dt.timedelta(hours=+9), "JST")  # Define JST timezone
    now = dt.datetime.now(jst)
    hour = now.hour  # JST hour

    # Weekdays, between 9 AM and 5 PM JST
    if 9 <= hour <= 17:
        try:
            slack_app.client.chat_postMessage(
                channel=channel_id,
                text=reminder_message,
            )
            print(f"Reminder sent at {now.strftime('%Y-%m-%d %H:%M:%S')} JST")
        except Exception as e:
            print(f"Error sending message: {e}")
    else:
        print(f"Reminder should not sent at {now.strftime('%Y-%m-%d %H:%M:%S')} JST")


if __name__ == "__main__":
    # Call the reminder function (single execution for GitHub Actions workflow)
    send_reminder()
