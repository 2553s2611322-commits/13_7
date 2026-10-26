
import streamlit as st
import requests
from urllib.parse import quote_plus

st.set_page_config(
    page_title="꿈을 찾는 책장",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------
# 기본 설정
# ----------------------------------
API_URL = "https://www.googleapis.com/books/v1/volumes"

CATEGORIES = {
    "전체 분야": "",
    "진로·자기이해": "진로 직업 청소년",
    "IT·컴퓨터": "컴퓨터 프로그래밍 인공지능",
    "공학·기술": "공학 기술 로봇",
    "과학": "과학 과학자",
    "환경·생태": "환경 기후변화 생태",
    "의료·보건": "의학 간호사 보건",
    "심리·상담": "심리학 상담 심리상담사",
    "교육·교사": "교육 교사 교육학",
    "경영·경제": "경제 경영 기업",
    "창업·마케팅": "창업 마케팅 브랜드",
    "법·사회": "법학 사회학 인권",
    "경찰·소방": "경찰 소방 공공안전",
    "요리·식품": "요리 제과제빵 식품",
    "예술·미술": "미술 예술 디자이너",
    "음악·공연": "음악 작곡 공연",
    "영상·미디어": "영상 영화 미디어",
    "언어·출판": "번역가 출판 작가",
    "건축·인테리어": "건축 인테리어 디자인",
    "항공·교통": "항공 조종사 교통",
    "농업·동물": "농업 동물 수의사",
    "스포츠·체육": "스포츠 체육 운동",
    "금융·회계": "금융 회계 세금",
    "역사·인문": "역사 인문학 철학",
    "여행·관광": "여행 관광 호텔",
}

# 표지 이미지가 없는 경우 사용할 이미지
FALLBACK_COVER = (
    "https://placehold.co/300x430/e9e3ff/514878"
    "?text=Book+Cover"
)

# ----------------------------------
# 디자인
# ----------------------------------
st.markdown("""
<style>
.stApp {
    background: #f7f8fc;
}
.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(120deg, #dcecff, #eee4ff);
    padding: 30px;
    border-radius: 24px;
    margin-bottom: 20px;
}
.hero h1 {
    color: #283650;
    font-size: 36px;
    margin: 0;
}
.hero p {
    color: #586681;
    font-size: 16px;
    margin-bottom: 0;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 17px;
    border-color: #e5e7f0;
    background-color: #ffffff;
}
div.stButton > button,
div.stLinkButton > a {
    border-radius: 12px;
}
.book-title {
    font-size: 17px;
    font-weight: 700;
    color: #293750;
    line-height: 1.5;
    overflow-wrap: anywhere;
}
.book-meta {
    color: #748096;
    font-size: 13px;
}
.small-note {
    color: #748096;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📚 꿈을 찾는 책장</h1>
    <p>책으로 만나 보는 다양한 직업과 진로 이야기</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# 세션 상태
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "selected_field" not in st.session_state:
    st.session_state.selected_field = "전체 분야"

if "search_text" not in st.session_state:
    st.session_state.search_text = ""

if "page_number" not in st.session_state:
    st.session_state.page_number = 0

# ----------------------------------
# Google Books API
# ----------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def search_books(query, start_index=0, max_results=20):
    """도서 정보를 검색하고 결과를 캐시에 저장한다."""
    try:
        response = requests.get(
            API_URL,
            params={
                "q": query,
                "startIndex": start_index,
                "maxResults": max_results,
                "printType": "books",
                "orderBy": "relevance",
                "langRestrict": "ko",
            },
            headers={"User-Agent": "DreamBookshelf/1.0"},
            timeout=12,
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            title = info.get("title", "").strip()

            if not title:
                continue

            authors = info.get("authors", [])
            image_links = info.get("imageLinks", {})
            cover = (
                image_links.get("thumbnail")
                or image_links.get("smallThumbnail")
                or FALLBACK_COVER
            )
            # HTTPS 주소로 정리
            cover = cover.replace("http://", "https://")

            identifiers = info.get("industryIdentifiers", [])
            isbn = next(
                (
                    identifier.get("identifier", "")
                    for identifier in identifiers
                    if identifier.get("type") == "ISBN_13"
                ),
                "",
            )

            book_id = item.get("id", "")
            book = {
                "id": book_id,
                "title": title,
                "authors": ", ".join(authors) if authors else "저자 정보 없음",
                "publisher": info.get("publisher", "출판사 정보 없음"),
                "published": info.get("publishedDate", ""),
                "description": info.get(
                    "description", "등록된 책 소개가 없습니다."
                ),
                "cover": cover,
                "link": info.get(
                    "infoLink",
                    "https://books.google.com/",
                ),
                "isbn": isbn,
                "categories": ", ".join(info.get("categories", [])),
            }
            results.append(book)

        return results, data.get("totalItems", 0), None

    except requests.exceptions.Timeout:
        return [], 0, "도서 검색 시간이 초과됐어요. 잠시 후 다시 시도해 주세요."
    except requests.exceptions.RequestException:
        return [], 0, "도서 정보를 가져오지 못했어요. 인터넷 연결을 확인해 주세요."
    except (ValueError, TypeError):
        return [], 0, "도서 정보를 읽는 중 문제가 발생했어요."

# ----------------------------------
# 상단 메뉴
# ----------------------------------
menu1, menu2, menu3 = st.columns(3)

with menu1:
    if st.button("🏠 홈", use_container_width=True):
        st.session_state.page = "홈"
        st.rerun()

with menu2:
    if st.button("🔎 도서 검색", use_container_width=True):
        st.session_state.page = "검색"
        st.rerun()

with menu3:
    if st.button(
        f"💜 내 서재 ({len(st.session_state.favorites)})",
        use_container_width=True,
    ):
        st.session_state.page = "서재"
        st.rerun()

st.divider()

# ----------------------------------
# 분야 선택
# ----------------------------------
def select_field(field):
    st.session_state.selected_field = field
    st.session_state.page = "검색"
    st.session_state.page_number = 0
    st.rerun()

# ----------------------------------
# 검색 결과 카드
# ----------------------------------
def show_books(books, empty_message="검색 결과가 없습니다."):
    if not books:
        st.info(empty_message)
        return

    columns = st.columns(4)

    for i, book in enumerate(books):
        with columns[i % 4]:
            with st.container(border=True):
                st.image(
                    book["cover"],
                    use_container_width=True,
                )

                st.markdown(
                    f"<div class='book-title'>"
                    f"{book['title']}</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"<div class='book-meta'>"
                    f"{book['authors']}</div>",
                    unsafe_allow_html=True,
                )

                st.caption(
                    f"출판사: {book['publisher']}"
                )

                if book["published"]:
                    st.caption(f"출판일: {book['published']}")

                with st.expander("책 소개"):
                    st.write(book["description"])

                    if book["isbn"]:
                        st.caption(f"ISBN: {book['isbn']}")

                    if book["categories"]:
                        st.caption(f"분류: {book['categories']}")

                book_id = book["id"]
                is_saved = book_id in st.session_state.favorites

                if st.button(
                    "💜 찜 취소" if is_saved else "🤍 찜하기",
                    key=f"fav_{book_id}_{i}",
                    use_container_width=True,
                ):
                    if is_saved:
                        del st.session_state.favorites[book_id]
                    else:
                        st.session_state.favorites[book_id] = book
                    st.rerun()

                if book["link"].startswith("https://"):
                    st.link_button(
                        "📖 도서 정보 보기",
                        book["link"],
                        use_container_width=True,
                    )

                # 국내 서점에서 제목 검색
                store_url = (
                    "https://www.yes24.com/Product/Search?query="
                    + quote_plus(book["title"])
                )
                st.link_button(
                    "🛒 서점에서 찾기",
                    store_url,
                    use_container_width=True,
                )

# ----------------------------------
# 홈 화면
# ----------------------------------
if st.session_state.page == "홈":
    st.subheader("🌈 어떤 분야가 궁금한가요?")
    st.write("관심 있는 분야를 누르면 관련 도서를 찾아볼 수 있어요.")

    category_items = list(CATEGORIES.keys())[1:]

    for start in range(0, len(category_items), 4):
        row_fields = category_items[start:start + 4]
        cols = st.columns(4)

        for col, field in zip(cols, row_fields):
            with col:
                if st.button(
                    field,
                    key=f"field_{field}",
                    use_container_width=True,
                ):
                    select_field(field)

    st.divider()
    st.subheader("✨ 추천 도서 찾아보기")
    st.write("다양한 분야의 책을 무작위가 아닌 관련 검색으로 찾아요.")

    featured_query = st.selectbox(
        "추천 분야",
        [
            "진로·자기이해",
            "IT·컴퓨터",
            "과학",
            "심리·상담",
            "예술·미술",
            "환경·생태",
        ],
    )

    if st.button("추천 도서 불러오기", use_container_width=True):
        st.session_state.selected_field = featured_query
        st.session_state.page = "검색"
        st.session_state.page_number = 0
        st.rerun()

    st.caption(
        "책 표지와 도서 정보는 Google Books 검색 결과를 이용합니다."
    )

# ----------------------------------
# 검색 화면
# ----------------------------------
elif st.session_state.page == "검색":
    st.subheader("🔎 분야별 도서 검색")

    field_options = list(CATEGORIES.keys())
    current_field = st.session_state.selected_field

    if current_field not in field_options:
        current_field = "전체 분야"

    field_index = field_options.index(current_field)

    selected_field = st.selectbox(
        "관심 분야",
        field_options,
        index=field_index,
        key="field_selector",
    )

    keyword = st.text_input(
        "책 제목 또는 저자 검색",
        value=st.session_state.search_text,
        placeholder="예: 데이터과학자, 심리학, 김영하",
        key="keyword_input",
    )

    search_col1, search_col2 = st.columns(2)

    with search_col1:
        if st.button("🔍 검색하기", use_container_width=True):
            st.session_state.selected_field = selected_field
            st.session_state.search_text = keyword.strip()
            st.session_state.page_number = 0
            st.rerun()

    with search_col2:
        if st.button("전체 분야 보기", use_container_width=True):
            st.session_state.selected_field = "전체 분야"
            st.session_state.search_text = ""
            st.session_state.page_number = 0
            st.rerun()

    # 검색어가 입력되지 않았다면 선택한 분야를 검색
    active_keyword = st.session_state.search_text
    active_field = st.session_state.selected_field

    if active_keyword:
        query = active_keyword
    elif active_field != "전체 분야":
        query = CATEGORIES[active_field]
    else:
        query = "청소년 진로 직업 과학 예술"

    page_size = 20
    start_index = st.session_state.page_number * page_size

    with st.spinner("도서와 표지를 불러오는 중..."):
        books, total, error = search_books(
            query=query,
            start_index=start_index,
            max_results=page_size,
        )

    if error:
        st.error(error)
    else:
        st.caption(f"검색 결과 약 {total:,}권")

        if not books:
            st.info(
                "검색 결과가 없어요. 다른 검색어를 입력하거나 "
                "전체 분야를 선택해 주세요."
            )
        else:
            show_books(books)

            st.divider()
            prev_col, page_col, next_col = st.columns([1, 2, 1])

            with prev_col:
                if st.button(
                    "⬅️ 이전",
                    disabled=st.session_state.page_number == 0,
                    use_container_width=True,
                ):
                    st.session_state.page_number -= 1
                    st.rerun()

            with page_col:
                st.markdown(
                    f"<p style='text-align:center'>"
                    f"{st.session_state.page_number + 1} 페이지"
                    f"</p>",
                    unsafe_allow_html=True,
                )

            with next_col:
                has_next = start_index + page_size < total
                if st.button(
                    "다음 ➡️",
                    disabled=not has_next,
                    use_container_width=True,
                ):
                    st.session_state.page_number += 1
                    st.rerun()

# ----------------------------------
# 내 서재 화면
# ----------------------------------
elif st.session_state.page == "서재":
    st.subheader("💜 나만의 서재")
    st.write("마음에 드는 책을 찜해 두고 다시 확인할 수 있어요.")

    saved_books = list(st.session_state.favorites.values())

    if saved_books:
        show_books(saved_books, "찜한 책이 없습니다.")
        if st.button("🗑️ 찜 목록 전체 비우기"):
            st.session_state.favorites = {}
            st.rerun()
    else:
        st.info("아직 찜한 책이 없어요. 검색 화면에서 책을 찜해 보세요.")

# ----------------------------------
# 하단 안내
# ----------------------------------
st.divider()
st.caption(
    "📚 꿈을 찾는 책장 | 도서 정보와 표지는 외부 도서 데이터에서 가져옵니다. "
    "표지 이미지가 없거나 정보가 다를 수 있으므로 서점에서 확인해 주세요. "
    "찜 목록은 현재 세션에서 유지되며 영구 저장되지는 않습니다."
)
