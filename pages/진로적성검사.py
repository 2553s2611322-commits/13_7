import streamlit as st

st.set_page_config(
    page_title="나를 알아가는 진로적성검사",
    page_icon="🧭",
    layout="centered",
)

TYPE_INFO = {
    "탐구형": {
        "emoji": "🔬",
        "summary": "궁금한 것을 깊이 파고들고 자료와 근거를 바탕으로 문제를 해결하는 활동을 좋아해요.",
        "jobs": ["연구원", "데이터 분석가", "과학자", "수의사", "시장 조사 분석가"],
        "strengths": ["분석하기", "관찰하기", "논리적으로 생각하기"],
        "tip": "관심 있는 주제를 정해 자료를 찾아보고, 결과를 표나 짧은 보고서로 정리해 보세요.",
    },
    "창의형": {
        "emoji": "🎨",
        "summary": "새로운 아이디어를 떠올리고 글·그림·영상 등으로 자신만의 생각을 표현하는 것을 좋아해요.",
        "jobs": ["디자이너", "작가", "영상 제작자", "콘텐츠 기획자", "건축가"],
        "strengths": ["상상하기", "표현하기", "새롭게 만들기"],
        "tip": "작은 작품이나 콘텐츠를 하나 완성해 보고, 어떤 과정이 가장 즐거웠는지 기록해 보세요.",
    },
    "실행형": {
        "emoji": "🛠️",
        "summary": "직접 만들고 조작하거나 몸을 움직여 실제 결과물을 완성하는 활동을 좋아해요.",
        "jobs": ["로봇·기계 기술자", "요리사", "제품 제작자", "운동 지도자", "정비 기술자"],
        "strengths": ["실행하기", "도구 활용하기", "직접 시험해 보기"],
        "tip": "과학 실험, 만들기, 요리, 스포츠처럼 직접 해 볼 수 있는 활동에 참여해 보세요.",
    },
    "도움형": {
        "emoji": "🤝",
        "summary": "다른 사람의 이야기를 듣고 돕거나 함께 배우고 성장하는 활동에서 보람을 느껴요.",
        "jobs": ["교사", "상담사", "간호사", "사회복지사", "작업치료사"],
        "strengths": ["공감하기", "설명하기", "협력하기"],
        "tip": "친구에게 공부 내용을 설명하거나 봉사활동에 참여하며 잘 맞는 역할을 찾아보세요.",
    },
    "도전형": {
        "emoji": "🚀",
        "summary": "목표를 세우고 사람들을 설득하거나 계획을 이끌며 새로운 일에 도전하는 것을 좋아해요.",
        "jobs": ["기업가", "마케팅 기획자", "프로젝트 매니저", "변호사", "행사 기획자"],
        "strengths": ["목표 세우기", "의견 전달하기", "주도하기"],
        "tip": "모둠 활동에서 작은 목표와 역할을 정해 진행을 맡아 보고 결과를 돌아보세요.",
    },
    "체계형": {
        "emoji": "📊",
        "summary": "정보를 정리하고 순서와 규칙을 세우며 꼼꼼하게 계획을 실행하는 활동을 좋아해요.",
        "jobs": ["회계 담당자", "사서", "행정 담당자", "품질 관리 담당자", "정보 관리 전문가"],
        "strengths": ["정리하기", "계획하기", "세부 사항 확인하기"],
        "tip": "관심 있는 과제의 일정표나 체크리스트를 만들어 계획대로 진행해 보세요.",
    },
}

QUESTIONS = [
    ("새로운 주제의 원리나 이유를 찾아보는 것이 재미있다.", "탐구형"),
    ("그림, 글, 영상 등으로 나만의 아이디어를 표현하고 싶다.", "창의형"),
    ("설명서를 보고 물건을 직접 조립하거나 만들어 보는 편이다.", "실행형"),
    ("친구가 고민을 이야기하면 들어주고 해결을 도와주고 싶다.", "도움형"),
    ("모둠에서 목표를 정하고 사람들을 이끄는 역할이 좋다.", "도전형"),
    ("자료와 물건을 기준에 따라 정리하는 것이 편하다.", "체계형"),
    ("실험이나 조사로 사실을 확인하는 과정이 흥미롭다.", "탐구형"),
    ("정해진 답보다 여러 가지 독창적인 방법을 생각하는 편이다.", "창의형"),
    ("직접 움직이거나 도구를 사용해 결과를 만드는 것이 좋다.", "실행형"),
    ("누군가에게 내용을 알려 주거나 함께 연습하는 것이 좋다.", "도움형"),
    ("발표나 토론에서 내 의견을 말하고 다른 사람을 설득하는 편이다.", "도전형"),
    ("숫자, 일정, 목록을 꼼꼼하게 확인하는 편이다.", "체계형"),
    ("복잡한 문제를 작은 부분으로 나누어 분석하는 것이 좋다.", "탐구형"),
    ("새로운 디자인이나 이야기의 분위기를 구상하는 것이 좋다.", "창의형"),
    ("생각만 하기보다 먼저 시도해 보며 배우는 편이다.", "실행형"),
    ("사람들의 기분을 살피고 서로 협력하도록 돕는 편이다.", "도움형"),
    ("계획을 세워 목표를 달성하거나 프로젝트를 추진하는 것이 좋다.", "도전형"),
    ("정해진 절차를 따라 정확하게 일을 마무리하는 것이 좋다.", "체계형"),
]

CHOICES = ["매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "전혀 그렇지 않다"]
CHOICE_SCORE = {
    "매우 그렇다": 4,
    "그렇다": 3,
    "보통이다": 2,
    "그렇지 않다": 1,
    "전혀 그렇지 않다": 0,
}

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fff2f7 0%, #fffafd 55%, #ffffff 100%);
    }
    .main .block-container {
        max-width: 880px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(135deg, #ffd7e8, #ffeaf2);
        border: 1px solid #ff9fc5;
        border-radius: 24px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.4rem;
    }
    .hero h1 {
        color: #8b2453;
        font-size: 2.25rem;
        margin: 0 0 .5rem 0;
    }
    .hero p {
        color: #984b6d;
        font-size: 1.05rem;
        margin: 0;
    }
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #e75491;
        border: 1px solid #e75491;
        color: white;
        border-radius: 12px;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: #c93676;
        border-color: #c93676;
        color: white;
    }
    .job-card {
        background: #ffe3ef;
        border: 1px solid #f6a6c7;
        border-radius: 18px;
        padding: 1.1rem;
        margin: .4rem 0;
        color: #792448;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🧭 나를 알아가는 진로적성검사</h1>
      <p>간단한 질문에 답하고, 나의 흥미 유형과 어울리는 진로를 탐색해 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "show_result" not in st.session_state:
    st.session_state.show_result = False

st.subheader("검사 안내")
st.write("각 문항을 읽고 평소 나의 모습과 가장 가까운 답을 골라 주세요. 정답은 없으며, 솔직하게 답할수록 나를 이해하는 데 도움이 됩니다.")
st.caption("총 18문항 · 약 3분 · 결과는 진로 탐색을 위한 참고 자료입니다.")

if not st.session_state.show_result:
    answered_count = sum(
        1 for i in range(len(QUESTIONS))
        if st.session_state.get(f"answer_{i}") is not None
    )
    st.progress(answered_count / len(QUESTIONS), text=f"진행 상황: {answered_count}/{len(QUESTIONS)}문항")

    with st.form("career_test_form"):
        for i, (question, _kind) in enumerate(QUESTIONS):
            st.markdown(f"**Q{i + 1}. {question}**")
            st.radio(
                "나와 얼마나 비슷한가요?",
                options=CHOICES,
                index=None,
                key=f"answer_{i}",
                horizontal=False,
                label_visibility="collapsed",
            )
            if i < len(QUESTIONS) - 1:
                st.divider()
        submitted = st.form_submit_button("검사 결과 확인하기 💗", type="primary", use_container_width=True)

    if submitted:
        missing = [
            i + 1 for i in range(len(QUESTIONS))
            if st.session_state.get(f"answer_{i}") is None
        ]
        if missing:
            st.warning(f"아직 답하지 않은 문항이 {len(missing)}개 있어요. 모든 문항에 답해 주세요.")
        else:
            st.session_state.show_result = True
            st.rerun()
else:
    scores = {kind: 0 for kind in TYPE_INFO}
    for i, (_question, kind) in enumerate(QUESTIONS):
        answer = st.session_state.get(f"answer_{i}")
        if answer in CHOICE_SCORE:
            scores[kind] += CHOICE_SCORE[answer]

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top_type = ranked[0][0]
    second_type = ranked[1][0]
    info = TYPE_INFO[top_type]

    st.markdown("## 💗 검사 결과")
    st.success(f"가장 높은 흥미 유형은 {info['emoji']} {top_type}입니다!")
    st.markdown(f"### {info['summary']}")

    st.markdown("### 📈 유형별 점수")
    for kind, score in ranked:
        st.write(f"{TYPE_INFO[kind]['emoji']} **{kind}** — {score}/12점")
        st.progress(score / 12)

    st.markdown("### 💼 추천 직업")
    st.caption("관심 있는 직업을 골라 실제 하는 일과 필요한 역량도 조사해 보세요.")
    for job in info["jobs"]:
        st.markdown(f'<div class="job-card">{job}</div>', unsafe_allow_html=True)

    st.markdown("### ✨ 나의 강점 키워드")
    st.write(" · ".join(info["strengths"]))

    st.markdown("### 🌷 다음 단계")
    st.info(info["tip"])

    st.markdown("### 함께 살펴볼 유형")
    st.write(f"두 번째로 점수가 높은 유형은 **{second_type}** {TYPE_INFO[second_type]['emoji']}입니다. 두 유형의 특징을 함께 살펴보면 진로 선택의 폭을 넓힐 수 있어요.")

    with st.expander("유형별 특징 모두 보기"):
        for kind, details in TYPE_INFO.items():
            st.markdown(f"**{details['emoji']} {kind}**")
            st.write(details["summary"])
            st.caption("추천 직업: " + ", ".join(details["jobs"]))

    st.caption("이 검사는 진로 탐색을 돕기 위한 간단한 활동이며 전문적인 진로검사나 상담을 대체하지 않습니다.")
    if st.button("처음부터 다시 검사하기", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("answer_"):
                del st.session_state[key]
        st.session_state.show_result = False
        st.rerun()
