import cv2
import logging
import queue
import threading
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from enum import Enum

logger = logging.getLogger(__name__)

class RecordingMode(Enum):
    CONTINUOUS = "continuous"
    EVENT_TRIGGERED = "event_triggered"

class VideoRecorder:
    """
    Sovereign Video Recording Engine.
    Handles high-fidelity video persistence with pre-event buffering and motion awareness.
    """
    def __init__(
        self,
        output_dir: str = "./recordings",
        fps: int = 15,
        resolution: Tuple[int, int] = (1280, 720),
        pre_buffer_seconds: int = 5,
        segment_duration: int = 60
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.fps = fps
        self.resolution = resolution
        self.segment_duration = segment_duration
        
        # Pre-event buffering
        self.pre_buffer_size = pre_buffer_seconds * fps
        self.pre_buffer = queue.Queue(maxsize=self.pre_buffer_size)
        
        self.current_writer: Optional[cv2.VideoWriter] = None
        self.current_file: Optional[Path] = None
        self.segment_start: Optional[datetime] = None
        self.is_recording = False
        self.lock = threading.Lock()

    def _get_filename(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"sentinel_capture_{timestamp}.mp4"

    def _start_segment(self):
        self.current_file = self._get_filename()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.current_writer = cv2.VideoWriter(
            str(self.current_file),
            fourcc,
            self.fps,
            self.resolution
        )
        self.segment_start = datetime.now()
        logger.info(f"Technical Recording Initiated: {self.current_file}")

    def _stop_segment(self):
        if self.current_writer:
            self.current_writer.release()
            self.current_writer = None
            logger.info(f"Recording Segment Finalized: {self.current_file}")

    def write(self, frame: np.ndarray, trigger: bool = False):
        """
        Ingest a frame into the recording engine.
        Supports continuous sliding-window buffering.
        """
        with self.lock:
            if trigger and not self.is_recording:
                self.is_recording = True
                self._start_segment()
                self._flush_pre_buffer()

            if self.is_recording:
                # Automatic segment rotation
                if self.segment_start and (datetime.now() - self.segment_start).total_seconds() > self.segment_duration:
                    self._stop_segment()
                    self._start_segment()

                resized = cv2.resize(frame, self.resolution)
                self.current_writer.write(resized)
            else:
                self._add_to_buffer(frame)

    def stop(self):
        """Terminate active recording and cleanup resources."""
        with self.lock:
            self.is_recording = False
            self._stop_segment()

    def _add_to_buffer(self, frame: np.ndarray):
        if self.pre_buffer.full():
            try: self.pre_buffer.get_nowait()
            except queue.Empty: pass
        
        try: self.pre_buffer.put_nowait(frame.copy())
        except queue.Full: pass

    def _flush_pre_buffer(self):
        if not self.current_writer: return
        
        count = 0
        while not self.pre_buffer.empty():
            try:
                f = self.pre_buffer.get_nowait()
                resized = cv2.resize(f, self.resolution)
                self.current_writer.write(resized)
                count += 1
            except queue.Empty: break
        
        if count > 0:
            logger.debug(f"Pre-event buffer flushed: {count} frames acquired.")
