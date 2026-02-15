import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class SovereignMemory:
    """
    Sovereign Persistence Engine.
    Handles high-throughput storage of situational intelligence using a local SQLite substrate.
    """
    def __init__(self, db_path: str = "./sentinel_memory.db"):
        self.db_path = Path(db_path)
        self._initialize_vault()

    def _initialize_vault(self):
        """Initialize the database schema if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table: Situational Detections
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS detections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        camera_id INTEGER,
                        label TEXT,
                        confidence REAL,
                        bbox_json TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Table: Institutional Alerts
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        camera_id INTEGER,
                        title TEXT,
                        message TEXT,
                        severity TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
            logger.info(f"Sovereign Memory Vault initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Vault Initialization Error: {e}")

    def save_detection(self, camera_id: int, label: str, confidence: float, bbox: tuple):
        """Persist a single intelligence detection."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO detections (camera_id, label, confidence, bbox_json) VALUES (?, ?, ?, ?)",
                    (camera_id, label, confidence, json.dumps(bbox))
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Detection Persistence Error: {e}")

    def save_alert(self, camera_id: int, title: str, message: str, severity: str):
        """Persist a high-severity alert."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO alerts (camera_id, title, message, severity) VALUES (?, ?, ?, ?)",
                    (camera_id, title, message, severity)
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Alert Persistence Error: {e}")

    def query_detections(self, camera_id: Optional[int] = None, hours: int = 24) -> List[Dict[str, Any]]:
        """Retrieve historical intelligence detections."""
        try:
            since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
            query = "SELECT camera_id, label, confidence, bbox_json, timestamp FROM detections WHERE timestamp > ?"
            params = [since]
            
            if camera_id is not None:
                query += " AND camera_id = ?"
                params.append(camera_id)

            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Query Execution Error: {e}")
            return []

    def purge_old_data(self, retention_days: int = 7):
        """Institutional data retention protocol. Purges data older than the retention period."""
        try:
            cutoff = (datetime.now() - timedelta(days=retention_days)).strftime("%Y-%m-%d %H:%M:%S")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM detections WHERE timestamp < ?", (cutoff,))
                cursor.execute("DELETE FROM alerts WHERE timestamp < ?", (cutoff,))
                conn.commit()
            logger.info(f"Data Retention Protocol: Purged entries older than {retention_days} days.")
        except Exception as e:
            logger.error(f"Retention Protocol Failure: {e}")
