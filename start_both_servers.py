"""
Script to start both the main backend server and the WebSocket server
"""
import subprocess
import sys
import threading
import time
import signal
import os

def run_server(command, name):
    """Run a server process"""
    print(f"Starting {name}...")
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
    except KeyboardInterrupt:
        print(f"\nStopping {name}...")
        process.terminate()
        process.wait()

def main():
    # Commands to start both servers
    main_server_cmd = "uvicorn backend.main:app --reload --port 8000"
    ws_server_cmd = "python -m backend.websocket_main"
    
    # Create threads for both servers
    main_thread = threading.Thread(target=run_server, args=(main_server_cmd, "Main Server (port 8000)"))
    ws_thread = threading.Thread(target=run_server, args=(ws_server_cmd, "WebSocket Server (port 3001)"))
    
    # Start both servers
    main_thread.start()
    time.sleep(2)  # Give main server a moment to start
    ws_thread.start()
    
    try:
        # Wait for both threads to complete
        main_thread.join()
        ws_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        # The run_server function handles termination
        sys.exit(0)

if __name__ == "__main__":
    main()