
import streamlit as st

st.set_page_config(
    page_title="진로책방 | 나의 미래를 찾는 책장",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 1. 앱 데이터
# 시연용 데이터이며 실제 출판 도서 목록과는 다를 수 있습니다.
# -----------------------------
BOOKS = [
    {
        "id": 1,
        "title": "의사라는 직업 알아보기",
        "author": "진로책방 자료팀",
        "field": "의학·보건",
        "level": "입문",
        "jobs": ["의사", "간호사", "약사"],
        "description": "의료 분야의 주요 직업과 하는 일, 필요한 역량을 알아보는 진로 탐색 자료입니다.",
        "reason": "사람의 건강을 지키는 일에 관심이 있는 학생에게 추천합니다.",
        "question": "의료 분야에서 가장 중요하다고 생각하는 태도는 무엇일까?",
        "keywords": "병원 건강 치료 생명",
    },
    {
        "id": 2,
        "title": "생명과학자의 하루",
        "author": "진로책방 자료팀",
        "field": "과학·공학",
        "level": "보통",
        "jobs": ["생명과학자", "연구원", "생명공학자"],
        "description": "생명 현상을 연구하는 과학자의 업무와 연구 과정, 필요한 과학적 사고를 소개합니다.",
        "reason": "생물과 실험, 새로운 발견에 흥미가 있는 학생에게 어울립니다.",
        "question": "과학 연구가 우리 생활을 어떻게 바꿀 수 있을까?",
        "keywords": "생물 실험 연구 자연",
    },
    {
        "id": 3,
        "title": "인공지능과 미래 직업",
        "author": "진로책방 자료팀",
        "field": "IT·AI",
        "level": "입문",
        "jobs": ["AI 개발자", "데이터 분석가", "로봇공학자"],
        "description": "인공지능의 기본 개념과 디지털 기술을 활용하는 직업들을 살펴봅니다.",
        "reason": "컴퓨터와 새로운 기술, 미래 사회의 변화가 궁금한 학생에게 추천합니다.",
        "question": "인공지능이 발전해도 사람이 꼭 해야 할 일은 무엇일까?",
        "keywords": "컴퓨터 코딩 데이터 로봇",
    },
    {
        "id": 4,
        "title": "건축가의 공간 디자인",
        "author": "진로책방 자료팀",
        "field": "예술·디자인",
        "level": "보통",
        "jobs": ["건축가", "실내디자이너", "도시계획가"],
        "description": "건물과 공간이 만들어지는 과정, 디자인과 안전을 함께 고려하는 방법을 알아봅니다.",
        "reason": "그림 그리기와 공간 구성, 건물에 관심이 있는 학생에게 적합합니다.",
        "question": "내가 만들고 싶은 공간에는 어떤 특징이 있어야 할까?",
        "keywords": "건물 설계 공간 미술",
    },
    {
        "id": 5,
        "title": "선생님이라는 길",
        "author": "진로책방 자료팀",
        "field": "교육",
        "level": "입문",
        "jobs": ["초등교사", "중등교사", "교육연구원"],
        "description": "교사의 역할과 수업 준비, 학생과 소통하는 방법을 살펴봅니다.",
        "reason": "다른 사람에게 지식을 알려 주거나 함께 성장하는 일에 관심이 있다면 추천합니다.",
        "question": "좋은 선생님에게 가장 필요한 능력은 무엇일까?",
        "keywords": "학교 수업 학생 교육",
    },
    {
        "id": 6,
        "title": "경제와 기업의 세계",
        "author": "진로책방 자료팀",
        "field": "경영·경제",
        "level": "보통",
        "jobs": ["기업가", "회계사", "경제연구원"],
        "description": "기업이 운영되는 방식과 돈의 흐름, 경제 활동의 기본 원리를 소개합니다.",
        "reason": "경제 뉴스나 기업 운영, 창업에 관심이 있는 학생에게 추천합니다.",
        "question": "기업이 이익과 사회적 책임을 함께 추구하려면 어떻게 해야 할까?",
        "keywords": "돈 금융 창업 회사",
    },
    {
        "id": 7,
        "title": "법과 정의를 만드는 사람들",
        "author": "진로책방 자료팀",
        "field": "사회·법률",
        "level": "보통",
        "jobs": ["변호사", "판사", "검사"],
        "description": "법률 분야의 주요 직업과 사회에서 법이 수행하는 역할을 알아봅니다.",
        "reason": "사회 문제와 토론, 공정한 규칙에 관심이 있는 학생에게 어울립니다.",
        "question": "모두에게 공정한 규칙을 만들려면 무엇을 고려해야 할까?",
        "keywords": "법원 정의 권리 사회",
    },
    {
        "id": 8,
        "title": "기후를 연구하는 과학자",
        "author": "진로책방 자료팀",
        "field": "환경·생태",
        "level": "보통",
        "jobs": ["환경연구원", "기상예보관", "생태학자"],
        "description": "기후와 생태계를 연구하고 환경 문제 해결에 참여하는 직업을 소개합니다.",
        "reason": "자연과 환경 보호, 기후 변화에 관심이 있는 학생에게 추천합니다.",
        "question": "환경 문제를 해결하기 위해 내가 실천할 수 있는 일은 무엇일까?",
        "keywords": "기후 지구 자연 동물",
    },
    {
        "id": 9,
        "title": "뉴스를 만드는 사람들",
        "author": "진로책방 자료팀",
        "field": "미디어·콘텐츠",
        "level": "입문",
        "jobs": ["기자", "PD", "영상편집자"],
        "description": "뉴스와 영상 콘텐츠가 기획되고 제작되는 과정을 알아봅니다.",
        "reason": "글쓰기와 영상 제작, 사람들에게 정보를 전달하는 일에 관심이 있다면 추천합니다.",
        "question": "믿을 수 있는 정보를 전달하려면 무엇이 중요할까?",
        "keywords": "방송 영상 기사 유튜브",
    },
    {
        "id": 10,
        "title": "패션과 나만의 디자인",
        "author": "진로책방 자료팀",
        "field": "예술·디자인",
        "level": "입문",
        "jobs": ["패션디자이너", "스타일리스트", "제품디자이너"],
        "description": "아이디어가 디자인으로 발전하는 과정과 창의적인 표현 방법을 소개합니다.",
        "reason": "옷과 색상, 새로운 아이디어를 표현하는 활동을 좋아하는 학생에게 적합합니다.",
        "question": "내 디자인에 나만의 개성을 담으려면 어떻게 해야 할까?",
        "keywords": "패션 옷 그림 창작",
    },
    {
        "id": 11,
        "title": "동물을 돌보는 직업",
        "author": "진로책방 자료팀",
        "field": "동물·생명",
        "level": "입문",
        "jobs": ["수의사", "동물훈련사", "동물보호전문가"],
        "description": "동물의 건강과 행동을 이해하고 동물을 돌보는 다양한 직업을 알아봅니다.",
        "reason": "동물과 생명 존중, 동물 복지에 관심이 있는 학생에게 추천합니다.",
        "question": "동물을 책임감 있게 돌본다는 것은 어떤 의미일까?",
        "keywords": "반려동물 수의 동물원 생명",
    },
    {
        "id": 12,
        "title": "우주를 탐험하는 공학자",
        "author": "진로책방 자료팀",
        "field": "과학·공학",
        "level": "도전",
        "jobs": ["항공우주공학자", "천문학자", "위성개발자"],
        "description": "우주 탐사에 필요한 과학 기술과 항공우주 분야의 직업을 살펴봅니다.",
        "reason": "우주와 천체, 복잡한 문제를 해결하는 과정에 흥미가 있는 학생에게 어울립니다.",
        "question": "우주 탐사가 인류에게 어떤 도움을 줄 수 있을까?",
        "keywords": "우주 별 로켓 행성",
    },
    {
        "id": 13,
        "title": "사람의 마음을 이해하는 심리학",
        "author": "진로책방 자료팀",
        "field": "심리·상담",
        "level": "보통",
        "jobs": ["심리학자", "상담사", "임상심리전문가"],
        "description": "사람의 생각과 행동을 연구하는 심리학과 상담 관련 직업을 소개합니다.",
        "reason": "사람의 마음과 행동, 의사소통에 관심이 있는 학생에게 추천합니다.",
        "question": "다른 사람의 이야기를 잘 듣는다는 것은 무엇일까?",
        "keywords": "마음 감정 상담 행동",
    },
    {
        "id": 14,
        "title": "호텔과 여행을 기획하는 사람들",
        "author": "진로책방 자료팀",
        "field": "관광·서비스",
        "level": "입문",
        "jobs": ["호텔리어", "여행기획자", "관광통역안내사"],
        "description": "여행과 관광 서비스를 기획하고 다양한 사람을 만나는 직업을 알아봅니다.",
        "reason": "여행과 외국어, 사람을 응대하는 일에 관심이 있는 학생에게 적합합니다.",
        "question": "여행객에게 좋은 경험을 제공하려면 무엇이 필요할까?",
        "keywords": "여행 호텔 외국어 관광",
    },
    {
        "id": 15,
        "title": "스포츠와 건강을 연구하는 사람들",
        "author": "진로책방 자료팀",
        "field": "스포츠·건강",
        "level": "보통",
        "jobs": ["스포츠지도사", "운동처방사", "스포츠분석가"],
        "description": "스포츠 활동과 건강 관리, 경기 분석과 관련된 직업을 살펴봅니다.",
        "reason": "스포츠와 건강, 팀 활동에 관심이 있는 학생에게 추천합니다.",
        "question": "스포츠 분야에서 협동과 공정성이 중요한 이유는 무엇일까?",
        "keywords": "운동 경기 건강 체육",
    },
]

FIELDS = ["전체", *sorted({book["field"] for book in BOOKS})]
LEVELS = ["전체", "입문", "보통", "도전"]


# -----------------------------
# 2. 세션 상태 초기화
# -----------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "selected_book" not in st.session_state:
    st.session_state.selected_book = None


# -----------------------------
# 3. 화면 디자인
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f8fc;
    }
    .hero {
        background: linear-gradient(120deg, #e5edff, #f3eaff);
        padding: 28px;
        border-radius: 18px;
        margin-bottom: 18px;
    }
    .hero h1 {
        color: #24365b;
        margin-bottom: 8px;
    }
    .hero p {
        color: #475569;
        font-size: 16px;
    }
    .book-card {
        background: white;
        padding: 18px;
        border: 1px solid #e6eaf2;
        border-radius: 14px;
        min-height: 220px;
        margin-bottom: 8px;
    }
    .book-category {
        color: #5267a8;
        font-size: 13px;
        font-weight: 700;
    }
    .book-title {
        font-size: 19px;
        font-weight: 700;
        color: #24365b;
        margin: 8px 0;
    }
    .book-description {
        color: #596579;
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("# 📚 진로책방")
    st.caption("책에서 시작하는 나의 미래 탐색")
    page = st.radio(
        "메뉴",
        ["책 둘러보기", "분야별 탐색", "관심 도서", "진로 탐색 노트"],
    )
    st.divider()
    st.markdown("**이용 안내**")
    st.caption("분야를 선택하고 책을 살펴보세요.")
    st.caption("마음에 드는 책은 ☆ 버튼으로 저장할 수 있어요.")
    st.caption("현재 자료는 앱 시연용 예시입니다.")


st.markdown(
    """
    <div class="hero">
        <h1>📖 진로책방</h1>
        <p>어떤 일을 하며 살아가고 싶나요?<br>
        다양한 분야의 책을 살펴보며 나에게 맞는 진로를 찾아보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 4. 책 상세 정보 표시 함수
# -----------------------------
def show_book_detail(book):
    st.subheader("📘 책 자세히 보기")
    st.markdown(f"### {book['title']}")
    st.write(f"**분야:** {book['field']}  ·  **읽기 수준:** {book['level']}")
    st.write(f"**저자/제작:** {book['author']}")
    st.write(book["description"])
    st.write("**관련 직업**")
    st.write(" · ".join(book["jobs"]))
    st.info(f"💡 추천 이유: {book['reason']}")
    st.write("**읽고 생각해 볼 질문**")
    st.write(book["question"])

    is_favorite = book["id"] in st.session_state.favorites
    label = "★ 관심 도서 해제" if is_favorite else "☆ 관심 도서에 저장"

    if st.button(label, key=f"detail_fav_{book['id']}"):
        if is_favorite:
            st.session_state.favorites.remove(book["id"])
            st.success("관심 도서에서 제외했어요.")
        else:
            st.session_state.favorites.append(book["id"])
            st.success("관심 도서에 저장했어요.")
        st.rerun()


# -----------------------------
# 5. 책 목록 표시 함수
# -----------------------------
def show_book_grid(books):
    if not books:
        st.warning("조건에 맞는 책이 없어요. 검색어나 필터를 바꿔 보세요.")
        return

    st.caption(f"검색 결과 {len(books)}권")

    for start in range(0, len(books), 3):
        cols = st.columns(3)
        for col, book in zip(cols, books[start:start + 3]):
            with col:
                st.markdown(
                    f"""
                    <div class="book-card">
                        <div class="book-category">
                            {book['field']} · {book['level']}
                        </div>
                        <div class="book-title">
                            📗 {book['title']}
                        </div>
                        <div class="book-description">
                            {book['description']}
                        </div>
                        <p><b>관련 직업</b><br>
                        {', '.join(book['jobs'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                left, right = st.columns([3, 2])
                with left:
                    if st.button(
                        "상세 보기",
                        key=f"detail_{book['id']}_{page}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_book = book["id"]
                        st.rerun()

                with right:
                    favorite = book["id"] in st.session_state.favorites
                    button_label = "★ 저장됨" if favorite else "☆ 저장"
                    if st.button(
                        button_label,
                        key=f"fav_{book['id']}_{page}",
                        use_container_width=True,
                    ):
                        if favorite:
                            st.session_state.favorites.remove(book["id"])
                        else:
                            st.session_state.favorites.append(book["id"])
                        st.rerun()


# -----------------------------
# 6. 메뉴별 화면
# -----------------------------
if page == "책 둘러보기":
    st.subheader("🔎 나에게 맞는 진로책 찾기")
    st.write("관심 있는 분야와 직업을 검색해 보세요.")

    query = st.text_input(
        "책 제목, 직업, 키워드 검색",
        placeholder="예: 의사, 인공지능, 디자인, 환경",
    )
    col1, col2 = st.columns(2)
    with col1:
        field_filter = st.selectbox("관심 분야", FIELDS, key="main_field")
    with col2:
        level_filter = st.selectbox("읽기 수준", LEVELS, key="main_level")

    filtered = []
    for book in BOOKS:
        searchable = " ".join([
            book["title"],
            book["author"],
            book["field"],
            book["description"],
            book["reason"],
            book["keywords"],
            " ".join(book["jobs"]),
        ]).lower()

        if query.strip().lower() not in searchable and query.strip():
            continue
        if field_filter != "전체" and book["field"] != field_filter:
            continue
        if level_filter != "전체" and book["level"] != level_filter:
            continue
        filtered.append(book)

    show_book_grid(filtered)

elif page == "분야별 탐색":
    st.subheader("🧭 분야별 책장")
    st.write("관심 있는 분야를 골라 관련 직업과 진로 자료를 탐색하세요.")

    field = st.selectbox(
        "탐색할 분야를 선택하세요",
        sorted({book["field"] for book in BOOKS}),
        key="category_field",
    )
    field_books = [book for book in BOOKS if book["field"] == field]

    st.markdown(f"### 🗂️ {field}")
    st.write(f"이 분야의 진로 탐색 자료는 {len(field_books)}권입니다.")
    jobs = sorted({job for book in field_books for job in book["jobs"]})
    st.markdown("**살펴볼 수 있는 직업**")
    st.write(" · ".join(jobs))
    show_book_grid(field_books)

elif page == "관심 도서":
    st.subheader("⭐ 나의 관심 도서")
    st.write("저장한 책을 모아 보고 다시 살펴보세요.")

    favorite_books = [
        book for book in BOOKS
        if book["id"] in st.session_state.favorites
    ]
    show_book_grid(favorite_books)

    if favorite_books:
        if st.button("관심 도서 전체 해제"):
            st.session_state.favorites = []
            st.session_state.selected_book = None
            st.rerun()
    else:
        st.info("아직 저장한 책이 없어요. 책 둘러보기에서 ☆ 저장을 눌러 보세요.")

elif page == "진로 탐색 노트":
    st.subheader("📝 나의 진로 탐색 노트")
    st.write("책을 읽고 알게 된 점과 앞으로 알아보고 싶은 내용을 기록해 보세요.")

    with st.form("career_note_form"):
        name = st.text_input("기록 제목", placeholder="예: 내가 관심 있는 직업")
        interest = st.text_input("관심 있는 직업 또는 분야")
        learned = st.text_area(
            "새롭게 알게 된 점",
            placeholder="책에서 알게 된 직업의 특징이나 필요한 능력을 적어 보세요.",
        )
        next_step = st.text_area(
            "앞으로 해 보고 싶은 활동",
            placeholder="관련 책 더 읽기, 직업 인터뷰 찾아보기 등",
        )
        submitted = st.form_submit_button("탐색 노트 확인")

    if submitted:
        if not name.strip() and not interest.strip() and not learned.strip() and not next_step.strip():
            st.warning("한 가지 이상 작성해 주세요.")
        else:
            st.markdown("### 작성한 탐색 노트")
            st.markdown(f"**기록 제목:** {name or '제목 없음'}")
            st.markdown(f"**관심 직업/분야:** {interest or '미입력'}")
            st.markdown(f"**새롭게 알게 된 점:** {learned or '미입력'}")
            st.markdown(f"**앞으로 해 보고 싶은 활동:** {next_step or '미입력'}")
            st.caption("이 노트는 화면에 표시되는 임시 기록이며, 앱을 새로 열면 저장되지 않습니다.")

# -----------------------------
# 7. 선택한 책의 상세 정보
# -----------------------------
if st.session_state.selected_book is not None:
    selected = next(
        (book for book in BOOKS
         if book["id"] == st.session_state.selected_book),
        None,
    )
    if selected is None:
        st.session_state.selected_book = None
    else:
        st.divider()
        show_book_detail(selected)
        if st.button("상세 보기 닫기"):
            st.session_state.selected_book = None
            st.rerun()

# -----------------------------
# 8. 하단 안내
# -----------------------------
st.divider()
st.caption(
    "진로책방 · 진로 탐색을 위한 교육용 시연 앱 | "
    "도서 데이터는 예시이며 실제 도서 정보와 다를 수 있습니다."
)
