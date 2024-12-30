# services/monitoring/src/core/session.py
from redis import Redis
from uuid import uuid4
import json
from datetime import timedelta

class SessionManager:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url)
        self.session_ttl = timedelta(hours=24)

    async def create_session(self, user_data: dict) -> str:
        session_id = str(uuid4())
        self.redis.setex(
            f"session:{session_id}",
            self.session_ttl,
            json.dumps(user_data)
        )
        return session_id

    async def get_session(self, session_id: str) -> dict:
        data = self.redis.get(f"session:{session_id}")
        if data:
            return json.loads(data)
        return None

    async def delete_session(self, session_id: str):
        self.redis.delete(f"session:{session_id}")

    async def refresh_session(self, session_id: str):
        data = await self.get_session(session_id)
        if data:
            self.redis.expire(f"session:{session_id}", self.session_ttl)
            return True
        return False
