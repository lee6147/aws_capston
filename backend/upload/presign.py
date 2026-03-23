"""Generate presigned URL for S3 PDF upload."""

import json
import logging
import os
import re
import uuid
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger, Tracer

# Use shared modules via layer
from shared.auth import get_user_id
from shared.responses import bad_request, error, success

logger = Logger()
tracer = Tracer()

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

PDF_BUCKET = os.environ.get("PDF_BUCKET", "")
DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Generate a presigned S3 PUT URL for uploading a PDF.

    Expects JSON body:
        {
            "fileName": "lecture-notes.pdf",
            "contentType": "application/pdf",
            "fileSize": 1048576
        }

    Returns:
        {
            "uploadUrl": "https://s3.amazonaws.com/...",
            "documentId": "uuid",
            "s3Key": "userId/documentId/filename.pdf"
        }
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return bad_request("Invalid JSON body")

    file_name = body.get("fileName")
    content_type = body.get("contentType", "application/pdf")
    file_size = body.get("fileSize", 0)

    if not file_name:
        return bad_request("fileName is required")

    # Validate file type
    if not file_name.lower().endswith(".pdf"):
        return bad_request("Only PDF files are supported")

    # Validate file size (max 10MB — matches frontend and project spec)
    max_size = 10 * 1024 * 1024
    if file_size > max_size:
        return bad_request(f"File size exceeds maximum of {max_size // (1024*1024)}MB")

    document_id = str(uuid.uuid4())
    safe_name = re.sub(r'[^\w\-.]', '_', file_name)
    s3_key = f"{user_id}/{document_id}/{safe_name}"

    try:
        # Generate presigned URL (valid for 5 minutes)
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": PDF_BUCKET,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=300,
        )

        # Create document record with PENDING status
        table = dynamodb.Table(DOCUMENTS_TABLE)
        table.put_item(
            Item={
                "userId": user_id,
                "documentId": document_id,
                "fileName": file_name,
                "s3Key": s3_key,
                "contentType": content_type,
                "fileSize": file_size,
                "status": "PENDING_UPLOAD",
                "createdAt": datetime.utcnow().isoformat(),
                "updatedAt": datetime.utcnow().isoformat(),
            }
        )

        logger.info("Generated presigned URL for document %s", document_id)

        return success(
            {
                "uploadUrl": presigned_url,
                "documentId": document_id,
                "s3Key": s3_key,
            }
        )

    except Exception as e:
        logger.exception("Failed to generate presigned URL")
        return error("Failed to generate upload URL")
