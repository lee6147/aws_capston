"""Trigger Step Functions workflow after PDF upload completion."""

import json
import logging
import os
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared.auth import get_user_id
from shared.responses import bad_request, error, success

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
sfn_client = boto3.client("stepfunctions")

DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")
STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN", "")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Mark upload as complete and start PDF processing pipeline.

    Expects JSON body:
        {
            "documentId": "uuid",
            "s3Key": "userId/documentId/filename.pdf"
        }

    Returns:
        {
            "documentId": "uuid",
            "executionArn": "arn:aws:states:..."
        }
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return bad_request("Invalid JSON body")

    document_id = body.get("documentId")
    s3_key = body.get("s3Key")

    if not document_id or not s3_key:
        return bad_request("documentId and s3Key are required")

    try:
        # Update document status
        table = dynamodb.Table(DOCUMENTS_TABLE)
        table.update_item(
            Key={"userId": user_id, "documentId": document_id},
            UpdateExpression="SET #status = :status, updatedAt = :now",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "PROCESSING",
                ":now": datetime.utcnow().isoformat(),
            },
        )

        # Start Step Functions execution
        execution = sfn_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=f"pdf-{document_id}",
            input=json.dumps(
                {
                    "userId": user_id,
                    "documentId": document_id,
                    "s3Key": s3_key,
                    "bucket": os.environ.get("PDF_BUCKET", ""),
                }
            ),
        )

        logger.info(
            "Started processing for document %s, execution: %s",
            document_id,
            execution["executionArn"],
        )

        return success(
            {
                "documentId": document_id,
                "executionArn": execution["executionArn"],
                "status": "PROCESSING",
            }
        )

    except Exception as e:
        logger.exception("Failed to trigger processing pipeline")
        return error(f"Failed to start processing: {str(e)}")
