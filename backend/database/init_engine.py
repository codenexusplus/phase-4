from sqlalchemy.ext.asyncio import create_async_engine
from config.settings import settings
from urllib.parse import urlparse

# Get database URL from environment
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

    # If there are query parameters, we'll handle them separately if needed
    if parsed_url.query:
        # For Neon, we might need to handle SSL differently
        pass

# Create async engine specifically for initialization
init_engine = create_async_engine(DATABASE_URL)
