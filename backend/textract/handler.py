"""Amazon Textract OCR handler for image processing."""

import json
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared.auth import get_user_id
from shared.responses import bad_request, error, success

logger = Logger()
tracer = Tracer()

textract_client = boto3.client("textract")
s3_client = boto3.client("s3")

PDF_BUCKET = os.environ.get("PDF_BUCKET", "")
DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Analyze an image or document page with Textract OCR.

    Expects JSON body:
        {
            "s3Key": "userId/documentId/page.png",
            "features": ["TABLES", "FORMS"]    (optional)
        }

    Returns:
        {
            "text": "Extracted text content...",
            "blocks": [...],
            "confidence": 98.5
        }
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return bad_request("Invalid JSON body")

    s3_key = body.get("s3Key", "").strip()
    features = body.get("features", [])

    if not s3_key:
        return bad_request("s3Key is required")

    # Ensure the user can only access their own files
    if not s3_key.startswith(f"{user_id}/"):
        return bad_request("Access denied: you can only analyze your own documents")

    try:
        document_location = {
            "S3Object": {
                "Bucket": PDF_BUCKET,
                "Name": s3_key,
            }
        }

        if features:
            # Use AnalyzeDocument for tables/forms
            response = textract_client.analyze_document(
                Document=document_location,
                FeatureTypes=features,
            )
        else:
            # Use DetectDocumentText for simple OCR
            response = textract_client.detect_document_text(
                Document=document_location
            )

        # Extract text from LINE blocks
        lines = []
        total_confidence = 0.0
        line_count = 0

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                lines.append(block.get("Text", ""))
                total_confidence += block.get("Confidence", 0)
                line_count += 1

        extracted_text = "\n".join(lines)
        avg_confidence = total_confidence / line_count if line_count > 0 else 0

        logger.info(
            "Extracted %d lines from %s (avg confidence: %.1f%%)",
            line_count,
            s3_key,
            avg_confidence,
        )

        return success(
            {
                "text": extracted_text,
                "lineCount": line_count,
                "confidence": round(avg_confidence, 2),
            }
        )

    except Exception as e:
        logger.exception("Textract analysis failed for %s", s3_key)
        return error(f"Failed to analyze document: {str(e)}")
