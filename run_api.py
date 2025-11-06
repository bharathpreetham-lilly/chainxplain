#!/usr/bin/env python3
"""Start the ChainXplain REST API server."""

import uvicorn
from chainxplain.api.server import app

if __name__ == "__main__":
    print("🚀 Starting ChainXplain API server...")
    print("📖 API documentation: http://localhost:8000/docs")
    print("📚 ReDoc documentation: http://localhost:8000/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,  # Auto-reload on code changes
    )
