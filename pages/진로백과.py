
import streamlit as st
import requests
from urllib.parse import quote_plus

st.set_page_config(
    page_title="꿈을 찾는 책장",
    page_icon="📚",
    layout="wide"
)

API_URL = "https://www.googleapis.com/books/v1/volumes"
PLACEHOLDER = (
    "https://placehold.co/300x430/e9e3ff/514878"
    "?text=Book+Cover"
)

FIELDS = {
    "전체 분야": "청소년 진로 직업",
    "진로·자기이해": "진로 직업 자기이해 청소년",
    "IT·컴퓨터": "컴퓨터 프로그래밍 인공지능",
    "공학·기술": "공학 기술 로봇",
    "과학": "과학 과학자",
    "환경·생태": "환경 기후변화 생태",
    "의료·보건": "의학 간호 보건",
    "심리·상담": "심리학 상담",
    "교육·교사": "교육 교사 교육학",
    "경영·경제": "경제 경영 기업",
    "창업·마케팅": "창업 마케팅",
    "법·사회": "법학 사회 인권",
    "경찰·소방": "경찰 소방 안전",
    "요리·식품": "요리 제과제빵 식품",
    "예술·미술": "미술 예술 디자인",
    "음악·공연": "음악 작곡 공연",
    "영상·미디어": "영화 영상 미디어",
    "언어·출판": "번역 출판 작가",
    "건축·인테리어": "건축 인테리어",
    "항공·교통": "항공 조종사 교통",
    "농업·동물": "농업 동물 수의사",
    "스포츠·체육": "스포츠 체육 운동",
    "금융·회계": "금융 회계",
    "역사·인문": "역사 인문학 철학",
    "여행·관광": "여행 관광 호텔"
}

# -------------------------
# 스타일
# -------------------------
st.markdown("""
<style>
.stApp { background: #f7f8fc; }
.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
}
.hero {
    background: linear-gradient(120deg,#dcecff,#eee4ff);
    padding: 28px;
    border-radius: 22px;
    margin-bottom: 20px;
}
.hero h1 { color: #283650; margin: 0; }
.hero p { color: #586681; margin-bottom: 0; }
.book-title {
    color: #293750;
    font-size: 17px;
    font-weight: 700;
    overflow-wrap: anywhere;
}
.book-author { color: #748096; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>📚 꿈을 찾는 책장</h1>
<p>책으로 만나 보는 다양한 직업과 진로 이야기</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 세션 상태
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "field" not in st.session_state:
    st.session_state.field = "전체 분야"

if "keyword" not in st.session_state:
    st.session_state.keyword = ""

if "page_num" not in st.session_state:
    st.session_state.page_num = 0

# -------------------------
# 검색 함수
# -------------------------
def get_books(query, start=0, limit=20):
    """Google Books 검색. 실패 시 앱 대신 오류 메시지를 반환한다."""
    try:
        response = requests.get(
            API_URL,
            params={
                "q": query,
                "startIndex": start,
                "maxResults": limit,
                "printType": "books",
                "langRestrict": "ko",
            },
            timeout=20,
        )

        if response.status_code == 429:
            return [], 0, "검색 요청이 많아요. 잠시 기다린 뒤 다시 시도해 주세요."

        if response.status_code == 403:
            return [], 0, (
                "도서 검색 서비스의 접근이 제한됐어요. "
                "잠시 후 다시 시도해 주세요."
            )

        response.raise_for_status()
        data = response.json()

        books = []
        for item in data.get("items", []):
            info = item.get("volumeInfo") or {}
            title = info.get("title")

            if not title:
                continue

            image_links = info.get("imageLinks") or {}
            cover = (
                image_links.get("thumbnail")
                or image_links.get("smallThumbnail")
                or PLACEHOLDER
            )
            cover = cover.replace("http://", "https://")

            ids = info.get("industryIdentifiers") or []
            isbn = next(
                (
                    x.get("identifier", "")
                    for x in ids
                    if x.get("type") == "ISBN_13"
                ),
                ""
            )

            book_id = item.get("id") or (
                title + "_" + ", ".join(info.get("authors") or [])
            )

            books.append({
                "id": book_id,
                "title": title,
                "author": ", ".join(
                    info.get("authors") or ["저자 정보 없음"]
                ),
                "publisher": info.get("publisher") or "출판사 정보 없음",
                "published": info.get("publishedDate") or "",
                "description": info.get("description") or "등록된 책 소개가 없습니다.",
                "cover": cover,
                "link": info.get("infoLink") or "https://books.google.com/",
                "isbn": isbn,
            })

        return books, data.get("totalItems", 0), None

    except requests.exceptions.Timeout:
        return [], 0, "검색 시간이 초과됐어요. 다시 검색해 주세요."
    except requests.exceptions.ConnectionError:
        return [], 0, "도서 검색 서버에 연결할 수 없어요. 잠시 후 다시 시도해 주세요."
    except requests.exceptions.HTTPError as e:
        return [], 0, f"검색 서버 응답 오류가 발생했어요 (HTTP {e.response.status_code})."
    except (requests.exceptions.RequestException, ValueError):
        return [], 0, "도서 정보를 불러오지 못했어요. 검색어를 바꿔 다시 시도해 주세요."

# -------------------------
# 메뉴
# -------------------------
m1, m2, m3 = st.columns(3)

with m1:
    if st.button("🏠 홈", use_container_width=True):
        st.session_state.page = "홈"
        st.rerun()

with m2:
    if st.button("🔎 도서 검색", use_container_width=True):
        st.session_state.page = "검색"
        st.rerun()

with m3:
    if st.button(
        f"💜 내 서재 ({len(st.session_state.favorites)})",
        use_container_width=True
    ):
        st.session_state.page = "서재"
        st.rerun()

st.divider()

# -------------------------
# 분야 버튼
# -------------------------
def open_field(field):
    st.session_state.field = field
    st.session_state.keyword = ""
    st.session_state.page_num = 0
    st.session_state.page = "검색"
    st.rerun()

# -------------------------
# 도서 카드
# -------------------------
def show_books(books):
    if not books:
        st.info("검색 결과가 없어요. 다른 검색어로 다시 시도해 주세요.")
        return

    cols = st.columns(4)

    for i, book in enumerate(books):
        with cols[i % 4]:
            with st.container(border=True):
                st.image(book["cover"], use_container_width=True)

                st.markdown(
                    f"<div class='book-title'>{book['title']}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='book-author'>{book['author']}</div>",
                    unsafe_allow_html=True
                )
                st.caption(f"출판사: {book['publisher']}")

                with st.expander("책 소개"):
                    st.write(book["description"])
                    if book["published"]:
                        st.caption("출판일: " + book["published"])
                    if book["isbn"]:
                        st.caption("ISBN: " + book["isbn"])

                book_id = book["id"]
                saved = book_id in st.session_state.favorites

                if st.button(
                    "💜 찜 취소" if saved else "🤍 찜하기",
                    key=f"fav_{i}_{book_id}",
                    use_container_width=True
                ):
                    if saved:
                        del st.session_state.favorites[book_id]
                    else:
                        st.session_state.favorites[book_id] = book
                    st.rerun()

                if book["link"].startswith("https://"):
                    st.link_button(
                        "📖 도서 정보",
                        book["link"],
                        use_container_width=True
                    )

                st.link_button(
                    "🛒 서점에서 찾기",
                    "https://www.yes24.com/Product/Search?query="
                    + quote_plus(book["title"]),
                    use_container_width=True
                )

# -------------------------
# 홈
# -------------------------
if st.session_state.page == "홈":
    st.subheader("🌈 관심 있는 분야를 선택해 보세요")
    st.write("관심 분야를 선택하면 관련 도서를 검색할 수 있어요.")

    field_list = list(FIELDS.keys())[1:]

    for start in range(0, len(field_list), 4):
        row_fields = field_list[start:start + 4]
        cols = st.columns(4)

        for col, field in zip(cols, row_fields):
            with col:
                if st.button(
                    "📘 " + field,
                    key="cat_" + field,
                    use_container_width=True
                ):
                    open_field(field)

    st.divider()
    st.subheader("🔎 바로 책 찾기")

    home_keyword = st.text_input(
        "책 제목, 저자 또는 직업 입력",
        placeholder="예: 뭘 해도 괜찮아, 수의사, 인공지능"
    )

    if st.button("도서 검색하기", use_container_width=True):
        st.session_state.keyword = home_keyword.strip()
        st.session_state.field = "전체 분야"
        st.session_state.page_num = 0
        st.session_state.page = "검색"
        st.rerun()

# -------------------------
# 검색
# -------------------------
elif st.session_state.page == "검색":
    st.subheader("🔎 분야별 도서 검색")

    field_list = list(FIELDS.keys())
    current = st.session_state.field
    if current not in field_list:
        current = "전체 분야"

    selected = st.selectbox(
        "분야 선택",
        field_list,
        index=field_list.index(current)
    )

    keyword = st.text_input(
        "검색어",
        value=st.session_state.keyword,
        placeholder="예: 심리학, 과학자, 김영하"
    )

    c1, c2 = st.columns(2)

    with c1:
        search_clicked = st.button(
            "🔍 검색",
            use_container_width=True
        )

    with c2:
        reset_clicked = st.button(
            "전체 분야 초기화",
            use_container_width=True
        )

    if search_clicked:
        st.session_state.field = selected
        st.session_state.keyword = keyword.strip()
        st.session_state.page_num = 0
        st.rerun()

    if reset_clicked:
        st.session_state.field = "전체 분야"
        st.session_state.keyword = ""
        st.session_state.page_num = 0
        st.rerun()

    # 제목/저자 검색어가 있으면 해당 검색어 우선
    active_keyword = st.session_state.keyword
    active_field = st.session_state.field

    if active_keyword:
        query = active_keyword
    else:
        query = FIELDS.get(active_field, FIELDS["전체 분야"])

    start = st.session_state.page_num * 20

    with st.spinner("책 정보를 검색하고 있어요..."):
        books, total, error = get_books(query, start=start, limit=20)

    if error:
        st.error(error)
        st.caption(
            "인터넷 연결이 정상이어도 외부 검색 서버의 제한이나 "
            "일시적인 장애 때문에 검색이 실패할 수 있어요."
        )
    else:
        st.caption(f"검색 결과: 약 {total:,}권")
        show_books(books)

        if books:
            st.divider()
            p1, p2, p3 = st.columns([1, 2, 1])

            with p1:
                if st.button(
                    "⬅️ 이전",
                    disabled=st.session_state.page_num == 0,
                    use_container_width=True
                ):
                    st.session_state.page_num -= 1
                    st.rerun()

            with p2:
                st.markdown(
                    f"<p style='text-align:center'>"
                    f"{st.session_state.page_num + 1}페이지"
                    f"</p>",
                    unsafe_allow_html=True
                )

            with p3:
                if st.button(
                    "다음 ➡️",
                    disabled=(start + 20 >= total),
                    use_container_width=True
                ):
                    st.session_state.page_num += 1
                    st.rerun()

# -------------------------
# 내 서재
# -------------------------
elif st.session_state.page == "서재":
    st.subheader("💜 내 서재")

    saved_books = list(st.session_state.favorites.values())

    if saved_books:
        show_books(saved_books)

        if st.button("🗑️ 찜 목록 비우기"):
            st.session_state.favorites = {}
            st.rerun()
    else:
        st.info("아직 찜한 책이 없어요. 검색 화면에서 책을 찜해 보세요.")

st.divider()
st.caption(
    "📚 꿈을 찾는 책장 | 외부 도서 검색 결과를 사용합니다. "
    "표지나 출판 정보가 없을 수 있으며, 찜 목록은 현재 세션에서 유지됩니다."
)
