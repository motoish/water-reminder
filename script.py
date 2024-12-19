import os
from slack_bolt import App
from datetime import datetime
from pytz import timezone

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
    jst = timezone("Asia/Tokyo")  # Define JST timezone
    now = datetime.now(jst)
    day = now.weekday()  # 0: Monday, 6: Sunday
    hour = now.hour  # JST hour

    if day < 5 and 9 <= hour <= 17:  # Weekdays, between 9 AM and 5 PM JST
        try:
            slack_app.client.chat_postMessage(
                channel=channel_id,
                text=reminder_message,
            )
            print(f"Reminder sent at {now.strftime('%Y-%m-%d %H:%M:%S')} JST")
        except Exception as e:
            print(f"Error sending message: {e}")


if __name__ == "__main__":
    # Call the reminder function (single execution for GitHub Actions workflow)
    send_reminder()
