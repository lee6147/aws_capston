# StudyBot — AI 학습 도우미 챗봇

> PDF를 업로드하면 AI가 해당 문서를 기반으로 질문에 답변하는 **RAG 챗봇**을 AWS 완전 서버리스 아키텍처로 구축합니다.

## 프로젝트 개요

| 항목 | 내용 |
|:-----|:-----|
| 과목 | AWS실전프로젝트I (1670501-01) |
| 학과 | 국민대학교 AWS·양자통신융합전공, 4학년 |
| 기간 | 2026-03-06 ~ 2026-06-12 (15주) |
| 팀 규모 | 2~3인 |
| 공적가치 | 청소년 교육 접근성 향상 |
| 15주 총 비용 | $5~8 (학생 크레딧 $100의 5~8%) |

## 핵심 가치

| 관점 | 내용 |
|:-----|:-----|
| Problem | 학생이 교과서를 복습할 때 즉각적 Q&A 도구 부재 |
| Solution | PDF → RAG(청킹→임베딩→벡터검색) → Bedrock LLM 답변 |
| UX Effect | 문서 업로드 후 즉시 대화형 Q&A, 답변마다 출처 표시 |
| Core Value | 완전 서버리스, 월 운영비 $1 미만, 교육 접근성 향상 |

## 시스템 아키텍처

```
사용자 → CloudFront + S3 (React SPA) → API Gateway
  ├─ /api/upload    → Lambda:upload    → S3 (PDF) → Bedrock KB → S3 Vectors
  ├─ /api/chat      → Lambda:chat      → Bedrock KB (RetrieveAndGenerate) → Claude 3 Haiku
  └─ /api/documents → Lambda:documents → S3 (PDF)
```

### AWS 서비스 구성

| 서비스 | 역할 | 과금 |
|:-------|:-----|:-----|
| S3 (정적 호스팅) | React SPA 호스팅 | 프리티어 |
| CloudFront | CDN + HTTPS | 프리티어 |
| API Gateway | REST API | 프리티어 |
| Lambda ×4 | upload, chat, documents | 프리티어 |
| S3 (문서 버킷) | 원본 PDF 저장 | 프리티어 |
| Bedrock KB | RAG 파이프라인 | 종량제 |
| S3 Vectors | 벡터 저장/검색 | ~$0.04/월 |
| Titan Embedding V2 | 임베딩 생성 | ~$0.02/월 |
| Claude 3 Haiku | LLM 답변 생성 | ~$0.50/월 |
| IAM | 권한 관리 | 무료 |
| CloudWatch | 모니터링 | 기본 무료 |

### 핵심 설계 결정

| 결정 | 선택 | 기각 | 근거 |
|:-----|:-----|:-----|:-----|
| 벡터DB | S3 Vectors | OpenSearch ($350/월) | 99.9% 비용 절감 |
| RAG | Bedrock KB | LangChain 직접 구현 | 코드량 80% 감소 |
| LLM | Claude 3 Haiku | Sonnet, Titan | 비용 최저 + 충분한 품질 |
| 프론트 | React + Vite | Next.js | SSR 불필요 |
| 백엔드 | Python 3.12 Lambda | TypeScript | boto3 기본 포함 |
| IaC | AWS SAM | CDK, Terraform | 학습 곡선 낮음 |

## 아이디어 비교

3개 후보 아이디어를 비교 분석 후 **A안 (RAG 챗봇)**을 선정했습니다.

| 항목 | A. RAG 챗봇 | B. 뉴스 감정분석 | C. 이미지 검색 |
|:-----|:---:|:---:|:---:|
| 15주 총 비용 | **$5~8** | $8~50 | $270+ |
| 구현 난이도 | ★★☆ | ★★☆ | ★★★☆ |
| 공적가치 | 직접 | 간접 | 간접 |
| 취업 어필 | RAG 트렌드 | 데이터 엔지니어링 | 멀티모달 AI |
| 비용 리스크 | 매우 낮음 | 낮음 | 높음 |

**선정 근거:**
1. 수업 공적가치("청소년-교육")에 유일하게 직접 부합
2. 15주 비용 $5~8 — 학생 크레딧의 5~8%
3. RAG = 2026년 산업계 최고 수요 기술
4. Bedrock 활용 → 멘토의 적극적 서포트

## 문서 구조

```
├── aws-capstone-framework.md              # 프로젝트 프레임워크 (선정안 상세)
├── 2026-03-13-aws-capstone-executive-report.md  # 기획 보고서 (전체)
├── 2026-03-13-capstone-idea-A-rag-chatbot.md    # A안: RAG 챗봇 설계
├── 2026-03-13-capstone-idea-B-news-sentiment.md # B안: 뉴스 감정분석 설계
├── 2026-03-13-capstone-idea-C-image-search.md   # C안: 이미지 검색 설계
├── index.html                             # 기획 보고서 포털 (GitHub Pages)
├── aws-capstone-all.html                  # 통합 HTML (탭 네비게이션)
├── aws캡스톤.pdf                           # 원본 PDF
└── .github/workflows/pages.yml            # GitHub Pages 배포 워크플로우
```

## 개발 타임라인

| 주차 | 활동 | 산출물 |
|:----:|:-----|:-------|
| 1~2 | 팀 빌딩, 아이디어 탐색 | 팀 구성표, 비교 분석 |
| 3 | 요구사항 정의, PoC 검증 | PoC 결과 |
| 4~5 | 아키텍처 설계, Bedrock KB 구축 | 설계서, KB 동기화 |
| 6~7 | Lambda 구현, React UI, API 연동 | 프로토타입 |
| **8** | **중간고사 — MVP 발표** | **MVP 데모** |
| 9 | 대화 이력, 다중 문서, UI 개선 | 고도화 |
| 10~12 | 보안, 테스트, 문서화 | 보안 설계서, 기술 문서 |
| 13~14 | 발표 준비, 데모 영상 | 발표 자료 |
| **15** | **기말 발표** | **최종 보고서** |

## API 명세

| Method | Path | 설명 |
|:-------|:-----|:-----|
| POST | /api/upload/presign | Presigned URL 생성 |
| POST | /api/upload/complete | 업로드 완료 + KB 동기화 |
| GET | /api/upload/status/{jobId} | 동기화 상태 조회 |
| POST | /api/chat | 질문-답변 |
| GET | /api/documents | 문서 목록 |
| DELETE | /api/documents/{id} | 문서 삭제 |

## MVP 기능 (8주차)

- PDF 업로드 (≤10MB)
- 문서 인덱싱 (Bedrock KB 자동)
- 질문-답변 (문서 기반)
- 출처 표시 (페이지/문단)
- 기본 채팅 UI

## 비용 분석

| 서비스 | 월 비용 | 15주 비용 |
|:-------|-------:|----------:|
| 프리티어 (Lambda, API GW, S3, CF) | $0 | $0 |
| Bedrock Claude 3 Haiku | ~$0.50 | ~$2.00 |
| Bedrock Titan Embedding V2 | ~$0.02 | ~$0.08 |
| S3 Vectors | ~$0.04 | ~$0.16 |
| 개발/테스트 추가 | ~$0.50 | ~$2.00 |
| **합계** | **~$1.06** | **~$4.25** |

> 벡터DB 비교: S3 Vectors($0.04/월) vs pgvector RDS($15, 375배) vs OpenSearch Serverless($350, 8,750배)

## 배포

기획 문서는 GitHub Pages로 자동 배포됩니다.

- `main` 브랜치 push 시 `.github/workflows/pages.yml` 워크플로우 실행
- `index.html` → 기획 보고서 포털 페이지

## 현재 진행 상태

> 📅 2주차 (2026-03-16 기준) — 주제 선정 및 팀 구성 단계

- [x] 팀 빌딩, AWS 계정 설정
- [x] 3안 아이디어 비교 분석
- [x] A안 (RAG 챗봇) 선정
- [x] 기획 보고서 작성 (v1.1)
- [ ] 요구사항 정의 (3주차)
- [ ] PoC 검증 — Bedrock KB + S3 Vectors (3주차)
- [ ] 아키텍처 설계 확정 (4주차)

## 기술 스택

| 영역 | 기술 |
|:-----|:-----|
| 프론트엔드 | React + Vite |
| 백엔드 | Python 3.12 (AWS Lambda) |
| AI/ML | Amazon Bedrock (Claude 3 Haiku, Titan Embedding V2) |
| RAG | Bedrock Knowledge Base + S3 Vectors |
| 인프라 | AWS SAM, CloudFront, S3, API Gateway |
| CI/CD | GitHub Actions (Pages 배포) |
