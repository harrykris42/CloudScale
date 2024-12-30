# services/monitoring/src/api/v1/endpoints/metrics.py
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import logging
import psutil

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/metrics/{resource_id}")
async def get_resource_metrics(resource_id: str):
    try:
        # Generate mock data
        mock_data = []
        current_time = datetime.utcnow()

        # Generate 10 data points
        for i in range(10):
            timestamp = current_time - timedelta(minutes=i*5)
            mock_data.append({
                "id": i+1,
                "resource_id": resource_id,
                "resource_type": "vm",
                "cpu_usage": 45.5 + (i % 5),
                "memory_usage": 60.2 + (i % 3),
                "disk_usage": 72.8 - (i % 4),
                "network_in": 1024.0 * (1 + i % 3),
                "network_out": 2048.0 * (1 + i % 2),
                "timestamp": timestamp.isoformat()
            })

        return mock_data

    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve metrics")

@router.get("/")
async def get_latest_metrics():
    try:
        return {
            "id": 1,
            "resource_id": "system",
            "resource_type": "host",
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_in": 0,
            "network_out": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting latest metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not get latest metrics")

@router.post("/metrics/")
async def create_metrics(metrics: dict):
    try:
        return {
            **metrics,
            "id": 1,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create metrics")
