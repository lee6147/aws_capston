"""Standard API response helpers with CORS headers."""

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

CORS_HEADERS = {
    "Access-Control-Allow-Origin": _ALLOWED_ORIGIN,
    "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    "Content-Type": "application/json",
}


def success(body: Any, status_code: int = 200) -> dict:
    """Return a successful API Gateway response."""
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body, ensure_ascii=False, default=str),
    }


def created(body: Any) -> dict:
    """Return a 201 Created response."""
    return success(body, status_code=201)


def error(message: str, status_code: int = 500, details: Any = None) -> dict:
    """Return an error API Gateway response."""
    error_body = {"error": message}
    if details:
        error_body["details"] = details

    logger.error("API error %d: %s", status_code, message)

    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(error_body, ensure_ascii=False, default=str),
    }


def bad_request(message: str = "Bad request") -> dict:
    return error(message, status_code=400)


def not_found(message: str = "Resource not found") -> dict:
    return error(message, status_code=404)


def unauthorized(message: str = "Unauthorized") -> dict:
    return error(message, status_code=401)
