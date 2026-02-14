import logging
import asyncio
import httpx
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AlertSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertProtocol(ABC):
    """
    Base protocol for sovereign alert delivery.
    Ensures that mission-critical data reaches its destination via secure channels.
    """
    @abstractmethod
    async def dispatch(self, title: str, message: str, severity: AlertSeverity, metadata: Dict[str, Any]) -> bool:
        pass

class WebhookProtocol(AlertProtocol):
    """
    Standard Webhook delivery.
    Sends situational data to a technical endpoint via HTTPS POST.
    """
    def __init__(self, url: str):
        self.url = url

    async def dispatch(self, title: str, message: str, severity: AlertSeverity, metadata: Dict[str, Any]) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                data = {
                    "title": title,
                    "message": message,
                    "severity": severity.value,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": metadata
                }
                response = await client.post(self.url, json=data)
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Webhook dispatch failed: {e}")
            return False

class TelegramProtocol(AlertProtocol):
    """
    Institutional Telegram delivery.
    Sends formatted alerts via the Telegram Bot API.
    """
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def dispatch(self, title: str, message: str, severity: AlertSeverity, metadata: Dict[str, Any]) -> bool:
        try:
            severity_icons = {
                AlertSeverity.INFO: "ℹ️",
                AlertSeverity.LOW: "🟡",
                AlertSeverity.MEDIUM: "🟠",
                AlertSeverity.HIGH: "🔴",
                AlertSeverity.CRITICAL: "🚨"
            }
            icon = severity_icons.get(severity, "⚠️")
            
            text = f"{icon} *{title}*\n\n"
            text += f"_{message}_\n\n"
            text += f"Unit: {metadata.get('camera_id', 'Unknown')}\n"
            text += f"Time: {datetime.now().strftime('%H:%M:%S')}"

            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                response = await client.post(url, json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "Markdown"
                })
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Telegram dispatch failed: {e}")
            return False

class AlertManager:
    """
    Centralized dispatcher for situational intelligence alerts.
    Manages multiple delivery protocols and handles asynchronous dispatch.
    """
    def __init__(self):
        self.protocols: List[AlertProtocol] = []

    def register_protocol(self, protocol: AlertProtocol):
        """Register a new delivery channel."""
        self.protocols.append(protocol)
        logger.info(f"Alert Protocol Registered: {type(protocol).__name__}")

    async def notify(self, title: str, message: str, severity: AlertSeverity = AlertSeverity.MEDIUM, metadata: Optional[Dict[str, Any]] = None):
        """
        Broadcast an alert across all registered protocols.
        """
        if not self.protocols:
            logger.warning("No alert protocols registered. Broadcaster is idle.")
            return

        metadata = metadata or {}
        logger.info(f"Broadcasting Alert: [{severity.value.upper()}] {title}")
        
        tasks = [p.dispatch(title, message, severity, metadata) for p in self.protocols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if r is True)
        logger.debug(f"Alert broadcast complete. Success: {success_count}/{len(self.protocols)}")
