"""
AI 챗봇 라우터 (스켈레톤) - TVING

[Day3 구현 가이드]
DB에서 콘텐츠 정보를 가져와 Bedrock FM에 전달하여 추천하는 방식입니다.
Knowledge Base 없이 DB 데이터를 직접 프롬프트 컨텍스트로 사용합니다.

사전 준비:
- AWS CLI 설정 (aws configure)
- Bedrock 모델 접근 권한 활성화
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import ChatRequest, ChatResponse
from crud import get_all_contents_for_chat
from config import AWS_REGION, BEDROCK_MODEL_ID

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    AI 콘텐츠 추천 챗봇 (AWS Bedrock)

    사용 예시:
    - "요즘 인기 있는 드라마 추천해줘"
    - "범죄 스릴러 장르로 뭐 볼 게 있어?"
    - "주말에 볼 만한 예능 추천"
    """
    user_message = request.message
    
    # [Step 1] DB에서 콘텐츠 정보 가져오기
    contents = get_all_contents_for_chat(db)
    content_info = "\n".join([
        f"- {c.title} (카테고리: {c.category}, 장르: {c.genre}, 시즌: {c.total_seasons}, 에피소드: {c.total_episodes}편)"
        for c in contents
    ])

    # ============================================
    # TODO: 여기에 AWS Bedrock 연동 코드를 작성하세요
    # ============================================
    """
    import boto3
    import json
    
    client = boto3.client('bedrock-runtime', region_name=AWS_REGION)
    
    prompt = f'''당신은 TVING의 AI 콘텐츠 추천 전문가입니다.
아래 콘텐츠 목록을 참고하여 시청자의 취향에 맞는 콘텐츠를 추천해주세요.
장르, 분위기, 시청 시간을 고려하여 추천합니다.

[보유 콘텐츠 목록]
{content_info}

[고객 질문]
{user_message}

친절한 톤으로 한국어로 답변해주세요.'''
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })
    
    response = client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        contentType='application/json'
    )
    
    result = json.loads(response['body'].read())
    reply = result['content'][0]['text']
    return ChatResponse(reply=reply)
    """
    
    # [임시 응답]
    return ChatResponse(
        reply=f"[AI 챗봇 준비 중] '{user_message}'에 대한 답변을 준비하고 있습니다. "
              f"Day3에 AWS Bedrock을 연동하면 실제 AI 추천을 받을 수 있습니다! "
              f"현재 {len(contents)}개의 콘텐츠가 등록되어 있습니다."
    )
