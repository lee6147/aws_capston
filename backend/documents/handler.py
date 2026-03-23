"""Documents CRUD handler."""

import json
import os
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger, Tracer
from boto3.dynamodb.conditions import Key

from shared.auth import get_user_id
from shared.responses import bad_request, error, not_found, success

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
s3_client = boto3.client("s3")

DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")
PDF_BUCKET = os.environ.get("PDF_BUCKET", "")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Route to appropriate CRUD operation based on HTTP method.

    GET /documents          — list all documents for the user
    GET /documents/{id}     — get a single document
    DELETE /documents/{id}  — delete a document
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    http_method = event.get("httpMethod", "GET")
    path_params = event.get("pathParameters") or {}
    document_id = path_params.get("documentId")

    if http_method == "GET" and not document_id:
        return _list_documents(user_id)
    elif http_method == "GET" and document_id:
        return _get_document(user_id, document_id)
    elif http_method == "DELETE" and document_id:
        return _delete_document(user_id, document_id)
    else:
        return bad_request(f"Unsupported method: {http_method}")


def _list_documents(user_id: str) -> dict:
    """List all documents for a user."""
    try:
        table = dynamodb.Table(DOCUMENTS_TABLE)
        response = table.query(
            KeyConditionExpression=Key("userId").eq(user_id),
            ScanIndexForward=False,  # Newest first
        )

        documents = []
        for item in response.get("Items", []):
            documents.append(
                {
                    "documentId": item["documentId"],
                    "fileName": item.get("fileName", ""),
                    "status": item.get("status", "UNKNOWN"),
                    "fileSize": item.get("fileSize", 0),
                    "createdAt": item.get("createdAt", ""),
                    "updatedAt": item.get("updatedAt", ""),
                }
            )

        return success({"documents": documents, "count": len(documents)})

    except Exception as e:
        logger.exception("Failed to list documents")
        return error(f"Failed to list documents: {str(e)}")


def _get_document(user_id: str, document_id: str) -> dict:
    """Get a single document by ID."""
    try:
        table = dynamodb.Table(DOCUMENTS_TABLE)
        response = table.get_item(
            Key={"userId": user_id, "documentId": document_id}
        )

        item = response.get("Item")
        if not item:
            return not_found("Document not found")

        return success(item)

    except Exception as e:
        logger.exception("Failed to get document %s", document_id)
        return error(f"Failed to get document: {str(e)}")


def _delete_document(user_id: str, document_id: str) -> dict:
    """Delete a document and its S3 object."""
    try:
        table = dynamodb.Table(DOCUMENTS_TABLE)

        # Get the document first to find the S3 key
        response = table.get_item(
            Key={"userId": user_id, "documentId": document_id}
        )
        item = response.get("Item")
        if not item:
            return not_found("Document not found")

        # Delete from S3
        s3_key = item.get("s3Key")
        if s3_key:
            try:
                s3_client.delete_object(Bucket=PDF_BUCKET, Key=s3_key)
            except Exception:
                logger.warning("Failed to delete S3 object %s", s3_key)

        # Delete from DynamoDB
        table.delete_item(Key={"userId": user_id, "documentId": document_id})

        logger.info("Deleted document %s for user %s", document_id, user_id)
        return success({"message": "Document deleted", "documentId": document_id})

    except Exception as e:
        logger.exception("Failed to delete document %s", document_id)
        return error(f"Failed to delete document: {str(e)}")
