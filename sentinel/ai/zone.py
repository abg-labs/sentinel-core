import numpy as np
import cv2
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from sentinel.ai.base import Detection

logger = logging.getLogger(__name__)

@dataclass
class ZoneConfig:
    """
    Configuration for a Strategic Observation Zone.
    Supports complex polygon boundaries and class-specific sensitivity.
    """
    id: int
    name: str
    coordinates: List[List[float]]  # Normalized [[x,y], ...] polygon points
    zone_type: str = "restricted" # "restricted", "loitering"
    detection_classes: Optional[List[str]] = None
    loiter_threshold: int = 30 # seconds
    color: str = "#1F4FD8" # Strategic Blue
    is_active: bool = True

    def __post_init__(self):
        if self.detection_classes is None:
            self.detection_classes = ["person"]

@dataclass
class ZoneViolation:
    """
    Data container for a sovereign boundary breach.
    """
    zone_id: int
    zone_name: str
    event_type: str  # "entered", "inside", "exited", "loitering"
    detection: Detection
    timestamp: datetime
    dwell_time: Optional[float] = None

class ZoneEngine:
    """
    Industrial-grade polygon zone detection engine.
    Handles intrusion detection and dwell-time monitoring.
    """
    def __init__(self):
        self.zones: Dict[int, ZoneConfig] = {}
        self.object_entries: Dict[str, Dict[int, datetime]] = {}
        self.last_state: Dict[int, set] = {}

    def add_zone(self, zone: ZoneConfig):
        """Register a new observation zone."""
        self.zones[zone.id] = zone
        self.last_state[zone.id] = set()
        logger.info(f"Strategic Zone Registered: {zone.name} [ID: {zone.id}]")

    def _point_in_polygon(self, point: Tuple[float, float], polygon: List[List[float]]) -> bool:
        """Ray-casting algorithm for technical boundary verification."""
        x, y = point
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    def process(self, detections: List[Detection]) -> List[ZoneViolation]:
        """Verify situational awareness data against all active zones."""
        violations = []
        current_time = datetime.now()

        for zone in self.zones.values():
            if not zone.is_active: continue
            
            current_inside = set()
            for detection in detections:
                if detection.class_name not in zone.detection_classes: continue
                
                # Check bottom-center of bbox (contact point)
                x1, y1, x2, y2 = detection.bbox
                point = ((x1 + x2) / 2, y2)
                
                if self._point_in_polygon(point, zone.coordinates):
                    track_id = str(detection.track_id or id(detection))
                    current_inside.add(track_id)
                    
                    # Entry Logic
                    if track_id not in self.last_state.get(zone.id, set()):
                        if track_id not in self.object_entries:
                            self.object_entries[track_id] = {}
                        self.object_entries[track_id][zone.id] = current_time
                        
                        violations.append(ZoneViolation(
                            zone_id=zone.id, zone_name=zone.name,
                            event_type="entered", detection=detection,
                            timestamp=current_time
                        ))
                    
                    # Loitering Logic
                    elif zone.zone_type == "loitering":
                        entry_time = self.object_entries.get(track_id, {}).get(zone.id)
                        if entry_time:
                            dwell = (current_time - entry_time).total_seconds()
                            if dwell >= zone.loiter_threshold:
                                violations.append(ZoneViolation(
                                    zone_id=zone.id, zone_name=zone.name,
                                    event_type="loitering", detection=detection,
                                    timestamp=current_time, dwell_time=dwell
                                ))

            self.last_state[zone.id] = current_inside
        return violations

    def overlay(self, frame: np.ndarray, violations: List[ZoneViolation]) -> np.ndarray:
        """Render the tactical zone overlay on a video frame."""
        h, w = frame.shape[:2]
        violation_ids = {v.zone_id for v in violations}
        
        for zone in self.zones.values():
            # Convert normalized to pixel coords
            pts = np.array([[int(x*w), int(y*h)] for x, y in zone.coordinates], np.int32)
            
            # Color logic: Red if violated, Alpha-Blue if clear
            color = (0, 0, 255) if zone.id in violation_ids else (216, 79, 31)
            
            # Fill
            mask = frame.copy()
            cv2.fillPoly(mask, [pts], color)
            cv2.addWeighted(mask, 0.15, frame, 0.85, 0, frame)
            
            # Outline
            cv2.polylines(frame, [pts], True, color, 2)
            
            # Label
            cv2.putText(frame, zone.name, (pts[0][0], pts[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return frame
