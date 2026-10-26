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

# Custom CSS - 통일된 카드 버튼 크기
st.markdown("""
<style>
    /* 전체 배경 */
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

    /* AI 인사말 박스 */
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

    /* 카드 버튼 크기 및 텍스트 정렬 완벽 통일 */
    div[data-testid="stColumn"] {
        display: flex;
        justify-content: center;
    }
    
    div[data-testid="stColumn"] > div {
        width: 100%;
    }

    .stButton > button {
        width: 100% !important;
        height: 100px !important;
        min-height: 100px !important;
        max-height: 100px !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #1E293B !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: pre-wrap !important;
        word-break: keep-all !important;
        text-align: center !important;
        padding: 10px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
        border-color: #93C5FD !important;
        background-color: #F1F5F9 !important;
    }

    /* 현재 선택된 모드 안내 바 */
    .selected-mode-badge {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 10px 16px;
        border-radius: 12px;
        font-weight: 600;
        margin-bottom: 15px;
        display: inline-block;
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
# 2. Gemini API 클라이언트 초기화
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
        st.error(f"GenAI 클라이언트 초기화 오류: {e}")
        return None

client = get_genai_client()

# ==========================================
# 3. 세션 상태 (Session State) 초기화
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = None

# ==========================================
# 4. 사이드바 구성
# ==========================================
with st.sidebar:
    st.markdown("### 🤖 AI 진로 상담")
    st.caption("너의 고민, AI와 함께")
    st.markdown("---")

    # 새로운 상담 시작 버튼
    if st.button("💬 처음부터 다시 상담하기", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_mode = None
        st.rerun()

    st.markdown("---")
    st.markdown("#### 👤 내 프로필 (선택 입력)")
    st.caption("미리 입력해 두면 대화 시 자동 반영됩니다.")
    mbti = st.selectbox("성격 유형 (MBTI)", [
        "선택 안함", "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ])
    interests = st.text_input("관심 분야 / 흥미", placeholder="예: IT, 경영, 미술, 생명과학")
    strengths = st.text_input("강점 / 잘하는 과목", placeholder="예: 수학, 영어, 문제 해결력")

    st.markdown("""
    <div class="sidebar-footer">
        🌱 <br>
        지금의 고민이<br>
        너의 더 멋진<br>
        미래를 만들 거야 :)
    </div>
    """, unsafe_allow_html=True)

profile_summary = f"""
[사용자 기본 프로필]
- MBTI: {mbti}
- 관심 분야: {interests if interests else '대화 내용 참고'}
- 강점/잘하는 과목: {strengths if strengths else '대화 내용 참고'}
"""

# ==========================================
# 5. 메인 화면 헤더 및 API 키 검증
# ==========================================
st.markdown('<div class="app-header">🤖 AI 진로 상담</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">너의 고민, AI와 함께 나누어 보세요.</div>', unsafe_allow_html=True)

if not client:
    st.warning("⚠️ **GEMINI_API_KEY**가 설정되지 않았습니다. Secrets 설정을 확인해 주세요.")
    st.stop()

# AI 인사말 상자
st.markdown("""
<div class="ai-welcome-box">
    <strong>🤖 안녕하세요! 저는 여러분의 진로를 함께 고민해주는 AI 상담사예요 😊</strong><br><br>
    아래 버튼에서 어떤 상담을 받고 싶은지 메뉴를 먼저 선택해 주세요.<br>
    선택 후 질문에 맞춰 자신의 이야기나 정보를 적어주시면 맞춤형 상담을 도와드릴게요!
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. 통일된 카드 옵션 선택 영역
# ==========================================
st.markdown("#### ✨ 상담 옵션을 선택해 주세요")

col1, col2, col3 = st.columns(3)

def select_mode(mode_name, initial_ai_msg):
    st.session_state.selected_mode = mode_name
    if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["content"] != initial_ai_msg:
        st.session_state.messages.append({"role": "assistant", "content": initial_ai_msg})

with col1:
    if st.button("👤\n나에게 맞는 학과 추천", key="btn1"):
        select_mode(
            "학과 추천",
            "🎓 **학과 추천 상담**을 선택하셨네요!\n\n본인에게 꼭 맞는 학과를 추천해 드리기 위해 몇 가지를 여쭤볼게요. 아래 채팅창에 자유롭게 적어주세요:\n1. 평소 흥미가 있거나 좋아하는 분야\n2. 자신 있는 과목이나 강점\n3. 본인의 성격이나 희망하는 대학 생활이 있다면 말해주세요!"
        )
    if st.button("📄\n진로 정보 제공", key="btn4"):
        select_mode(
            "진로 정보 제공",
            "📄 **진로 정보 탐색** 모드입니다!\n\n궁금하신 직업군, 특정 학과, 혹은 '요즘 유망한 IT 분야 전망'처럼 알고 싶은 진로 주제나 분야를 채팅창에 입력해 주세요."
        )

with col2:
    if st.button("💼\n직업 추천", key="btn2"):
        select_mode(
            "직업 추천",
            "💼 **맞춤 직업 추천**을 원하시네요!\n\n원하시는 직업을 찾아드리기 위해 정보가 필요해요. 채팅창에 아래 내용을 남겨주세요:\n- 좋아하는 일이나 취미\n- 일할 때 중요하게 생각하는 가치 (예: 연봉, 워라밸, 창의성, 안정성 등)"
        )
    if st.button("🧩\n진로 탐구 활동 추천", key="btn5"):
        select_mode(
            "진로 탐구 활동 추천",
            "🧩 **진로 탐구 활동 추천** 모드입니다!\n\n생활기록부나 포트폴리오를 채울 활동을 찾아드릴게요. 현재 희망하는 학과/직업이나 관심 있는 탐구 주제(예: 인공지능 윤리, 기후변화 등)를 알려주세요."
        )

with col3:
    if st.button("💬\n진로 고민 상담", key="btn3"):
        select_mode(
            "진로 고민 상담",
            "💬 **진로 고민 상담소**에 오신 것을 환영해요.\n\n요즘 어떤 점이 가장 고민이신가요? (예: 적성을 모르는 문제, 진로 결정의 부담감, 공부 방법 등) 편하게 이야기해 주세요."
        )
    if st.button("📚\n추천 콘텐츠 보기\n(도서/영화 등)", key="btn6"):
        select_mode(
            "추천 콘텐츠 보기",
            "📚 **진로 영감 콘텐츠 추천** 모드입니다!\n\n관심 있는 분야나 현재 느끼는 진로 관련 감정/상태를 알려주시면 영감을 줄 수 있는 책, 영화, 강연 등을 추천해 드릴게요."
        )

st.markdown("---")

# 현재 선택된 모드 안내 표시
if st.session_state.selected_mode:
    st.markdown(f'<div class="selected-mode-badge">📌 현재 선택된 옵션: {st.session_state.selected_mode}</div>', unsafe_allow_html=True)

# ==========================================
# 7. 대화 세션 및 스트리밍 처리
# ==========================================
# 이전 대화 내역 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("답변이나 궁금한 점을 여기에 입력하세요..."):
    if not st.session_state.selected_mode:
        st.session_state.selected_mode = "일반 상담"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # 과거 대화 맥락 수집
        history_text = ""
        for msg in st.session_state.messages[:-1]:
            role_name = "사용자" if msg["role"] == "user" else "AI"
            history_text += f"{role_name}: {msg['content']}\n"

        prompt_instruction = f"""
        당신은 따뜻하고 전문적인 대한민국 진로 전문 AI 상담사입니다.
        현재 진행 중인 상담 모드: [{st.session_state.selected_mode}]
        
        {profile_summary}
        
        [이전 대화 맥락]
        {history_text}
        
        [사용자의 최근 메시지]
        {prompt}
        
        [필수 규칙 및 지침]
        1. 학과 및 직업 추천 시 **현재 대한민국 대학교에 실제로 존재하고 개설되어 있는 학과명**과 **실제 존재하는 직업명**만을 추천하세요.
        2. 학과/직업을 추천할 때 해당 분야의 핵심 진로, 배우는 내용, 그리고 사용자에게 추천하는 이유를 명확하게 설명하세요.
        3. 친절하고 공감해주는 어조로 작성하고, 이모지와 마크다운 서식을 활용해 가독성 있게 답변해 주세요.
        """

        try:
            # 요구되는 최신 모델인 gemini-3.5-flash-lite로 변경
            response = client.models.generate_content_stream(
                model='gemini-3.5-flash-lite',
                contents=prompt_instruction,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1500,
                )
            )

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
