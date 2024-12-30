# services/monitoring/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import metrics, auth
from .core.metrics_collector import MetricsCollector
from contextlib import asynccontextmanager
import logging
import asyncio

from .config import settings
from .api.v1.endpoints import metrics, auth
from .database import get_db
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
    title="CloudScale Monitoring",
    description="Resource monitoring and metrics collection service",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(
    metrics.router,
    prefix="/api/v1/monitoring",
    tags=["monitoring"],
    dependencies=[Depends(get_current_active_user)]  # Require authentication for all metrics endpoints
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "collecting_metrics": metrics_collector is not None and metrics_collector.is_running
    }

@app.on_event("startup")
async def startup_event():
    # Create initial admin user if not exists
    try:
        async for db in get_db():
            stmt = select(User).where(User.username == "admin")
            result = await db.execute(stmt)
            if not result.scalar_one_or_none():
                admin_user = User(
                    username="admin",
                    email="admin@cloudscale.local",
                    hashed_password=get_password_hash("admin123"),
                    is_admin=True
                )
                db.add(admin_user)
                await db.commit()
                logging.info("Created initial admin user")
    except Exception as e:
        logging.error(f"Error creating admin user: {e}")
