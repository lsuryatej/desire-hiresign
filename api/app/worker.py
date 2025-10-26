"""Background worker for processing tasks."""

import os
import redis
from rq import Worker, Queue
from app.core.config import settings

# Initialize Redis connection
redis_conn = redis.from_url(settings.redis_queue_url)

# Create queues
task_queue = Queue("default", connection=redis_conn)
