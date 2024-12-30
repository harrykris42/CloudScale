# services/monitoring/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import asyncio

from .config import settings
from .api.v1.endpoints import metrics
from .core.metrics_collector import MetricsCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global metrics collector instance
metrics_collector: MetricsCollector | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up monitoring service...")

    # Initialize metrics collector
    global metrics_collector
    metrics_collector = MetricsCollector()
    collection_task = asyncio.create_task(metrics_collector.start_collection())

    yield

    # Shutdown
    logger.info("Shutting down monitoring service...")
    if metrics_collector:
        await metrics_collector.stop_collection()
    if collection_task:
        collection_task.cancel()
        try:
            await collection_task
        except asyncio.CancelledError:
            pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Resource monitoring and metrics collection service",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(metrics.router, prefix=settings.API_V1_STR + "/monitoring", tags=["monitoring"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "collecting_metrics": metrics_collector is not None and metrics_collector.is_running
    }
