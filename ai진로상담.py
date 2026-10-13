import streamlit as st
st.title('ai 진로상담')
st.write('내용')
import os
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ==========================================
# 1. 페이지 및 스티일 기본 설정
# ==========================================
st.set_page_config(
    page_title="AI 진로 멘토링 서비스",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI improvement
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px 8px 0px 0px;
        padding-left: 16px;
        padding-right: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Gemini API 클라이언트 초기화 함수
# ==========================================
@st.cache_resource
def get_genai_client():
    api_key = None
    # 1) Streamlit secrets 확인
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    # 2) OS 환경변수 확인
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]

    if not api_key:
        return None
    
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"GenAI 클라이언트 생성 중 오류가 발생했습니다: {e}")
        return None

client = get_genai_client()

# ==========================================
# 3. 사이드바: 사용자 진로 프로필 입력
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/illustrations/100/graduation-cap.png", width=80)
    st.title("👤 내 진로 프로필")
    st.caption("프로필을 입력하면 AI가 더 정교한 상담을 제공합니다.")

    mbti = st.selectbox("성격 유형 (MBTI)", [
        "선택 안함", "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ])
    
    interests = st.text_input("주요 관심 분야 / 흥미", placeholder="예: AI, 미술, 심리학, 환경 문제")
    strengths = st.text_input("자신있는 과목 / 강점", placeholder="예: 수학, 영어, 문제 해결력, 공감 능력")
    target_field = st.text_input("희망 학과 / 희망 직업 (선택)", placeholder="예: 컴퓨터공학과, 마케터")
    academic_level = st.select_slider(
        "현재 학업/성적 만족도",
        options=["상위권", "중상위권", "중위권", "노력 필요"],
        value="중상위권"
    )

    st.markdown("---")
    st.caption("💡 설정된 프로필은 AI 상담에 자동 조합됩니다.")

# 프로필 요약 텍스트 생성
profile_summary = f"""
[사용자 프로필 정보]
- MBTI: {mbti}
- 관심 분야: {interests if interests else '미입력'}
- 강점/자신있는 과목: {strengths if strengths else '미입력'}
- 희망 학과/직업: {target_field if target_field else '미입력'}
- 학업 성적 수준: {academic_level}
"""

# ==========================================
# 4. 메인 화면 헤더 및 API 키 검증
# ==========================================
st.markdown("<div class='main-header'>🎓 AI 진로 & 직업 탐구 멘토</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>성격, 흥미, 적성을 분석하여 최적의 학과, 직업, 탐구 활동을 추천해 드립니다.</div>", unsafe_allow_html=True)

if not client:
    st.warning("⚠️ **GEMINI_API_KEY**가 설정되지 않았습니다. Secrets 설정 또는 환경 변수를 확인해주세요.")
    st.info("""
    **설정 방법:**
    1. Streamlit Cloud 배포 시 **App Settings > Secrets** 항목으로 이동합니다.
    2. 아래와 같이 API 키를 입력합니다:
       ```toml
       GEMINI_API_KEY = "your_gemini_api_key_here"
       ```
    """)
    st.stop()

# ==========================================
# 5. 탭 구성 (상담실 / 리포트 / 탐구활동)
# ==========================================
tab1, tab2, tab3 = st.tabs(["💬 AI 진로 상담실", "📊 맞춤형 진로/학과 리포트", "🎯 진로 탐구 활동 추천"])

# ------------------------------------------
# TAB 1: AI 진로 대화 상담실
# ------------------------------------------
with tab1:
    st.subheader("💬 진로 고민 전문 AI 멘토와의 대화")
    st.write("진로 선택, 학과 정보, 공부법, 미래 직업 전망 등 궁금한 점을 편하게 질문하세요.")

    # 세션 상태 내 대화 기록 관리
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 당신의 진로 멘토입니다. 어떤 고민이나 질문이 있으신가요? 프로필 정보를 바탕으로 정성껏 답변해 드릴게요!"}
        ]

    # 기존 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("예: 인공지능 분야로 가려면 어떤 학과를 선택해야 할까요?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 *생각 중...*")

            system_instruction = f"""
            당신은 친절하고 전문적인 진로 및 진학 상담 전문가입니다.
            다음 사용자 프로필 정보를 바탕으로 공감하며 구체적이고 현실적인 진로 조언을 제공하세요.
            답변은 가독성 좋게 마크다운 형식을 활용하세요.

            {profile_summary}
            """

            try:
                # API 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=f"{system_instruction}\n\n사용자 질문: {prompt}",
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=1500,
                    )
                )
                
                bot_response = response.text
                message_placeholder.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})

            except APIError as e:
                message_placeholder.error(f"Gemini API 호출 중 오류가 발생했습니다: {e.message}")
            except Exception as e:
                message_placeholder.error(f"예기치 못한 오류가 발생했습니다: {str(e)}")

# ------------------------------------------
# TAB 2: 맞춤형 진로/학과 진단 리포트
# ------------------------------------------
with tab2:
    st.subheader("📊 프로필 기반 맞춤형 진로 분석")
    st.write("사이드바에 입력하신 프로필 정보를 바탕으로 AI가 적합한 학과와 직업을 종합 분석합니다.")

    if st.button("🚀 맞춤 진로 분석 리포트 생성하기", use_container_width=True):
        with st.spinner("사용자의 성격, 흥미, 적성을 종합 분석 중입니다..."):
            prompt = f"""
            {profile_summary}

            위 사용자 프로필을 종합적으로 분석하여 아래 형식으로 상세한 진로 추천 리포트를 작성해 주세요:

            ### 1. 💡 사용자 진로 성향 요약
            - 주요 특징 및 강점 분석

            ### 🎓 2. 추천 학과 Top 3
            1. **학과명**: (추천 이유 및 관련 핵심 과목)
            2. **학과명**: (추천 이유 및 관련 핵심 과목)
            3. **학과명**: (추천 이유 및 관련 핵심 과목)

            ### 💼 3. 추천 직업 Top 3
            1. **직업명**: (직무 설명 및 향후 전망)
            2. **직업명**: (직무 설명 및 향후 전망)
            3. **직업명**: (직무 설명 및 향후 전망)

            ### 🛠️ 4. 단기/장기 로드맵 제안
            - 현재 준비할 수 있는 사항 및 준비 전략
            """

            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.6)
                )
                st.markdown(response.text)
            except APIError as e:
                st.error(f"API 오류: {e.message}")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")

# ------------------------------------------
# TAB 3: 진로 탐구 활동 추천
# ------------------------------------------
with tab3:
    st.subheader("🎯 학종 & 포트폴리오를 위한 진로 탐구 활동 제안")
    st.write("관심 분야나 학과에 맞춰 학교 생활기록부나 개인 포트폴리오에 활용할 수 있는 심화 탐구 활동을 추천받으세요.")

    col1, col2 = st.columns(2)
    with col1:
        target_subject = st.text_input("탐구하고자 하는 주요 주제/분야", value=interests if interests else "인공지능과 윤리")
    with col2:
        activity_type = st.selectbox("원하는 활동 유형", ["전체", "독서 및 탐구 보고서", "동아리 프로젝트", "자율 연구 주제"])

    if st.button("✨ 맞춤 탐구 활동 아이디어 받기", use_container_width=True):
        with st.spinner("창의적이고 구체적인 탐구 활동을 구성 중입니다..."):
            prompt = f"""
            {profile_summary}

            - 목표 탐구 주제/분야: {target_subject}
            - 선택한 활동 유형: {activity_type}

            위 정보를 기반으로 학생/취업준비생이 실행할 수 있는 실용적이고 우수한 진로 탐구 활동 3가지를 추천해 주세요.
            각 활동마다 [활동 제목], [추천 배경/목적], [세부 실행 단계], [예상 결과물]을 포함하여 깔끔하게 마크다운으로 정리해 주세요.
            """

            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.7)
                )
                st.markdown(response.text)
            except APIError as e:
                st.error(f"API 오류: {e.message}")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
