import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
from app.config.setting_config import settings
from app.config import redis_config as redis_config_module

EXEMPT_PATHS='{"/docs": "Docs", "/openapi.json": "OpenAPI", "/redoc": "Redoc", "/favicon.ico": "Favicon"}'

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce rate limiting based on client IP"""

    async def dispatch(self, request: Request, call_next):

        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        if redis_config_module.redis_client is None:
            return Response(
                "Internal Server Error: Redis not available", status_code=500
            )

        client_ip = request.client.host if request.client else "unknown"

        current_window = (
            int(time.time() / settings.rate_limit_window) * settings.rate_limit_window
        )

        key = f"rate_limit:{client_ip}:{current_window}"

        count = await redis_config_module.redis_client.incr(key)

        if count == 1:
            await redis_config_module.redis_client.expire(key, settings.rate_limit_window)

        if count > settings.rate_limit_count:
            return Response(
                status_code=429,
                content='{"detail": "Too many requests"}',
                headers={"Retry-After": str(settings.rate_limit_window)},
                media_type="application/json",
            )
        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_count)
        response.headers["X-RateLimit-Remaining"] = str(
            settings.rate_limit_count - count
        )
        response.headers["X-RateLimit-Reset"] = str(
            current_window + settings.rate_limit_window
        )
        return response
