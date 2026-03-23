"""Embedding step — generate vector embeddings for text chunks via Bedrock Titan."""

import json
import logging
import os
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared.bedrock import generate_embedding

logger = Logger()
tracer = Tracer()

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

PDF_BUCKET = os.environ.get("PDF_BUCKET", "")
DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")
EMBEDDING_MODEL_ID = os.environ.get("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Generate embeddings for each text chunk and store them.

    Input (from Step Functions):
        {
            "userId": "...",
            "documentId": "...",
            "s3Key": "...",
            "bucket": "...",
            "chunking": { "chunkCount": 25, "chunksS3Key": "..." }
        }

    Returns:
        {
            "embeddedCount": 25,
            "embeddingsS3Key": "userId/documentId/embeddings.json"
        }

    The embeddings are stored in S3 in a format compatible with
    Bedrock Knowledge Base S3 vector ingestion.
    """
    user_id = event["userId"]
    document_id = event["documentId"]
    bucket = event.get("bucket", PDF_BUCKET)
    chunks_s3_key = event["chunking"]["chunksS3Key"]

    logger.info("Embedding chunks from: s3://%s/%s", bucket, chunks_s3_key)

    # Load chunks from S3
    response = s3_client.get_object(Bucket=bucket, Key=chunks_s3_key)
    chunks = json.loads(response["Body"].read().decode("utf-8"))

    if not chunks:
        raise ValueError("No chunks to embed")

    # Generate embeddings for each chunk
    embedded_chunks = []
    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        if not text.strip():
            continue

        try:
            embedding = generate_embedding(text)
            embedded_chunks.append(
                {
                    **chunk,
                    "embedding": embedding,
                    "embeddingModel": EMBEDDING_MODEL_ID,
                    "embeddedAt": datetime.utcnow().isoformat(),
                }
            )
        except Exception as e:
            logger.warning("Failed to embed chunk %d: %s", i, str(e))
            # Continue with other chunks instead of failing entirely
            continue

        if (i + 1) % 10 == 0:
            logger.info("Embedded %d / %d chunks", i + 1, len(chunks))

    # Save embeddings to S3
    embeddings_key = f"{user_id}/{document_id}/embeddings.json"
    s3_client.put_object(
        Bucket=bucket,
        Key=embeddings_key,
        Body=json.dumps(embedded_chunks, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json; charset=utf-8",
    )

    # Update document status to READY
    table = dynamodb.Table(DOCUMENTS_TABLE)
    table.update_item(
        Key={"userId": user_id, "documentId": document_id},
        UpdateExpression=(
            "SET #status = :status, updatedAt = :now, "
            "chunkCount = :chunks, embeddingCount = :embeds"
        ),
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={
            ":status": "READY",
            ":now": datetime.utcnow().isoformat(),
            ":chunks": len(chunks),
            ":embeds": len(embedded_chunks),
        },
    )

    logger.info(
        "Embedded %d / %d chunks for document %s",
        len(embedded_chunks),
        len(chunks),
        document_id,
    )

    return {
        "embeddedCount": len(embedded_chunks),
        "embeddingsS3Key": embeddings_key,
    }
