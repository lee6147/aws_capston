"""Bedrock client wrapper for RAG and embedding operations."""

import json
import logging
import os
from typing import Any

import boto3

logger = logging.getLogger(__name__)

# Clients are created at module level for Lambda container reuse
_bedrock_runtime = None
_bedrock_agent_runtime = None


def _get_bedrock_runtime():
    global _bedrock_runtime
    if _bedrock_runtime is None:
        _bedrock_runtime = boto3.client("bedrock-runtime")
    return _bedrock_runtime


def _get_bedrock_agent_runtime():
    global _bedrock_agent_runtime
    if _bedrock_agent_runtime is None:
        _bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")
    return _bedrock_agent_runtime


def retrieve_and_generate(
    query: str,
    knowledge_base_id: str,
    model_id: str | None = None,
    max_results: int = 5,
    session_id: str | None = None,
) -> dict[str, Any]:
    """Query Bedrock Knowledge Base with RetrieveAndGenerate.

    Args:
        query: The user's question.
        knowledge_base_id: The Bedrock Knowledge Base ID.
        model_id: Foundation model ARN. Defaults to env var BEDROCK_MODEL_ID.
        max_results: Number of retrieval results.
        session_id: Optional session ID for multi-turn conversation.

    Returns:
        Dict with 'answer', 'citations', and 'session_id'.
    """
    client = _get_bedrock_agent_runtime()
    model = model_id or os.environ.get(
        "BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
    )

    # Build the model ARN
    region = os.environ.get("AWS_REGION", "ap-northeast-2")
    model_arn = f"arn:aws:bedrock:{region}::foundation-model/{model}"

    params = {
        "input": {"text": query},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": knowledge_base_id,
                "modelArn": model_arn,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": max_results,
                    }
                },
            },
        },
    }

    if session_id:
        params["sessionId"] = session_id

    logger.info("RetrieveAndGenerate query: %s", query[:100])
    response = client.retrieve_and_generate(**params)

    # Extract citations
    citations = []
    for citation in response.get("citations", []):
        for ref in citation.get("retrievedReferences", []):
            citations.append(
                {
                    "text": ref.get("content", {}).get("text", "")[:200],
                    "source": ref.get("location", {})
                    .get("s3Location", {})
                    .get("uri", ""),
                }
            )

    return {
        "answer": response.get("output", {}).get("text", ""),
        "citations": citations,
        "session_id": response.get("sessionId", ""),
    }


def generate_embedding(text: str, model_id: str | None = None) -> list[float]:
    """Generate an embedding vector using Bedrock Titan.

    Args:
        text: The text to embed.
        model_id: Embedding model ID. Defaults to env var EMBEDDING_MODEL_ID.

    Returns:
        List of floats representing the embedding vector.
    """
    client = _get_bedrock_runtime()
    model = model_id or os.environ.get(
        "EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"
    )

    response = client.invoke_model(
        modelId=model,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": text}),
    )

    result = json.loads(response["body"].read())
    return result["embedding"]


def invoke_model(prompt: str, model_id: str | None = None, max_tokens: int = 2048) -> str:
    """Invoke a Bedrock model directly (without RAG).

    Args:
        prompt: The prompt text.
        model_id: Model ID. Defaults to env var BEDROCK_MODEL_ID.
        max_tokens: Maximum tokens in the response.

    Returns:
        The model's response text.
    """
    client = _get_bedrock_runtime()
    model = model_id or os.environ.get(
        "BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
    )

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
    )

    response = client.invoke_model(
        modelId=model,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
