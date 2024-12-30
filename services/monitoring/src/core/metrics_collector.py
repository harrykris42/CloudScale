# services/monitoring/src/core/metrics_collector.py
import asyncio
import psutil
import logging
from datetime import datetime
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.is_running = False
        self._stop_event = asyncio.Event()
        self.collection_interval = 60  # seconds
        self._initial_network_io = psutil.net_io_counters()
        self._last_network_io = self._initial_network_io
        self._last_collection_time = datetime.now()

    async def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect detailed system metrics."""
        try:
            current_time = datetime.now()
            time_delta = (current_time - self._last_collection_time).total_seconds()

            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_times = psutil.cpu_times_percent()
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()

            # Network metrics
            current_network_io = psutil.net_io_counters()

            # Calculate network speeds
            bytes_sent = current_network_io.bytes_sent - self._last_network_io.bytes_sent
            bytes_recv = current_network_io.bytes_recv - self._last_network_io.bytes_recv

            network_speed_in = bytes_recv / time_delta if time_delta > 0 else 0
            network_speed_out = bytes_sent / time_delta if time_delta > 0 else 0

            # Update last values
            self._last_network_io = current_network_io
            self._last_collection_time = current_time

            metrics = {
                "timestamp": current_time.isoformat(),
                "cpu": {
                    "usage": cpu_percent,
                    "user": cpu_times.user,
                    "system": cpu_times.system,
                    "idle": cpu_times.idle,
                    "cores": cpu_count,
                    "frequency_mhz": cpu_freq.current if cpu_freq else None
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "usage": memory.percent,
                    "swap_used": swap.used,
                    "swap_total": swap.total
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "usage": disk.percent,
                    "read_bytes": disk_io.read_bytes if disk_io else 0,
                    "write_bytes": disk_io.write_bytes if disk_io else 0
                },
                "network": {
                    "bytes_sent": current_network_io.bytes_sent,
                    "bytes_recv": current_network_io.bytes_recv,
                    "speed_in": network_speed_in,
                    "speed_out": network_speed_out,
                    "packets_sent": current_network_io.packets_sent,
                    "packets_recv": current_network_io.packets_recv
                }
            }

            # Log metrics for debugging
            logger.info(f"Collected metrics: {json.dumps(metrics, default=str)}")

            # Format metrics for database storage
            return {
                "resource_id": "system",
                "resource_type": "host",
                "cpu_usage": metrics["cpu"]["usage"],
                "memory_usage": metrics["memory"]["usage"],
                "disk_usage": metrics["disk"]["usage"],
                "network_in": metrics["network"]["speed_in"],
                "network_out": metrics["network"]["speed_out"]
            }

        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return None

    async def start_collection(self):
        """Start the metrics collection loop."""
        self.is_running = True
        try:
            while not self._stop_event.is_set():
                metrics = await self.collect_system_metrics()
                if metrics:
                    # Here we would typically store metrics in the database
                    logger.info(f"Collected metrics: {metrics}")

                try:
                    await asyncio.wait_for(
                        self._stop_event.wait(),
                        timeout=self.collection_interval
                    )
                except asyncio.TimeoutError:
                    continue
        except Exception as e:
            logger.error(f"Error in metrics collection loop: {str(e)}")
            self.is_running = False
            raise
        finally:
            self.is_running = False

    async def stop_collection(self):
        """Stop the metrics collection loop."""
        self._stop_event.set()
        self.is_running = False
