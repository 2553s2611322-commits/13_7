import streamlit as st

st.set_page_config(
    page_title="나의 진로 탐험실",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- 기본 데이터 ----------
TYPE_INFO = {
    "탐구형": {
        "emoji": "🔬",
        "tagline": "질문하고 분석하며 답을 찾는 탐구자",
        "description": "궁금한 점을 깊이 파고들고, 자료와 근거를 바탕으로 문제를 해결하는 활동에 흥미가 있어요.",
        "careers": ["연구원", "데이터 분석가", "과학자", "의료·보건 분야", "소프트웨어 개발자"],
        "tips": ["관심 있는 주제를 정해 자료를 찾아보고 요약해 보세요.", "과학·수학·정보 관련 프로젝트를 경험해 보세요."],
    },
    "창의형": {
        "emoji": "🎨",
        "tagline": "새로운 아이디어를 만드는 창작자",
        "description": "기존의 방식에 얽매이기보다 상상력을 발휘하고, 자신만의 아이디어를 표현하는 활동을 좋아해요.",
        "careers": ["디자이너", "콘텐츠 기획자", "작가", "영상·미디어 제작자", "광고 기획자"],
        "tips": ["떠오르는 아이디어를 글·그림·영상으로 표현해 보세요.", "작은 창작 프로젝트를 끝까지 완성해 보세요."],
    },
    "사회형": {
        "emoji": "🤝",
        "tagline": "사람과 함께 성장하는 소통가",
        "description": "다른 사람의 이야기를 듣고 돕거나, 함께 협력하며 목표를 이루는 활동에서 보람을 느껴요.",
        "careers": ["교사", "상담사", "사회복지사", "간호사", "인사·교육 담당자"],
        "tips": ["모둠 활동에서 의견을 조율하거나 발표 역할을 맡아 보세요.", "봉사나 또래 멘토링처럼 사람을 돕는 경험을 해 보세요."],
    },
    "현실형": {
        "emoji": "🛠️",
        "tagline": "직접 만들고 실행하는 실천가",
        "description": "도구를 사용하거나 직접 움직여 결과물을 만드는 등 구체적이고 실용적인 활동을 선호해요.",
        "careers": ["기계·전기 기술자", "건축 분야", "조리사", "제품 개발·제작", "스포츠 지도자"],
        "tips": ["만들기·실험·수리 등 손으로 직접 해보는 활동을 찾아보세요.", "관심 분야의 실습이나 체험 프로그램에 참여해 보세요."],
    },
    "관습형": {
        "emoji": "📊",
        "tagline": "계획하고 정리하는 체계적인 관리자",
        "description": "정보를 정확하게 정리하고, 순서와 규칙에 따라 일을 처리하는 활동에 강점이 있을 수 있어요.",
        "careers": ["회계·세무 분야", "사무 행정", "기록·자료 관리", "물류 관리", "프로젝트 운영"],
        "tips": ["할 일을 목록으로 정리하고 우선순위를 정해 보세요.", "스프레드시트나 일정 관리 도구를 활용해 보세요."],
    },
}

QUESTIONS = [
    ("새로운 주제의 원리나 이유를 찾아보는 것이 재미있다.", "탐구형"),
    ("자료를 비교하거나 숫자를 분석해 결론을 내리는 편이다.", "탐구형"),
    ("새로운 이야기, 그림, 디자인 또는 콘텐츠를 만드는 것이 좋다.", "창의형"),
    ("정답이 정해지지 않은 문제에서 다양한 아이디어를 내는 편이다.", "창의형"),
    ("친구의 고민을 들어주거나 누군가를 도울 때 보람을 느낀다.", "사회형"),
    ("사람들과 역할을 나누고 협력해서 일하는 것이 좋다.", "사회형"),
    ("직접 조립하거나 만들고, 도구를 사용해 결과를 내는 것이 좋다.", "현실형"),
    ("설명만 듣기보다 직접 해보면서 배우는 것이 편하다.", "현실형"),
    ("정보와 물건을 정리하고 계획에 맞춰 진행하는 것이 좋다.", "관습형"),
    ("세부 사항을 확인하고 실수를 줄이는 일에 자신이 있다.", "관습형"),
]

CHOICES = {
    "매우 그렇다": 5,
    "그렇다": 4,
    "보통이다": 3,
    "그렇지 않다": 2,
    "전혀 그렇지 않다": 1,
}

# ---------- 디자인 ----------
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f3f8ff 0%, #eef4fb 100%); }
    .block-container { max-width: 1050px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero { background: #d8e9f8; border: 1px solid #b8d0e6; border-radius: 26px; padding: 28px 30px; }
    .eyebrow { color: #416783; font-weight: 700; letter-spacing: .08em; font-size: .82rem; }
    .hero h1 { color: #203d54; margin: 8px 0; font-size: 2.35rem; }
    .hero p { color: #38566d; font-size: 1.05rem; margin-bottom: 0; }
    .panel { background: rgba(255,255,255,.85); border: 1px solid #d7e3ee; border-radius: 20px; padding: 22px; }
    .result-title { color: #203d54; font-size: 1.8rem; font-weight: 800; }
    div.stButton > button { border-radius: 12px; min-height: 3rem; font-weight: 700; }
    div[data-testid="stProgress"] > div > div { background-color: #4f83ad; }
    .small-note { color: #60788b; font-size: .9rem; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = {}

def reset_test():
    st.session_state.page = "intro"
    st.session_state.answers = {}

def calculate_scores():
