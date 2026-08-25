"""
TVING AI 콘텐츠 추천 챗봇 - Streamlit UI
접속: http://localhost:8501
"""
import streamlit as st
import requests
import os

st.set_page_config(page_title="TVING AI 추천", page_icon="📺", layout="centered")

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.title("📺 TVING AI 콘텐츠 추천")
st.markdown("장르, 분위기, 시청 이력 기반으로 맞춤 콘텐츠를 추천해드립니다!")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! TVING AI 추천 도우미입니다. 📺\n\n어떤 콘텐츠를 찾으시나요?\n\n예시:\n- 요즘 인기 있는 드라마 추천해줘\n- 범죄 스릴러 장르로 뭐 볼 게 있어?\n- 주말에 가볍게 볼 예능 추천"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("콘텐츠 관련 질문을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("콘텐츠를 찾고 있습니다..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={"message": prompt},
                    timeout=30
                )
                reply = response.json()["reply"] if response.status_code == 200 else "서버 오류가 발생했습니다."
            except requests.exceptions.ConnectionError:
                reply = "백엔드 서버에 연결할 수 없습니다."
            except Exception as e:
                reply = f"오류: {str(e)}"
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

with st.sidebar:
    st.header("💡 사용 팁")
    st.markdown("""
    **이런 질문을 해보세요:**
    - 카테고리 (드라마, 영화, 예능, 다큐)
    - 장르 (로맨스, 스릴러, 코미디, SF)
    - 분위기 (힐링, 긴장감, 감동)
    - 시청 시간 (짧은, 긴, 주말용)
    """)
    st.divider()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
    if aws_access_key:
        st.success("✅ AWS Bedrock 연동 준비 완료")
    else:
        st.info("ℹ️ Day3에 AWS Bedrock을 연동하세요")
        st.markdown("`.env`에 AWS 인증 정보를 설정해주세요.")
    st.divider()
    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = [
            {"role": "assistant", "content": "대화가 초기화되었습니다. 📺"}
        ]
        st.rerun()
