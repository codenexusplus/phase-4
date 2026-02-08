import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set the database URL to use SQLite before importing backend modules
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./todo_app.db'

from backend.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting backend server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)