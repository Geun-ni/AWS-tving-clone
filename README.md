# TVING 클론 프로젝트

CJ AI 클라우드 엔지니어 부트캠프 실습 프로젝트

---

## 프로젝트 소개

TVING OTT 스트리밍 서비스를 간소화하여 구현한 클론 프로젝트입니다.

### 핵심 기능
- 콘텐츠 목록 (드라마/영화/예능/다큐/애니 카테고리)
- 콘텐츠 상세 (줄거리, 에피소드 목록)
- 시청 이력 (마지막 시청 지점 저장)
- 찜 목록
- 회원가입/로그인 (JWT 인증)
- AI 콘텐츠 추천 챗봇 (Day3 택1 구현)

---

## 빠른 시작

```bash
git clone https://github.com/hy-cj-ai-cloud-bootcamp/tving-clone-template.git
cd tving-clone-template
cp .env.example .env
docker-compose up --build
```

### 내 GitHub 레포로 연결하기

원본 템플릿 레포는 수업 자료이므로 직접 수정하지 않습니다. 과제 제출이나 팀 프로젝트 작업은 본인 또는 팀 GitHub 레포를 새로 만든 뒤 그 레포로 push합니다.

가장 쉬운 방법은 GitHub의 `Use this template` 버튼을 사용하는 것입니다.

1. 원본 템플릿 레포에 접속합니다.
   - https://github.com/hy-cj-ai-cloud-bootcamp/tving-clone-template
2. 오른쪽 위의 `Use this template` 버튼을 클릭합니다.
3. 본인 또는 팀 계정에 새 레포를 생성합니다.
   - 예: `my-tving-project`
4. 생성된 내 레포를 clone해서 작업합니다.
   ```bash
   git clone https://github.com/<내-GitHub-아이디>/<내-레포명>.git
   cd <내-레포명>
   cp .env.example .env
   docker-compose up --build
   ```

`git clone`으로 원본 레포를 먼저 받은 경우에는 아래 방식으로 내 레포에 연결할 수 있습니다.

1. GitHub에서 빈 레포를 새로 생성합니다.
   - 예: `my-tving-project`
   - README, `.gitignore`, license는 생성하지 않는 것을 권장합니다.
2. 원본 레포를 `upstream`으로 이름 변경합니다.
   ```bash
   git remote rename origin upstream
   ```
3. 내 GitHub 레포를 새 `origin`으로 연결합니다.
   ```bash
   git remote add origin https://github.com/<내-GitHub-아이디>/<내-레포명>.git
   ```
4. 내 레포로 push합니다.
   ```bash
   git push -u origin main
   ```
5. remote 연결 상태를 확인합니다.
   ```bash
   git remote -v
   ```

정상이라면 `origin`은 내 레포, `upstream`은 수업 원본 레포를 가리킵니다.

```text
origin    https://github.com/<내-GitHub-아이디>/<내-레포명>.git
upstream  https://github.com/hy-cj-ai-cloud-bootcamp/tving-clone-template.git
```

### 접속 URL
| 서비스 | URL |
|--------|-----|
| 웹사이트 | http://localhost |
| API 문서 (Swagger) | http://localhost:8000/docs |
| AI 챗봇 (Streamlit) | http://localhost:8501 |

---

## 프로젝트 구조

```
tving-clone/
├── docker-compose.yml
├── .env.example
├── frontend/               # Nginx + HTML/CSS/JS
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── pages/
├── backend/                # FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── auth.py         # 회원가입/로그인
│       ├── items.py        # 콘텐츠/찜/시청기록
│       └── chat.py         # AI 챗봇 (스켈레톤)
├── streamlit/              # AI 챗봇 UI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── db/
    ├── init.sql
    └── seed.sql
```

---

## API 엔드포인트

### 인증
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /api/auth/register | 회원가입 |
| POST | /api/auth/login | 로그인 (JWT 발급) |

### 콘텐츠
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | /api/contents | 목록 (?category=드라마&limit=50) |
| GET | /api/contents/{id} | 상세 (에피소드 포함) |

### 찜 목록 (로그인 필요)
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | /api/wishlist | 조회 |
| POST | /api/wishlist | 추가 |
| DELETE | /api/wishlist/{content_id} | 삭제 |

### 시청 이력 (로그인 필요)
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | /api/history | 조회 |
| POST | /api/history | 추가/업데이트 |

### AI 챗봇
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /api/chat | 메시지 전송 |

---

## 클라우드 배포 가이드 (Day2)

### AWS RDS 연결

1. **RDS 생성** — PostgreSQL 15, db.t3.micro, 퍼블릭 액세스 허용
2. **데이터 투입**
   ```bash
   psql -h <RDS엔드포인트> -U <유저> -d <DB명> -f db/init.sql
   psql -h <RDS엔드포인트> -U <유저> -d <DB명> -f db/seed.sql
   ```
3. **환경변수 변경**
   ```
   DATABASE_URL=postgresql://유저:비밀번호@<RDS엔드포인트>:5432/DB명
   ```
4. **docker-compose.yml에서 db 서비스 제거 또는 주석 처리**

### 백엔드 ECS 배포
1. `backend/` 이미지를 ECR에 Push
2. ECS Task Definition 작성
   - 컨테이너 포트: 8000
   - 환경변수: `DATABASE_URL`, `JWT_SECRET`, `AWS_REGION`, `BEDROCK_MODEL_ID`
3. ECS Service 생성 (Fargate)
4. Application Load Balancer(ALB) 연결
   - Target Group 헬스 체크 경로: `/health`
   - 보안 그룹: CloudFront 또는 실습용 접속 IP에서 8000/ALB 리스너 접근 허용

### 프론트엔드 S3 + CloudFront 배포

프론트엔드는 정적 파일이므로 ECS가 아니라 S3와 CloudFront로 배포합니다.

1. S3 버킷 생성
   ```bash
   aws s3 mb s3://<버킷명>
   ```
2. `frontend/` 정적 파일 업로드
   ```bash
   aws s3 sync frontend/ s3://<버킷명> \
     --exclude "Dockerfile" \
     --exclude "nginx.conf"
   ```
   - `aws s3 sync`: 로컬 폴더와 S3 버킷의 파일을 동기화하는 명령어입니다.
   - `frontend/`: 업로드할 로컬 폴더입니다. HTML, CSS, JS 파일이 들어 있습니다.
   - `s3://<버킷명>`: 파일을 올릴 S3 버킷 주소입니다. `<버킷명>`은 학생이 만든 실제 버킷명으로 바꿉니다.
   - `--exclude`: S3에 올리지 않을 파일을 지정합니다. `Dockerfile`, `nginx.conf`는 Docker/Nginx 배포용 파일이라 S3 정적 배포에는 필요 없습니다.

   `Dockerfile`, `nginx.conf`는 언제 사용하나요?
   - 로컬에서 `docker-compose up --build`로 실행할 때는 필요합니다.
   - 프론트엔드를 ECS 컨테이너로 배포할 때도 필요합니다.
   - S3 + CloudFront로 정적 배포할 때는 사용하지 않습니다. 이 경우 CloudFront가 정적 파일을 서빙하고, `/api/*` 라우팅도 CloudFront Behavior가 처리합니다.
3. CloudFront Distribution 생성
   - Origin 1: S3 버킷
   - Origin 2: 백엔드 ALB 주소
4. CloudFront Behavior 설정

| Path pattern | Origin | 설명 |
|--------------|--------|------|
| `/api/*` | 백엔드 ALB | FastAPI API 요청 |
| `/*` | S3 | HTML/CSS/JS 정적 파일 |

`/api/*` Behavior 권장 설정:
- Allowed HTTP methods: `GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`
- Cache policy: `CachingDisabled`
- Origin request policy: `AllViewerExceptHostHeader` 또는 `Authorization` 헤더가 포함된 정책
- Viewer protocol policy: `Redirect HTTP to HTTPS`

S3 Origin 권장 설정:
- S3 버킷은 퍼블릭 오픈 대신 CloudFront OAC(Origin Access Control)로 접근 제한
- 정적 파일 캐싱을 위해 기본 Cache policy 사용 가능

5. 기본 루트 객체(Default root object)를 `index.html`로 설정
6. CloudFront 도메인으로 접속하여 화면과 API 호출 확인

> 중요: 현재 프론트 코드는 `/api/contents`, `/api/auth/login`처럼 상대 경로로 API를 호출합니다. 따라서 CloudFront에서 `/api/*` 요청을 ALB로 보내야 합니다. S3만 연결하면 API 요청이 실패합니다.

### Streamlit 챗봇 배포
1. `streamlit/` 이미지를 ECR에 Push
2. ECS Service로 배포
3. 환경변수 `BACKEND_URL`에 백엔드 ALB 주소 입력
   ```
   BACKEND_URL=http://<백엔드-ALB-DNS>
   ```
4. 필요 시 별도 ALB 또는 CloudFront Behavior로 Streamlit 접속 경로 구성

---

## AI 챗봇 구현 (Day3 택1) — AWS Bedrock

### 아키텍처
```
사용자 질문 → Streamlit → FastAPI → DB에서 콘텐츠 데이터 조회
                                         ↓
                                  콘텐츠 정보를 프롬프트에 포함
                                         ↓
                                  AWS Bedrock (Claude) → 답변
```

### 구현 방식
- 데이터: RDS에 저장된 콘텐츠 데이터를 DB에서 직접 조회
- 이미지: S3에 썸네일 업로드 후 DB의 thumbnail_url 컬럼 업데이트
- AI: Bedrock InvokeModel로 Claude 직접 호출

### 구현 순서
1. Bedrock 모델 접근 활성화 (AWS 콘솔)
2. `.env`에 AWS 인증 정보 설정
3. `backend/routers/chat.py`에서 TODO 주석 해제
4. 재시작 후 http://localhost:8501 에서 테스트

---

## AIOps 구현 (Day3 택1) — 자유 주제

| 아이디어 | 설명 |
|----------|------|
| CloudWatch 대시보드 | CPU/메모리/요청수 모니터링 |
| 로그 분석 | Bedrock으로 에러 로그 자동 분석 |
| 이상 탐지 알람 | CloudWatch Anomaly Detection + SNS |
| 자동 스케일링 | ECS Auto Scaling + 부하 테스트 |
| CI/CD | CodePipeline 자동 배포 |
| 장애 자동 복구 | Lambda + EventBridge |

---

## 프로젝트 일정

| Day | 활동 |
|-----|------|
| Day 1 | 코드 이해 + Docker 로컬 실행 + 코드 수정 |
| Day 2 | AWS 클라우드 배포 (S3 + CloudFront + ECS + RDS) |
| Day 3 | **택1**: AI 챗봇 or AIOps 구현 + 발표 |

---

## 기술 스택

- Frontend: HTML/CSS/JS (Nginx 서빙)
- Backend: Python FastAPI
- AI Chatbot UI: Python Streamlit
- Database: PostgreSQL 15
- Container: Docker + docker-compose
- Cloud: AWS ECS, RDS, Bedrock, S3

---

## 사용 시 주의사항

- 이 프로젝트는 CJ AI 클라우드 엔지니어 부트캠프 교육용 클론 프로젝트입니다.
- 실제 TVING 서비스와 무관하며, 상업적 목적이 아닌 클라우드/AI 실습 목적으로만 사용합니다.
- `.env` 파일에는 실제 DB 비밀번호, AWS 키, Bedrock 설정 등이 들어갈 수 있으므로 GitHub에 올리지 않습니다.
- 공유할 때는 `.env.example`만 사용하고, 개인 AWS 인증 정보는 각자 로컬 또는 AWS 콘솔에서 직접 설정합니다.
- S3 + CloudFront 배포 시 `Dockerfile`, `nginx.conf`는 업로드하지 않습니다. 이 파일들은 로컬 Docker/Nginx 실행용입니다.

---

## 트러블슈팅

```bash
# 데이터 초기화 (볼륨 삭제)
docker-compose down -v
docker-compose up --build

# 백엔드 로그 확인
docker-compose logs backend

# 캐시 무시 재빌드
docker-compose build --no-cache
docker-compose up
```
