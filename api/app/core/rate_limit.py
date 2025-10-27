"""Rate limiting middleware."""

from typing import Callable
from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from collections import defaultdict
import time

# Simple in-memory rate limit storage
# In production, use Redis for distributed rate limiting
_rate_limit_storage = defaultdict(list)


def rate_limit(
    calls: int = 60, period: int = 60, per_user: bool = False
) -> Callable[[Request], None]:
    """
    Rate limiting middleware.

    Args:
        calls: Maximum number of calls allowed
        period: Time period in seconds
        per_user: If True, rate limit per user; otherwise, per IP

    Returns:
        Middleware function
    """

    def rate_limit_middleware(request: Request):
        # Get identifier (user ID or IP address)
        if per_user and hasattr(request.state, "user"):
            identifier = str(request.state.user.id)
        else:
            identifier = request.client.host or "unknown"

        # Get current time
        now = datetime.utcnow()

        # Clean old entries
        cutoff_time = now - timedelta(seconds=period)
        _rate_limit_storage[identifier] = [
            timestamp for timestamp in _rate_limit_storage[identifier] if timestamp > cutoff_time
        ]

        # Check if limit exceeded
        if len(_rate_limit_storage[identifier]) >= calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {calls} requests per {period} seconds.",
                headers={"Retry-After": str(period)},
            )

        # Record this request
        _rate_limit_storage[identifier].append(now)

    return rate_limit_middleware


# Pre-configured rate limiters
def create_rate_limiter(calls: int, period: int, per_user: bool = False):
    """
    Create a rate limiter with specific configuration.

    Args:
        calls: Maximum number of calls allowed
        period: Time period in seconds
        per_user: If True, rate limit per user; otherwise, per IP
    """
    return rate_limit(calls=calls, period=period, per_user=per_user)


# Common rate limiters
auth_rate_limiter = create_rate_limiter(calls=5, period=300)  # 5 calls per 5 minutes
swipe_rate_limiter = create_rate_limiter(calls=100, period=60)  # 100 swipes per minute
api_rate_limiter = create_rate_limiter(calls=1000, period=3600)  # 1000 calls per hour
