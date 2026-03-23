"""Amazon Polly text-to-speech handler."""

import base64
import json
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared.auth import get_user_id
from shared.responses import bad_request, error

logger = Logger()
tracer = Tracer()

polly_client = boto3.client("polly")

# Korean voice: Seoyeon; English voice: Joanna
VOICE_MAP = {
    "ko": "Seoyeon",
    "en": "Joanna",
}

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
}


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Synthesize speech from text using Amazon Polly.

    Expects JSON body:
        {
            "text": "Text to convert to speech",
            "language": "ko",       (optional, default: "ko")
            "engine": "neural"      (optional, default: "neural")
        }

    Returns:
        Audio content as base64-encoded MP3 in the response body.
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return bad_request("Invalid JSON body")

    text = body.get("text", "").strip()
    language = body.get("language", "ko")
    engine = body.get("engine", "neural")

    if not text:
        return bad_request("text is required")

    if len(text) > 3000:
        return bad_request("Text is too long (max 3000 characters)")

    voice_id = VOICE_MAP.get(language, "Seoyeon")

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId=voice_id,
            Engine=engine,
            LanguageCode=f"{language}-KR" if language == "ko" else f"{language}-US",
        )

        audio_stream = response["AudioStream"].read()
        audio_base64 = base64.b64encode(audio_stream).decode("utf-8")

        logger.info(
            "Synthesized %d chars with voice %s for user %s",
            len(text),
            voice_id,
            user_id,
        )

        return {
            "statusCode": 200,
            "headers": {
                **CORS_HEADERS,
                "Content-Type": "audio/mpeg",
            },
            "body": audio_base64,
            "isBase64Encoded": True,
        }

    except Exception as e:
        logger.exception("Polly synthesis failed")
        return error(f"Failed to synthesize speech: {str(e)}")
