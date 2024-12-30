from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from typing import List, Optional

from ..models.metrics import ResourceMetrics, Alert, ResourceMetadata
from ..schemas.metrics import MetricsCreate, AlertCreate, ResourceMetadataCreate

class MetricsCRUD:
    @staticmethod
    async def create_metrics(db: AsyncSession, metrics: MetricsCreate) -> ResourceMetrics:
        db_metrics = ResourceMetrics(**metrics.model_dump())
        db.add(db_metrics)
        await db.commit()
        await db.refresh(db_metrics)
        return db_metrics

    @staticmethod
    async def get_metrics(
        db: AsyncSession,
        resource_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[ResourceMetrics]:
        query = select(ResourceMetrics).where(
            and_(
                ResourceMetrics.resource_id == resource_id,
                ResourceMetrics.timestamp >= start_time,
                ResourceMetrics.timestamp <= end_time
            )
        ).order_by(ResourceMetrics.timestamp.desc())

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_alert(db: AsyncSession, alert: AlertCreate) -> Alert:
        db_alert = Alert(**alert.model_dump())
        db.add(db_alert)
        await db.commit()
        await db.refresh(db_alert)
        return db_alert

    @staticmethod
    async def resolve_alert(db: AsyncSession, alert_id: int) -> Optional[Alert]:
        query = select(Alert).where(Alert.id == alert_id)
        result = await db.execute(query)
        db_alert = result.scalar_one_or_none()

        if db_alert:
            db_alert.resolved = datetime.utcnow()
            await db.commit()
            await db.refresh(db_alert)

        return db_alert

    @staticmethod
    async def create_resource_metadata(
        db: AsyncSession,
        metadata: ResourceMetadataCreate
    ) -> ResourceMetadata:
        db_metadata = ResourceMetadata(**metadata.model_dump())
        db.add(db_metadata)
        await db.commit()
        await db.refresh(db_metadata)
        return db_metadata
