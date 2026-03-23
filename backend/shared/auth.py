"""Cognito token validation helper.

When using API Gateway with a Cognito Authorizer, the token is already
validated by the time the Lambda is invoked. This module extracts user
information from the request context provided by API Gateway.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def get_user_id(event: dict) -> Optional[str]:
    """Extract the authenticated user ID (Cognito sub) from API Gateway event.

    The Cognito authorizer places claims in
    event['requestContext']['authorizer']['claims'].

    Returns:
        The Cognito 'sub' claim (user ID), or None if not found.
    """
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        user_id = claims.get("sub")
        if not user_id:
            logger.warning("No 'sub' claim found in authorizer context")
        return user_id
    except (KeyError, TypeError):
        logger.warning("Could not extract user claims from event")
        return None


def get_user_email(event: dict) -> Optional[str]:
    """Extract the authenticated user's email from API Gateway event."""
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        return claims.get("email")
    except (KeyError, TypeError):
        return None
