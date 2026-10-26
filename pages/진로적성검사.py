import streamlit as st
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #fff0f6 0%, #fff9fc 55%, #ffffff 100%); }
    .main .block-container { max-width: 850px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero { background: linear-gradient(135deg, #ffd6e7, #ffeaf3); border: 1px solid #f4aeca; border-radius: 22px; padding: 1.4rem 1.5rem; }
    .hero h1 { margin: 0; color: #7d244b; }
    .hero p { color: #934866; margin-bottom: 0; }
    .small-note { color: #536779; font-size: 0.9rem; }
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
st.write("")

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if not st.session_state.show_result:
    st.subheader("검사 안내")
    st.write("각 문항을 읽고 평소 나의 모습과 가장 가까운 답을 골라 주세요. 정답은 없으며, 솔직하게 답할수록 나를 이해하는 데 도움이 됩니다.")
    st.caption("총 18문항 · 약 3분 · 결과는 진로 탐색을 위한 참고 자료입니다.")
    st.progress(
        sum(1 for i in range(len(QUESTIONS)) if st.session_state.get(f"answer_{i}") is not None)
        / len(QUESTIONS)
    )

    with st.form("career_test_form"):
        for i, (question, kind) in enumerate(QUESTIONS):
            st.markdown(f"**Q{i + 1}. {question}**")
            st.radio(
                "나와 얼마나 비슷한가요?",
                options=list(CHOICES.keys()),
                index=None,
                key=f"answer_{i}",
                horizontal=True,
                label_visibility="collapsed",
            )
            if i < len(QUESTIONS) - 1:
                st.divider()

        submitted = st.form_submit_button("검사 결과 확인하기", type="primary", use_container_width=True)

    if submitted:
        missing = [i + 1 for i in range(len(QUESTIONS)) if st.session_state.get(f"answer_{i}") is None]
        if missing:
            st.warning(f"아직 답하지 않은 문항이 {len(missing)}개 있어요. 모든 문항에 답한 뒤 결과를 확인해 주세요.")
        else:
            st.session_state.show_result = True
            st.rerun()
else:
    answers = {i: st.session_state.get(f"answer_{i}") for i in range(len(QUESTIONS))}
    scores = calculate_scores(answers)
    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top_type, top_score = ranked[0]
    second_type = ranked[1][0]

    st.subheader("검사 결과")
    st.success(f"가장 높은 흥미 유형은 **{top_type}** {TYPE_INFO[top_type]['emoji']} 입니다!")
    st.markdown(f"### {TYPE_INFO[top_type]['summary']}")
    st.write("이 결과는 현재 답변에서 드러난 흥미를 요약한 것으로, 여러분의 능력이나 미래를 확정하는 결과는 아니에요.")

    st.markdown("#### 흥미 유형별 점수")
    max_score = 12
    for kind, score in ranked:
        st.write(f"**{TYPE_INFO[kind]['emoji']} {kind}** · {score}/{max_score}점")
        st.progress(score / max_score)

    st.markdown("### 💼 추천 직업")
    st.write("관심을 더 알아볼 만한 직업들이에요. 직업 이름을 보고 실제 하는 일과 필요한 역량도 함께 조사해 보세요.")
    jobs_html = "".join(
        f'<div style="font-size:1.35rem;font-weight:700;padding:0.7rem 0.9rem;margin:0.45rem 0;'
        f'background:#ffe3ef;border:1px solid #f4b6d0;border-radius:12px;color:#8a2852;">'
        f'⭐ {job}</div>'
        for job in TYPE_INFO[top_type]["jobs"]
    )
    st.markdown(jobs_html, unsafe_allow_html=True)

    st.markdown("#### 나의 강점 키워드")
    st.write(" · ".join(TYPE_INFO[top_type]["strengths"]))
    st.markdown("#### 다음 단계")
    st.info(TYPE_INFO[top_type]["tips"])

    st.markdown("#### 함께 살펴볼 유형")
    st.write(f"두 번째로 점수가 높은 유형은 **{second_type}** {TYPE_INFO[second_type]['emoji']} 입니다. 두 유형의 특징을 함께 살펴보면 진로 선택의 폭을 넓힐 수 있어요.")

    with st.expander("유형별 특징 모두 보기"):
        for kind, info in TYPE_INFO.items():
            st.markdown(f"**{info['emoji']} {kind}**")
            st.write(info["summary"])
            st.caption("추천 직업: " + ", ".join(info["jobs"]))

    st.caption("참고: 이 검사는 학습·진로 탐색을 돕기 위한 간단한 자기보고형 활동이며, 전문적인 진로검사나 상담을 대체하지 않습니다.")
    if st.button("처음부터 다시 검사하기", type="primary", use_container_width=True):
        reset_test()
        st.rerun()
