from fastapi import FastAPI
from app.api import routes_system
from app.dependencies import db, redis_client
from contextlib import asynccontextmanager

# Lifespan handler for Redis and DB connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB and Redis
    await db.connect()
    await redis_client.connect()  # Connect to Redis
    yield
    # Shutdown: Disconnect DB and Redis
    await db.disconnect()
    await redis_client.close()  # Close Redis connection

# Create the app with lifespan (DB + Redis)
app = FastAPI(lifespan=lifespan)

# Register API routes:
app.include_router(routes_system.router, prefix='/system')
