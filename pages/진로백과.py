
import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="꿈을 찾는 책장",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 실제 출판 정보가 확인된 도서 중심의 목록
# 분야는 앱 탐색을 위한 분류이며, 도서 설명을 임의로 단정하지 않습니다.
BOOKS = [
    {
        "title": "뭘 해도 괜찮아",
        "author": "이남석",
        "publisher": "사계절",
        "field": "인문·사회",
        "icon": "🌱",
        "color": "#DDEBFF",
        "description": "꿈을 찾는 과정과 진로 설계를 고민하는 청소년을 위한 책.",
    },
    {
        "title": "청소년 자립/직업 진로 길라잡이",
        "author": "모세종",
        "publisher": "생각나눔",
        "field": "인문·사회",
        "icon": "🧭",
        "color": "#E9E0FF",
        "description": "청소년의 자립과 직업 진로, 직업 선택을 다루는 책.",
    },
    {
        "title": "나의 직업 제과제빵떡사",
        "author": "청소년행복연구실",
        "publisher": "동천출판",
        "field": "예술·체육",
        "icon": "🥐",
        "color": "#FFE8D0",
        "description": "제과·제빵·떡 관련 직업을 알아볼 수 있는 직업 정보 도서.",
    },
    {
        "title": "AI의 혁신을 이끄는 데이터과학자",
        "author": "김태헌",
        "publisher": "토크쇼",
        "field": "IT·디지털",
        "icon": "💻",
        "color": "#E5DEFF",
        "description": "데이터과학자라는 직업을 알아볼 수 있는 직업 분야 도서.",
    },
    {
        "title": "SW를 세상에 알리는 소프트웨어비즈니스전문가",
        "author": "권준혁",
        "publisher": "토크쇼",
        "field": "IT·디지털",
        "icon": "🖥️",
        "color": "#DDEBFF",
        "description": "소프트웨어와 비즈니스를 연결하는 직업을 알아보는 책.",
    },
    {
        "title": "기술혁신을 주도하는 최고기술경영자(CTO)",
        "author": "홍영훈",
        "publisher": "토크쇼",
        "field": "공학",
        "icon": "⚙️",
        "color": "#E0F1F0",
        "description": "기술 개발과 기업의 기술 전략을 이끄는 직업에 관한 책.",
    },
    {
        "title": "기후변화시대 10대가 알아야할 미래 직업의 이동",
        "author": "신지나",
        "publisher": "한스미디어",
        "field": "자연과학",
        "icon": "🌍",
        "color": "#E4F4D2",
        "description": "기후 변화와 미래 직업의 변화를 함께 살펴보는 책.",
    },
    {
        "title": "날씨를 전하며 내일을 준비하는 기상캐스터",
        "author": "최아리",
        "publisher": "토크쇼",
        "field": "언론·미디어",
        "icon": "🌤️",
        "color": "#DDEBFF",
        "description": "날씨 정보를 전달하는 기상캐스터라는 직업을 알아보는 책.",
    },
    {
        "title": "마음 속 기억창고를 만드는 K-POP작곡가",
        "author": "서정진",
        "publisher": "토크쇼",
        "field": "예술·체육",
        "icon": "🎵",
        "color": "#FFE0E8",
        "description": "K-POP 작곡가라는 음악 분야 직업을 알아보는 책.",
    },
    {
        "title": "범죄자를 끝까지 추적해 검거하는 형사",
        "author": "윤석호",
        "publisher": "토크쇼",
        "field": "인문·사회",
        "icon": "🔎",
        "color": "#E9E0FF",
        "description": "형사라는 직업의 역할을 알아볼 수 있는 직업 정보 도서.",
    },
    {
        "title": "변신을 통해 행복을 선물하는 헤어디자이너",
        "author": "김원일",
        "publisher": "토크쇼",
        "field": "예술·체육",
        "icon": "🎨",
        "color": "#FFE8D0",
        "description": "헤어디자인 분야의 직업을 알아보는 책.",
    },
    {
        "title": "아이들과 함께 걷는 초등교사",
        "author": "전소영",
        "publisher": "토크쇼",
        "field": "교육",
        "icon": "📖",
        "color": "#FFF0C7",
        "description": "초등교사라는 직업을 알아볼 수 있는 직업 분야 도서.",
    },
    {
        "title": "전 세계의 책을 우리말로 풀어내는 멋진 직업 출판번역가",
        "author": "이세진",
        "publisher": "토크쇼",
        "field": "인문·사회",
        "icon": "📚",
        "color": "#E9E0FF",
        "description": "책을 다른 언어로 옮기는 출판번역가라는 직업에 관한 책.",
    },
    {
        "title": "차갑고 뜨거운 종합예술인 드라마PD",
        "author": "민영홍",
        "publisher": "토크쇼",
        "field": "언론·미디어",
        "icon": "🎬",
        "color": "#DDEBFF",
        "description": "드라마를 기획하고 제작하는 PD라는 직업을 알아보는 책.",
    },
    {
        "title": "하늘의 신호등 항공교통관제사",
        "author": "유영미, 임은정",
        "publisher": "토크쇼",
        "field": "공학",
        "icon": "✈️",
        "color": "#DDEBFF",
        "description": "항공교통관제사라는 항공 분야 직업을 알아보는 책.",
    },
    {
        "title": "10대를 위한 1세대 창업가 수업",
        "author": "김정진",
        "publisher": "넥스트씨",
        "field": "경영·경제",
        "icon": "💡",
        "color": "#D4F0EC",
        "description": "창업가의 경험과 기업가 정신을 살펴볼 수 있는 책.",
    },
    {
        "title": "공부머리를 역전하는 7가지 진로 공부법",
        "author": "앤디 림, 윤규훈",
        "publisher": "온더페이지",
        "field": "교육",
        "icon": "✏️",
        "color": "#FFF0C7",
        "description": "공부 방법과 진로 탐색을 연결해 생각해 볼 수 있는 책.",
    },
    {
        "title": "10년 후 우리는, AI 로봇을 구독하다!",
        "author": "박재용",
        "publisher": "이상북스",
        "field": "IT·디지털",
        "icon": "🤖",
        "color": "#E5DEFF",
        "description": "인공지능과 로봇이 바꿀 미래를 생각해 볼 수 있는 책.",
    },
    {
        "title": "10년 후 우리는, AI와 친구가 될 수 있을까?",
        "author": "박재용",
        "publisher": "이상북스",
        "field": "IT·디지털",
        "icon": "🧠",
        "color": "#E5DEFF",
        "description": "인공지능과 인간의 관계, 미래 사회를 생각해 볼 수 있는 책.",
    },
    {
        "title": "과학선생님이 읽어 주는 기후변화 보고서",
        "author": "김추령",
        "publisher": "서해문집",
        "field": "자연과학",
        "icon": "🌿",
        "color": "#E4F4D2",
        "description": "기후 변화에 대한 과학적 이해를 넓힐 수 있는 책.",
    },
    {
        "title": "미래 세대를 위한 과학 기술 문해력",
        "author": "임완수, 배성호",
        "publisher": "철수와영희",
        "field": "자연과학",
        "icon": "🔬",
        "color": "#DDEBFF",
        "description": "과학기술 정보를 이해하고 판단하는 능력을 생각해 보는 책.",
    },
    {
        "title": "미래 세대를 위한 자연사 이야기",
        "author": "신나미",
        "publisher": "철수와영희",
        "field": "자연과학",
        "icon": "🦕",
        "color": "#E4F4D2",
        "description": "자연과 생명의 역사를 살펴볼 수 있는 과학 분야 도서.",
    },
    {
        "title": "청소년을 위한 법학 에세이",
        "author": "곽한영",
        "publisher": "해냄출판사",
        "field": "인문·사회",
        "icon": "⚖️",
        "color": "#E9E0FF",
        "description": "법과 사회를 이해하는 데 도움을 주는 청소년 대상 도서.",
    },
    {
        "title": "청소년을 위한 개념 있는 지구 생활",
        "author": "박지은",
        "publisher": "뜨인돌출판사",
        "field": "농림·수산",
        "icon": "🌎",
        "color": "#E4F4D2",
        "description": "지구 환경과 지속 가능한 생활을 생각해 볼 수 있는 책.",
    },
]

FIELDS = ["전체"] + sorted({book["field"] for book in BOOKS})

if "page" not in st.session_state:
    st.session_state.page = "홈"
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "selected" not in st.session_state:
    st.session_state.selected = None


st.markdown("""
<style>
.stApp { background:#F1F6FF; color:#263454; }
.block-container { max-width:1100px; padding-top:1.3rem; }
.hero {
    background:linear-gradient(120deg,#C8E5FF,#EDF4FF,#D9EEFF);
    padding:26px; border-radius:24px;
    border:1px solid #C5DFFA; margin-bottom:20px;
}
.hero h1 { color:#24345F; font-size:30px; }
.hero p { color:#536789; line-height:1.8; }
.section-title {
    font-size:22px; font-weight:800; color:#27375E;
    margin:24px 0 14px;
}
.category {
    border-radius:20px; padding:15px 4px; text-align:center;
    min-height:95px; margin-bottom:5px;
}
.category-icon { font-size:30px; }
.category-name { font-size:13px; font-weight:700; margin-top:7px; }
.book-card {
    background:white; border:1px solid #E1E9F6;
    border-radius:17px; padding:11px; margin-bottom:8px;
}
.book-cover {
    height:160px; border-radius:10px; padding:12px 6px;
    display:flex; flex-direction:column;
    justify-content:center; align-items:center; text-align:center;
    color:#2D4265; box-shadow:2px 4px 8px #DDE5F0;
}
.cover-icon { font-size:34px; margin-bottom:12px; }
.cover-title { font-size:14px; font-weight:800; line-height:1.5; }
.book-title { font-weight:750; font-size:14px; line-height:1.6; margin-top:10px; }
.book-meta { color:#7786A4; font-size:12px; margin-top:6px; }
div.stButton > button { border-radius:12px; }
</style>
""", unsafe_allow_html=True)


def navigate(page):
    st.session_state.page = page
    st.session_state.selected = None


def search_link(title):
    return "https://www.yes24.com/Product/Search?query=" + quote(title)


def show_books(books, prefix):
    if not books:
        st.info("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")
        return

    st.caption(f"총 {len(books)}권")
    for start in range(0, len(books), 4):
        cols = st.columns(4)
        for col, book in zip(cols, books[start:start + 4]):
            with col:
                st.markdown(f"""
                <div class="book-card">
                    <div class="book-cover" style="background:{book['color']}">
                        <div class="cover-icon">{book['icon']}</div>
                        <div class="cover-title">{book['title']}</div>
                    </div>
                    <div class="book-title">{book['title']}</div>
                    <div class="book-meta">{book['author']} · {book['publisher']}</div>
                    <div class="book-meta">{book['field']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("상세 정보", key=f"{prefix}_detail_{book['title']}",
                             use_container_width=True):
                    st.session_state.selected = book["title"]
                    st.rerun()

                saved = book["title"] in st.session_state.favorites
                if st.button(
                    "★ 내 서재에 저장" if not saved else "✓ 저장됨",
                    key=f"{prefix}_save_{book['title']}",
                    use_container_width=True,
                ):
                    if saved:
                        st.session_state.favorites.remove(book["title"])
                    else:
                        st.session_state.favorites.append(book["title"])
                    st.rerun()


st.markdown("""
<div class="hero">
    <div style="font-size:44px">📘 🌱</div>
    <h1>꿈을 찾는 책장</h1>
    <p>다양한 진로 정보책을 통해<br>
    나의 미래를 더 가까이!</p>
    <b>💬 네 꿈은 어떤 모습인가요?</b>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

if page == "홈":
    query = st.text_input(
        "책 검색",
        placeholder="🔎 관심 있는 분야나 직업을 검색해보세요",
        label_visibility="collapsed",
    )

    if query.strip():
        results = [
            b for b in BOOKS
            if query.lower() in (
                b["title"] + b["author"] + b["publisher"]
                + b["field"] + b["description"]
            ).lower()
        ]
        st.markdown('<div class="section-title">🔍 검색 결과</div>',
                    unsafe_allow_html=True)
        show_books(results, "home_search")
    else:
        st.markdown('<div class="section-title">▦ 분야별 찾아보기</div>',
                    unsafe_allow_html=True)

        category_colors = {
            "자연과학": "#DCEAFF", "공학": "#EAE2FF",
            "의료·보건": "#FFE0E5", "예술·체육": "#FFEAD3",
            "인문·사회": "#D8F3E4", "교육": "#FFF0BF",
            "경영·경제": "#D5F1F0", "농림·수산": "#E7F5CD",
            "언론·미디어": "#DCE7FF", "IT·디지털": "#E9DDFF",
        }
        category_icons = {
            "자연과학": "🧪", "공학": "🖥️", "의료·보건": "💗",
            "예술·체육": "🎨", "인문·사회": "👥", "교육": "📖",
            "경영·경제": "📊", "농림·수산": "🌿",
            "언론·미디어": "🎬", "IT·디지털": "💻",
        }

        categories = list(category_colors.keys())
        for start in range(0, len(categories), 5):
            cols = st.columns(5)
            for col, field in zip(cols, categories[start:start + 5]):
                with col:
                    st.markdown(f"""
                    <div class="category" style="background:{category_colors[field]}">
                        <div class="category-icon">{category_icons[field]}</div>
                        <div class="category-name">{field}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("둘러보기", key=f"category_{field}",
                                 use_container_width=True):
                        st.session_state.category_filter = field
                        navigate("분야별 검색")
                        st.rerun()

        st.markdown('<div class="section-title">📚 추천 진로 정보책</div>',
                    unsafe_allow_html=True)
        show_books(BOOKS[:8], "recommend")

        if st.button("책 더 보기  ›", use_container_width=True):
            navigate("분야별 검색")
            st.rerun()

elif page == "분야별 검색":
    st.markdown('<div class="section-title">🔎 분야별 진로책</div>',
                unsafe_allow_html=True)

    default_field = st.session_state.get("category_filter", "전체")
    options = ["전체"] + sorted({b["field"] for b in BOOKS})
    if default_field not in options:
        default_field = "전체"

    field = st.selectbox("분야 선택", options,
                         index=options.index(default_field))
    query = st.text_input("제목·저자·출판사 검색", key="catalog_search")

    results = [
        b for b in BOOKS
        if (field == "전체" or b["field"] == field)
        and query.lower() in (
            b["title"] + b["author"] + b["publisher"] + b["description"]
        ).lower()
    ]
    show_books(results, "catalog")

elif page == "내 서재":
    st.markdown('<div class="section-title">🔖 나의 서재</div>',
                unsafe_allow_html=True)
    saved_books = [b for b in BOOKS if b["title"] in st.session_state.favorites]
    show_books(saved_books, "favorites")

    if saved_books and st.button("저장한 책 모두 해제"):
        st.session_state.favorites = []
        st.rerun()

elif page == "마이페이지":
    st.markdown('<div class="section-title">👤 마이페이지</div>',
                unsafe_allow_html=True)
    st.write(f"현재 등록된 도서: **{len(BOOKS)}권**")
    st.write(f"내 서재에 저장한 도서: **{len(st.session_state.favorites)}권**")
    st.caption("관심 도서는 현재 세션에서만 유지됩니다.")

# 선택한 책 상세 정보
if st.session_state.selected:
    book = next(
        (b for b in BOOKS if b["title"] == st.session_state.selected),
        None,
    )
    if book:
        st.markdown("---")
        st.markdown(f"## {book['icon']} {book['title']}")
        st.write(f"**저자:** {book['author']}")
        st.write(f"**출판사:** {book['publisher']}")
        st.write(f"**분야:** {book['field']}")
        st.write(book["description"])
        st.link_button(
            "서점에서 도서 정보 확인하기",
            search_link(book["title"]),
            use_container_width=True,
        )
        st.caption("서점 검색 결과에서 정확한 판본과 출판 정보를 확인하세요.")
        if st.button("상세 정보 닫기"):
            st.session_state.selected = None
            st.rerun()

st.markdown("---")
nav_cols = st.columns(4)
for col, (icon, label) in zip(
    nav_cols,
    [("🏠", "홈"), ("🔎", "분야별 검색"),
     ("🔖", "내 서재"), ("👤", "마이페이지")],
):
    with col:
        if st.button(f"{icon}\n{label}", use_container_width=True,
                     type="primary" if page == label else "secondary"):
            navigate(label)
            st.rerun()

st.caption(
    "꿈을 찾는 책장 | 도서 정보는 서점 검색을 통해 확인할 수 있습니다. "
    "분야 분류는 탐색 편의를 위한 것입니다."
)
