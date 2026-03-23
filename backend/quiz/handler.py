"""Quiz generation handler — generate quizzes from document chunks via Bedrock."""

import json
import os
import uuid
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared.auth import get_user_id
from shared.bedrock import invoke_model
from shared.responses import bad_request, error, success

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
bedrock_agent = boto3.client("bedrock-agent-runtime")

QUIZ_RESULTS_TABLE = os.environ.get("QUIZ_RESULTS_TABLE", "")
DOCUMENTS_TABLE = os.environ.get("DOCUMENTS_TABLE", "")
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")


QUIZ_PROMPT_TEMPLATE = """You are a quiz generator for Korean university students.
Based on the following study material, generate {count} multiple-choice questions.

Study Material:
{context}

Topic: {topic}
Difficulty: {difficulty}

Return the quiz as a JSON array with this structure:
[
  {{
    "question": "Question text (in Korean if the source material is Korean)",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correctAnswer": "A",
    "explanation": "Brief explanation of the correct answer"
  }}
]

Return ONLY the JSON array, no other text."""


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """Generate a quiz from knowledge base content.

    Expects JSON body:
        {
            "topic": "machine learning basics",
            "documentId": "optional-uuid",
            "count": 5,
            "difficulty": "medium"
        }

    Returns:
        {
            "quizId": "uuid",
            "questions": [...]
        }
    """
    user_id = get_user_id(event)
    if not user_id:
        return bad_request("Could not identify user")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return bad_request("Invalid JSON body")

    topic = body.get("topic", "").strip()
    count = min(body.get("count", 5), 10)  # Max 10 questions
    difficulty = body.get("difficulty", "medium")

    if not topic:
        return bad_request("topic is required")

    if difficulty not in ("easy", "medium", "hard"):
        return bad_request("difficulty must be one of: easy, medium, hard")

    try:
        # Step 1: Retrieve relevant chunks from knowledge base
        retrieval_response = bedrock_agent.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": topic},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": 5}
            },
        )

        # Combine retrieved chunks as context
        chunks = retrieval_response.get("retrievalResults", [])
        context = "\n\n---\n\n".join(
            chunk.get("content", {}).get("text", "") for chunk in chunks
        )

        if not context.strip():
            return bad_request(
                "No relevant content found for this topic. "
                "Please upload study materials first."
            )

        # Step 2: Generate quiz using Bedrock
        prompt = QUIZ_PROMPT_TEMPLATE.format(
            count=count, context=context, topic=topic, difficulty=difficulty
        )

        response_text = invoke_model(prompt)

        # Step 3: Parse the generated quiz
        # TODO: Add more robust JSON parsing (handle markdown code blocks, etc.)
        questions = json.loads(response_text)

        # Step 4: Save quiz result
        quiz_id = str(uuid.uuid4())
        table = dynamodb.Table(QUIZ_RESULTS_TABLE)
        table.put_item(
            Item={
                "userId": user_id,
                "quizId": quiz_id,
                "topic": topic,
                "difficulty": difficulty,
                "questions": questions,
                "score": None,  # Set when user submits answers
                "createdAt": datetime.utcnow().isoformat(),
            }
        )

        logger.info("Generated quiz %s with %d questions", quiz_id, len(questions))

        return success({"quizId": quiz_id, "questions": questions})

    except json.JSONDecodeError:
        logger.exception("Failed to parse quiz JSON from model response")
        return error("Failed to generate valid quiz. Please try again.")
    except Exception as e:
        logger.exception("Quiz generation failed")
        return error(f"Failed to generate quiz: {str(e)}")
