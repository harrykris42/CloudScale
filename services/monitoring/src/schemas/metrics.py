# services/monitoring/src/schemas/metrics.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict

class MetricsBase(BaseModel):
    resource_id: str
    resource_type: str
    cpu_usage: float = Field(..., ge=0, le=100)
    memory_usage: float = Field(..., ge=0, le=100)
    disk_usage: float = Field(..., ge=0, le=100)
    network_in: float = Field(..., ge=0)
    network_out: float = Field(..., ge=0)

class MetricsCreate(MetricsBase):
    pass

class MetricsRead(MetricsBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    resource_id: str
    alert_type: str
    severity: str
    message: str

class AlertCreate(AlertBase):
    pass

class AlertRead(AlertBase):
    id: int
    timestamp: datetime
    resolved: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResourceMetadataBase(BaseModel):
    resource_id: str
    resource_type: str
    name: str
    region: str
    tags: Dict[str, str] = Field(default_factory=dict)

class ResourceMetadataCreate(ResourceMetadataBase):
    pass

class ResourceMetadataRead(ResourceMetadataBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
