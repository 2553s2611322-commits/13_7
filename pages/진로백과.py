
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# 기존 앱의 페이지 설정과 사이드바 메뉴는 건드리지 않습니다.

BOOKS = [
    {"title":"아주 작은 습관의 힘","author":"제임스 클리어","field":"자기계발","isbn":"9780735211292","desc":"작은 습관을 통해 성장하는 방법"},
    {"title":"그릿","author":"앤절라 더크워스","field":"심리","isbn":"9781501111105","desc":"열정과 끈기가 성공에 미치는 영향"},
    {"title":"콰이어트","author":"수전 케인","field":"심리","isbn":"9780307352156","desc":"내향적인 사람의 특징과 강점"},
    {"title":"생각에 관한 생각","author":"대니얼 카너먼","field":"심리","isbn":"9780374533557","desc":"사람의 판단과 의사결정 과정"},
    {"title":"돈의 심리학","author":"모건 하우절","field":"경제·금융","isbn":"9780857197689","desc":"돈에 대한 행동과 생각"},
    {"title":"아웃라이어","author":"말콤 글래드웰","field":"경영·기업","isbn":"9780316017930","desc":"성공을 만드는 환경과 기회"},
    {"title":"스티브 잡스","author":"월터 아이작슨","field":"경영·기업","isbn":"9781451648539","desc":"애플 창업자의 삶과 도전"},
    {"title":"스타트 위드 와이","author":"사이먼 시넥","field":"경영·기업","isbn":"9781591846444","desc":"목적을 중심으로 생각하는 리더십"},
    {"title":"파이썬 크래시 코스","author":"에릭 매티스","field":"IT·인공지능","isbn":"9781718502703","desc":"파이썬 프로그래밍 기초"},
    {"title":"클린 코드","author":"로버트 C. 마틴","field":"IT·인공지능","isbn":"9780132350884","desc":"읽기 쉽고 관리하기 좋은 코드"},
    {"title":"코스모스","author":"칼 세이건","field":"과학·연구","isbn":"9780345539434","desc":"우주와 과학에 관한 이야기"},
    {"title":"이기적 유전자","author":"리처드 도킨스","field":"과학·연구","isbn":"9780199291151","desc":"진화와 유전자의 관점에서 생명 이해하기"},
    {"title":"침묵의 봄","author":"레이첼 카슨","field":"환경·생태","isbn":"9780618249060","desc":"환경오염이 생태계에 미치는 영향"},
    {"title":"월든","author":"헨리 데이비드 소로","field":"환경·생태","isbn":"9780140390445","desc":"자연 속 생활과 단순한 삶"},
    {"title":"총, 균, 쇠","author":"재레드 다이아몬드","field":"사회·역사","isbn":"9780393354324","desc":"문명 발전의 원인을 살펴보는 책"},
    {"title":"팩트풀니스","author":"한스 로슬링 외","field":"사회·역사","isbn":"9781250107817","desc":"데이터로 세계를 이해하는 방법"},
    {"title":"정의란 무엇인가","author":"마이클 샌델","field":"사회·법","isbn":"9780374532505","desc":"정의와 공정성에 관한 다양한 관점"},
    {"title":"보이지 않는 여자들","author":"캐럴라인 크리아도 페레스","field":"사회·법","isbn":"9781419729072","desc":"데이터에 나타나는 사회적 편향"},
    {"title":"디자인 오브 에브리데이 씽스","author":"도널드 노먼","field":"디자인·예술","isbn":"9780465050659","desc":"사용하기 편리한 디자인의 원리"},
    {"title":"훅","author":"니르 이얄","field":"디자인·예술","isbn":"9781591847786","desc":"제품 디자인과 사용자 행동"},
    {"title":"파라슈트","author":"리처드 N. 볼스","field":"진로·직업","isbn":"9780399581683","desc":"자신의 강점과 진로를 탐색하는 방법"},
    {"title":"그들이 당신을 무시하지 못하게 하라","author":"칼 뉴포트","field":"진로·직업","isbn":"9781455509126","desc":"실력을 쌓고 의미 있는 일을 찾는 방법"},
    {"title":"죽은 시인의 사회","author":"N. H. 클라인바움","field":"교육·상담","isbn":"978B000FC1L8","desc":"교육과 성장, 스스로 생각하는 삶"},
    {"title":"어린 왕자","author":"앙투안 드 생텍쥐페리","field":"교육·상담","isbn":"9780156012195","desc":"관계와 책임, 삶의 의미를 생각하는 이야기"},
    {"title":"보물섬","author":"로버트 루이스 스티븐슨","field":"여행·관광","isbn":"9780141321004","desc":"항해와 모험을 다룬 고전 소설"},
    {"title":"딥 워크","author":"칼 뉴포트","field":"자기계발","isbn":"9781455586691","desc":"집중력과 몰입을 높이는 방법"},
    {"title":"그릿: IQ, 재능, 환경을 뛰어넘는 열정적 끈기의 힘","author":"앤절라 더크워스","field":"교육·상담","isbn":"9781501111105","desc":"목표를 향해 꾸준히 노력하는 태도"},
    {"title":"습관의 힘","author":"찰스 두히그","field":"자기계발","isbn":"9780812981605","desc":"습관이 만들어지고 바뀌는 과정"},
    {"title":"마인드셋","author":"캐럴 드웩","field":"교육·상담","isbn":"9780345472328","desc":"성장하는 사고방식과 학습 태도"},
    {"title":"린 스타트업","author":"에릭 리스","field":"경영·기업","isbn":"9780307887894","desc":"새로운 사업을 검증하고 발전시키는 방법"},
    {"title":"시간의 역사","author":"스티븐 호킹","field":"과학·연구","isbn":"9780553380163","desc":"시간과 우주에 관한 과학적 질문"},
    {"title":"인간의 의미 추구","author":"빅터 프랭클","field":"심리","isbn":"9780807014295","desc":"삶의 의미와 인간의 선택에 대한 성찰"},
    {"title":"친구를 얻고 사람을 움직이는 방법","author":"데일 카네기","field":"자기계발","isbn":"9780671027032","desc":"의사소통과 인간관계의 기본 원칙"},
]

FIELDS = ["전체"] + sorted(set(book["field"] for book in BOOKS))

if "career_book_favorites" not in st.session_state:
    st.session_state.career_book_favorites = []

@st.cache_data(ttl=3600, show_spinner=False)
def load_cover(isbn):
    """표지는 별도로 가져오며, 실패하면 앱 검색은 계속 작동합니다."""
    if not isbn.isdigit() or len(isbn) not in (10, 13):
        return None
    url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    try:
        response = requests.get(
            url,
            timeout=3,
            headers={"User-Agent": "CareerBookShelf/1.0"}
        )
        if response.status_code != 200:
            return None
        if len(response.content) < 1000:
            return None
        image = Image.open(BytesIO(response.content))
        image.verify()
        image = Image.open(BytesIO(response.content)).convert("RGB")
        return image
    except Exception:
        return None

def render_book(book, number):
    with st.container(border=True):
        cover = load_cover(book["isbn"])
        if cover is not None:
            st.image(cover, use_container_width=True)
        else:
            st.markdown(
                "<div style='background:#f1eafa;height:190px;"
                "border-radius:12px;display:flex;align-items:center;"
                "justify-content:center;font-size:55px;'>📚</div>",
                unsafe_allow_html=True,
            )

        st.markdown(f"**{book['title']}**")
        st.caption(f"{book['author']} · {book['field']}")
        st.write(book["desc"])

        query = requests.utils.quote(book["title"] + " " + book["author"])
        st.markdown(
            f"[📖 책 정보 및 판본 확인](https://books.google.com/books?q={query})"
        )

        isbn = book["isbn"]
        saved = isbn in st.session_state.career_book_favorites
        button_text = "💗 찜 취소" if saved else "♡ 찜하기"

        if st.button(button_text, key=f"career_fav_{number}_{isbn}",
                     use_container_width=True):
            if saved:
                st.session_state.career_book_favorites.remove(isbn)
            else:
                st.session_state.career_book_favorites.append(isbn)
            st.rerun()

def render_books(books, offset=0):
    if not books:
        st.info("검색 결과가 없어요. 다른 검색어나 분야를 선택해 보세요.")
        return

    st.caption(f"검색 결과: {len(books)}권")

    for start in range(0, len(books), 3):
        cols = st.columns(3)
        for j, book in enumerate(books[start:start + 3]):
            with cols[j]:
                render_book(book, offset + start + j)

# 페이지 본문
st.title("📚 진로백과")
st.caption("책을 통해 관심 분야를 탐색하고 나에게 맞는 진로를 찾아보세요.")

st.markdown("""
<div style="background:linear-gradient(120deg,#e6edff,#f9e8ef);
padding:22px;border-radius:16px;margin-bottom:18px;">
<h3 style="margin-top:0;">나의 관심 분야를 책으로 찾아봐요!</h3>
<p style="margin-bottom:0;">분야를 선택하거나 제목, 저자, 관심 키워드로 검색할 수 있어요.</p>
</div>
""", unsafe_allow_html=True)

tab_search, tab_favorites = st.tabs(["🔎 분야별 도서 검색", "💗 찜한 도서"])

with tab_search:
    with st.form("career_book_search_form"):
        field = st.selectbox("분야 선택", FIELDS, key="career_book_field")
        keyword = st.text_input(
            "검색어",
            placeholder="예: 심리, 과학자, 인공지능, 김영하",
            key="career_book_keyword",
        )
        submitted = st.form_submit_button("🔎 검색", use_container_width=True)

    # 등록된 도서 목록에서 검색하므로 검색 API 호출 제한에 걸리지 않습니다.
    results = BOOKS
    if field != "전체":
        results = [b for b in results if b["field"] == field]

    if keyword.strip():
        term = keyword.strip().casefold()
        results = [
            b for b in results
            if term in b["title"].casefold()
            or term in b["author"].casefold()
            or term in b["field"].casefold()
            or term in b["desc"].casefold()
        ]

    if submitted:
        st.session_state.career_book_last_search = keyword.strip()
        st.session_state.career_book_last_field = field

    st.subheader("📚 도서 목록")
    render_books(results)

with tab_favorites:
    st.subheader("💗 내가 찜한 책")
    favorites = [
        book for book in BOOKS
        if book["isbn"] in st.session_state.career_book_favorites
    ]
    render_books(favorites, offset=500)

st.divider()
st.caption(
    "※ 책 표지는 외부 표지 서비스에서 제공되며, 일부 책은 표지가 표시되지 않을 수 있습니다. "
    "책 정보 링크에서 판본과 출판 정보를 확인해 주세요."
)
