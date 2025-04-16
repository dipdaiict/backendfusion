# Shared dependencies like DB, JWT
import asyncpg # type: ignore
import logging
from typing import Optional
import redis.asyncio as redis
from app.config import (postgres_settings, redis_settings)

# Configure logging
logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger(__name__)

# Build connection strings
DATABASE_URL = (
    f"postgresql://{postgres_settings.postgres_username}:"
    f"{postgres_settings.postgres_password}@"
    f"{postgres_settings.postgres_hostname}:"
    f"{postgres_settings.postgres_port}/"
    f"{postgres_settings.postgres_name}")

# Database connection
class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Initialize the connection pool."""
        try:
            self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=10)
        except Exception as e:
            Logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    async def disconnect(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()

    async def get_connection(self):
        """Get a connection from the pool."""
        if not self.pool:
            raise RuntimeError("Database pool is not initialized.")
        return await self.pool.acquire()

    async def release_connection(self, conn):
        """Release a connection back to the pool."""
        await self.pool.release(conn)

class RedisClient:
    def __init__(self):
        self._client: Optional[redis.Redis] = None

    def connect(self) -> redis.Redis:
        if not self._client:
            self._client = redis.Redis(
                host=redis_settings.redis_host,
                port=redis_settings.redis_port,
                username=redis_settings.redis_username,
                password=redis_settings.redis_password,
                db=redis_settings.redis_db,
                decode_responses=True)
            Logger.info("Redis client initialized.")
        return self._client

# Create instances
db = Database(DATABASE_URL)
redis_client = RedisClient()
Logger.info("Postgres Database set up.")