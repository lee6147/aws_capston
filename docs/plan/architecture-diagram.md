# StudyBot Enhanced — Architecture Diagrams

> Detailed text-based and Mermaid architecture diagrams for all system flows.

**Version:** v2.0 | **Date:** 2026-03-19

---

## 1. High-Level System Architecture (Mermaid)

```mermaid
graph TB
    subgraph Client["Client Layer"]
        Browser["Student Browser"]
        Mobile["Mobile Browser"]
    end

    subgraph CDN["Content Delivery"]
        CF["CloudFront<br/>(CDN + HTTPS)"]
        S3Web["S3 Bucket<br/>(React SPA)"]
    end

    subgraph Auth["Authentication"]
        Cognito["Amazon Cognito<br/>(User Pool)"]
    end

    subgraph API["API Layer"]
        APIGW["API Gateway<br/>(REST API + JWT Authorizer)"]
    end

    subgraph Compute["Compute Layer (Lambda x7)"]
        LUpload["Lambda: upload<br/>(presign + complete)"]
        LChat["Lambda: chat<br/>(RAG query)"]
        LQuiz["Lambda: quiz<br/>(generate + score)"]
        LDocs["Lambda: documents<br/>(list + delete)"]
        LTextract["Lambda: textract<br/>(OCR processing)"]
        LPolly["Lambda: polly<br/>(TTS synthesis)"]
        LProcessing["Lambda: processing<br/>(Step Functions callback)"]
    end

    subgraph Storage["Storage Layer"]
        S3Docs["S3 Bucket<br/>(PDF Documents)"]
        S3Vec["S3 Vectors<br/>(Vector Store)"]
        DDB["DynamoDB<br/>(Chat History, Quizzes)"]
    end

    subgraph AI["AI/ML Layer"]
        BKB["Bedrock KB<br/>(RAG Pipeline)"]
        Haiku["Claude 3 Haiku<br/>(LLM)"]
        Titan["Titan Embedding V2<br/>(Embeddings)"]
        Textract["Amazon Textract<br/>(OCR)"]
        Polly["Amazon Polly<br/>(TTS - Seoyeon)"]
    end

    subgraph Orchestration["Orchestration"]
        SF["Step Functions<br/>(PDF Pipeline)"]
    end

    subgraph Monitoring["Monitoring"]
        CW["CloudWatch<br/>(Metrics + Alarms)"]
        XRay["X-Ray<br/>(Distributed Tracing)"]
    end

    Browser --> CF
    Mobile --> CF
    CF --> S3Web
    CF --> APIGW

    Browser --> Cognito
    Cognito -->|JWT| APIGW

    APIGW --> LUpload
    APIGW --> LChat
    APIGW --> LQuiz
    APIGW --> LDocs
    APIGW --> LTextract
    APIGW --> LPolly

    LUpload --> S3Docs
    S3Docs --> SF
    SF --> LProcessing
    SF --> BKB
    BKB --> Titan
    Titan --> S3Vec

    LChat --> BKB
    BKB --> Haiku
    LChat --> DDB

    LQuiz --> BKB
    LQuiz --> Haiku
    LQuiz --> DDB

    LTextract --> Textract
    LTextract --> LChat

    LPolly --> Polly

    LDocs --> S3Docs
    LDocs --> DDB

    LUpload -.-> CW
    LChat -.-> CW
    LQuiz -.-> CW
    SF -.-> CW
    APIGW -.-> XRay
    LChat -.-> XRay
```

---

## 2. User Flow — Student Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                     STUDENT USER FLOW                           │
└─────────────────────────────────────────────────────────────────┘

  ┌──────┐    ┌──────────┐    ┌───────────┐    ┌──────────────┐
  │ Sign │───▶│  Upload   │───▶│  Ask      │───▶│  Generate    │
  │ Up / │    │  PDF      │    │  Question │    │  Quiz        │
  │ Login│    │  Textbook │    │           │    │              │
  └──────┘    └──────────┘    └───────────┘    └──────────────┘
     │             │               │                  │
     ▼             ▼               ▼                  ▼
  Cognito     S3 + Step       Bedrock KB +       Claude 3 Haiku
  (JWT)       Functions       Claude Haiku       (quiz generation)
                  │               │                  │
                  ▼               ▼                  ▼
             "Indexing       "Answer with       "5 questions
              complete!"      citations:         generated!
                              see p.34"          Score: 4/5"
                                  │
                          ┌───────┴───────┐
                          ▼               ▼
                    ┌──────────┐   ┌──────────┐
                    │  Listen  │   │  Photo   │
                    │  (TTS)   │   │  OCR     │
                    │  Polly   │   │ Textract │
                    └──────────┘   └──────────┘
                         │               │
                         ▼               ▼
                    "Audio plays     "Text extracted,
                     answer in        querying RAG..."
                     Korean"
```

---

## 3. PDF Upload + Processing Pipeline (Step Functions)

```mermaid
stateDiagram-v2
    [*] --> UploadRequested: User clicks Upload

    UploadRequested --> GeneratePresignedURL: Lambda: upload/presign
    GeneratePresignedURL --> ClientUploadToS3: Return presigned URL
    ClientUploadToS3 --> TriggerPipeline: POST /upload/complete

    state StepFunctions {
        TriggerPipeline --> ValidatePDF: Step 1
        ValidatePDF --> CheckFileSize: Is PDF valid?

        CheckFileSize --> RejectFile: > 10MB or not PDF
        CheckFileSize --> SyncToBedrockKB: Valid

        RejectFile --> [*]: Return error

        SyncToBedrockKB --> WaitForIndexing: Step 2 - StartIngestionJob
        WaitForIndexing --> CheckStatus: Step 3 - Poll status

        CheckStatus --> WaitForIndexing: Still processing (wait 10s)
        CheckStatus --> UpdateDynamoDB: Indexing complete

        UpdateDynamoDB --> NotifyComplete: Step 4 - Write metadata
        NotifyComplete --> [*]: Step 5 - Return success
    }
```

### ASCII Version

```
User                    API GW          Lambda:upload       S3            Step Functions      Bedrock KB
 │                        │                  │               │                 │                  │
 │  POST /upload/presign  │                  │               │                 │                  │
 │───────────────────────▶│─────────────────▶│               │                 │                  │
 │                        │                  │──── Generate ─▶               │                  │
 │                        │                  │◀─── URL ──────│               │                  │
 │◀──────── presigned URL─│◀─────────────────│               │                 │                  │
 │                        │                  │               │                 │                  │
 │  PUT (direct to S3)    │                  │               │                 │                  │
 │────────────────────────┼──────────────────┼──────────────▶│                 │                  │
 │                        │                  │               │                 │                  │
 │  POST /upload/complete │                  │               │                 │                  │
 │───────────────────────▶│─────────────────▶│               │                 │                  │
 │                        │                  │────── Start ──┼────────────────▶│                  │
 │◀──── jobId ────────────│◀─────────────────│               │                 │                  │
 │                        │                  │               │  Step 1: Validate               │
 │                        │                  │               │  Step 2: Sync ──┼─────────────────▶│
 │                        │                  │               │                 │  StartIngestion  │
 │                        │                  │               │  Step 3: Wait   │◀──── jobId ──────│
 │  GET /upload/status    │                  │               │  (poll loop)    │                  │
 │───────────────────────▶│─────────────────▶│               │      ...        │                  │
 │◀──── "processing" ─────│◀─────────────────│               │  Step 4: Done   │                  │
 │                        │                  │               │  Update DDB     │                  │
 │  GET /upload/status    │                  │               │                 │                  │
 │───────────────────────▶│─────────────────▶│               │                 │                  │
 │◀──── "ready" ──────────│◀─────────────────│               │                 │                  │
```

---

## 4. Chat Query Flow (RAG with Citations)

```mermaid
sequenceDiagram
    participant U as Student
    participant CF as CloudFront
    participant AG as API Gateway
    participant CG as Cognito
    participant LC as Lambda: chat
    participant BK as Bedrock KB
    participant SV as S3 Vectors
    participant TE as Titan V2
    participant CH as Claude Haiku
    participant DB as DynamoDB

    U->>CF: "세포 분열의 단계를 설명해줘"
    CF->>AG: POST /api/chat (JWT in header)
    AG->>CG: Validate JWT token
    CG-->>AG: Valid (userId, role=student)
    AG->>LC: Invoke with question + userId

    LC->>BK: RetrieveAndGenerate(question, knowledgeBaseId)
    BK->>TE: Embed question → vector
    TE-->>BK: [0.023, -0.156, ...]
    BK->>SV: Semantic search (top 5 chunks)
    SV-->>BK: Relevant chunks + metadata (page numbers)
    BK->>CH: Generate answer using retrieved chunks
    CH-->>BK: "세포 분열은 4단계로..." + citations

    BK-->>LC: Response with retrievedReferences
    LC->>DB: Save chat record (userId, Q, A, timestamp)
    LC-->>AG: JSON response
    AG-->>CF: 200 OK
    CF-->>U: Answer + citations (p.34, p.37)
```

### Response JSON Structure

```json
{
  "answer": "세포 분열은 4단계로 진행됩니다: 전기, 중기, 후기, 말기...",
  "citations": [
    {
      "pageNumber": 34,
      "passage": "세포 분열의 첫 번째 단계인 전기에서는...",
      "score": 0.92
    },
    {
      "pageNumber": 37,
      "passage": "후기와 말기에서는 염색체가...",
      "score": 0.87
    }
  ],
  "conversationId": "conv-abc123",
  "timestamp": "2026-04-15T10:30:00Z"
}
```

---

## 5. Authentication Flow (Cognito)

```mermaid
sequenceDiagram
    participant U as User
    participant App as React App
    participant CG as Cognito User Pool
    participant AG as API Gateway
    participant L as Lambda

    Note over U,L: Sign-Up Flow
    U->>App: Enter email + password
    App->>CG: SignUp(email, password)
    CG-->>App: Confirmation code sent to email
    U->>App: Enter confirmation code
    App->>CG: ConfirmSignUp(code)
    CG-->>App: User confirmed

    Note over U,L: Sign-In Flow
    U->>App: Enter email + password
    App->>CG: InitiateAuth(email, password)
    CG-->>App: {idToken, accessToken, refreshToken}
    App->>App: Store tokens in localStorage

    Note over U,L: Authenticated API Call
    App->>AG: POST /api/chat (Authorization: Bearer idToken)
    AG->>AG: Cognito Authorizer validates JWT
    AG->>L: Invoke (claims: userId, email, role)
    L-->>AG: Response
    AG-->>App: 200 OK

    Note over U,L: Token Refresh
    App->>CG: InitiateAuth(REFRESH_TOKEN)
    CG-->>App: New {idToken, accessToken}
```

### Cognito User Pool Configuration

```
User Pool:
  ├── Sign-in: email
  ├── Password policy: 8+ chars, uppercase, number, symbol
  ├── MFA: off (student convenience)
  ├── Custom attributes:
  │   ├── custom:role = "student" | "teacher"
  │   └── custom:school = string
  └── Groups:
      ├── students (default)
      └── teachers (dashboard access)

API Gateway Authorizer:
  ├── Type: Cognito User Pool
  ├── Token source: Authorization header
  └── Token validation: JWT signature + expiry
```

---

## 6. Quiz Generation Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    QUIZ GENERATION FLOW                       │
└──────────────────────────────────────────────────────────────┘

Student clicks                Lambda:quiz              Claude 3 Haiku
"Generate Quiz"                   │                         │
     │                            │                         │
     │  POST /api/quiz/generate   │                         │
     │  {documentId, numQ: 5}     │                         │
     │───────────────────────────▶│                         │
     │                            │                         │
     │                            │  Retrieve top 10 chunks │
     │                            │  from Bedrock KB        │
     │                            │────────────────────────▶│
     │                            │                         │
     │                            │  Prompt:                │
     │                            │  "Generate 5 quiz Qs    │
     │                            │   from these chunks.    │
     │                            │   Include: 3 MCQ +      │
     │                            │   2 short answer.       │
     │                            │   Return as JSON."      │
     │                            │────────────────────────▶│
     │                            │                         │
     │                            │◀────── Quiz JSON ───────│
     │                            │                         │
     │                            │  Store quiz in DynamoDB │
     │                            │  (quizId, questions,    │
     │                            │   correct answers)      │
     │                            │                         │
     │◀──── Quiz Questions ───────│                         │
     │                            │                         │
     │  (Student answers)         │                         │
     │                            │                         │
     │  POST /api/quiz/submit     │                         │
     │  {quizId, answers: [...]}  │                         │
     │───────────────────────────▶│                         │
     │                            │  Compare with stored    │
     │                            │  correct answers        │
     │                            │  Calculate score        │
     │                            │  Store result in DDB    │
     │◀──── Score: 4/5 ──────────│                         │
```

---

## 7. OCR Flow (Textract)

```mermaid
sequenceDiagram
    participant U as Student
    participant App as React App
    participant AG as API Gateway
    participant LT as Lambda: textract
    participant S3 as S3 (Images)
    participant TX as Amazon Textract
    participant LC as Lambda: chat
    participant BK as Bedrock KB

    U->>App: Take photo of textbook page
    App->>AG: POST /api/textract/analyze (image base64)
    AG->>LT: Invoke

    LT->>S3: Upload image to S3
    LT->>TX: DetectDocumentText(S3 object)
    TX-->>LT: Extracted text blocks

    LT->>LT: Clean and join text blocks
    LT->>LC: Internal invoke with extracted text as question
    LC->>BK: RetrieveAndGenerate(extracted_text)
    BK-->>LC: Answer with citations

    LC-->>LT: RAG response
    LT-->>AG: {extractedText, answer, citations}
    AG-->>App: Response
    App-->>U: Show extracted text + AI answer
```

---

## 8. Text-to-Speech Flow (Polly)

```
Student clicks "Listen"         Lambda:polly          Amazon Polly
on an answer                        │                     │
     │                              │                     │
     │  POST /api/polly/synthesize  │                     │
     │  {text: "세포 분열은...",     │                     │
     │   voiceId: "Seoyeon"}        │                     │
     │─────────────────────────────▶│                     │
     │                              │                     │
     │                              │  SynthesizeSpeech   │
     │                              │  (text, Seoyeon,    │
     │                              │   mp3, Korean)      │
     │                              │────────────────────▶│
     │                              │                     │
     │                              │◀── Audio stream ────│
     │                              │                     │
     │                              │  Upload to S3       │
     │                              │  Generate presigned  │
     │                              │  URL (5 min expiry) │
     │                              │                     │
     │◀── {audioUrl: "https://..."}─│                     │
     │                              │                     │
     │  <audio> plays mp3           │                     │
```

---

## 9. Teacher Dashboard Flow

```
┌──────────────────────────────────────────────────────────────┐
│                   TEACHER DASHBOARD                          │
└──────────────────────────────────────────────────────────────┘

Teacher logs in                                CloudWatch
(role: teacher)                                    │
     │                                             │
     │  GET /api/dashboard/metrics                 │
     │─────────▶ API GW ─────▶ Lambda:documents    │
     │                              │              │
     │                              │  GetMetricData
     │                              │─────────────▶│
     │                              │              │
     │                              │  Query DDB   │
     │                              │  for stats   │
     │                              │              │
     │◀──── Dashboard JSON ─────────│              │
     │                                             │
     │  Dashboard shows:                           │
     │  ┌─────────────────────────────┐            │
     │  │  Total Queries: 342         │            │
     │  │  Active Students: 12        │            │
     │  │  Quizzes Taken: 45          │            │
     │  │  Avg Quiz Score: 78%        │            │
     │  │  Popular Topics:            │            │
     │  │    1. 세포 분열 (28 queries) │            │
     │  │    2. 광합성 (22 queries)    │            │
     │  │  Documents: 8 PDFs          │            │
     │  │  Cost This Week: $0.32      │            │
     │  └─────────────────────────────┘            │
```

---

## 10. Complete Infrastructure (SAM Resources)

```yaml
# Logical resource layout for template.yaml

Resources:
  # --- Auth ---
  CognitoUserPool:           # User authentication
  CognitoUserPoolClient:     # App client
  CognitoAuthorizer:         # API GW JWT authorizer

  # --- API ---
  ApiGateway:                # REST API (regional)
    Routes:
      - POST   /api/upload/presign
      - POST   /api/upload/complete
      - GET    /api/upload/status/{jobId}
      - POST   /api/chat
      - GET    /api/chat/history
      - POST   /api/quiz/generate
      - POST   /api/quiz/submit
      - GET    /api/quiz/history
      - POST   /api/textract/analyze
      - POST   /api/polly/synthesize
      - GET    /api/documents
      - DELETE /api/documents/{id}
      - GET    /api/dashboard/metrics

  # --- Compute ---
  UploadFunction:            # Python 3.12, 256MB, 30s
  ChatFunction:              # Python 3.12, 256MB, 25s
  QuizFunction:              # Python 3.12, 256MB, 25s
  DocumentsFunction:         # Python 3.12, 128MB, 10s
  TextractFunction:          # Python 3.12, 256MB, 30s
  PollyFunction:             # Python 3.12, 256MB, 15s
  ProcessingFunction:        # Python 3.12, 256MB, 30s (Step Functions callback)

  # --- Storage ---
  DocumentBucket:            # S3 - PDF storage
  WebsiteBucket:             # S3 - React SPA
  S3VectorsStore:            # S3 Vectors - managed by Bedrock KB
  ChatTable:                 # DynamoDB - chat history
  QuizTable:                 # DynamoDB - quiz results

  # --- AI/ML ---
  BedrockKnowledgeBase:      # Bedrock KB (created via console/CLI)
  # Claude 3 Haiku:          # Model access (pre-configured)
  # Titan Embedding V2:      # Model access (pre-configured)

  # --- Orchestration ---
  PdfProcessingStateMachine: # Step Functions state machine
    Definition:
      StartAt: ValidatePdf
      States:
        ValidatePdf:         # Check size, type
        SyncToBedrockKB:     # Start ingestion job
        WaitForIndexing:     # Wait state (10s)
        CheckIndexingStatus: # Poll Bedrock KB
        UpdateMetadata:      # Write to DynamoDB
        NotifyComplete:      # Success

  # --- CDN ---
  CloudFrontDistribution:    # CDN for SPA + API

  # --- Monitoring ---
  CostAlarm5:                # CloudWatch alarm at $5
  CostAlarm10:               # CloudWatch alarm at $10
  CostAlarm15:               # CloudWatch alarm at $15
  DashboardMetrics:          # Custom metrics for teacher dashboard
```

---

## 11. Network and Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
└─────────────────────────────────────────────────────────┘

Internet
    │
    ▼
┌──────────────┐
│  CloudFront  │ ← HTTPS only, TLS 1.2+
│  (WAF-ready) │ ← Geo-restriction optional
└──────┬───────┘
       │
       ├──── Static content ────▶ S3 (OAC, no public access)
       │
       └──── /api/* ────────────▶ API Gateway
                                     │
                                     ├── Cognito Authorizer (JWT validation)
                                     ├── Throttling: 100 req/s burst
                                     ├── Request validation
                                     │
                                     ▼
                                  Lambda
                                     │
                                     ├── IAM execution role (least privilege)
                                     ├── Environment variables (encrypted)
                                     ├── VPC: not needed (all AWS services)
                                     │
                                     ▼
                              AWS Services
                                     │
                                     ├── S3: bucket policy (Lambda role only)
                                     ├── DynamoDB: IAM-based access
                                     ├── Bedrock: model access policy
                                     ├── Textract: IAM-based access
                                     └── Polly: IAM-based access

IAM Role Summary:
  ├── LambdaUploadRole:    s3:PutObject, s3:GetObject, states:StartExecution
  ├── LambdaChatRole:      bedrock:RetrieveAndGenerate, dynamodb:PutItem
  ├── LambdaQuizRole:      bedrock:Retrieve, bedrock:InvokeModel, dynamodb:*
  ├── LambdaDocsRole:      s3:ListBucket, s3:DeleteObject, dynamodb:Query
  ├── LambdaTextractRole:  s3:PutObject, textract:DetectDocumentText
  ├── LambdaPollyRole:     polly:SynthesizeSpeech, s3:PutObject
  └── StepFunctionsRole:   lambda:InvokeFunction, bedrock:*, dynamodb:PutItem
```

---

> Document version: v2.0 | 2026-03-19 | Architecture Diagrams
