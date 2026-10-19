
import streamlit as st
from urllib.parse import quote_plus

st.set_page_config(
    page_title="꿈을 찾는 책장",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# 실제 출간 도서 데이터
# -----------------------------
BOOKS = [
    {"title":"뭘 해도 괜찮아: 꿈을 찾는 진로의 심리학","author":"이남석","publisher":"사계절","field":"진로·자기이해","emoji":"🌱","desc":"자신의 관심과 가능성을 돌아보며 진로를 고민하는 책"},
    {"title":"청소년 자립/직업 진로 길라잡이","author":"모세종","publisher":"생각나눔","field":"진로·자기이해","emoji":"🧭","desc":"자립과 직업 선택을 고민할 때 참고할 수 있는 진로 안내서"},
    {"title":"나의 직업 제과제빵떡사","author":"청소년행복연구실","publisher":"동천출판","field":"요리·식품","emoji":"🥐","desc":"제과·제빵·떡 관련 직업을 알아보는 책"},
    {"title":"AI의 혁신을 이끄는 데이터과학자","author":"김태헌","publisher":"토크쇼","field":"IT·디지털","emoji":"💻","desc":"데이터과학자의 역할과 업무를 소개하는 책"},
    {"title":"SW를 세상에 알리는 소프트웨어비즈니스전문가","author":"권준혁","publisher":"토크쇼","field":"IT·디지털","emoji":"🖥️","desc":"소프트웨어와 비즈니스를 연결하는 직업 이야기"},
    {"title":"기술혁신을 주도하는 최고기술경영자(CTO)","author":"홍영훈","publisher":"토크쇼","field":"공학·기술","emoji":"⚙️","desc":"기술 개발과 경영을 함께 이끄는 CTO에 관한 책"},
    {"title":"기후변화시대 10대가 알아야할 미래 직업의 이동","author":"신지나","publisher":"한스미디어","field":"자연과학·환경","emoji":"🌍","desc":"기후변화가 미래 직업에 미치는 영향을 살펴보는 책"},
    {"title":"날씨를 전하며 내일을 준비하는 기상캐스터","author":"최아리","publisher":"토크쇼","field":"언론·미디어","emoji":"🌦️","desc":"날씨 정보를 전달하는 기상캐스터의 업무를 알아보는 책"},
    {"title":"마음 속 기억창고를 만드는 K-POP작곡가","author":"서정진","publisher":"토크쇼","field":"예술·음악","emoji":"🎵","desc":"대중음악 작곡가의 작업과 음악 산업을 소개하는 책"},
    {"title":"범죄자를 끝까지 추적해 검거하는 형사","author":"윤석호","publisher":"토크쇼","field":"법·공공안전","emoji":"🔎","desc":"수사와 사건 해결을 담당하는 형사의 직업 이야기"},
    {"title":"변신을 통해 행복을 선물하는 헤어디자이너","author":"김원일","publisher":"토크쇼","field":"미용·서비스","emoji":"✂️","desc":"헤어디자이너의 기술과 고객 소통을 알아보는 책"},
    {"title":"아이들과 함께 걷는 초등교사","author":"전소영","publisher":"토크쇼","field":"교육","emoji":"🍎","desc":"초등교사의 역할과 학교생활을 소개하는 책"},
    {"title":"전 세계의 책을 우리말로 풀어내는 멋진 직업 출판번역가","author":"이세진","publisher":"토크쇼","field":"언어·출판","emoji":"📖","desc":"외국의 책을 우리말로 옮기는 출판번역가의 이야기"},
    {"title":"차갑고 뜨거운 종합예술인 드라마PD","author":"민영홍","publisher":"토크쇼","field":"언론·미디어","emoji":"🎬","desc":"드라마 기획과 제작을 이끄는 PD에 관한 책"},
    {"title":"하늘의 신호등 항공교통관제사","author":"유영미·임은정","publisher":"토크쇼","field":"항공·교통","emoji":"✈️","desc":"항공기의 안전한 이동을 돕는 관제사에 관한 책"},
    {"title":"10대를 위한 1세대 창업가 수업","author":"김정진","publisher":"넥스트씨","field":"경영·경제","emoji":"🚀","desc":"창업가의 경험과 도전 과정을 알아보는 책"},
    {"title":"공부머리를 역전하는 7가지 진로 공부법","author":"앤디 림·윤규훈","publisher":"온더페이지","field":"진로·자기이해","emoji":"📝","desc":"진로와 공부 방법을 함께 고민하는 책"},
    {"title":"10년 후 우리는, AI 로봇을 구독하다!","author":"박재용","publisher":"이상북스","field":"IT·디지털","emoji":"🤖","desc":"AI와 로봇이 바꿀 미래 사회를 생각해 보는 책"},
    {"title":"10년 후 우리는, AI와 친구가 될 수 있을까?","author":"박재용","publisher":"이상북스","field":"IT·디지털","emoji":"🧠","desc":"인공지능과 인간의 관계를 살펴보는 책"},
    {"title":"과학선생님이 읽어 주는 기후변화 보고서","author":"김추령","publisher":"서해문집","field":"자연과학·환경","emoji":"🌱","desc":"기후변화의 원인과 영향을 과학적으로 알아보는 책"},
    {"title":"미래 세대를 위한 과학 기술 문해력","author":"임완수·배성호","publisher":"철수와영희","field":"자연과학·기술","emoji":"🔬","desc":"과학기술 정보를 이해하고 판단하는 힘을 기르는 책"},
    {"title":"미래 세대를 위한 자연사 이야기","author":"신나미","publisher":"철수와영희","field":"자연과학·환경","emoji":"🦕","desc":"자연과 생명의 역사를 알아보는 책"},
    {"title":"청소년을 위한 법학 에세이","author":"곽한영","publisher":"해냄출판사","field":"법·사회","emoji":"⚖️","desc":"법과 사회의 관계를 청소년 눈높이에서 설명하는 책"},
    {"title":"청소년을 위한 개념 있는 지구 생활","author":"박지은","publisher":"뜨인돌출판사","field":"환경·사회","emoji":"♻️","desc":"환경 문제와 지속 가능한 생활을 생각해 보는 책"},
    {"title":"고흐의 귀, 퀴리의 골수","author":"수지 에지","publisher":"타인의사유","field":"과학·인문","emoji":"🎨","desc":"예술과 과학 분야 인물들의 삶을 살펴보는 책"},
]

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {background-color:#f7f9fc;}
.block-container {max-width:1150px;padding-top:2rem;}
.hero {
    background:linear-gradient(120deg,#dcecff,#e9e3ff);
    padding:30px;border-radius:24px;margin-bottom:22px;
}
.hero h1 {color:#283650;margin:0;}
.hero p {color:#52627b;margin-bottom:0;}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius:18px;
}
.book-title {font-size:17px;font-weight:700;color:#293750;}
.book-meta {font-size:13px;color:#6c7890;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>📚 꿈을 찾는 책장</h1>
<p>책으로 만나 보는 다양한 직업과 진로 이야기</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 세션 상태
# -----------------------------
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []
if "page" not in st.session_state:
    st.session_state["page"] = "홈"
if "chosen_field" not in st.session_state:
    st.session_state["chosen_field"] = "전체 분야"

# -----------------------------
# 상단 메뉴
# -----------------------------
nav1, nav2, nav3 = st.columns(3)

with nav1:
    if st.button("🏠 홈", use_container_width=True):
        st.session_state["page"] = "홈"

with nav2:
    if st.button("🔎 분야별 검색", use_container_width=True):
        st.session_state["page"] = "검색"

with nav3:
    if st.button(
        f"💜 내 서재 ({len(st.session_state['favorites'])})",
        use_container_width=True
    ):
        st.session_state["page"] = "서재"

st.divider()

fields = sorted(set(book["field"] for book in BOOKS))
all_fields = ["전체 분야"] + fields

# -----------------------------
# 홈 화면
# -----------------------------
if st.session_state["page"] == "홈":
    st.subheader("어떤 분야가 궁금한가요?")
    st.write("관심 있는 분야를 선택해 관련 도서를 찾아보세요.")

    emojis = {
        "IT·디지털": "💻",
        "공학·기술": "⚙️",
        "자연과학·환경": "🌿",
        "자연과학·기술": "🔬",
        "교육": "🍎",
        "예술·음악": "🎨",
        "언론·미디어": "🎬",
        "경영·경제": "📈",
        "진로·자기이해": "🧭",
        "법·사회": "⚖️",
        "법·공공안전": "🔎",
        "요리·식품": "🥐",
        "미용·서비스": "✂️",
        "언어·출판": "📖",
        "항공·교통": "✈️",
        "환경·사회": "♻️",
        "과학·인문": "🧪",
    }

    category_cols = st.columns(4)
    for i, field_name in enumerate(fields):
        with category_cols[i % 4]:
            if st.button(
                f"{emojis.get(field_name, '📘')} {field_name}",
                key=f"category_{i}",
                use_container_width=True
            ):
                st.session_state["chosen_field"] = field_name
                st.session_state["page"] = "검색"
                st.rerun()

    st.subheader("📚 추천 도서")
    displayed_books = BOOKS[:8]

# -----------------------------
# 검색 화면
# -----------------------------
elif st.session_state["page"] == "검색":
    st.subheader("🔎 분야별 도서 검색")

    search_col, field_col = st.columns([2, 1])

    with search_col:
        keyword = st.text_input(
            "책 제목이나 저자 검색",
            placeholder="예: 데이터과학자, 이남석",
            key="search_keyword"
        )

    with field_col:
        default_field = st.session_state["chosen_field"]
        if default_field not in all_fields:
            default_field = "전체 분야"

        selected_field = st.selectbox(
            "분야 선택",
            all_fields,
            index=all_fields.index(default_field),
            key="search_field"
        )

    displayed_books = [
        book for book in BOOKS
        if (
            selected_field == "전체 분야"
            or book["field"] == selected_field
        )
        and keyword.strip().lower() in (
            book["title"] + " " +
            book["author"] + " " +
            book["publisher"] + " " +
            book["field"]
        ).lower()
    ]

    st.caption(f"검색 결과: {len(displayed_books)}권")

# -----------------------------
# 내 서재 화면
# -----------------------------
else:
    st.subheader("💜 내 서재")
    st.caption("찜한 도서를 모아 볼 수 있어요.")

    displayed_books = [
        book for book in BOOKS
        if book["title"] in st.session_state["favorites"]
    ]

    if not displayed_books:
        st.info("아직 찜한 책이 없어요. 홈이나 검색 화면에서 책을 찜해 보세요.")

# -----------------------------
# 도서 카드
# -----------------------------
st.write(f"총 {len(displayed_books)}권")

if displayed_books:
    columns = st.columns(3)

    for i, book in enumerate(displayed_books):
        with columns[i % 3]:
            with st.container(border=True):
                st.markdown(f"## {book['emoji']}")
                st.markdown(
                    f"<div class='book-title'>{book['title']}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='book-meta'>{book['author']} · {book['publisher']}</div>",
                    unsafe_allow_html=True
                )

                st.caption(f"분야: {book['field']}")
                st.write(book["desc"])

                is_favorite = (
                    book["title"] in st.session_state["favorites"]
                )

                if st.button(
                    "💜 찜 취소" if is_favorite else "🤍 찜하기",
                    key=f"favorite_{i}_{book['title']}",
                    use_container_width=True
                ):
                    if is_favorite:
                        st.session_state["favorites"].remove(book["title"])
                    else:
                        st.session_state["favorites"].append(book["title"])
                    st.rerun()

                store_url = (
                    "https://www.yes24.com/Product/Search?query="
                    + quote_plus(book["title"])
                )
                st.link_button(
                    "서점에서 찾기",
                    store_url,
                    use_container_width=True
                )

st.divider()
st.caption(
    "도서 소개는 탐색을 돕기 위한 요약입니다. "
    "책의 상세 정보와 구매 가능 여부는 서점에서 확인하세요. "
    "찜 목록은 현재 접속 세션에서 유지됩니다."
)
