"""Korean-aware text chunking step.

Splits extracted text into overlapping chunks suitable for embedding.
Uses sentence-level boundaries that respect Korean grammar.
"""

import json
import logging
import os
import re

import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

s3_client = boto3.client("s3")

PDF_BUCKET = os.environ.get("PDF_BUCKET", "")

# Chunking configuration
CHUNK_SIZE = 500       # Target tokens per chunk (approximate)
CHUNK_OVERLAP = 100    # Overlap tokens between consecutive chunks
CHARS_PER_TOKEN = 3.5  # Rough estimate for Korean text (Korean chars ~ 2-4 tokens each)

# Target characters per chunk (derived from token estimates)
CHUNK_CHARS = int(CHUNK_SIZE * CHARS_PER_TOKEN)
OVERLAP_CHARS = int(CHUNK_OVERLAP * CHARS_PER_TOKEN)

# Korean sentence-ending patterns
SENTENCE_ENDINGS = re.compile(
    r"(?<=[.!?。？！])\s+"       # Standard punctuation
    r"|(?<=다[.!?])\s+"          # Korean declarative ending (e.g., ~합니다.)
    r"|(?<=요[.!?])\s+"          # Korean polite ending (e.g., ~해요.)
    r"|(?<=\n)\s*"               # Newlines
)


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Chunk extracted text into overlapping segments.

    Input (from Step Functions):
        {
            "userId": "...",
            "documentId": "...",
            "s3Key": "...",
            "bucket": "...",
            "extraction": { "textS3Key": "...", ... }
        }

    Returns:
        {
            "chunkCount": 25,
            "chunksS3Key": "userId/documentId/chunks.json"
        }
    """
    user_id = event["userId"]
    document_id = event["documentId"]
    bucket = event.get("bucket", PDF_BUCKET)
    text_s3_key = event["extraction"]["textS3Key"]

    logger.info("Chunking text from: s3://%s/%s", bucket, text_s3_key)

    # Read extracted text from S3
    response = s3_client.get_object(Bucket=bucket, Key=text_s3_key)
    full_text = response["Body"].read().decode("utf-8")

    if not full_text.strip():
        raise ValueError("Extracted text is empty")

    # Split into sentences first
    sentences = _split_sentences(full_text)

    # Build overlapping chunks from sentences
    chunks = _build_chunks(sentences)

    # Add metadata to each chunk
    chunk_records = []
    for i, chunk_text in enumerate(chunks):
        chunk_records.append(
            {
                "chunkId": f"{document_id}-chunk-{i:04d}",
                "documentId": document_id,
                "userId": user_id,
                "chunkIndex": i,
                "text": chunk_text,
                "charCount": len(chunk_text),
            }
        )

    # Save chunks to S3 as JSON
    chunks_key = f"{user_id}/{document_id}/chunks.json"
    s3_client.put_object(
        Bucket=bucket,
        Key=chunks_key,
        Body=json.dumps(chunk_records, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json; charset=utf-8",
    )

    logger.info("Created %d chunks from %d characters", len(chunks), len(full_text))

    return {
        "chunkCount": len(chunks),
        "chunksS3Key": chunks_key,
    }


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences, respecting Korean grammar."""
    # Remove page markers
    text = re.sub(r"\n--- Page \d+ ---\n", "\n", text)

    # Split on sentence endings
    raw_sentences = SENTENCE_ENDINGS.split(text)

    # Filter out empty strings and strip whitespace
    sentences = [s.strip() for s in raw_sentences if s.strip()]
    return sentences


def _build_chunks(sentences: list[str]) -> list[str]:
    """Build overlapping chunks from sentences.

    Each chunk targets ~CHUNK_CHARS characters with OVERLAP_CHARS overlap.
    """
    if not sentences:
        return []

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        # If a single sentence exceeds chunk size, split it further
        if sentence_len > CHUNK_CHARS:
            # Flush current chunk
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            # Split long sentence by character boundaries
            for start in range(0, sentence_len, CHUNK_CHARS - OVERLAP_CHARS):
                sub = sentence[start : start + CHUNK_CHARS]
                chunks.append(sub)

            current_chunk = []
            current_length = 0
            continue

        # If adding this sentence would exceed the limit, start new chunk
        if current_length + sentence_len > CHUNK_CHARS and current_chunk:
            chunks.append(" ".join(current_chunk))

            # Overlap: carry over the last few sentences
            overlap_chunk = []
            overlap_length = 0
            for prev in reversed(current_chunk):
                if overlap_length + len(prev) > OVERLAP_CHARS:
                    break
                overlap_chunk.insert(0, prev)
                overlap_length += len(prev)

            current_chunk = overlap_chunk
            current_length = overlap_length

        current_chunk.append(sentence)
        current_length += sentence_len

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
