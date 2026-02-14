# Sentinel Core

<p align="left">
  <img src="https://img.shields.io/badge/version-v0.2.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-Linux%20|%20macOS%20|%20Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/security-vetted-gold.svg" alt="Security">
</p>

**The Mission-Critical Surveillance Framework.**

Sentinel Core is the open-source foundational layer of the Sentinel platform. It provides the architectural primitives required for high-performance, autonomous video intelligence, object detection, and multi-stream camera management.

This core library is maintained by **AB Group** and is engineered for environments where reliability and low-latency processing are non-negotiable.

---

## High-Level Architecture

Sentinel Core is designed as a modular pipeline:

1.  **Ingestion**: Multi-protocol stream handling (RTSP, RTMP, Local).
2.  **Detection**: Abstraction layers for AI model inference (YOLO, CLIP, Custom).
3.  **Intelligence**: Data-schema for persistent tracking and situational awareness.
4.  **Spatial Awareness**: Polygon-based zone detection, intrusion alerts, and loitering analysis.
5.  **Semantic Search**: Natural language querying of technical data streams via sovereign CLIP embeddings.

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

- **v0.1.0** (Feb 2026): Core Schema & AI Abstraction Interfaces.
- **v0.2.0** (Feb 2026): Functional Stream Processing & Native Intelligence wrappers (YOLO).
- **v0.3.0** (Feb 2026): Sovereign Semantic Search via CLIP embeddings.
- **In-development**: Distributed indexing, GPU-accelerated inference, and autonomous alerting protocols.

---

## Philosophy

Surveillance is not just about recording video; it's about **autonomous situational awareness.** Sentinel Core provides the schemas that transform raw pixels into strategic data.

© 2026 [AB Group](https://abgroupglobal.com) • Strategic Systems Engineering.
