# StudyBot Enhanced — Comprehensive Project Plan

> AI Learning Assistant Chatbot with Quiz Generation, OCR, and Text-to-Speech

**Version:** v2.0 | **Date:** 2026-03-19 | **Status:** Active (Week 3 of 15)

---

## 1. Executive Summary

| Item | Detail |
|:-----|:-------|
| Project Name | StudyBot Enhanced — AI Learning Assistant Chatbot |
| Course | AWS Practical Project I (1670501-01) |
| University | Kookmin University, AWS & Quantum Communication Convergence, 4th year |
| Professor | Prof. Park Jun-seok (박준석) |
| Team Size | 2~3 members |
| Period | 2026-03-06 ~ 2026-06-12 (15 weeks) |
| Budget | $8~15 (from $100 student credit, ~10~15%) |
| Target Grade | **A+** |

### One-Line Value Proposition

> Upload a PDF textbook, get instant AI-powered Q&A with citations, auto-generated quizzes, photo-to-question OCR, and audio answers — a fully serverless study companion that closes the education gap for Korean high school students.

---

## 2. Problem, Solution, and Value

### Problem

학생이 교과서를 복습할 때 즉각적 Q&A 도구가 없다 (Students have no instant Q&A tool when reviewing textbooks).

- Students study alone without a teacher available for questions
- Traditional search engines give generic answers, not textbook-specific ones
- Students with visual impairments cannot easily use text-based tools
- No easy way to test understanding through practice quizzes

### Solution

**PDF --> RAG --> AI Answers with Citations + Quizzes + OCR + Audio**

1. Upload PDF textbook to S3
2. Step Functions pipeline: parse, chunk, embed, store in S3 Vectors
3. Student asks a question --> Bedrock KB retrieves relevant chunks --> Claude 3 Haiku generates answer with page citations
4. Quiz generation: AI creates multiple-choice and short-answer questions from document content
5. Textract OCR: Take a photo of a textbook page --> extract text --> query RAG
6. Polly TTS: Convert any answer to spoken audio for accessibility

### Public Value (공적가치)

| Dimension | Impact |
|:----------|:-------|
| Education Gap (교육 격차 해소) | Free AI tutor for any student with internet access |
| Accessibility (접근성 향상) | Text-to-speech for visually impaired students (시각장애 학생) |
| Self-Study Empowerment | Quiz generation enables active recall without a teacher |
| Digital Literacy | Exposes 고등학생 to AI-powered learning tools |

---

## 3. Enhanced Architecture

### 3.1 AWS Services (15 serverless services)

| # | Service | Role | Pricing |
|:-:|:--------|:-----|:--------|
| 1 | S3 (Static Hosting) | React SPA hosting | Free tier |
| 2 | CloudFront | CDN + HTTPS | Free tier |
| 3 | API Gateway | REST API with Cognito authorizer | Free tier |
| 4 | Lambda x7 | upload, chat, quiz, documents, textract, polly, processing | Free tier |
| 5 | S3 (Document Bucket) | Original PDF storage | Free tier |
| 6 | Bedrock KB | RAG pipeline orchestration | Pay-per-use |
| 7 | S3 Vectors | Vector storage and search | ~$0.04/mo |
| 8 | Bedrock - Titan Embedding V2 | Embedding generation | ~$0.02/mo |
| 9 | Bedrock - Claude 3 Haiku | LLM answer + quiz generation | ~$0.80/mo |
| 10 | Cognito | User authentication (student/teacher roles) | Free tier (50K MAU) |
| 11 | DynamoDB | Chat history, quiz results, user profiles | Free tier (25 WCU/RCU) |
| 12 | Textract | OCR from photo uploads | ~$0.50/mo |
| 13 | Polly | Text-to-speech audio generation | ~$0.30/mo |
| 14 | Step Functions | PDF processing pipeline orchestration | Free tier (4K transitions) |
| 15 | CloudWatch + X-Ray | Monitoring, logging, tracing, teacher dashboard | Free tier (basic) |
| 16 | SAM (IaC) | Infrastructure as Code | Free |

### 3.2 Architecture Diagram (Text)

```
                                  ┌─────────────────────────────────┐
                                  │         Amazon Cognito          │
                                  │   (User Pool + Identity Pool)   │
                                  │   Student / Teacher roles       │
                                  └──────────┬──────────────────────┘
                                             │ JWT Token
                                             ▼
┌──────────┐    ┌──────────────┐    ┌──────────────────┐
│  Student  │───▶│  CloudFront  │───▶│   S3 (React SPA) │
│  Browser  │    │  (CDN+HTTPS) │    │   Frontend App   │
└──────────┘    └──────┬───────┘    └──────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │   API Gateway      │ ◀── Cognito Authorizer (JWT)
              │   (REST API)       │
              └──┬──┬──┬──┬──┬──┬─┘
                 │  │  │  │  │  │
    ┌────────────┘  │  │  │  │  └────────────────┐
    ▼               ▼  │  ▼  │                   ▼
┌────────┐   ┌────────┐│┌────────┐│         ┌────────────┐
│Lambda: │   │Lambda: │││Lambda: │││         │Lambda:     │
│upload  │   │chat    │││quiz    │││         │documents   │
└───┬────┘   └───┬────┘│└───┬────┘│         └──────┬─────┘
    │            │     │    │     │                │
    ▼            │     ▼    │     ▼                ▼
┌─────────┐     │ ┌────────┐│ ┌──────────┐   ┌─────────┐
│S3 (PDF) │     │ │Lambda: ││ │Lambda:   │   │S3 (PDF) │
│Document │     │ │textract││ │polly     │   │list/del │
│Bucket   │     │ └───┬────┘│ └────┬─────┘   └─────────┘
└────┬────┘     │     │     │      │
     │          │     ▼     │      ▼
     ▼          │ ┌────────┐│ ┌──────────┐
┌──────────┐    │ │Amazon  ││ │Amazon    │
│Step      │    │ │Textract││ │Polly     │
│Functions │    │ └────────┘│ │(TTS)     │
│Pipeline  │    │           │ └──────────┘
└────┬─────┘    │           │
     │          ▼           │
     ▼     ┌──────────────┐ │
┌────────┐ │ Bedrock KB   │ │
│Chunk + │ │ Retrieve &   │ │
│Embed   │ │ Generate     │ │
└───┬────┘ └──────┬───────┘ │
    │             │         │
    ▼             ▼         │
┌──────────┐ ┌──────────┐  │
│S3 Vectors│ │Claude 3  │  │
│(Vector   │ │Haiku     │  │
│Store)    │ │(LLM)     │  │
└──────────┘ └──────────┘  │
                            │
    ┌───────────────────────┘
    ▼
┌──────────────────────────────────┐
│          DynamoDB                │
│  - Chat history (per user)      │
│  - Quiz results & scores        │
│  - Document metadata             │
└──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  CloudWatch + X-Ray              │
│  - Lambda metrics & traces       │
│  - Teacher Dashboard (custom)    │
│  - Cost alerts ($5, $10, $15)    │
└──────────────────────────────────┘
```

### 3.3 Key Flows

**PDF Upload Flow:**
```
User uploads PDF --> API GW --> Lambda:upload --> S3 (PDF bucket)
  --> S3 event triggers Step Functions
  --> Step 1: Validate PDF (size, type)
  --> Step 2: Bedrock KB data source sync
  --> Step 3: Wait for indexing complete
  --> Step 4: Update DynamoDB (status: ready)
  --> Step 5: Notify frontend via status API
```

**Chat Query Flow:**
```
User asks question --> API GW (JWT auth) --> Lambda:chat
  --> Bedrock KB RetrieveAndGenerate
  --> S3 Vectors (semantic search)
  --> Titan V2 (embedding) + Claude 3 Haiku (generation)
  --> Response with citations (page numbers, passages)
  --> Save to DynamoDB (chat history)
  --> Return to frontend with highlighted sources
```

**Quiz Generation Flow:**
```
User clicks "Generate Quiz" --> API GW --> Lambda:quiz
  --> Retrieve document chunks from Bedrock KB
  --> Claude 3 Haiku generates 5 quiz questions (MCQ + short answer)
  --> Return questions to frontend
  --> User submits answers --> Lambda scores & stores in DynamoDB
```

**OCR Flow:**
```
User takes photo of textbook page --> API GW --> Lambda:textract
  --> Upload image to S3
  --> Amazon Textract DetectDocumentText
  --> Extracted text --> Lambda:chat (same RAG flow)
  --> Return answer based on extracted question
```

**TTS Flow:**
```
User clicks "Listen" on an answer --> API GW --> Lambda:polly
  --> Amazon Polly SynthesizeSpeech (Korean, Seoyeon voice)
  --> Return audio stream / S3 presigned URL
  --> Frontend plays audio
```

---

## 4. A+ Recipe Checklist

### Phase 1: Foundation (Weeks 1-5)

| # | Task | Week | Status | Owner |
|:-:|:-----|:----:|:------:|:------|
| 1 | Architecture diagram finalized | 2 | Done | Team |
| 2 | SAM IaC setup (template.yaml, deploy scripts) | 3 | **NOW** | Backend |
| 3 | PDF ingestion pipeline (S3 + Step Functions + Bedrock KB) | 4 | Pending | Backend |
| 4 | Basic RAG query flow (chat Lambda + Bedrock KB) | 5 | Pending | Backend |

### Phase 2: MVP for 중간고사 (Weeks 5-8)

| # | Task | Week | Status | Owner |
|:-:|:-----|:----:|:------:|:------|
| 5 | Cognito authentication (sign-up, sign-in, JWT) | 6 | Pending | Backend |
| 6 | React frontend (chat UI + citation highlighting + PDF viewer) | 7 | Pending | Frontend |
| 7 | **Midterm MVP demo** — end-to-end working prototype | **8** | Pending | Team |

### Phase 3: Enhancement (Weeks 9-12)

| # | Task | Week | Status | Owner |
|:-:|:-----|:----:|:------:|:------|
| 8 | Quiz generation feature (MCQ + short answer from document) | 10 | Pending | Backend |
| 9 | Textract OCR integration (photo --> text --> RAG query) | 11 | Pending | Backend |
| 10 | Polly text-to-speech (Korean Seoyeon voice) | 11 | Pending | Backend |
| 11 | Teacher dashboard (CloudWatch custom metrics, usage stats) | 12 | Pending | Frontend |

### Phase 4: Polish for 기말고사 (Weeks 13-15)

| # | Task | Week | Status | Owner |
|:-:|:-----|:----:|:------:|:------|
| 12 | Real user testing with 고등학생 (5+ testers, feedback form) | 13 | Pending | Team |
| 13 | Cost optimization report (actual vs projected, per-service) | 14 | Pending | Backend |
| 14 | README + demo video (3 min) + live CloudFront URL | 15 | Pending | Team |
| 15 | Final demo rehearsal 5x (timing, backup plan, Q&A prep) | 15 | Pending | Team |

---

## 5. Risk Matrix

| # | Risk | Probability | Impact | Mitigation |
|:-:|:-----|:----------:|:------:|:-----------|
| 1 | S3 Vectors is new (GA Dec 2025) — limited docs/examples | Medium | High | Early PoC in Week 3; fallback to pgvector on RDS if needed |
| 2 | Korean PDF parsing quality (tables, math formulas) | High | Medium | Test with 3+ real 교과서 PDFs in Week 4; use Textract as fallback parser |
| 3 | Demo failure during 중간고사/기말고사 | Low | Very High | Record backup video; rehearse 5x; have offline fallback screenshots |
| 4 | Bedrock region availability (ap-northeast-2) | Medium | High | Use us-east-1 from start; document latency tradeoff |
| 5 | Lambda cold start affecting UX | High | Low | Show loading spinner; use provisioned concurrency for demo day only |
| 6 | Cognito integration complexity | Medium | Medium | Use Amplify Auth library; start simple (email/password only) |
| 7 | Cost overrun beyond $15 | Low | Medium | CloudWatch billing alarm at $5, $10, $15; API Gateway throttling |
| 8 | Textract accuracy on handwritten Korean | Medium | Low | Limit to printed text; clearly document scope in presentation |
| 9 | Team member dropout (팀원 이탈) | Medium | High | MVP-first strategy; both members know full stack |
| 10 | Step Functions state machine complexity | Medium | Medium | Start with simple sequential flow; add error handling incrementally |
| 11 | Citation page number extraction fails | Medium | High | Week 3 PoC must validate this; fallback to chunk-level citation |
| 12 | Polly Korean pronunciation quality | Low | Low | Test early; Seoyeon voice is high quality for Korean |

---

## 6. Cost Projection (15 Weeks)

### Per-Service Breakdown

| Service | Monthly Cost | 15-Week Cost | Notes |
|:--------|:-----------:|:------------:|:------|
| S3 (Static + Docs) | $0.00 | $0.00 | Free tier: 5GB storage, 20K GET |
| CloudFront | $0.00 | $0.00 | Free tier: 10M requests |
| API Gateway | $0.00 | $0.00 | Free tier: 1M calls/mo |
| Lambda x7 | $0.00 | $0.00 | Free tier: 1M requests, 400K GB-sec |
| Cognito | $0.00 | $0.00 | Free tier: 50K MAU |
| DynamoDB | $0.00 | $0.00 | Free tier: 25 WCU/RCU |
| Step Functions | $0.00 | $0.00 | Free tier: 4K state transitions |
| CloudWatch | $0.00 | $0.00 | Basic monitoring free |
| X-Ray | $0.00 | $0.00 | Free tier: 100K traces |
| Bedrock - Claude 3 Haiku | $0.80 | $3.20 | ~200 queries/day, input+output tokens |
| Bedrock - Titan Embedding V2 | $0.02 | $0.08 | Embedding generation for ~50 PDFs |
| S3 Vectors | $0.04 | $0.16 | Vector storage + queries |
| Textract | $0.15 | $0.60 | ~100 pages/month OCR |
| Polly | $0.10 | $0.40 | ~50K characters/month TTS |
| SAM / CloudFormation | $0.00 | $0.00 | Free |
| **TOTAL** | **~$1.11** | **~$4.44** |  |

### Budget Safety Margin

| Scenario | 15-Week Cost | % of $100 Credit |
|:---------|:-----------:|:----------------:|
| Best case (low usage) | $4.44 | 4.4% |
| Expected (moderate testing) | $8.00 | 8.0% |
| Worst case (heavy testing + demo prep) | $15.00 | 15.0% |
| Budget alarm threshold | $15.00 | 15.0% |

**Cost Controls:**
- CloudWatch billing alarm at $5, $10, $15
- API Gateway throttling: 100 requests/sec burst, 50 sustained
- Lambda concurrency limit: 10 per function
- S3 lifecycle policy: delete test files after 30 days

---

## 7. Grading Strategy

### 7.1 중간고사 (Midterm) — 20%

**Strategy: Impressive MVP Demo**

| Demo Step | Time | What to Show |
|:----------|:----:|:-------------|
| 1. Login | 30s | Cognito sign-in (student account) |
| 2. Upload PDF | 30s | Upload "생물학 교과서.pdf", show Step Functions progress |
| 3. Ask Question | 45s | "세포 분열의 단계를 설명해줘" --> answer with citations |
| 4. Show Citations | 30s | Click citation --> PDF viewer highlights the source paragraph |
| 5. Architecture | 60s | Show SAM template, explain 10+ services |
| 6. Cost Report | 30s | Show actual costs vs projection |
| **Total** | **~4 min** | |

**Key Talking Points:**
- "15 AWS serverless services, zero EC2"
- "S3 Vectors — released December 2025, cutting-edge"
- "Total cost under $5 so far"

### 7.2 기말고사 (Final) — 30%

**Strategy: Full Feature Demo + Real User Results**

| Demo Step | Time | What to Show |
|:----------|:----:|:-------------|
| 1. User Testing Results | 60s | Show feedback from 5+ 고등학생 testers |
| 2. Full Flow | 90s | Upload --> Q&A --> Quiz --> OCR --> TTS |
| 3. Teacher Dashboard | 45s | CloudWatch metrics: queries/day, popular topics, quiz scores |
| 4. Architecture Deep Dive | 60s | Step Functions workflow, X-Ray traces, error handling |
| 5. Cost Analysis | 45s | 15-week actual cost report, optimization strategies |
| 6. Live Q&A Prep | — | Anticipate 5 tough questions from professor |
| **Total** | **~6 min** | |

### 7.3 프로젝트 (Project) — 30%

| Criterion | Our Approach |
|:----------|:-------------|
| Technical Complexity | 15 AWS services, 7 Lambda functions, Step Functions orchestration |
| Completeness | End-to-end: auth --> upload --> RAG --> quiz --> OCR --> TTS |
| Innovation | S3 Vectors (latest), Textract + RAG combo, quiz generation |
| Public Value | Real user testing with 고등학생, accessibility (TTS) |
| IaC | 100% SAM-managed, reproducible with `sam deploy` |

### 7.4 과제물 (Assignments) — 10%

| Document | Content |
|:---------|:--------|
| Architecture Diagram | Detailed text + Mermaid diagrams |
| API Documentation | OpenAPI spec for all 7+ endpoints |
| Cost Analysis Report | Per-service projected vs actual |
| User Testing Report | 고등학생 feedback analysis |
| README | Setup guide, demo video link, live URL |

### 7.5 출석 + 참여 (Attendance) — 10%

- Every Friday 09:00~12:00 attendance
- Active participation in mentor sessions (Weeks 6, 7, 13, 14)
- Prepare specific questions for each mentor session

---

## 8. Differentiation Points (vs Other Capstone Teams)

### 1. Cutting-Edge AWS Service: S3 Vectors

S3 Vectors became GA in December 2025. Most teams will use OpenSearch or pgvector. We use the newest AWS-native vector store, showing we stay ahead of the technology curve. This will impress the professor and AWS mentors.

### 2. Real User Testing with 고등학생

Most capstone teams test only among themselves. We will recruit 5+ high school students for real user testing in Week 13. This proves our public value claim is not just theoretical — we have actual feedback data.

### 3. Accessibility Through Multi-Modal Output

Text answers + audio (Polly TTS) + visual citations (PDF highlighting). No other team will likely address accessibility for visually impaired students. This directly maps to the 공적가치 requirement.

### 4. AI-Generated Quizzes for Active Recall

Going beyond passive Q&A to active learning. The quiz feature transforms the chatbot from an "answer machine" into a "study partner." This shows deeper thinking about the educational problem.

### 5. Photo-to-Question OCR Pipeline

Students can photograph a textbook page and get instant AI explanations. This bridges the physical-digital gap. The Textract + Bedrock pipeline is a unique technical combination that demonstrates integration skills.

### Bonus Differentiator: 15-Week Cost Under $15

While other teams may burn through their $100 credit, our extreme cost efficiency (under 15% of budget) demonstrates production-ready cost awareness — a skill highly valued in the industry.

---

## 9. Technology Decisions (ADR Summary)

| Decision | Choice | Rejected | Reason |
|:---------|:-------|:---------|:-------|
| Vector DB | S3 Vectors | OpenSearch ($350/mo) | 99.9% cost reduction, AWS-native |
| RAG Engine | Bedrock KB | LangChain DIY | 80% less code, managed service |
| LLM | Claude 3 Haiku | Sonnet, Titan | Lowest cost + sufficient quality |
| Embedding | Titan V2 | Cohere | AWS-native, lowest price |
| Auth | Cognito | Custom JWT | Managed, free tier, role-based |
| State Management | DynamoDB | RDS PostgreSQL | Serverless, free tier, simple schema |
| Orchestration | Step Functions | SQS + Lambda | Visual workflow, error handling, tracing |
| OCR | Textract | Tesseract | AWS-native, better Korean support |
| TTS | Polly | Google TTS | AWS-native, Korean Seoyeon voice |
| Frontend | React + Vite | Next.js | No SSR needed, simpler deployment |
| Backend | Python 3.12 Lambda | TypeScript | boto3 included, team familiarity |
| IaC | AWS SAM | CDK, Terraform | Low learning curve, Lambda-focused |

---

## 10. API Endpoints (Enhanced)

| Method | Path | Lambda | Auth | Description |
|:-------|:-----|:-------|:----:|:------------|
| POST | /api/auth/signup | (Cognito) | No | User registration |
| POST | /api/auth/signin | (Cognito) | No | User login, returns JWT |
| POST | /api/upload/presign | upload | JWT | Get presigned URL for PDF upload |
| POST | /api/upload/complete | upload | JWT | Trigger Step Functions pipeline |
| GET | /api/upload/status/{jobId} | upload | JWT | Check indexing status |
| POST | /api/chat | chat | JWT | Send question, get RAG answer |
| GET | /api/chat/history | chat | JWT | Get conversation history |
| POST | /api/quiz/generate | quiz | JWT | Generate quiz from document |
| POST | /api/quiz/submit | quiz | JWT | Submit quiz answers, get score |
| GET | /api/quiz/history | quiz | JWT | Get past quiz results |
| POST | /api/textract/analyze | textract | JWT | Upload image for OCR |
| POST | /api/polly/synthesize | polly | JWT | Convert text to speech |
| GET | /api/documents | documents | JWT | List uploaded documents |
| DELETE | /api/documents/{id} | documents | JWT | Delete a document |
| GET | /api/dashboard/metrics | documents | JWT (teacher) | Teacher dashboard data |

---

## 11. Team Workflow

### Git Strategy
- `main` branch: stable releases only
- `dev` branch: integration
- Feature branches: `feature/quiz-generation`, `feature/textract-ocr`, etc.
- PR required for merging to `dev` and `main`

### Communication
- Weekly sprint planning: Friday after class
- Daily async updates in team chat
- Mentor session prep: 2 days before each session

### Definition of Done
- Code works locally and in AWS
- SAM template updated
- API tested with curl/Postman
- Brief documentation in code comments
- Cost impact checked

---

> Document version: v2.0 | 2026-03-19 | StudyBot Enhanced Project Plan
