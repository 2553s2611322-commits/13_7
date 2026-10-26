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

# Custom CSS - 통일된 카드 버튼 크기 및 UI 스타일링
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
