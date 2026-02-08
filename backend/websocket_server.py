"""
WebSocket server for real-time updates in the AI Todo Assistant.
This server handles WebSocket connections for live updates between the frontend and backend.
"""
import asyncio
import json
import logging
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
from database.connection import async_engine
from services.task_service import TaskService
from sqlalchemy.ext.asyncio import AsyncSession


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"WebSocket connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logging.info(f"WebSocket connection closed. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


# Global connection manager instance
manager = ConnectionManager()


async def handle_websocket_connection(websocket: WebSocket):
    """
    Handle individual WebSocket connections
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Listen for messages from the client (though we mainly use this for broadcasting)
            data = await websocket.receive_text()
            
            # Parse the received data
            try:
                message_data = json.loads(data)
                
                # Respond to ping messages or other client requests
                if message_data.get("type") == "ping":
                    await manager.send_personal_message(
                        json.dumps({"type": "pong", "timestamp": asyncio.get_event_loop().time()}),
                        websocket
                    )
            except json.JSONDecodeError:
                # If it's not JSON, just ignore it (we're primarily using this for broadcasting)
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logging.error(f"Error in WebSocket connection: {e}")
        manager.disconnect(websocket)


async def notify_task_updates(user_id: str):
    """
    Notify all connected clients about task updates for a specific user
    """
    message = json.dumps({
        "type": "task_update",
        "user_id": user_id,
        "timestamp": asyncio.get_event_loop().time()
    })
    
    await manager.broadcast(message)
    logging.info(f"Broadcasted task update notification to {len(manager.active_connections)} clients")
