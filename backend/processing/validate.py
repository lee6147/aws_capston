"""PDF validation step — validates file exists, is a real PDF, and checks size limits."""

import logging
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

PDF_BUCKET = os.environ.get("PDF_BUCKET", "")
DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
PDF_MAGIC_BYTES = b"%PDF"


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Validate the uploaded PDF file.

    Input (from Step Functions):
        {
            "userId": "...",
            "documentId": "...",
            "s3Key": "...",
            "bucket": "..."
        }

    Returns:
        {
            "valid": true,
            "fileSize": 1234567,
            "contentType": "application/pdf"
        }

    Raises:
        ValueError: If the PDF is invalid.
    """
    s3_key = event["s3Key"]
    bucket = event.get("bucket", PDF_BUCKET)
    user_id = event["userId"]
    document_id = event["documentId"]

    logger.info("Validating PDF: s3://%s/%s", bucket, s3_key)

    try:
        # Check if file exists and get metadata
        head_response = s3_client.head_object(Bucket=bucket, Key=s3_key)
        file_size = head_response["ContentLength"]
        content_type = head_response.get("ContentType", "")

        # Check file size
        if file_size > MAX_FILE_SIZE:
            _update_status(user_id, document_id, "FAILED", "File too large")
            raise ValueError(
                f"File size {file_size} exceeds maximum {MAX_FILE_SIZE} bytes"
            )

        if file_size == 0:
            _update_status(user_id, document_id, "FAILED", "Empty file")
            raise ValueError("File is empty")

        # Read first 4 bytes to check PDF magic number
        range_response = s3_client.get_object(
            Bucket=bucket, Key=s3_key, Range="bytes=0-3"
        )
        first_bytes = range_response["Body"].read()

        if not first_bytes.startswith(PDF_MAGIC_BYTES):
            _update_status(user_id, document_id, "FAILED", "Not a valid PDF")
            raise ValueError("File does not appear to be a valid PDF")

        _update_status(user_id, document_id, "VALIDATING")

        logger.info("PDF validation passed: %d bytes", file_size)
        return {
            "valid": True,
            "fileSize": file_size,
            "contentType": content_type,
        }

    except ValueError:
        raise
    except Exception as e:
        _update_status(user_id, document_id, "FAILED", str(e))
        raise ValueError(f"Validation failed: {str(e)}")


def _update_status(user_id: str, document_id: str, status: str, error_msg: str = ""):
    """Update the document status in DynamoDB."""
    from datetime import datetime

    table = dynamodb.Table(DOCUMENTS_TABLE)
    update_expr = "SET #status = :status, updatedAt = :now"
    expr_values = {
        ":status": status,
        ":now": datetime.utcnow().isoformat(),
    }

    if error_msg:
        update_expr += ", errorMessage = :err"
        expr_values[":err"] = error_msg

    table.update_item(
        Key={"userId": user_id, "documentId": document_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues=expr_values,
    )
