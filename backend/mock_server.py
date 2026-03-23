"""
Mock API server for the StudyBot RAG chatbot prototype.
Simulates all backend endpoints that the frontend expects.

Run:
    python mock_server.py
    # or
    uvicorn mock_server:app --host 0.0.0.0 --port 3001 --reload
"""

import asyncio
import copy
import uuid
from random import choice, random

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from mock_data import (
    MOCK_CHAT_RESPONSES,
    MOCK_DASHBOARD_STATS,
    MOCK_DOCUMENTS,
    MOCK_QUIZ,
)

app = FastAPI(title="StudyBot Mock Server", version="0.1.0")

# CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory state
# ---------------------------------------------------------------------------
documents: list[dict] = copy.deepcopy(MOCK_DOCUMENTS)
pending_uploads: dict[str, str] = {}  # document_id -> filename


# ---------------------------------------------------------------------------
# Keyword-based response matching
# ---------------------------------------------------------------------------
KEYWORD_MAP: list[tuple[list[str], int]] = [
    (["lambda", "람다", "서버리스"], 0),
    (["s3", "스토리지", "저장"], 1),
    (["vpc", "네트워크", "서브넷"], 2),
    (["iam", "권한", "보안", "인증"], 3),
    (["dynamo", "데이터베이스", "nosql"], 4),
    (["cloudfront", "cdn", "캐시"], 5),
    (["요약", "핵심", "정리"], 6),
    (["bedrock", "rag", "ai", "챗봇"], 7),
]


def match_response(message: str) -> dict:
    """Return the best matching mock response based on keywords in message."""
    msg_lower = message.lower()
    for keywords, index in KEYWORD_MAP:
        if any(kw in msg_lower for kw in keywords):
            return copy.deepcopy(MOCK_CHAT_RESPONSES[index])
    return copy.deepcopy(choice(MOCK_CHAT_RESPONSES))


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------
@app.get("/api/documents")
async def list_documents():
    return documents


@app.post("/api/documents/upload")
async def upload_document(request: Request):
    body = await request.json()
    file_name = body.get("fileName", "unknown.pdf")
    document_id = str(uuid.uuid4())
    mock_key = str(uuid.uuid4())
    pending_uploads[document_id] = file_name

    base = str(request.base_url).rstrip("/")
    return {
        "uploadUrl": f"{base}/api/upload/{mock_key}",
        "documentId": document_id,
    }


@app.put("/api/upload/{key}")
async def presigned_upload(key: str, request: Request):
    # Accept the file body and discard it (mock)
    await request.body()
    return JSONResponse(status_code=200, content={"message": "Upload successful"})


@app.post("/api/documents/{document_id}/confirm")
async def confirm_document(document_id: str):
    file_name = pending_uploads.pop(document_id, f"document_{document_id[:8]}.pdf")
    # Create a new document record in memory
    new_doc = {
        "id": document_id,
        "name": file_name,
        "size": int(random() * 5_000_000) + 500_000,
        "pages": int(random() * 50) + 5,
        "status": "processing",
        "uploadedAt": "2026-03-19T00:00:00Z",
    }
    documents.insert(0, new_doc)
    asyncio.create_task(auto_ready(document_id))
    return {"status": "processing", "documentId": document_id}


async def auto_ready(document_id: str):
    """Transition document status from 'processing' to 'ready' after a delay."""
    await asyncio.sleep(5)
    for doc in documents:
        if doc["id"] == document_id:
            doc["status"] = "ready"
            break


@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    idx = next((i for i, d in enumerate(documents) if d["id"] == document_id), None)
    if idx is not None:
        documents.pop(idx)
    return {"success": True}


@app.get("/api/documents/{document_id}/status")
async def document_status(document_id: str):
    for doc in documents:
        if doc["id"] == document_id:
            return {"status": doc["status"]}
    return {"status": "ready"}


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------
@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    conversation_id = body.get("conversationId") or str(uuid.uuid4())

    # Simulate RAG latency (500–1000 ms)
    await asyncio.sleep(0.5 + random() * 0.5)

    message = body.get("message", "")
    if len(message) > 2000:
        return JSONResponse(status_code=400, content={"error": "Message is too long (max 2000 characters)"})
    response = match_response(message)
    response["conversationId"] = conversation_id
    return response


@app.get("/api/chat/{conversation_id}/history")
async def chat_history(conversation_id: str):
    return {"messages": []}


# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------
@app.post("/api/quiz/generate")
async def generate_quiz(request: Request):
    body = await request.json()
    quiz = copy.deepcopy(MOCK_QUIZ)
    quiz["quizId"] = str(uuid.uuid4())
    quiz["documentId"] = body.get("documentId")
    return quiz


@app.post("/api/quiz/answer")
async def submit_answer(request: Request):
    body = await request.json()
    question_index = body.get("questionIndex", 0)
    user_answer = body.get("answer", -1)

    questions = MOCK_QUIZ["questions"]
    if 0 <= question_index < len(questions):
        q = questions[question_index]
        correct = user_answer == q["correctAnswer"]
        return {
            "correct": correct,
            "explanation": q["explanation"],
        }

    return {"correct": False, "explanation": "Invalid question index."}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@app.get("/api/dashboard/stats")
async def dashboard_stats():
    stats = copy.deepcopy(MOCK_DASHBOARD_STATS)
    stats["totalDocuments"] = len(documents)
    return stats


# ---------------------------------------------------------------------------
# TTS (Text-to-Speech) — stub
# ---------------------------------------------------------------------------
@app.post("/api/tts")
async def tts(request: Request):
    return {"audioUrl": None, "message": "TTS not available in demo"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=3001)
