import time
import uuid
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class TechnicalStream:
    """
    Representation of a mission-critical data feed.
    Tracks operational metrics and connectivity state for a single sensing unit.
    """
    source: str
    camera_id: int
    name: Optional[str] = None
    stream_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)
    
    # Operational Metrics
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = False
    reconnect_attempts: int = 0
    
    def get_uptime(self) -> float:
        """Calculate the duration of the current operational session."""
        if not self.is_active:
            return 0.0
        return time.time() - self.start_time

    def to_summary(self) -> Dict[str, Any]:
        """Generate an institutional summary of the stream status."""
        return {
            "id": self.stream_id,
            "camera_id": self.camera_id,
            "status": "OPERATIONAL" if self.is_active else "IDLE",
            "uptime": f"{self.get_uptime():.2f}s",
            "source_type": self.source.split('://')[0] if '://' in self.source else "local",
            "name": self.name or f"UNIT-{self.camera_id}"
        }
