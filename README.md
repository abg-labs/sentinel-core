# Sentinel Core

**The Mission-Critical Surveillance Framework.**

Sentinel Core is the open-source foundational layer of the Sentinel platform. It provides the architectural primitives required for high-performance, autonomous video intelligence, object detection, and multi-stream camera management.

This core library is maintained by **AB Group** and is engineered for environments where reliability and low-latency processing are non-negotiable.

---

## High-Level Architecture

Sentinel Core is designed as a modular pipeline:

1.  **Ingestion**: Multi-protocol stream handling (RTSP, RTMP, Local).
2.  **Detection**: Abstraction layers for AI model inference (YOLO, CLIP, Custom).
3.  **Intelligence**: Data-schema for persistent tracking and spatial awareness.

## Getting Started

Sentinel Core is designed to be highly extensible. Below is a minimal implementation of a custom situational awareness detector:

```python
from sentinel.ai.base import BaseDetector, Detection
from sentinel.core.manager import StreamManager

class CustomUnitDetector(BaseDetector):
    def detect(self, frame):
        # Implementation of your AI model inference logic
        return [
            Detection(class_id=0, class_name="person", confidence=0.98, bbox=(0.1, 0.1, 0.5, 0.5))
        ]

# Initialize the Orchestrator
manager = StreamManager()
manager.set_detector(CustomUnitDetector())

# Initiate a stream session
import asyncio
asyncio.run(manager.start_stream(camera_id=101, source="rtsp://internal.secure-feed.local/stream1"))
```

## Progressive Evolution

Sentinel Core is a living framework. We push technical updates and architectural refinements as they are validated through our ongoing strategic deployments. Our goal is to maintain a continuous stream of progress:

- **Current focus**: Core Schema & AI Abstraction Interfaces.
- **In-development**: High-performance stream acquisition and buffer management logic.
- **Future engineering**: Standardized wrappers for real-time model inference (YOLO/CLIP).

---

## Philosophy

Surveillance is not just about recording video; it's about **autonomous situational awareness.** Sentinel Core provides the schemas that transform raw pixels into strategic data.

© 2026 [AB Group](https://abgroupglobal.com) • Strategic Systems Engineering.
