
import streamlit as st
from urllib.parse import quote_plus

st.set_page_config(
    page_title="꿈을 찾는 책장",
    page_icon="📚",
    layout="wide",
)

# 실제 출간된 도서 목록
# ISBN은 표지 조회용이며, 표지는 영문판으로 표시될 수도 있습니다.
BOOKS = [
    {"title": "아웃라이어", "author": "말콤 글래드웰", "field": "자기계발", "isbn": "9780316017930", "desc": "성공에 영향을 주는 환경과 기회를 살펴보는 책."},
    {"title": "아주 작은 습관의 힘", "author": "제임스 클리어", "field": "자기계발", "isbn": "9780735211292", "desc": "작은 습관이 일상과 성장에 미치는 영향을 알려 준다."},
    {"title": "딥 워크", "author": "칼 뉴포트", "field": "자기계발", "isbn": "9781455586691", "desc": "집중력을 높이고 중요한 일에 몰입하는 방법을 다룬다."},
    {"title": "그릿", "author": "앤절라 더크워스", "field": "자기계발", "isbn": "9781501111105", "desc": "열정과 끈기가 목표 달성에 미치는 영향을 설명한다."},
    {"title": "콰이어트", "author": "수전 케인", "field": "심리", "isbn": "9780307352156", "desc": "내향적인 사람의 특성과 강점을 살펴본다."},
    {"title": "생각에 관한 생각", "author": "대니얼 카너먼", "field": "심리", "isbn": "9780374533557", "desc": "사람이 판단하고 결정하는 과정을 탐구한다."},
    {"title": "돈의 심리학", "author": "모건 하우절", "field": "경제·금융", "isbn": "9780857197689", "desc": "돈에 대한 태도와 행동을 이해하도록 돕는다."},
    {"title": "부의 추월차선", "author": "엠제이 드마코", "field": "경제·금융", "isbn": "9780984358106", "desc": "경제적 목표와 사업에 대한 관점을 다룬다."},
    {"title": "왜 일하는가", "author": "이나모리 가즈오", "field": "경영·기업", "isbn": "978B00E4W7M5", "desc": "일의 의미와 직업을 대하는 태도를 생각하게 한다."},
    {"title": "스티브 잡스", "author": "월터 아이작슨", "field": "경영·기업", "isbn": "9781451648539", "desc": "애플 창업자의 삶과 제품 개발 과정을 소개한다."},
    {"title": "스타트 위드 와이", "author": "사이먼 시넥", "field": "경영·기업", "isbn": "9781591846444", "desc": "조직과 리더가 목표와 목적을 전달하는 방식을 설명한다."},
    {"title": "생각하는 기계", "author": "토비 월시", "field": "IT·인공지능", "isbn": "978B08N5J8Y6", "desc": "인공지능의 발전과 사회에 미치는 영향을 살펴본다."},
    {"title": "파이썬 크래시 코스", "author": "에릭 매티스", "field": "IT·인공지능", "isbn": "9781718502703", "desc": "파이썬 프로그래밍의 기초를 실습으로 익힌다."},
    {"title": "클린 코드", "author": "로버트 C. 마틴", "field": "IT·인공지능", "isbn": "9780132350884", "desc": "읽기 쉽고 관리하기 좋은 프로그램 코드를 다룬다."},
    {"title": "코스모스", "author": "칼 세이건", "field": "과학·연구", "isbn": "9780345539434", "desc": "우주와 과학의 발전을 폭넓게 소개한다."},
    {"title": "이기적 유전자", "author": "리처드 도킨스", "field": "과학·연구", "isbn": "9780199291151", "desc": "진화와 유전자 관점에서 생명 현상을 설명한다."},
    {"title": "침묵의 봄", "author": "레이첼 카슨", "field": "환경·생태", "isbn": "9780618249060", "desc": "화학 물질이 생태계에 미치는 영향을 다룬다."},
    {"title": "총, 균, 쇠", "author": "재레드 다이아몬드", "field": "사회·역사", "isbn": "9780393354324", "desc": "문명과 사회의 발전 과정을 다양한 요인으로 분석한다."},
    {"title": "정의란 무엇인가", "author": "마이클 샌델", "field": "사회·법", "isbn": "9780374532505", "desc": "정의와 공정성에 관한 여러 관점을 살펴본다."},
    {"title": "팩트풀니스", "author": "한스 로슬링 외", "field": "사회·역사", "isbn": "9781250107817", "desc": "세계의 변화를 데이터로 바라보는 방법을 알려 준다."},
    {"title": "디자인 오브 에브리데이 씽스", "author": "도널드 노먼", "field": "디자인·예술", "isbn": "9780465050659", "desc": "사람이 제품을 편리하게 사용하는 디자인 원리를 다룬다."},
    {"title": "훅", "author": "니르 이얄", "field": "디자인·예술", "isbn": "9781591847786", "desc": "사람의 행동과 제품 설계의 관계를 설명한다."},
    {"title": "죽은 시인의 사회", "author": "N. H. 클라인바움", "field": "교육·상담", "isbn": "978B000FC1L8", "desc": "교육과 성장, 스스로 생각하는 삶을 이야기한다."},
    {"title": "어린 왕자", "author": "앙투안 드 생텍쥐페리", "field": "교육·상담", "isbn": "9780156012195", "desc": "관계와 책임, 삶의 의미를 생각하게 하는 소설."},
    {"title": "파라슈트", "author": "리처드 N. 볼스", "field": "진로·직업", "isbn": "9780399581683", "desc": "자신의 강점과 관심사를 바탕으로 진로를 탐색한다."},
    {"title": "So Good They Can't Ignore You", "author": "칼 뉴포트", "field": "진로·직업", "isbn": "9781455509126", "desc": "일에서 실력을 쌓고 의미를 찾는 방법을 다룬다."},
    {"title": "보이지 않는 여자들", "author": "캐럴라인 크리아도 페레스", "field": "사회·법", "isbn": "9781419729072", "desc": "데이터에서 누락되는 사람들과 사회적 편향을 살펴본다."},
    {"title": "침팬지 폴리틱스", "author": "프란스 드 발", "field": "과학·연구", "isbn": "9780805209764", "desc": "영장류의 행동을 통해 사회적 관계를 살펴본다."},
    {"title": "보물섬", "author": "로버트 루이스 스티븐슨", "field": "여행·관광", "isbn": "9780141321004", "desc": "모험과 항해를 다룬 고전 소설이다."},
    {"title": "월든", "author": "헨리 데이비드 소로", "field": "환경·생태", "isbn": "9780140390445", "desc": "자연 속 생활과 단순한 삶에 대한 생각을 담았다."},
]

FIELDS = ["전체"] + sorted({book["field"] for book in BOOKS})

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "page" not in st.session_state:
    st.session_state.page = "🏠 홈"

st.markdown("""
<style>
.stApp {
    background: #f7f8fc;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #e4eafa, #f8e8ef);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 20px;
}
.book-card {
    background: white;
    border: 1px solid #e6e8f0;
    border-radius: 15px;
    padding: 16px;
    min-height: 170px;
}
.small-note {
    color: #73798a;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📚 꿈을 찾는 책장")
    st.caption("책으로 발견하는 나의 진로")
    page = st.radio(
        "메뉴",
        ["🏠 홈", "🔎 분야별 도서 검색", "💗 찜한 도서"],
        key="page",
    )
    st.divider()
    st.caption(f"현재 등록된 도서: {len(BOOKS)}권")
    st.caption("검색은 앱에 저장된 도서 목록에서 진행됩니다.")

def book_card(book, index):
    with st.container(border=True):
        isbn = book["isbn"]
        cover_url = (
            f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
            if isbn.isdigit() and len(isbn) in (10, 13)
            else None
        )

        if cover_url:
            st.image(cover_url, use_container_width=True)
        else:
            st.markdown(
                "<div style='background:#f0eaf8;border-radius:10px;"
                "padding:35px 5px;text-align:center;font-size:38px;'>📚</div>",
                unsafe_allow_html=True,
            )

        st.markdown(f"**{book['title']}**")
        st.caption(f"{book['author']} · {book['field']}")
        st.write(book["desc"])

        search_url = (
            "https://books.google.com/books?q="
            + quote_plus(book["title"] + " " + book["author"])
        )
        st.markdown(f"[도서 정보 더 보기 ↗]({search_url})")

        saved = isbn in st.session_state.favorites
        label = "💗 찜 취소" if saved else "♡ 찜하기"
        if st.button(label, key=f"fav_{index}_{isbn}", use_container_width=True):
            if saved:
                st.session_state.favorites.remove(isbn)
            else:
                st.session_state.favorites.append(isbn)
            st.rerun()

def show_books(books, start_index=0):
    if not books:
        st.info("검색 결과가 없어요. 다른 검색어나 분야를 선택해 보세요.")
        return

    st.caption(f"총 {len(books)}권의 도서를 찾았어요.")

    for start in range(0, len(books), 3):
        cols = st.columns(3)
        for offset, book in enumerate(books[start:start + 3]):
            with cols[offset]:
                book_card(book, start_index + start + offset)

if page == "🏠 홈":
    st.markdown("""
    <div class="hero">
        <h1>📚 꿈을 찾는 책장</h1>
        <p>관심 있는 분야의 책을 읽으며 나에게 맞는 진로를 찾아보세요.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔎 어떤 책을 찾고 있나요?")
    keyword = st.text_input(
        "책 제목, 저자 또는 관심 분야",
        placeholder="예: 심리학, 과학자, 인공지능",
        key="home_keyword",
    )

    if st.button("도서 검색하기", type="primary", use_container_width=True):
        st.session_state.search_keyword = keyword
        st.session_state.page = "🔎 분야별 도서 검색"
        st.rerun()

    st.subheader("🧭 관심 분야 둘러보기")
    cols = st.columns(3)
    for i, field in enumerate(FIELDS[1:]):
        with cols[i % 3]:
            if st.button(f"📖 {field}", key=f"field_{i}", use_container_width=True):
                st.session_state.selected_field = field
                st.session_state.page = "🔎 분야별 도서 검색"
                st.rerun()

    st.subheader("✨ 추천 도서")
    show_books(BOOKS[:6])

elif page == "🔎 분야별 도서 검색":
    st.title("🔎 분야별 도서 검색")
    st.write("관심 분야를 고르거나 책 제목과 저자를 검색해 보세요.")

    default_field = st.session_state.get("selected_field", "전체")
    if default_field not in FIELDS:
        default_field = "전체"

    field = st.selectbox(
        "분야 선택",
        FIELDS,
        index=FIELDS.index(default_field),
    )
    keyword = st.text_input(
        "검색어",
        value=st.session_state.get("search_keyword", ""),
        placeholder="예: 심리학, 과학자, 김영하",
    )

    if st.button("🔎 검색", type="primary", use_container_width=True):
        st.session_state.search_keyword = keyword
        st.session_state.selected_field = field

    results = BOOKS
    if field != "전체":
        results = [b for b in results if b["field"] == field]

    if keyword.strip():
        term = keyword.strip().lower()
        results = [
            b for b in results
            if term in b["title"].lower()
            or term in b["author"].lower()
            or term in b["field"].lower()
            or term in b["desc"].lower()
        ]

    show_books(results)

elif page == "💗 찜한 도서":
    st.title("💗 찜한 도서")
    favorites = [
        b for b in BOOKS
        if b["isbn"] in st.session_state.favorites
    ]
    if favorites:
        show_books(favorites, start_index=1000)
    else:
        st.info("아직 찜한 도서가 없어요. 마음에 드는 책을 찜해 보세요!")

st.divider()
st.markdown(
    '<p class="small-note">📚 꿈을 찾는 책장 | 도서 정보는 진로 탐색을 위한 참고용입니다. '
    '표지 이미지가 없을 경우 도서 정보 링크에서 확인할 수 있습니다.</p>',
    unsafe_allow_html=True,
)
