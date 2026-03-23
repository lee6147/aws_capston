# StudyBot Enhanced — Weekly Sprint Plan

> 15-week sprint plan with tasks, deliverables, and risk checkpoints.

**Version:** v2.0 | **Date:** 2026-03-19 | **Current Week:** 3

---

## Sprint Overview

| Phase | Weeks | Goal |
|:------|:-----:|:-----|
| Phase 1: Foundation | 1-5 | Backend infrastructure + basic RAG working |
| Phase 2: MVP | 5-8 | Auth + frontend + 중간고사 demo |
| Phase 3: Enhancement | 9-12 | Quiz, OCR, TTS, dashboard |
| Phase 4: Polish | 13-15 | User testing, optimization, 기말고사 demo |

---

## Week 1 (2026-03-06) — Team Formation

**Sprint Goal:** Form team, set up AWS accounts, get Bedrock model access

**Course Topic:** 오리엔테이션 (Orientation)

| Task | Owner | Status |
|:-----|:------|:------:|
| Form team (2-3 members) | Team | Done |
| Create AWS account with student credit ($100) | Team | Done |
| Request Bedrock model access (Claude 3 Haiku, Titan V2) | Backend | Done |
| Set up GitHub repository | Team | Done |
| Review syllabus and grading criteria | Team | Done |

**Deliverables:**
- [x] Team registration form submitted
- [x] AWS account active with Bedrock access

---

## Week 2 (2026-03-13) — Idea Selection + Architecture

**Sprint Goal:** Compare 3 ideas, select RAG chatbot, design initial architecture

**Course Topic:** 주제 선정 + 팀 구성

| Task | Owner | Status |
|:-----|:------|:------:|
| Research and compare 3 project ideas | Team | Done |
| Write comparison analysis document | Team | Done |
| Select Idea A (RAG Chatbot) with justification | Team | Done |
| Draft initial architecture diagram | Backend | Done |
| Create project proposal document | Team | Done |
| Deploy GitHub Pages for documentation | Frontend | Done |

**Deliverables:**
- [x] 3-idea comparison document
- [x] Project proposal (v1.0)
- [x] Architecture diagram (basic)
- [x] GitHub Pages live

---

## Week 3 (2026-03-20) — Requirements + PoC ← CURRENT WEEK

**Sprint Goal:** Define requirements, validate S3 Vectors + Bedrock KB with real PDF

**Course Topic:** 문제 정의 + 요구사항

| Task | Owner | Status |
|:-----|:------|:------:|
| Write enhanced project plan (this document) | Team | In Progress |
| Set up SAM project structure (template.yaml) | Backend | To Do |
| PoC: Upload test PDF to S3, create Bedrock KB | Backend | To Do |
| PoC: Verify S3 Vectors works as vector store | Backend | To Do |
| PoC: Test citation extraction (page numbers) | Backend | To Do |
| PoC: Test Korean PDF parsing quality | Backend | To Do |
| Set up React + Vite project skeleton | Frontend | Done |
| Define API endpoints (enhanced, 15 routes) | Team | Done |

**Deliverables:**
- [ ] SAM template.yaml (initial skeleton)
- [ ] PoC results document (S3 Vectors, citations, Korean PDF)
- [ ] Enhanced project plan (this document)
- [ ] React project bootstrapped

**Risk Checkpoint:**
- Does S3 Vectors work reliably with Bedrock KB? If not, plan pgvector fallback
- Can we extract page numbers from citations? If not, use chunk-level citations
- How well does Bedrock KB handle Korean PDFs with tables?

---

## Week 4 (2026-03-27) — PDF Ingestion Pipeline

**Sprint Goal:** Build the complete PDF upload and processing pipeline with Step Functions

**Course Topic:** AWS 아키텍처 설계

| Task | Owner | Status |
|:-----|:------|:------:|
| Create S3 document bucket via SAM | Backend | To Do |
| Implement Lambda:upload (presign + complete) | Backend | To Do |
| Build Step Functions state machine (PDF pipeline) | Backend | To Do |
| Integrate Bedrock KB sync in Step Functions | Backend | To Do |
| Create DynamoDB table for document metadata | Backend | To Do |
| Test end-to-end: upload PDF --> indexed in KB | Backend | To Do |
| Design UI wireframes (Figma or sketch) | Frontend | To Do |

**Deliverables:**
- [ ] Working PDF upload pipeline (API --> S3 --> Step Functions --> Bedrock KB)
- [ ] SAM template with S3, Lambda, Step Functions, DynamoDB
- [ ] UI wireframes for all screens

**Risk Checkpoint:**
- Step Functions state machine works without errors?
- Bedrock KB sync time acceptable? (target: < 2 minutes for 10MB PDF)

---

## Week 5 (2026-04-03) — Basic RAG Query

**Sprint Goal:** Ask questions and get answers with citations from uploaded PDFs

**Course Topic:** 데이터 전략 수립

| Task | Owner | Status |
|:-----|:------|:------:|
| Implement Lambda:chat (RetrieveAndGenerate) | Backend | To Do |
| Parse citation references (page numbers, passages) | Backend | To Do |
| Implement Lambda:documents (list, delete) | Backend | To Do |
| Create DynamoDB table for chat history | Backend | To Do |
| Save conversation history per user | Backend | To Do |
| Test with 3+ different Korean textbook PDFs | Backend | To Do |
| Start basic chat UI component | Frontend | To Do |

**Deliverables:**
- [ ] Working Q&A: question in --> answer with citations out
- [ ] Chat history stored in DynamoDB
- [ ] Tested with multiple Korean PDF textbooks

**Risk Checkpoint:**
- Citation quality good enough for demo?
- Response time under 5 seconds?
- Korean language quality of answers acceptable?

---

## Week 6 (2026-04-10) — Authentication (Cognito)

**Sprint Goal:** Add user authentication; prepare for mentor session

**Course Topic:** 시스템 구현 I

| Task | Owner | Status |
|:-----|:------|:------:|
| Create Cognito User Pool via SAM | Backend | To Do |
| Configure Cognito app client | Backend | To Do |
| Add Cognito authorizer to API Gateway | Backend | To Do |
| Create student and teacher user groups | Backend | To Do |
| Implement sign-up / sign-in / sign-out in React | Frontend | To Do |
| Add JWT token handling (storage, refresh) | Frontend | To Do |
| Protected routes in React (auth required) | Frontend | To Do |

**Deliverables:**
- [ ] Users can sign up, sign in, sign out
- [ ] All API calls require valid JWT
- [ ] Student and teacher roles working

**Mentor Session Prep (멘토링 준비):**
- Prepare architecture diagram to show mentor
- List of 3 specific technical questions for mentor
- Demo current state: upload + RAG working
- Ask about: S3 Vectors best practices, Bedrock KB optimization

---

## Week 7 (2026-04-17) — React Frontend + Citations

**Sprint Goal:** Build complete frontend with chat UI and PDF citation viewer

**Course Topic:** 시스템 구현 II

| Task | Owner | Status |
|:-----|:------|:------:|
| Build chat interface (message list, input, send) | Frontend | To Do |
| Display citations with page numbers | Frontend | To Do |
| PDF viewer component (react-pdf) | Frontend | To Do |
| Citation click --> highlight in PDF viewer | Frontend | To Do |
| File upload UI with progress indicator | Frontend | To Do |
| Document list and delete UI | Frontend | To Do |
| Responsive design (mobile-friendly) | Frontend | To Do |
| Connect all API endpoints to frontend | Frontend | To Do |

**Deliverables:**
- [ ] Full React app: login --> upload --> chat --> citations
- [ ] PDF viewer with citation highlighting
- [ ] Mobile-responsive layout

**Mentor Session Prep (멘토링 준비):**
- Full end-to-end demo for mentor feedback
- Ask about: CloudFront setup, CORS configuration
- Ask about: midterm demo tips from previous years

---

## Week 8 (2026-04-24) — 중간고사 MVP Demo

**Sprint Goal:** Deliver an impressive midterm demo; everything works end-to-end

**Course Topic:** 중간고사 (Midterm Exam)

| Task | Owner | Status |
|:-----|:------|:------:|
| Integration testing (all flows) | Team | To Do |
| Deploy to CloudFront (live URL) | Backend | To Do |
| Prepare demo script (4 minutes) | Team | To Do |
| Rehearse demo 3x | Team | To Do |
| Prepare backup: recorded demo video | Team | To Do |
| Create architecture slide for presentation | Team | To Do |
| Prepare cost report (actual vs projected) | Backend | To Do |
| Bug fixes and UI polish | Team | To Do |

**Demo Script (4 minutes):**
1. (30s) Open app, show login with Cognito
2. (30s) Upload "생물학 교과서.pdf", show Step Functions processing
3. (45s) Ask: "세포 분열의 단계를 설명해줘" --> show answer + citations
4. (30s) Click citation --> PDF viewer highlights source
5. (60s) Show architecture: 10+ services, SAM template, serverless
6. (30s) Show cost report: actual spend so far
7. (15s) Preview upcoming features: quiz, OCR, TTS

**Deliverables:**
- [ ] Working MVP (live CloudFront URL)
- [ ] Demo presentation (4 min)
- [ ] Midterm report document
- [ ] Backup demo video

**CRITICAL: No new features this week. Focus only on stability and demo prep.**

---

## Week 9 (2026-05-01) — Post-Midterm Improvements

**Sprint Goal:** Fix midterm feedback issues; improve core UX

**Course Topic:** 시스템 고도화

| Task | Owner | Status |
|:-----|:------|:------:|
| Review and address professor feedback from midterm | Team | To Do |
| Multi-document support (select which PDF to query) | Backend | To Do |
| Conversation history UI (past chats) | Frontend | To Do |
| Improve loading states and error handling | Frontend | To Do |
| Add streaming response support (if possible) | Backend | To Do |
| Performance optimization (Lambda cold start) | Backend | To Do |

**Deliverables:**
- [ ] Midterm feedback addressed
- [ ] Multi-document query support
- [ ] Improved UX (loading, errors, history)

---

## Week 10 (2026-05-08) — Quiz Generation

**Sprint Goal:** Build AI-powered quiz generation from document content

**Course Topic:** 보안/운영 설계

| Task | Owner | Status |
|:-----|:------|:------:|
| Implement Lambda:quiz (generate endpoint) | Backend | To Do |
| Design quiz prompt template for Claude Haiku | Backend | To Do |
| Generate MCQ (3) + short answer (2) questions | Backend | To Do |
| Implement quiz scoring logic | Backend | To Do |
| Store quiz results in DynamoDB | Backend | To Do |
| Build quiz UI (question display, answer input, score) | Frontend | To Do |
| Quiz history page (past scores) | Frontend | To Do |
| API Gateway throttling + API security review | Backend | To Do |

**Deliverables:**
- [ ] Working quiz generation from any uploaded document
- [ ] Quiz UI with scoring
- [ ] Security review document

---

## Week 11 (2026-05-15) — Textract OCR + Polly TTS

**Sprint Goal:** Add photo OCR and text-to-speech features

**Course Topic:** 테스트/검증

| Task | Owner | Status |
|:-----|:------|:------:|
| Implement Lambda:textract (image upload + OCR) | Backend | To Do |
| Connect Textract output to RAG query flow | Backend | To Do |
| Implement Lambda:polly (text-to-speech) | Backend | To Do |
| Configure Polly Korean voice (Seoyeon) | Backend | To Do |
| Build OCR UI (camera/upload image, show extracted text) | Frontend | To Do |
| Build TTS UI (play button on each answer) | Frontend | To Do |
| Audio player component | Frontend | To Do |
| Write test plan document | Team | To Do |

**Deliverables:**
- [ ] Photo OCR: take picture --> get AI answer
- [ ] TTS: click "Listen" --> hear answer in Korean
- [ ] Test plan document

---

## Week 12 (2026-05-22) — Teacher Dashboard + Documentation

**Sprint Goal:** Build teacher dashboard; write technical documentation

**Course Topic:** 프로젝트 문서화

| Task | Owner | Status |
|:-----|:------|:------:|
| Custom CloudWatch metrics (queries/day, quiz scores) | Backend | To Do |
| Implement dashboard API endpoint | Backend | To Do |
| Build teacher dashboard UI | Frontend | To Do |
| Show: total queries, active students, quiz avg, popular topics | Frontend | To Do |
| X-Ray tracing setup for all Lambda functions | Backend | To Do |
| Write API documentation (OpenAPI spec) | Backend | To Do |
| Write architecture documentation | Team | To Do |
| Write user guide (for 고등학생 testers) | Team | To Do |

**Deliverables:**
- [ ] Teacher dashboard with CloudWatch metrics
- [ ] X-Ray tracing enabled
- [ ] API documentation
- [ ] Architecture documentation
- [ ] User guide for testers

---

## Week 13 (2026-05-29) — Real User Testing

**Sprint Goal:** Test with 고등학생; collect real feedback data

**Course Topic:** 발표 준비

| Task | Owner | Status |
|:-----|:------|:------:|
| Recruit 5+ high school student testers | Team | To Do |
| Create testing protocol (tasks to perform) | Team | To Do |
| Create feedback form (Google Forms) | Team | To Do |
| Conduct user testing sessions | Team | To Do |
| Collect and analyze feedback | Team | To Do |
| Fix critical bugs found during testing | Team | To Do |
| Start final presentation outline | Team | To Do |

**Testing Protocol:**
1. Sign up and log in (test Cognito flow)
2. Upload a textbook PDF (test upload pipeline)
3. Ask 3 questions about the content (test RAG quality)
4. Generate a quiz and take it (test quiz feature)
5. Try photo OCR with a textbook page (test Textract)
6. Listen to an answer with TTS (test Polly)
7. Fill out feedback form (satisfaction, usability, suggestions)

**Mentor Session Prep (멘토링 준비):**
- Show user testing results and feedback
- Demo all features end-to-end
- Ask about: final presentation structure, grading priorities
- Ask about: any AWS best practices we are missing

**Deliverables:**
- [ ] User testing completed (5+ testers)
- [ ] Feedback analysis report
- [ ] Bug fixes from testing

---

## Week 14 (2026-06-05) — Cost Optimization + Final Prep

**Sprint Goal:** Optimize costs; prepare all final deliverables

**Course Topic:** 최종 멘토링

| Task | Owner | Status |
|:-----|:------|:------:|
| Generate cost report (actual vs projected, per service) | Backend | To Do |
| Identify and implement cost optimizations | Backend | To Do |
| Record 3-minute demo video | Team | To Do |
| Write comprehensive README.md | Team | To Do |
| Final presentation slides (6 min structure) | Team | To Do |
| Prepare answers for 10 likely professor questions | Team | To Do |
| End-to-end regression testing | Team | To Do |
| Verify live CloudFront URL works perfectly | Backend | To Do |

**Mentor Session Prep (최종 멘토링 / Proserve):**
- Full final demo rehearsal for mentor
- Show cost report and optimization
- Get final feedback before presentation
- Ask for any last-minute AWS tips

**Deliverables:**
- [ ] Cost optimization report
- [ ] 3-minute demo video (uploaded to YouTube/S3)
- [ ] README with setup guide and live URL
- [ ] Final presentation slides

---

## Week 15 (2026-06-12) — 기말고사 Final Demo

**Sprint Goal:** Deliver an A+ final demo

**Course Topic:** 기말고사 (Final Exam)

| Task | Owner | Status |
|:-----|:------|:------:|
| Rehearse final demo 5 times | Team | To Do |
| Time each rehearsal (target: 6 minutes) | Team | To Do |
| Prepare demo failure contingency plan | Team | To Do |
| Final bug fixes only (no new features!) | Team | To Do |
| Submit all documentation | Team | To Do |
| Submit GitHub repo link | Team | To Do |
| Submit live URL | Team | To Do |
| Deliver final presentation | Team | To Do |

**Final Demo Structure (6 minutes):**
1. (30s) Problem statement + public value
2. (30s) Login as student (Cognito)
3. (45s) Upload PDF, show Step Functions pipeline
4. (60s) Q&A with citations + PDF highlighting
5. (30s) Generate quiz, answer questions, show score
6. (30s) Photo OCR demo
7. (20s) TTS demo (play audio answer)
8. (20s) Switch to teacher account, show dashboard
9. (30s) Architecture overview (15 services, serverless)
10. (25s) Cost report ($X total for 15 weeks)
11. (20s) User testing results (고등학생 feedback)
12. (20s) Conclusion + future roadmap

**Contingency Plan:**
- If live demo fails: switch to recorded video immediately
- If internet is slow: use mobile hotspot as backup
- If Bedrock times out: have pre-cached response ready
- Bring laptop charger, have slides on USB drive too

**Deliverables:**
- [ ] Final presentation delivered
- [ ] All documentation submitted
- [ ] Live URL confirmed working
- [ ] Demo video link shared
- [ ] GitHub repository link submitted

**CRITICAL: Absolutely no new features. Only stability and rehearsal.**

---

## Summary: Key Milestones

| Week | Milestone | Importance |
|:----:|:----------|:----------:|
| 3 | PoC validation (S3 Vectors + citations) | Critical |
| 5 | RAG query working end-to-end | High |
| 7 | Frontend complete with citation viewer | High |
| **8** | **중간고사 MVP Demo** | **Critical** |
| 10 | Quiz generation working | Medium |
| 11 | OCR + TTS features complete | Medium |
| 13 | User testing with 고등학생 | High |
| **15** | **기말고사 Final Demo** | **Critical** |

---

## Team Velocity Notes

- Each sprint is 1 week (Friday to Friday)
- Sprint planning: Friday after class
- Sprint review: Thursday evening (day before class)
- If a task takes longer than expected, de-scope the lowest priority item
- MVP features are always prioritized over enhancement features
- Never add new features in demo weeks (Week 8, Week 15)

---

> Document version: v2.0 | 2026-03-19 | Weekly Sprint Plan
