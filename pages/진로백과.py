
import streamlit as st
import requests
from html import unescape

# 분야별 한국어 검색어
FIELDS = {
    "IT·인공지능": "인공지능 컴퓨터 프로그래밍 코딩",
    "심리": "심리학 인간심리 상담",
    "과학·연구": "과학 과학자 연구",
    "경제·금융": "경제 금융 돈",
    "경영·기업": "경영 기업 창업",
    "사회·역사": "사회 역사 한국사",
    "사회·법": "법 사회 법률",
    "디자인·예술": "디자인 미술 예술",
    "교육·상담": "교육 교사 상담",
    "환경·생태": "환경 생태 기후",
    "진로·직업": "진로 직업 직업정보",
    "여행·관광": "여행 관광 호텔",
    "자기계발": "자기계발 습관 성장",
    "의학·보건": "의학 보건 간호 건강",
    "수학": "수학 수학자",
    "공학": "공학 기계 전기",
    "문학·글쓰기": "글쓰기 문학 작가",
    "요리·식품": "요리 식품 영양",
    "스포츠": "스포츠 운동 체육",
    "철학": "철학 윤리 사상",
}

st.markdown("""
<style>
.stApp { background: #f7f8fc; }
.block-container { max-width: 1200px; padding-top: 2rem; }
.hero {
    background: linear-gradient(120deg, #e4eaff, #f9e8ef);
    padding: 26px;
    border-radius: 18px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

if "career_favorites" not in st.session_state:
    st.session_state.career_favorites = []

if "career_results" not in st.session_state:
    st.session_state.career_results = []

if "career_total" not in st.session_state:
    st.session_state.career_total = 0

if "career_page" not in st.session_state:
    st.session_state.career_page = 0

if "career_query" not in st.session_state:
    st.session_state.career_query = ""

if "career_field" not in st.session_state:
    st.session_state.career_field = "진로·직업"


@st.cache_data(ttl=21600, show_spinner=False)
def search_books(field, keyword, page):
    """검색 결과를 6시간 캐시하고 페이지별로 최대 40권을 요청합니다."""
    terms = FIELDS[field]
    query = f"{terms} {keyword}".strip()

    try:
        response = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={
                "q": query,
                "langRestrict": "ko",
                "maxResults": 40,
                "startIndex": page * 40,
                "printType": "books",
                "orderBy": "relevance",
            },
            timeout=15,
        )

        if response.status_code == 429:
            return [], 0, "검색 요청이 많아요. 잠시 기다린 뒤 다시 검색해 주세요."

        if response.status_code == 403:
            return [], 0, "현재 도서 검색 서비스의 요청 제한에 걸렸어요. 잠시 후 다시 시도해 주세요."

        response.raise_for_status()
        data = response.json()

        books = []
        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            title = info.get("title", "").strip()

            if not title:
                continue

            authors = info.get("authors", ["저자 정보 없음"])
            images = info.get("imageLinks", {})
            cover = (
                images.get("thumbnail")
                or images.get("smallThumbnail")
            )

            if cover:
                cover = cover.replace("http://", "https://")

            books.append({
                "id": item.get("id", title),
                "title": unescape(title),
                "author": ", ".join(authors[:3]),
                "publisher": info.get("publisher", "출판사 정보 없음"),
                "year": info.get("publishedDate", ""),
                "description": info.get(
                    "description", "등록된 책 소개가 없습니다."
                ),
                "cover": cover,
                "link": info.get(
                    "infoLink",
                    "https://books.google.com/",
                ),
            })

        return books, data.get("totalItems", 0), None

    except requests.Timeout:
        return [], 0, "검색 시간이 초과됐어요. 잠시 후 다시 검색해 주세요."
    except requests.RequestException:
        return [], 0, "도서 검색 서버에 연결하지 못했어요. 잠시 후 다시 시도해 주세요."
    except ValueError:
        return [], 0, "검색 결과를 읽지 못했어요. 다시 시도해 주세요."


def show_books(books, prefix):
    if not books:
        st.info("검색 결과가 없어요. 다른 검색어를 입력해 보세요.")
        return

    for start in range(0, len(books), 3):
        cols = st.columns(3)

        for i, book in enumerate(books[start:start + 3]):
            with cols[i]:
                with st.container(border=True):
                    if book["cover"]:
                        st.image(
                            book["cover"],
                            use_container_width=True,
                        )
                    else:
                        st.markdown(
                            "<div style='height:180px;background:#eee8f8;"
                            "border-radius:12px;display:flex;"
                            "align-items:center;justify-content:center;"
                            "font-size:48px;'>📚</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown(f"**{book['title']}**")
                    st.caption(book["author"])
                    st.caption(
                        f"{book['publisher']} · {book['year']}"
                    )

                    with st.expander("책 소개"):
                        st.write(book["description"])

                    st.markdown(
                        f"[📖 도서 정보 확인]({book['link']})"
                    )

                    book_id = book["id"]
                    saved = book_id in st.session_state.career_favorites

                    if st.button(
                        "💗 찜 취소" if saved else "♡ 찜하기",
                        key=f"{prefix}_{book_id}",
                        use_container_width=True,
                    ):
                        if saved:
                            st.session_state.career_favorites.remove(book_id)
                        else:
                            st.session_state.career_favorites.append(book_id)
                        st.rerun()


st.markdown("""
<div class="hero">
    <h1>📚 꿈을 찾는 책장</h1>
    <p>한국어 도서를 중심으로 다양한 진로 분야의 책을 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

tab_search, tab_saved = st.tabs([
    "🔎 분야별 도서 검색",
    "💗 찜한 도서",
])

with tab_search:
    with st.form("career_search_form"):
        field = st.selectbox(
            "관심 분야",
            list(FIELDS.keys()),
            index=list(FIELDS.keys()).index(
                st.session_state.career_field
            ),
        )

        keyword = st.text_input(
            "추가 검색어 (선택)",
            placeholder="예: 청소년, 직업 탐색, 간호사",
            value=st.session_state.career_query,
        )

        submitted = st.form_submit_button(
            "🔎 한국어 도서 검색",
            use_container_width=True,
        )

    if submitted:
        st.session_state.career_field = field
        st.session_state.career_query = keyword
        st.session_state.career_page = 0

        with st.spinner("도서를 검색하고 있어요..."):
            books, total, error = search_books(field, keyword, 0)

        st.session_state.career_results = books
        st.session_state.career_total = total
        st.session_state.career_error = error

    current_field = st.session_state.career_field
    current_query = st.session_state.career_query
    current_page = st.session_state.career_page

    if st.session_state.career_results or st.session_state.career_total:
        st.subheader(f"📖 {current_field} 도서")

        if current_query:
            st.caption(f"추가 검색어: {current_query}")

        st.caption(
            f"검색 결과 약 {st.session_state.career_total:,}권 · "
            "페이지당 최대 40권"
        )

        show_books(st.session_state.career_results, "search")

        left, middle, right = st.columns([1, 2, 1])

        with left:
            if st.button(
                "⬅ 이전",
                disabled=current_page == 0,
                use_container_width=True,
            ):
                st.session_state.career_page -= 1
                with st.spinner("이전 도서를 불러오는 중..."):
                    books, total, error = search_books(
                        current_field,
                        current_query,
                        st.session_state.career_page,
                    )
                st.session_state.career_results = books
                st.session_state.career_total = total
                st.session_state.career_error = error
                st.rerun()

        with middle:
            st.markdown(
                f"<div style='text-align:center;padding:8px;'>"
                f"{current_page + 1} 페이지</div>",
                unsafe_allow_html=True,
            )

        with right:
            if st.button(
                "다음 ➡",
                disabled=(current_page + 1) * 40 >= st.session_state.career_total,
                use_container_width=True,
            ):
                st.session_state.career_page += 1
                with st.spinner("다음 도서를 불러오는 중..."):
                    books, total, error = search_books(
                        current_field,
                        current_query,
                        st.session_state.career_page,
                    )
                st.session_state.career_results = books
                st.session_state.career_total = total
                st.session_state.career_error = error
                st.rerun()

    elif st.session_state.get("career_error"):
        st.warning(st.session_state.career_error)
    else:
        st.info("관심 분야를 선택하고 검색 버튼을 눌러 주세요.")

    if st.session_state.get("career_error"):
        st.warning(st.session_state.career_error)

with tab_saved:
    st.subheader("💗 찜한 도서")

    if not st.session_state.career_favorites:
        st.info("아직 찜한 책이 없어요.")
    else:
        saved_books = [
            book
            for book in st.session_state.career_results
            if book["id"] in st.session_state.career_favorites
        ]
        show_books(saved_books, "saved")

st.divider()
st.caption(
    "도서 정보는 Google Books에서 가져옵니다. "
    "검색 결과 수와 표지 제공 여부는 서비스에 따라 달라질 수 있습니다."
)
