"""
Centralized mock data for the StudyBot RAG chatbot prototype.
Used by mock_server.py to simulate backend responses.
"""

MOCK_DOCUMENTS = [
    {
        "id": "doc-1",
        "name": "AWS_Solutions_Architect_Study_Guide.pdf",
        "size": 4_521_000,
        "pages": 42,
        "status": "ready",
        "uploadedAt": "2026-03-17T09:30:00Z",
    },
    {
        "id": "doc-2",
        "name": "Cloud_Computing_Basics.pdf",
        "size": 2_103_000,
        "pages": 28,
        "status": "ready",
        "uploadedAt": "2026-03-16T14:20:00Z",
    },
    {
        "id": "doc-3",
        "name": "Serverless_Architecture_Patterns.pdf",
        "size": 6_780_000,
        "pages": 65,
        "status": "processing",
        "uploadedAt": "2026-03-18T11:05:00Z",
    },
]

MOCK_CHAT_RESPONSES = [
    {
        "answer": (
            "## AWS Lambda 개요\n\n"
            "AWS Lambda는 **서버리스 컴퓨팅 서비스**로, 서버를 직접 관리하지 않고도 코드를 실행할 수 있습니다.\n\n"
            "주요 특징:\n"
            "- **이벤트 기반 실행**: S3 업로드, API Gateway 요청 등 다양한 이벤트로 트리거\n"
            "- **자동 스케일링**: 요청 수에 따라 자동으로 확장/축소\n"
            "- **사용한 만큼만 비용 지불**: 실행 시간(ms 단위)과 메모리 기준 과금\n\n"
            "Lambda 함수는 최대 **15분**까지 실행 가능하며, 메모리는 128MB~10,240MB 범위에서 설정할 수 있습니다."
        ),
        "citations": [
            {"page": 12, "paragraph": 3, "text": "AWS Lambda lets you run code without provisioning or managing servers, creating workload-aware cluster scaling logic."},
            {"page": 12, "paragraph": 5, "text": "Lambda functions can run for up to 15 minutes per invocation with configurable memory from 128 MB to 10,240 MB."},
        ],
        "followUps": ["Lambda 함수의 콜드 스타트란?", "Lambda와 EC2의 차이점은?", "Lambda 비용은 어떻게 계산돼?"],
    },
    {
        "answer": (
            "## Amazon S3 스토리지 클래스\n\n"
            "Amazon S3는 다양한 **스토리지 클래스**를 제공하여 비용을 최적화할 수 있습니다.\n\n"
            "| 클래스 | 용도 | 가용성 |\n"
            "|--------|------|--------|\n"
            "| S3 Standard | 자주 접근하는 데이터 | 99.99% |\n"
            "| S3 IA | 가끔 접근하는 데이터 | 99.9% |\n"
            "| S3 Glacier | 아카이브용 장기 보관 | 99.99% |\n\n"
            "S3는 **11 nines(99.999999999%)**의 내구성을 보장하며, 데이터를 여러 가용 영역(AZ)에 자동으로 복제합니다."
        ),
        "citations": [
            {"page": 8, "paragraph": 1, "text": "Amazon S3 is designed for 99.999999999% (11 nines) of durability, automatically distributing data across a minimum of three Availability Zones."},
            {"page": 9, "paragraph": 2, "text": "S3 storage classes include Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant Retrieval, Glacier Flexible Retrieval, and Glacier Deep Archive."},
        ],
        "followUps": ["S3 버킷 정책 설정 방법은?", "S3 수명 주기 정책이란?", "S3 vs EBS 차이점은?"],
    },
    {
        "answer": (
            "## VPC (Virtual Private Cloud) 핵심 구성 요소\n\n"
            "VPC는 AWS 클라우드 내에서 **논리적으로 격리된 가상 네트워크**를 제공합니다.\n\n"
            "핵심 구성 요소:\n"
            "1. **서브넷**: 퍼블릭/프라이빗으로 나뉘며 각 AZ에 배치\n"
            "2. **라우트 테이블**: 네트워크 트래픽의 경로를 결정\n"
            "3. **인터넷 게이트웨이(IGW)**: VPC에서 인터넷으로의 연결 제공\n"
            "4. **NAT 게이트웨이**: 프라이빗 서브넷에서 인터넷 접근 허용\n"
            "5. **보안 그룹 & NACL**: 인바운드/아웃바운드 트래픽 제어\n\n"
            "VPC 피어링이나 Transit Gateway를 통해 여러 VPC를 연결할 수도 있습니다."
        ),
        "citations": [
            {"page": 22, "paragraph": 1, "text": "A VPC is a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define."},
            {"page": 23, "paragraph": 4, "text": "Security groups act as a virtual firewall at the instance level, while Network ACLs provide an additional layer of security at the subnet level."},
        ],
        "followUps": ["보안 그룹 vs NACL 차이는?", "VPC 피어링 설정 방법은?", "퍼블릭 vs 프라이빗 서브넷 차이?"],
    },
    {
        "answer": (
            "## IAM (Identity and Access Management) 모범 사례\n\n"
            "AWS IAM은 AWS 리소스에 대한 **접근을 안전하게 제어**하는 서비스입니다.\n\n"
            "### 보안 모범 사례\n"
            "- **루트 계정 사용 최소화**: MFA를 활성화하고 일상 작업에는 IAM 사용자 사용\n"
            "- **최소 권한 원칙**: 필요한 권한만 부여\n"
            "- **IAM 역할 활용**: EC2, Lambda 등에 역할을 할당하여 자격 증명 하드코딩 방지\n"
            "- **정기적인 자격 증명 교체**: 액세스 키를 주기적으로 변경\n\n"
            "IAM 정책은 **JSON 형식**으로 작성되며 Effect, Action, Resource 요소로 구성됩니다."
        ),
        "citations": [
            {"page": 15, "paragraph": 2, "text": "IAM enables you to manage access to AWS services and resources securely using users, groups, roles, and policies."},
            {"page": 16, "paragraph": 1, "text": "The principle of least privilege recommends granting only the permissions required to perform a task, reducing the potential impact of a security breach."},
        ],
        "followUps": ["IAM 역할 vs 사용자 차이는?", "MFA 설정 방법은?", "IAM 정책 JSON 예시를 보여줘"],
    },
    {
        "answer": (
            "## Amazon DynamoDB 핵심 개념\n\n"
            "DynamoDB는 AWS의 완전관리형 **NoSQL 데이터베이스** 서비스입니다.\n\n"
            "### 주요 개념\n"
            "- **테이블**: 데이터의 컬렉션\n"
            "- **항목(Item)**: 테이블의 개별 레코드\n"
            "- **속성(Attribute)**: 항목의 데이터 필드\n"
            "- **파티션 키**: 데이터 분산을 위한 기본 키\n"
            "- **정렬 키**: 같은 파티션 내 항목 정렬용 (선택사항)\n\n"
            "DynamoDB는 **한 자릿수 밀리초**의 일관된 응답 시간을 제공하며, "
            "온디맨드 모드와 프로비저닝 모드 두 가지 용량 모드를 지원합니다."
        ),
        "citations": [
            {"page": 30, "paragraph": 1, "text": "Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability."},
            {"page": 31, "paragraph": 3, "text": "DynamoDB supports two capacity modes: on-demand and provisioned, allowing you to optimize costs based on your workload patterns."},
        ],
        "followUps": ["DynamoDB vs RDS 차이는?", "GSI와 LSI의 차이점은?", "온디맨드 vs 프로비저닝 모드 비교"],
    },
    {
        "answer": (
            "## Amazon CloudFront CDN\n\n"
            "CloudFront는 AWS의 **콘텐츠 전송 네트워크(CDN)** 서비스로, "
            "전 세계 엣지 로케이션을 통해 콘텐츠를 빠르게 전달합니다.\n\n"
            "### 주요 기능\n"
            "- **엣지 캐싱**: 전 세계 400개 이상의 엣지 로케이션에서 콘텐츠 캐시\n"
            "- **오리진 설정**: S3, ALB, EC2, 외부 서버 등을 오리진으로 지정 가능\n"
            "- **HTTPS 지원**: ACM 인증서를 사용한 무료 SSL/TLS\n"
            "- **Lambda@Edge**: 엣지에서 코드 실행으로 응답 커스터마이징\n\n"
            "CloudFront는 DDoS 보호를 위해 **AWS Shield Standard**와 자동으로 통합됩니다."
        ),
        "citations": [
            {"page": 35, "paragraph": 2, "text": "Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency."},
            {"page": 36, "paragraph": 1, "text": "CloudFront integrates with AWS Shield Standard at no additional cost, providing protection against DDoS attacks."},
        ],
        "followUps": ["CloudFront 캐시 무효화 방법?", "Lambda@Edge 사용 사례는?", "CloudFront 비용 구조는?"],
    },
    {
        "answer": "## 문서 핵심 요약\n\n이 문서는 **AWS 클라우드 서비스**의 주요 개념을 다루고 있습니다.\n\n### 핵심 주제\n1. **컴퓨팅**: Lambda, EC2, ECS를 활용한 서버리스/컨테이너 아키텍처\n2. **스토리지**: S3, EBS, EFS의 특성과 사용 사례\n3. **네트워킹**: VPC, 서브넷, 보안 그룹 설계\n4. **데이터베이스**: DynamoDB, RDS, Aurora 선택 기준\n5. **보안**: IAM, KMS, CloudTrail을 통한 보안 관리\n\n이 문서는 AWS Solutions Architect 시험 준비에 적합하며, 총 **42페이지**로 구성되어 있습니다.",
        "citations": [
            {"page": 1, "paragraph": 1, "text": "This study guide covers the core AWS services needed for the Solutions Architect Associate certification."},
            {"page": 2, "paragraph": 1, "text": "Topics include compute, storage, networking, databases, and security services."},
        ],
        "followUps": ["가장 중요한 개념을 자세히 설명해줘", "시험에 자주 나오는 주제는?", "실습 프로젝트 아이디어 추천해줘"],
    },
    {
        "answer": "## Amazon Bedrock과 RAG 아키텍처\n\n**Amazon Bedrock**은 다양한 AI 모델을 API로 제공하는 완전관리형 서비스입니다.\n\n### RAG (Retrieval-Augmented Generation) 파이프라인\n1. **문서 수집**: PDF를 S3에 업로드\n2. **청킹**: 문서를 300~500 토큰 단위로 분할\n3. **임베딩**: Titan Embedding V2로 벡터화\n4. **저장**: S3 Vectors에 벡터 인덱스 저장\n5. **검색+생성**: 사용자 질문 → 유사 청크 검색 → Claude Haiku가 답변 생성\n\nBedrock Knowledge Bases를 사용하면 이 전체 파이프라인을 **코드 없이** 구성할 수 있습니다.",
        "citations": [
            {"page": 38, "paragraph": 1, "text": "Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models from leading AI companies."},
            {"page": 39, "paragraph": 2, "text": "RAG combines retrieval of relevant documents with generative AI to produce accurate, grounded responses."},
        ],
        "followUps": ["임베딩이 뭔지 설명해줘", "S3 Vectors vs OpenSearch 비교", "Bedrock 지원 모델 목록은?"],
    },
]

MOCK_QUIZ = {
    "quizId": "quiz-001",
    "questions": [
        {
            "question": "AWS Lambda 함수의 최대 실행 시간은 얼마입니까?",
            "options": ["5분", "10분", "15분", "30분"],
            "correctAnswer": 2,
            "explanation": "AWS Lambda 함수는 한 번 실행 시 최대 **15분(900초)**까지 실행할 수 있습니다. 이보다 오래 걸리는 작업은 Step Functions 등을 활용해야 합니다.",
        },
        {
            "question": "Amazon S3의 데이터 내구성(Durability)은 몇 퍼센트입니까?",
            "options": ["99.9%", "99.99%", "99.999%", "99.999999999%"],
            "correctAnswer": 3,
            "explanation": "Amazon S3는 **99.999999999%(11 nines)**의 내구성을 제공합니다. 이는 데이터가 여러 가용 영역(AZ)에 자동으로 복제되기 때문입니다.",
        },
        {
            "question": "VPC에서 프라이빗 서브넷의 인스턴스가 인터넷에 접근하려면 어떤 서비스가 필요합니까?",
            "options": ["인터넷 게이트웨이(IGW)", "NAT 게이트웨이", "VPN 게이트웨이", "Direct Connect"],
            "correctAnswer": 1,
            "explanation": "프라이빗 서브넷에서 인터넷으로 나가는 트래픽은 **NAT 게이트웨이**를 통해 라우팅됩니다. IGW는 퍼블릭 서브넷용이며, NAT 게이트웨이는 아웃바운드만 허용합니다.",
        },
        {
            "question": "IAM 정책에서 '최소 권한 원칙'이란 무엇입니까?",
            "options": [
                "모든 사용자에게 관리자 권한을 부여하는 것",
                "작업 수행에 필요한 최소한의 권한만 부여하는 것",
                "루트 계정만 사용하는 것",
                "모든 권한을 거부하는 것",
            ],
            "correctAnswer": 1,
            "explanation": "**최소 권한 원칙(Principle of Least Privilege)**은 사용자나 서비스에 업무 수행에 꼭 필요한 권한만 부여하여 보안 위험을 최소화하는 방법입니다.",
        },
        {
            "question": "DynamoDB에서 데이터를 고유하게 식별하는 데 사용되는 키는 무엇입니까?",
            "options": ["보조 인덱스", "파티션 키", "외래 키", "후보 키"],
            "correctAnswer": 1,
            "explanation": "DynamoDB에서 각 항목은 **파티션 키(Partition Key)**로 고유하게 식별됩니다. 선택적으로 정렬 키(Sort Key)를 추가하여 복합 기본 키를 구성할 수 있습니다.",
        },
    ],
}

MOCK_DASHBOARD_STATS = {
    "totalDocuments": 3,
    "totalQuestions": 47,
    "quizzesCompleted": 5,
    "studyHours": 12.5,
    "averageScore": 78,
}
