
import streamlit as st

st.set_page_config(
    page_title="꿈을 찾는 책장",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------
# 도서 데이터
# 실제 출판 도서가 아닌 앱 시연용 예시 자료
# -------------------------
CATEGORIES = [
    ("자연과학", "🧪", "#dceaff"),
    ("공학", "🖥️", "#eae2ff"),
    ("의료·보건", "💗", "#ffe0e5"),
    ("예술·체육", "🎨", "#ffead3"),
    ("인문·사회", "👥", "#d8f3e4"),
    ("교육", "📖", "#fff0bf"),
    ("경영·경제", "📊", "#d5f1f0"),
    ("농림·수산", "🌿", "#e7f5cd"),
    ("언론·미디어", "🎬", "#dce7ff"),
    ("IT·디지털", "💻", "#e9ddff"),
]

BOOKS = [
    {
        "id": 1, "title": "과학으로 만나는 미래의 직업들",
        "field": "자연과학", "emoji": "🔬", "color": "#b9dcf4",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "과학자, 생명과학자, 화학연구원",
        "description": "자연의 원리를 연구하고 새로운 사실을 발견하는 과학 분야의 직업을 알아봅니다.",
        "question": "내가 직접 연구해 보고 싶은 자연 현상은 무엇일까?",
    },
    {
        "id": 2, "title": "세상을 만드는 공학 이야기",
        "field": "공학", "emoji": "🏙️", "color": "#c9e5ec",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "건축가, 기계공학자, 항공우주공학자",
        "description": "우리 주변의 건물과 기계가 만들어지는 과정, 공학자의 역할을 소개합니다.",
        "question": "내가 새롭게 만들고 싶은 발명품은 무엇일까?",
    },
    {
        "id": 3, "title": "사람을 위한 의료의 세계",
        "field": "의료·보건", "emoji": "🩺", "color": "#f7cbd5",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "의사, 간호사, 약사",
        "description": "사람의 건강을 지키는 다양한 의료 직업과 필요한 역량을 살펴봅니다.",
        "question": "의료 분야에서 가장 중요하다고 생각하는 태도는 무엇일까?",
    },
    {
        "id": 4, "title": "예술이 있는 행복한 삶",
        "field": "예술·체육", "emoji": "🎨", "color": "#f8dfb7",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "화가, 디자이너, 체육지도사",
        "description": "창의적인 표현과 신체 활동을 통해 자신의 재능을 발전시키는 직업을 알아봅니다.",
        "question": "내가 좋아하는 활동을 직업으로 연결할 수 있을까?",
    },
    {
        "id": 5, "title": "사회를 이해하는 사람들",
        "field": "인문·사회", "emoji": "🌏", "color": "#d4eadc",
        "author": "진로책방 자료팀", "level": "보통",
        "jobs": "사회학자, 역사학자, 사회복지사",
        "description": "사람과 사회의 관계를 연구하고 사회 문제를 해결하는 직업을 알아봅니다.",
        "question": "우리 사회에서 함께 해결해야 할 문제는 무엇일까?",
    },
    {
        "id": 6, "title": "선생님이라는 멋진 꿈",
        "field": "교육", "emoji": "📚", "color": "#ffedb8",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "초등교사, 중등교사, 교육연구원",
        "description": "학생의 성장을 돕는 교사의 역할과 교육 분야의 다양한 진로를 소개합니다.",
        "question": "좋은 선생님에게 필요한 능력은 무엇일까?",
    },
    {
        "id": 7, "title": "돈과 기업의 흥미로운 이야기",
        "field": "경영·경제", "emoji": "📈", "color": "#c8eae7",
        "author": "진로책방 자료팀", "level": "보통",
        "jobs": "기업가, 회계사, 경제연구원",
        "description": "기업이 운영되는 방식과 경제 활동, 창업에 필요한 생각을 살펴봅니다.",
        "question": "좋은 기업은 어떤 역할을 해야 할까?",
    },
    {
        "id": 8, "title": "자연과 함께하는 미래",
        "field": "농림·수산", "emoji": "🌱", "color": "#dff0c2",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "농업연구원, 산림전문가, 수산생명과학자",
        "description": "식량과 숲, 바다를 지키고 지속 가능한 환경을 만드는 직업을 알아봅니다.",
        "question": "자연을 지키면서 생활에 필요한 것을 얻으려면 어떻게 해야 할까?",
    },
    {
        "id": 9, "title": "이야기를 전하는 미디어",
        "field": "언론·미디어", "emoji": "🎥", "color": "#cbdcff",
        "author": "진로책방 자료팀", "level": "입문",
        "jobs": "기자, PD, 영상편집자",
        "description": "뉴스와 영상 콘텐츠를 기획하고 사람들에게 정보를 전달하는 직업을 소개합니다.",
        "question": "믿을 수 있는 정보를 전하려면 무엇이 중요할까?",
    },
    {
        "id": 10, "title": "디지털 세상을 만드는 사람들",
        "field": "IT·디지털", "emoji": "💡", "color": "#e2d7fa",
        "author": "진로책방 자료팀", "level": "보통",
        "jobs": "프로그래머, AI 개발자, 데이터 분석가",
        "description": "컴퓨터와 인공지능 기술로 문제를 해결하는 디지털 분야의 직업을 알아봅니다.",
        "question": "기술을 이용해 우리 생활의 어떤 문제를 해결하고 싶을까?",
    },
]

# -------------------------
# 세션 상태
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "selected" not in st.session_state:
    st.session_state.selected = None
if "category" not in st.session_state:
    st.session_state.category = "전체"

# -------------------------
# 디자인 CSS
# -------------------------
st.markdown("""
<style>
.stApp {
    background: #f1f6ff;
    color: #202d50;
}
.block-container {
    max-width: 1050px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.hero {
    background: linear-gradient(125deg, #c8e6ff 0%, #e9f3ff 60%, #d9efff 100%);
    border: 1px solid #b9ddfb;
    border-radius: 24px;
    padding: 28px 26px;
    margin-bottom: 18px;
}
.hero-icon {
    font-size: 48px;
}
.hero h1 {
    color: #1e2e5b;
    font-size: 30px;
    margin: 4px 0 8px 0;
}
.hero p {
    color: #526483;
    font-size: 15px;
    line-height: 1.7;
}
.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #25345d;
    margin: 24px 0 14px 0;
}
div[data-testid="stTextInput"] input {
    border-radius: 28px;
    min-height: 48px;
    border: 1px solid #dce5f4;
    background: #ffffff;
}
div.stButton > button {
    border-radius: 13px;
    border: 1px solid #e0e8f5;
    min-height: 40px;
    transition: 0.15s;
}
div.stButton > button:hover {
    border-color: #8aa9ef;
    color: #3559bd;
}
.category-card {
    border-radius: 22px;
    padding: 15px 5px;
    text-align: center;
    min-height: 104px;
    border: 1px solid rgba(255,255,255,0.85);
}
.category-icon {
    font-size: 31px;
    margin-bottom: 7px;
}
.category-name {
    font-size: 14px;
    font-weight: 700;
    color: #2e3d60;
}
.book-card {
    background: #ffffff;
    border: 1px solid #e2eaf6;
    border-radius: 18px;
    padding: 12px;
    height: 100%;
}
.book-cover {
    border-radius: 9px;
    min-height: 165px;
    padding: 16px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #2b456a;
    box-shadow: 2px 4px 9px #dbe3ed;
}
.book-cover-icon {
    font-size: 38px;
    margin-bottom: 10px;
}
.book-cover-title {
    font-size: 15px;
    font-weight: 800;
    line-height: 1.55;
}
.book-title {
    font-size: 15px;
    font-weight: 750;
    line-height: 1.55;
    margin-top: 11px;
    min-height: 46px;
    color: #263454;
}
.field-pill {
    display: inline-block;
    background: #eaf1ff;
    color: #5777ba;
    border-radius: 30px;
    padding: 5px 10px;
    font-size: 12px;
    margin-top: 5px;
}
.detail-box {
    background: white;
    border: 1px solid #e1eafa;
    border-radius: 18px;
    padding: 22px;
}
div[data-testid="stBottom"] {
    background: #ffffff;
}
@media (max-width: 600px) {
    .hero { padding: 20px 16px; }
    .hero h1 { font-size: 25px; }
    .category-card { min-height: 88px; }
    .category-icon { font-size: 25px; }
    .category-name { font-size: 12px; }
}
</style>
""", unsafe_allow_html=True)


def go(page):
    st.session_state.page = page
    st.session_state.selected = None


def toggle_favorite(book_id):
    if book_id in st.session_state.favorites:
        st.session_state.favorites.remove(book_id)
    else:
        st.session_state.favorites.append(book_id)


def show_books(books, key_prefix="book"):
    if not books:
        st.info("조건에 맞는 책이 없어요. 다른 검색어나 분야를 선택해 보세요.")
        return

    for start in range(0, len(books), 4):
        cols = st.columns(4)
        for col, book in zip(cols, books[start:start + 4]):
            with col:
                st.markdown(
                    f"""
                    <div class="book-card">
                        <div class="book-cover"
                             style="background:{book['color']}">
                            <div class="book-cover-icon">{book['emoji']}</div>
                            <div class="book-cover-title">{book['title']}</div>
                        </div>
                        <div class="book-title">{book['title']}</div>
                        <div class="field-pill">{book['field']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "책 정보 보기",
                    key=f"{key_prefix}_detail_{book['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected = book["id"]
                    st.rerun()

                is_saved = book["id"] in st.session_state.favorites
                label = "★ 내 서재에 저장" if not is_saved else "✓ 저장됨"
                if st.button(
                    label,
                    key=f"{key_prefix}_save_{book['id']}",
                    use_container_width=True,
                ):
                    toggle_favorite(book["id"])
                    st.rerun()


def show_detail():
    selected_id = st.session_state.selected
    book = next((b for b in BOOKS if b["id"] == selected_id), None)
    if book is None:
        return

    st.markdown("---")
    st.markdown('<div class="section-title">📘 책 자세히 알아보기</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="detail-box">', unsafe_allow_html=True)
    st.markdown(f"### {book['emoji']} {book['title']}")
    st.write(f"**분야:** {book['field']}　|　**읽기 수준:** {book['level']}")
    st.write(f"**저자/제작:** {book['author']}")
    st.write(book["description"])
    st.write(f"**관련 직업:** {book['jobs']}")
    st.info(f"💭 생각해 볼 질문: {book['question']}")
    st.caption("이 책은 앱 시연을 위한 가상 자료이며 실제 출판 도서가 아닙니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    saved = book["id"] in st.session_state.favorites
    if st.button("★ 관심 도서 해제" if saved else "☆ 내 서재에 저장",
                 key="detail_save"):
        toggle_favorite(book["id"])
        st.rerun()
    if st.button("상세 정보 닫기", key="close_detail"):
        st.session_state.selected = None
        st.rerun()


# -------------------------
# 상단 배너
# -------------------------
st.markdown("""
<div class="hero">
    <div class="hero-icon">📘 🌱</div>
    <h1>꿈을 찾는 책장</h1>
    <p>다양한 진로 정보책을 통해<br>
    나의 미래를 더 가까이!</p>
    <b>💬 네 꿈은 어떤 모습인가요?</b>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 홈 화면
# -------------------------
page = st.session_state.page

if page == "홈":
    query = st.text_input(
        "🔎",
        placeholder="관심 있는 분야를 검색해보세요",
        label_visibility="collapsed",
        key="home_search",
    )
    if query.strip():
        results = [
            b for b in BOOKS
            if query.lower() in (
                b["title"] + b["field"] + b["jobs"] + b["description"]
            ).lower()
        ]
        st.markdown('<div class="section-title">🔍 검색 결과</div>',
                    unsafe_allow_html=True)
        show_books(results, "home_search")
    else:
        st.markdown('<div class="section-title">▦ 분야별 찾아보기</div>',
                    unsafe_allow_html=True)

        for start in range(0, len(CATEGORIES), 5):
            cols = st.columns(5)
            for col, (name, emoji, color) in zip(
                cols, CATEGORIES[start:start + 5]
            ):
                with col:
                    st.markdown(
                        f"""
                        <div class="category-card" style="background:{color}">
                            <div class="category-icon">{emoji}</div>
                            <div class="category-name">{name}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button("둘러보기", key=f"home_cat_{name}",
                                 use_container_width=True):
                        st.session_state.category = name
                        go("분야별 검색")
                        st.rerun()

        st.markdown(
            '<div class="section-title">📚 추천 진로 정보책 '
            '<span style="float:right;font-size:14px;color:#7b8aa9">'
            '추천 자료</span></div>',
            unsafe_allow_html=True,
        )
        show_books(BOOKS[:4], "home_recommend")

        if st.button("추천 자료 더 보기  ›", use_container_width=True):
            go("분야별 검색")
            st.rerun()

elif page == "분야별 검색":
    st.markdown('<div class="section-title">🔎 분야별 진로책 검색</div>',
                unsafe_allow_html=True)
    options = ["전체"] + [c[0] for c in CATEGORIES]
    current = st.session_state.category
    index = options.index(current) if current in options else 0

    chosen = st.selectbox("관심 분야", options, index=index)
    st.session_state.category = chosen
    query = st.text_input("책 제목 또는 관련 직업 검색", key="field_search")
    level = st.selectbox("읽기 수준", ["전체", "입문", "보통", "도전"])

    results = BOOKS[:]
    if chosen != "전체":
        results = [b for b in results if b["field"] == chosen]
    if query.strip():
        results = [
            b for b in results
            if query.lower() in (
                b["title"] + b["field"] + b["jobs"] + b["description"]
            ).lower()
        ]
    if level != "전체":
        results = [b for b in results if b["level"] == level]

    st.caption(f"찾은 자료: {len(results)}개")
    show_books(results, "field_results")

elif page == "내 서재":
    st.markdown('<div class="section-title">🔖 나의 서재</div>',
                unsafe_allow_html=True)
    saved_books = [
        b for b in BOOKS if b["id"] in st.session_state.favorites
    ]
    if saved_books:
        show_books(saved_books, "saved")
        if st.button("저장한 책 모두 해제"):
            st.session_state.favorites = []
            st.rerun()
    else:
        st.info("아직 저장한 책이 없어요. 마음에 드는 책을 서재에 담아 보세요.")
        if st.button("진로책 둘러보기"):
            go("분야별 검색")
            st.rerun()

elif page == "마이페이지":
    st.markdown('<div class="section-title">👤 마이페이지</div>',
                unsafe_allow_html=True)
    st.markdown("### 나의 진로 탐색")
    st.write("관심 있는 분야와 미래의 꿈을 기록해 보세요.")

    with st.form("profile_form"):
        nickname = st.text_input("별명", placeholder="예: 미래 탐험가")
        dream = st.text_input("관심 직업", placeholder="예: 과학자")
        favorite_field = st.selectbox(
            "가장 관심 있는 분야",
            [c[0] for c in CATEGORIES],
        )
        submitted = st.form_submit_button("내용 확인")

    if submitted:
        st.success("나의 진로 탐색 정보")
        st.write(f"**별명:** {nickname or '미입력'}")
        st.write(f"**관심 직업:** {dream or '아직 탐색 중'}")
        st.write(f"**관심 분야:** {favorite_field}")
        st.caption("개인 정보는 영구 저장되지 않으며 현재 화면에서만 확인할 수 있습니다.")

    st.markdown("---")
    st.metric("내 서재에 담은 책", len(st.session_state.favorites))
    st.metric("탐색할 수 있는 분야", len(CATEGORIES))

# 선택한 책의 상세 정보
show_detail()

# -------------------------
# 하단 메뉴
# -------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#8190ad;font-size:12px'>"
    "꿈을 찾는 책장 · 나의 미래를 탐색하는 작은 시작</p>",
    unsafe_allow_html=True,
)

nav_cols = st.columns(4)
navigation = [
    ("🏠", "홈"),
    ("🔎", "분야별 검색"),
    ("🔖", "내 서재"),
    ("👤", "마이페이지"),
]

for col, (emoji, label) in zip(nav_cols, navigation):
    with col:
        active = st.session_state.page == label
        button_label = f"{emoji}\n{label}"
        if st.button(
            button_label,
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            go(label)
            st.rerun()
