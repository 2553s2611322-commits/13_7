    scores = {name: 0 for name in TYPE_INFO}
    for idx, (_, kind) in enumerate(QUESTIONS):
        answer = st.session_state.answers.get(str(idx))
        if answer in CHOICES:
            scores[kind] += CHOICES[answer]
    return scores

# ---------- 상단 ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">CAREER EXPLORATION · 진로 탐험실</div>
  <h1>나의 흥미와 적성 발견하기 🧭</h1>
  <p>간단한 질문에 답하고, 나에게 어울릴 수 있는 활동과 직업 분야를 살펴보세요.</p>
</div>
""", unsafe_allow_html=True)
st.write("")

if st.session_state.page == "intro":
    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("✨ 검사 안내")
        st.write("총 10개의 문항으로 평소의 흥미와 활동 선호도를 살펴봅니다.")
        st.write("각 문항에 대해 가장 가까운 답을 선택하면 유형별 점수와 추천 직업 분야를 확인할 수 있어요.")
        st.markdown("**예상 소요 시간:** 약 2~3분")
        st.markdown("**답변 방법:** 맞고 틀린 답은 없어요. 평소의 나를 떠올리며 솔직하게 선택해 주세요.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("🔎 살펴볼 수 있는 유형")
        for name, info in TYPE_INFO.items():
            st.write(f"{info['emoji']} **{name}** — {info['tagline']}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.info("이 검사는 자기 이해를 돕기 위한 간단한 참고용 활동이며, 전문적인 진로검사를 대신하지 않습니다.")
    if st.button("검사 시작하기 →", type="primary", use_container_width=True):
        st.session_state.page = "questions"
        st.rerun()

elif st.session_state.page == "questions":
    st.subheader("📝 나에 대해 답해 보기")
    answered = sum(1 for i in range(len(QUESTIONS)) if str(i) in st.session_state.answers)
    st.progress(answered / len(QUESTIONS), text=f"진행 상황: {answered}/{len(QUESTIONS)} 문항")
    st.caption("각 문항에서 하나를 선택해 주세요.")
    with st.form("career_quiz"):
        for idx, (question, _) in enumerate(QUESTIONS):
            st.markdown(f"**{idx + 1}. {question}**")
            current = st.session_state.answers.get(str(idx), "보통이다")
            choice = st.radio(
                "답변을 선택하세요",
                list(CHOICES.keys()),
                index=list(CHOICES.keys()).index(current),
                key=f"question_{idx}",
                horizontal=True,
                label_visibility="collapsed",
            )
            # 폼 제출 시 저장할 답변을 별도 키에 둡니다.
            st.session_state[f"draft_{idx}"] = choice
            if idx != len(QUESTIONS) - 1:
                st.divider()
        submitted = st.form_submit_button("결과 확인하기 →", type="primary", use_container_width=True)
    if submitted:
        st.session_state.answers = {
            str(i): st.session_state.get(f"question_{i}", "보통이다")
            for i in range(len(QUESTIONS))
        }
        st.session_state.page = "result"
        st.rerun()
    if st.button("처음 화면으로 돌아가기", use_container_width=True):
        st.session_state.page = "intro"
        st.rerun()

elif st.session_state.page == "result":
    scores = calculate_scores()
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_score = ranked[0][1]
    top_types = [name for name, score in ranked if score == top_score]
    main_type = top_types[0]
    info = TYPE_INFO[main_type]

    st.markdown(f'<div class="panel"><div class="eyebrow">YOUR RESULT · 검사 결과</div><div class="result-title">{info["emoji"]} 나의 주요 유형: { " · ".join(top_types) }</div><p>{info["tagline"]}</p><p>{info["description"]}</p></div>', unsafe_allow_html=True)
    st.write("")
    col_a, col_b = st.columns([1, 1], gap="large")
    with col_a:
        st.subheader("📈 유형별 점수")
        max_score = max(scores.values()) if scores else 1
        for name, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
            st.write(f"**{TYPE_INFO[name]['emoji']} {name}** · {score}/10")
            st.progress(score / max_score if max_score else 0)
        st.caption("점수는 각 유형에 해당하는 문항 2개의 답변을 합산한 값입니다.")
    with col_b:
        st.subheader("💼 탐색해 볼 직업 분야")
        for career in info["careers"]:
            st.markdown(f"- {career}")
        st.subheader("🌱 다음 단계")
        for tip in info["tips"]:
            st.markdown(f"- {tip}")

    if len(top_types) > 1:
        st.info("여러 유형의 점수가 같아요. 아래 추천은 동점 유형 중 하나를 기준으로 표시했으니, 함께 나온 유형들도 같이 살펴보세요.")
    st.markdown("---")
    st.markdown("**기억해 주세요:** 한 가지 유형이 모든 가능성을 결정하지는 않아요. 관심사와 경험은 시간이 지나며 달라질 수 있습니다.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("답변 다시 살펴보기", use_container_width=True):
            st.session_state.page = "questions"
            st.rerun()
    with col2:
        if st.button("처음부터 다시 검사하기 ↻", type="primary", use_container_width=True):
            reset_test()
            st.rerun()

st.write("")
st.markdown('<p class="small-note" style="text-align:center;">나의 진로 탐험실 · 자기 이해를 위한 교육용 간이 검사</p>', unsafe_allow_html=True)
