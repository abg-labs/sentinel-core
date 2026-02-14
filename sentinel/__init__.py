# Sentinel Core
# The foundational framework for situational awareness.

from sentinel.ai.base import Detection, BaseDetector
from sentinel.ai.detector import YOLODetector
from sentinel.ai.zone import ZoneEngine, ZoneConfig
from sentinel.core.stream import TechnicalStream
from sentinel.core.manager import StreamManager
from sentinel.camera.processor import StreamProcessor

__version__ = "0.1.0"
__author__ = "AB Group"
