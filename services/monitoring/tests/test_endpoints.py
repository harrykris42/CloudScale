# services/monitoring/tests/test_endpoints.py
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from ..src.main import app
from ..src.database import get_db

# Test data
test_metrics = {
    "resource_id": "test-resource-1",
    "resource_type": "vm",
    "cpu_usage": 45.5,
    "memory_usage": 60.2,
    "disk_usage": 72.8,
    "network_in": 1024.0,
    "network_out": 2048.0
}

test_alert = {
    "resource_id": "test-resource-1",
    "alert_type": "high_cpu",
    "severity": "warning",
    "message": "CPU usage above 80%"
}

@pytest.mark.asyncio
async def test_create_metrics():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/monitoring/metrics/", json=test_metrics)
        assert response.status_code == 200
        data = response.json()
        assert data["resource_id"] == test_metrics["resource_id"]
        assert data["cpu_usage"] == test_metrics["cpu_usage"]

@pytest.mark.asyncio
async def test_get_metrics():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create some metrics
        await client.post("/api/v1/monitoring/metrics/", json=test_metrics)

        # Then retrieve them
        response = await client.get(
            f"/api/v1/monitoring/metrics/{test_metrics['resource_id']}",
            params={
                "start_time": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
                "end_time": datetime.utcnow().isoformat()
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["resource_id"] == test_metrics["resource_id"]

@pytest.mark.asyncio
async def test_create_alert():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/monitoring/alerts/", json=test_alert)
        assert response.status_code == 200
        data = response.json()
        assert data["resource_id"] == test_alert["resource_id"]
        assert data["alert_type"] == test_alert["alert_type"]

@pytest.mark.asyncio
async def test_resolve_alert():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create an alert
        create_response = await client.post("/api/v1/monitoring/alerts/", json=test_alert)
        alert_id = create_response.json()["id"]

        # Then resolve it
        response = await client.post(f"/api/v1/monitoring/alerts/{alert_id}/resolve")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == alert_id
        assert data["resolved"] is not None
