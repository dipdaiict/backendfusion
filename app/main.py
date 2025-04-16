from fastapi import FastAPI
from app.dependencies import db
from app.api import routes_system
from contextlib import asynccontextmanager

# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

# Create the app with lifespan
app = FastAPI(lifespan=lifespan)

# Register API routes:
app.include_router(routes_system.router, prefix='/system')

