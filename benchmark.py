import time
import torch
import numpy as np
import logging
from ai.detector import YOLODetector
from ai.semantic import SemanticEngine
from core.accelerator import HardwareAccelerator

# Configure institutional logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("sentinel.benchmarks")

def run_benchmark():
    """
    Sentinel Core Performance Benchmarking Utility.
    Measures throughput across different computational layers.
    """
    print("\n" + "="*50)
    print("      SENTINEL CORE PERFORMANCE BENCHMARKS      ")
    print("="*50)
    
    device = HardwareAccelerator.get_device()
    print(f"Operational Substrate: {device.upper()}")
    print("-" * 50)

    # 1. Inference Benchmarking (YOLO)
    print("\n[🧪] Testing Situation Awareness Throughput (YOLOv8n)...")
    detector = YOLODetector(model_type="yolov8n", device=device)
    dummy_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    
    # Warmup
    for _ in range(5):
        detector.detect(dummy_frame)
    
    start_time = time.time()
    iterations = 50
    for _ in range(iterations):
        detector.detect(dummy_frame)
    
    end_time = time.time()
    yolo_fps = iterations / (end_time - start_time)
    print(f"YOLO Throughput: {yolo_fps:.2f} FPS")

    # 2. Semantic Intelligence Benchmarking (CLIP)
    print("\n[🧪] Testing Semantic Intelligence Encoding (CLIP ViT-L/14)...")
    try:
        semantic = SemanticEngine()
        # Warmup
        semantic.index(dummy_frame, camera_id=0)
        
        start_time = time.time()
        semantic_iterations = 10
        for i in range(semantic_iterations):
            semantic.index(dummy_frame, camera_id=0)
        
        end_time = time.time()
        semantic_fps = semantic_iterations / (end_time - start_time)
        print(f"Semantic Encoding: {semantic_fps:.2f} FPS")
    except Exception as e:
        print(f"Semantic Intelligence Bypass: {e}")

    print("\n" + "="*50)
    print("        Institutional Benchmarking Complete       ")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_benchmark()
