from fastapi import FastAPI
from app.api import routes_system
from app.core.tracing import setup_tracer
from contextlib import asynccontextmanager
from app.dependencies import db, redis_client
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Lifespan handler for Redis and DB connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB and Redis
    await db.connect()
    await redis_client.connect()  # Connect to Redis
    yield
    # Shutdown: Disconnect DB and Redis
    await db.disconnect()

# Create the app with lifespan (DB + Redis)
app = FastAPI(lifespan=lifespan)

# Setup OpenTelemetry tracing
setup_tracer(service_name="backendfusion-service")

# Instrument FastAPI for every request:
FastAPIInstrumentor.instrument_app(app)

# Register API routes:
app.include_router(routes_system.router, prefix='/system')
