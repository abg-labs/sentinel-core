import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from ai.semantic import SemanticEngine
from core.memory import SovereignMemory

from fastapi.responses import FileResponse

# Institutional Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel.dashboard")

app = FastAPI(title="Sentinel Sovereign Intelligence Dashboard")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Engines
semantic_engine = SemanticEngine()
memory = SovereignMemory()

# Serve static snapshots
app.mount("/snapshots", StaticFiles(directory="search_index"), name="snapshots")

@app.get("/")
async def get_dashboard():
    return FileResponse("dashboard/index.html")

class SearchQuery(BaseModel):
    query: str
    top_k: int = 6

@app.get("/health")
def health():
    return {"status": "operational", "engine": "Sentinel Core v0.8.0"}

@app.post("/search")
async def semantic_search(payload: SearchQuery):
    """
    Execute a sovereign natural language query with relevance filtering.
    """
    try:
        results = semantic_engine.query(payload.query, top_k=payload.top_k)
        formatted = []
        
        # Institutional Relevance Floor (22%)
        # This filters out 'noisy' matches that are only partially relevant.
        RELEVANCE_FLOOR = 22.0

        for r in results:
            similarity_pct = round(r.similarity * 100, 2)
            
            if similarity_pct < RELEVANCE_FLOOR:
                continue

            formatted.append({
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "similarity": similarity_pct,
                "snapshot_url": f"/snapshots/{r.metadata.get('snapshot')}",
                "camera_id": r.camera_id
            })
        return formatted
    except Exception as e:
        logger.error(f"Search failure: {e}")
        raise HTTPException(status_code=500, detail="Intelligence retrieval failed.")

@app.get("/alerts")
async def get_alerts(hours: int = 24):
    """Retrieve recent institutional alerts from memory."""
    # Assuming SovereignMemory has a query_alerts or similar
    # For now, let's use the query_detections or a custom query
    return memory.query_detections(hours=hours)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
