"""Chat handler — RAG query via Bedrock RetrieveAndGenerate."""

import json
import os
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared.auth import get_user_id
from shared.bedrock import retrieve_and_generate
from shared.responses import bad_request, error, success

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
CHAT_HISTORY_TABLE = os.environ.get("CHAT_HISTORY_TABLE", "")
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Process a chat message using RAG.

    Expects JSON body:
        {
            "message": "What is machine learning?",
            "sessionId": "optional-session-id-for-multi-turn"
        }

    Returns:
        {
            "answer": "Machine learning is...",
            "citations": [...],
            "sessionId": "session-id"
        }
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return bad_request("Invalid JSON body")

    message = body.get("message", "").strip()
    session_id = body.get("sessionId")

    if not message:
        return bad_request("message is required")

    if len(message) > 2000:
        return bad_request("Message is too long (max 2000 characters)")

    try:
        # Query Bedrock Knowledge Base
        result = retrieve_and_generate(
            query=message,
            knowledge_base_id=KNOWLEDGE_BASE_ID,
            session_id=session_id,
        )

        # Save to chat history
        now = datetime.utcnow().isoformat()
        table = dynamodb.Table(CHAT_HISTORY_TABLE)
        table.put_item(
            Item={
                "userId": user_id,
                "timestamp": now,
                "message": message,
                "answer": result["answer"],
                "citations": result["citations"],
                "sessionId": result["session_id"],
            }
        )

        logger.info("Chat response generated for user %s", user_id)

        return success(
            {
                "answer": result["answer"],
                "citations": result["citations"],
                "sessionId": result["session_id"],
            }
        )

    except Exception as e:
        logger.exception("Chat query failed")
        return error("Failed to process chat message")
