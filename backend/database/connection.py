from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Get database URL from settings
DATABASE_URL = settings.DATABASE_URL

# Handle different database types appropriately
if DATABASE_URL.startswith("postgresql://"):
    # Replace postgresql:// with postgresql+asyncpg:// for async support
    from urllib.parse import urlparse

    parsed_url = urlparse(DATABASE_URL)
    scheme = parsed_url.scheme.replace('postgresql', 'postgresql+asyncpg')
    username = parsed_url.username
    password = parsed_url.password
    hostname = parsed_url.hostname
    port = parsed_url.port or 5432  # Default PostgreSQL port
    database = parsed_url.path.lstrip('/')

    # Reconstruct URL without problematic query parameters for asyncpg
    DATABASE_URL = f"{scheme}://{username}:{password}@{hostname}:{port}/{database}"

    # If there are query parameters, we'll handle them separately if needed
    if parsed_url.query:
        # For Neon, we might need to handle SSL differently
        DATABASE_URL += f"?{parsed_url.query}"

elif DATABASE_URL.startswith("sqlite://"):
    # Handle SQLite URLs properly for async usage
    if not DATABASE_URL.startswith("sqlite+aiosqlite://"):
        # Convert standard SQLite URL to async SQLite URL
        DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://", 1)

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

def get_async_session():
    """Dependency to get async session"""
    async def async_session():
        async with AsyncSessionLocal() as session:
            yield session

    return async_session
