"""
Simple test script to verify WebSocket server functionality
"""
import asyncio
import websockets
import json

async def test_websocket_connection():
    try:
        # Connect to the WebSocket server
        uri = "ws://localhost:3001/ws"
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server successfully!")
            
            # Send a test message
            test_message = json.dumps({"type": "ping", "message": "Hello from test client"})
            await websocket.send(test_message)
            print(f"Sent: {test_message}")
            
            # Wait for a response
            response = await websocket.recv()
            print(f"Received: {response}")
            
    except Exception as e:
        print(f"Error connecting to WebSocket server: {e}")

if __name__ == "__main__":
    print("Testing WebSocket connection...")
    asyncio.run(test_websocket_connection())