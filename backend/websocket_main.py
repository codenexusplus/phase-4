"""
WebSocket server implementation for real-time updates.
This server runs on port 3001 to handle WebSocket connections for live updates.
"""
import asyncio
import logging
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websocket_server import handle_websocket_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a separate FastAPI app for WebSocket server
ws_app = FastAPI(title="WebSocket Server", description="Real-time updates server")

@ws_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket_connection(websocket)

@ws_app.get("/")
async def root():
    return {"message": "WebSocket Server for AI Todo Assistant"}

if __name__ == "__main__":
    logger.info("Starting WebSocket server on port 3001...")
    uvicorn.run(ws_app, host="0.0.0.0", port=3001)
