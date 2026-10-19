import os
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ==========================================
# 1. 페이지 설정 및 디자인 스타일 (CSS)
# ==========================================
st.set_page_config(
    page_title="AI 진로 상담 - 너의 고민, AI와 함께",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* 전체 배경 및 폰트 느낌 설정 */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #EEF2FF;
        border-right: 1px solid #E2E8F0;
    }
    
    /* 메인 타이틀 */
    .app-header {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
        padding-bottom: 5px;
    }
    .app-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 20px;
    }

    /* AI 인사말 박스 스타일링 */
    .ai-welcome-box {
        background-color: #EFF6FF;
        border: 1px solid #DBEAFE;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        color: #1E3A8A;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 메인 바로가기 카드 버튼 스타일 */
    .stButton > button {
        width: 100%;
        height: 100px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        border-color: #93C5FD;
    }

    /* 사이드바 하단 감성 문구 */
    .sidebar-footer {
        margin-top: 40px;
        padding: 15px;
        background-color: #E0E7FF;
        border-radius: 12px;
        color: #3730A3;
        font-size: 0.9rem;
        line-height: 1.5;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Gemini API 클라이언트 초기화 함수
# ==========================================
@st.cache_resource
def get_genai_client():
    api_key = None
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]

    if not api_key:
        return None
    
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"GenAI 클라이언트 생성 오류: {e}")
        return None

client = get_genai_client()

# ==========================================
# 3. 사이드바 (프로필 및 메뉴 설정)
# ==========================================
with st.sidebar:
    st.markdown("### 🤖 AI 진로 상담")
    st.caption("너의 고민, AI와 함께")
    st.markdown("---")

    # 세션 상태 초기화 버튼 (새로운 상담)
    if st.button("💬 새로운 상담 시작하기", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_prompt = ""
        st.rerun()

    st.markdown("---")
    st.markdown("#### 👤 내 프로필 설정")
    mbti = st.selectbox("성격 유형 (MBTI)", [
        "선택 안함", "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ])
    interests = st.text_input("관심 분야 / 흥미", placeholder="예: IT, 디자인, 심리학")
    strengths = st.text_input("강점 / 잘하는 과목", placeholder="예: 수학, 영어, 소통능력")
    target_field = st.text_input("희망 학과 / 직업", placeholder="예: 컴퓨터공학과, PD")

    # 감성 문구
    st.markdown("""
    <div class="sidebar-footer">
        🌱 <br>
        지금의 고민이<br>
        너의 더 멋진<br>
        미래를 만들 거야 :)
    </div>
    """, unsafe_allow_html=True)

profile_summary = f"""
[사용자 프로필]
- MBTI: {mbti}
- 관심 분야: {interests if interests else '미입력'}
- 강점: {strengths if strengths else '미입력'}
- 희망 학과/직업: {target_field if target_field else '미입력'}
"""

# ==========================================
# 4. 메인 화면 헤더 및 API 키 검증
# ==========================================
st.markdown('<div class="app-header">🤖 AI 진로 상담</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">너의 고민, AI와 함께 나누어 보세요.</div>', unsafe_allow_html=True)

if not client:
    st.warning("⚠️ **GEMINI_API_KEY**가 설정되지 않았습니다. Secrets 설정을 확인해주세요.")
    st.info("""
    **Secrets 설정 방법:**
    ```toml
    GEMINI_API_KEY = "your_gemini_api_key_here"
    ```
    """)
    st.stop()

# ==========================================
# 5. AI 인사말 메인 안내 상자
# ==========================================
st.markdown("""
<div class="ai-welcome-box">
    <strong>🤖 안녕하세요! 저는 여러분의 진로를 함께 고민해주는 AI 상담사예요 😊</strong><br><br>
    궁금한 게 있으면 언제든지 편하게 말해주세요!<br>
    성격, 적성, 흥미, 학과, 직업 추천부터 진로 고민까지 다 들어줄게요.
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. 6가지 파스텔 카드 메뉴
# ==========================================
st.markdown("#### ✨ 지금 무엇을 도와드릴까요?")

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👤\n나에게 맞는 학과 추천", key="btn1"):
        st.session_state.current_prompt = "내 프로필과 성향을 분석해서 나에게 가장 잘 어울리는 학과 3가지를 추천해주고 이유를 설명해줘."
    if st.button("📄\n진로 정보 제공", key="btn4"):
        st.session_state.current_prompt = "최근 유망한 진로 분야 및 트렌드에 대해 자세히 알려줘."

with col2:
    if st.button("💼\n직업 추천", key="btn2"):
        st.session_state.current_prompt = "나의 관심사 및 강점을 바탕으로 미래 전망이 좋은 추천 직업 3가지를 제시해줘."
    if st.button("🧩\n진로 탐구 활동 추천", key="btn5"):
        st.session_state.current_prompt = "생활기록부나 포트폴리오에 활용하기 좋은 진로 심화 탐구 주제 및 활동 아이디어 3가지를 추천해줘."

with col3:
    if st.button("💬\n진로 고민 상담", key="btn3"):
        st.session_state.current_prompt = "요즘 진로를 어떻게 정해야 할지 고민이 많아. 어떤 순서로 진로를 탐색하면 좋을까?"
    if st.button("📚\n추천 콘텐츠 보기\n(도서/영화 등)", key="btn6"):
        st.session_state.current_prompt = "나의 진로 탐색 및 영감에 도움이 될 만한 추천 도서나 영화/강연 3가지를 소개해줘."

st.markdown("---")

# ==========================================
# 7. 대화 세션 관리 및 입력 창
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 채팅 입력 또는 카드 버튼 클릭 처리
user_input = st.chat_input("메시지를 입력하세요...")
prompt_to_send = None

if user_input:
    prompt_to_send = user_input
elif st.session_state.current_prompt:
    prompt_to_send = st.session_state.current_prompt
    st.session_state.current_prompt = ""  # 일회성 사용 후 초기화

# 질문 답변 생성
if prompt_to_send:
    st.session_state.messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user"):
        st.markdown(prompt_to_send)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 *답변을 작성하고 있어요...*")

        system_instruction = f"""
        당신은 따뜻하고 공감 능력이 뛰어난 진로 전문 AI 상담사입니다.
        아래 사용자 프로필을 바탕으로 친절하고 다정하게 답변해 주세요.
        답변은 읽기 쉽도록 마크다운 기호와 이모지를 적절히 활용하세요.

        {profile_summary}
        """

        try:
            # gemini-3.5-flash-lite 최신 모델로 변경
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=f"{system_instruction}\n\n사용자 질문: {prompt_to_send}",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1500,
                )
            )
            bot_response = response.text
            message_placeholder.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

        except APIError as e:
            message_placeholder.error(f"Gemini API 오류가 발생했습니다: {e.message}")
        except Exception as e:
            message_placeholder.error(f"오류가 발생했습니다: {str(e)}")
