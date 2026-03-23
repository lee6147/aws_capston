"""Text extraction step — extract text from PDF using Textract."""

import json
import logging
import os
import time

import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

s3_client = boto3.client("s3")
textract_client = boto3.client("textract")

PDF_BUCKET = os.environ.get("PDF_BUCKET", "")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Extract text from PDF using Amazon Textract.

    Input (from Step Functions):
        {
            "userId": "...",
            "documentId": "...",
            "s3Key": "...",
            "bucket": "...",
            "validation": { "valid": true, ... }
        }

    Returns:
        {
            "textLength": 12345,
            "pageCount": 10,
            "textS3Key": "userId/documentId/extracted.txt"
        }
    """
    s3_key = event["s3Key"]
    bucket = event.get("bucket", PDF_BUCKET)
    user_id = event["userId"]
    document_id = event["documentId"]

    logger.info("Extracting text from: s3://%s/%s", bucket, s3_key)

    try:
        # Start async Textract job for multi-page PDFs
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": s3_key,
                }
            }
        )
        job_id = response["JobId"]
        logger.info("Started Textract job: %s", job_id)

        # Poll for completion
        # TODO: For production, use SNS notification instead of polling
        extracted_text = _wait_for_textract_job(job_id)

        # Save extracted text to S3
        text_key = f"{user_id}/{document_id}/extracted.txt"
        s3_client.put_object(
            Bucket=bucket,
            Key=text_key,
            Body=extracted_text.encode("utf-8"),
            ContentType="text/plain; charset=utf-8",
        )

        page_count = extracted_text.count("\n--- Page") + 1 if extracted_text else 0

        logger.info(
            "Extracted %d characters, %d pages", len(extracted_text), page_count
        )

        return {
            "textLength": len(extracted_text),
            "pageCount": page_count,
            "textS3Key": text_key,
        }

    except Exception as e:
        logger.exception("Text extraction failed")
        raise RuntimeError(f"Text extraction failed: {str(e)}")


def _wait_for_textract_job(job_id: str, max_wait: int = 50) -> str:
    """Poll Textract until job completes. Returns extracted text.

    TODO: Replace polling with SNS-based notification for production.
    """
    for attempt in range(max_wait):
        response = textract_client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]

        if status == "SUCCEEDED":
            return _collect_textract_results(job_id, response)
        elif status == "FAILED":
            raise RuntimeError(
                f"Textract job failed: {response.get('StatusMessage', 'Unknown error')}"
            )

        time.sleep(1)

    raise RuntimeError("Textract job timed out")


def _collect_textract_results(job_id: str, first_response: dict) -> str:
    """Collect all pages of Textract results (handles pagination)."""
    pages_text = []
    current_page = 0
    response = first_response

    while True:
        for block in response.get("Blocks", []):
            if block["BlockType"] == "PAGE":
                current_page += 1
                pages_text.append(f"\n--- Page {current_page} ---\n")
            elif block["BlockType"] == "LINE":
                pages_text.append(block.get("Text", ""))

        next_token = response.get("NextToken")
        if not next_token:
            break

        response = textract_client.get_document_text_detection(
            JobId=job_id, NextToken=next_token
        )

    return "\n".join(pages_text)
