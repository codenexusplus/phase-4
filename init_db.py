import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from urllib.parse import urlparse

# Load environment variables before importing settings
load_dotenv(dotenv_path='backend/.env')

from backend.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def create_tables():
    """Create all database tables"""
    # Get database URL from settings
    DATABASE_URL = settings.DATABASE_URL

    # Parse the URL to handle special parameters for asyncpg
    parsed_url = urlparse(DATABASE_URL)

    # Replace postgresql:// with postgresql+asyncpg:// if not already set
    if DATABASE_URL.startswith("postgresql://"):
        # Extract components
        scheme = parsed_url.scheme.replace('postgresql', 'postgresql+asyncpg')
        username = parsed_url.username
        password = parsed_url.password
        hostname = parsed_url.hostname
        port = parsed_url.port or 5432  # Default PostgreSQL port
        database = parsed_url.path.lstrip('/')

        # Reconstruct URL without problematic query parameters for asyncpg
        DATABASE_URL = f"{scheme}://{username}:{password}@{hostname}:{port}/{database}"

    # Create a new engine specifically for this operation
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        # Import all models before creating tables
        from backend.models.conversation import Conversation
        from backend.models.message import Message
        from backend.models.task import Task
        from backend.models.user import User

        # Create all tables
        await conn.run_sync(Conversation.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)
        await conn.run_sync(Task.metadata.create_all)
        await conn.run_sync(User.metadata.create_all)

    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())