"""
1️⃣ Design a Notification System
❓ Problem Statement (Interview Version)

Design a system that can send notifications through multiple channels such as:
    Email
    Slack
    Push notification

The system should be easy to extend when new notification channels are added.

🎯 What Achievers is Evaluating

    Interface segregation
    Open/Closed Principle (without naming it)
    Clear responsibility boundaries
    Extensibility without modifying existing code
"""


from abc import ABC, abstractmethod
from typing import Dict


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailNotification(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"[EMAIL] To: {recipient} | Message: {message}")


class SlackNotification(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"[SLACK] Channel: {recipient} | Message: {message}")


class PushNotification(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"[PUSH] Device: {recipient} | Message: {message}")


class NotificationService:
    def __init__(self) -> None:
        self._channels: Dict[str, NotificationChannel] = {}

    def register_channel(self, name: str, channel: NotificationChannel) -> None:
        self._channels[name] = channel

    def notify(self, channel_name: str, recipient: str, message: str) -> None:
        if channel_name not in self._channels:
            raise ValueError(f"Unsupported notification channel: {channel_name}")

        self._channels[channel_name].send(recipient, message)


# ---- Usage Example ----
service = NotificationService()
service.register_channel("email", EmailNotification())
service.register_channel("slack", SlackNotification())
service.register_channel("push", PushNotification())

service.notify("email", "user@example.com", "Welcome to Achievers!")
service.notify("slack", "#engineering", "Deployment successful")
service.notify("push", "device-id-123", "You have a new reward!")
