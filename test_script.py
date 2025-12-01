import os
from unittest.mock import Mock, patch, MagicMock

import pytest

# Import the module to test
import script


class TestSendReminder:
    """Test cases for send_reminder function"""

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_CHANNEL_ID": "test-channel",
        },
    )
    @patch("script.slack_app")
    @patch("script.dt.datetime")
    def test_send_reminder_during_working_hours(self, mock_datetime, mock_slack_app):
        """Test that reminder is sent during working hours (9 AM - 5 PM JST)"""
        # Mock datetime.now to return a time during working hours (e.g., 10 AM JST)
        mock_now = Mock()
        mock_now.hour = 10
        mock_now.strftime = Mock(return_value="2024-01-15 10:00:00")
        # Mock datetime.now to accept timezone parameter and return mock_now
        mock_datetime.now = Mock(return_value=mock_now)
        # Keep timezone and timedelta available
        mock_datetime.timezone = script.dt.timezone
        mock_datetime.timedelta = script.dt.timedelta

        # Mock Slack client
        mock_client = MagicMock()
        mock_slack_app.client = mock_client

        # Call the function
        script.send_reminder()

        # Verify that chat_postMessage was called
        mock_client.chat_postMessage.assert_called_once_with(
            channel="test-channel",
            text="💧 Time to drink water! Stay hydrated!",
        )

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_CHANNEL_ID": "test-channel",
        },
    )
    @patch("script.slack_app")
    @patch("script.dt.datetime")
    def test_send_reminder_before_working_hours(self, mock_datetime, mock_slack_app):
        """Test that reminder is NOT sent before working hours (before 9 AM JST)"""
        # Mock datetime.now to return a time before working hours (e.g., 8 AM JST)
        mock_now = Mock()
        mock_now.hour = 8
        mock_now.strftime = Mock(return_value="2024-01-15 08:00:00")
        mock_datetime.now = Mock(return_value=mock_now)
        mock_datetime.timezone = script.dt.timezone
        mock_datetime.timedelta = script.dt.timedelta

        # Mock Slack client
        mock_client = MagicMock()
        mock_slack_app.client = mock_client

        # Call the function
        script.send_reminder()

        # Verify that chat_postMessage was NOT called
        mock_client.chat_postMessage.assert_not_called()

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_CHANNEL_ID": "test-channel",
        },
    )
    @patch("script.slack_app")
    @patch("script.dt.datetime")
    def test_send_reminder_after_working_hours(self, mock_datetime, mock_slack_app):
        """Test that reminder is NOT sent after working hours (after 5 PM JST)"""
        # Mock datetime.now to return a time after working hours (e.g., 6 PM JST)
        mock_now = Mock()
        mock_now.hour = 18
        mock_now.strftime = Mock(return_value="2024-01-15 18:00:00")
        mock_datetime.now = Mock(return_value=mock_now)
        mock_datetime.timezone = script.dt.timezone
        mock_datetime.timedelta = script.dt.timedelta

        # Mock Slack client
        mock_client = MagicMock()
        mock_slack_app.client = mock_client

        # Call the function
        script.send_reminder()

        # Verify that chat_postMessage was NOT called
        mock_client.chat_postMessage.assert_not_called()

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_CHANNEL_ID": "test-channel",
        },
    )
    @patch("script.slack_app")
    @patch("script.dt.datetime")
    def test_send_reminder_at_9am_boundary(self, mock_datetime, mock_slack_app):
        """Test that reminder is sent at 9 AM JST (boundary case)"""
        # Mock datetime.now to return 9 AM JST
        mock_now = Mock()
        mock_now.hour = 9
        mock_now.strftime = Mock(return_value="2024-01-15 09:00:00")
        mock_datetime.now = Mock(return_value=mock_now)
        mock_datetime.timezone = script.dt.timezone
        mock_datetime.timedelta = script.dt.timedelta

        # Mock Slack client
        mock_client = MagicMock()
        mock_slack_app.client = mock_client

        # Call the function
        script.send_reminder()

        # Verify that chat_postMessage was called
        mock_client.chat_postMessage.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_CHANNEL_ID": "test-channel",
        },
    )
    @patch("script.slack_app")
    @patch("script.dt.datetime")
    def test_send_reminder_at_5pm_boundary(self, mock_datetime, mock_slack_app):
        """Test that reminder is sent at 5 PM JST (boundary case)"""
        # Mock datetime.now to return 5 PM JST
        mock_now = Mock()
        mock_now.hour = 17
        mock_now.strftime = Mock(return_value="2024-01-15 17:00:00")
        mock_datetime.now = Mock(return_value=mock_now)
        mock_datetime.timezone = script.dt.timezone
        mock_datetime.timedelta = script.dt.timedelta

        # Mock Slack client
        mock_client = MagicMock()
        mock_slack_app.client = mock_client

        # Call the function
        script.send_reminder()

        # Verify that chat_postMessage was called
        mock_client.chat_postMessage.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_CHANNEL_ID": "test-channel",
        },
    )
    @patch("script.slack_app")
    @patch("script.dt.datetime")
    def test_send_reminder_handles_slack_error(self, mock_datetime, mock_slack_app):
        """Test that errors from Slack API are handled gracefully"""
        # Mock datetime.now to return a time during working hours
        mock_now = Mock()
        mock_now.hour = 10
        mock_now.strftime = Mock(return_value="2024-01-15 10:00:00")
        mock_datetime.now = Mock(return_value=mock_now)
        mock_datetime.timezone = script.dt.timezone
        mock_datetime.timedelta = script.dt.timedelta

        # Mock Slack client to raise an exception
        mock_client = MagicMock()
        mock_client.chat_postMessage.side_effect = Exception("Slack API error")
        mock_slack_app.client = mock_client

        # Call the function - should not raise an exception
        script.send_reminder()

        # Verify that chat_postMessage was called (even though it failed)
        mock_client.chat_postMessage.assert_called_once()
