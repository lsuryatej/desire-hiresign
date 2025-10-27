"""Monitoring and metrics utilities."""

import time
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


# Simple metrics storage (in production, use Prometheus)
metrics = {
    "requests_total": 0,
    "requests_by_status": {},
    "requests_by_endpoint": {},
    "response_time_avg": 0,
}


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to track API metrics."""

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate response time
        process_time = time.time() - start_time

        # Update metrics
        metrics["requests_total"] += 1
        status = response.status_code

        # Track by status
        if status not in metrics["requests_by_status"]:
            metrics["requests_by_status"][status] = 0
        metrics["requests_by_status"][status] += 1

        # Track by endpoint
        path = request.url.path
        if path not in metrics["requests_by_endpoint"]:
            metrics["requests_by_endpoint"][path] = 0
        metrics["requests_by_endpoint"][path] += 1

        # Update average response time
        current_avg = metrics.get("response_time_avg", 0)
        total = metrics.get("requests_total", 1)
        metrics["response_time_avg"] = (current_avg * (total - 1) + process_time) / total

        # Add header
        response.headers["X-Process-Time"] = str(process_time)

        return response


def get_metrics_summary():
    """Get metrics summary for monitoring."""
    return {
        "total_requests": metrics.get("requests_total", 0),
        "requests_by_status": metrics.get("requests_by_status", {}),
        "requests_by_endpoint": metrics.get("requests_by_endpoint", {}),
        "average_response_time": f"{metrics.get('response_time_avg', 0):.4f}s",
    }
