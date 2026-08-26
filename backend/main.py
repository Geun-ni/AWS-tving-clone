"""TVING 클론 - FastAPI 메인 애플리케이션"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, items, chat, ops

app = FastAPI(
    title="TVING 클론 API",
    description="CJ AI 클라우드 엔지니어 부트캠프 - TVING 클론 백엔드 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(items.router, prefix="/api", tags=["콘텐츠/찜/시청기록"])
app.include_router(chat.router, prefix="/api", tags=["AI 챗봇"])
app.include_router(ops.router, prefix="/ops", tags=["운영 장애 시뮬레이션"])

@app.get("/")
def root():
    return {"message": "TVING 클론 API 서버가 실행 중입니다!", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
