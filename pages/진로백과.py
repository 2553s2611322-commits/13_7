
import streamlit as st
import requests

st.set_page_config(
    page_title="진로백과 | 꿈을 찾는 책장",
    page_icon="📚",
    layout="wide",
)

FIELDS = {
    "IT·인공지능": "Computers",
    "심리": "Psychology",
    "과학·연구": "Science",
    "경제·금융": "Economics",
    "경영·기업": "Business",
    "사회·역사": "History",
    "사회·법": "Law",
    "디자인·예술": "Design",
    "교육·상담": "Education",
    "환경·생태": "Nature",
    "진로·직업": "Careers",
    "여행·관광": "Travel",
    "자기계발": "Self-help",
    "의학·보건": "Medicine",
    "수학": "Mathematics",
    "공학": "Engineering",
    "문학·글쓰기": "Literature",
    "요리·식품": "Cooking",
    "스포츠": "Sports",
    "철학": "Philosophy",
}

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
    background: linear-gradient(120deg, #e3eafe, #f8e8ef);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 22px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

if "career_favorites" not in st.session_state:
    st.session_state.career_favorites = []

@st.cache_data(ttl=21600, show_spinner=False)
def search_books(subject, keyword, page):
    """검색 결과를 저장해 반복적인 API 요청을 줄입니다."""
    query = f"subject:{subject}"
    if keyword.strip():
        query += f' AND "{keyword.strip()}"'

    try:
        response = requests.get(
            "https://openlibrary.org/search.json",
            params={
                "q": query,
                "limit": 40,
                "offset": page * 40,
                "fields": (
                    "key,title,author_name,first_publish_year,"
                    "cover_i,isbn,subject"
                ),
            },
            timeout=15,
            headers={"User-Agent": "CareerBookShelf/1.0"},
        )
        response.raise_for_status()
        data = response.json()
        books = []

        for item in data.get("docs", []):
            title = item.get("title")
            key = item.get("key")
            if not title or not key:
                continue

            authors = item.get("author_name") or ["저자 정보 없음"]
            books.append({
                "key": key,
                "title": title,
                "author": ", ".join(authors[:2]),
                "year": item.get("first_publish_year"),
                "cover": item.get("cover_i"),
                "isbn": (item.get("isbn") or [""])[0],
                "subjects": item.get("subject") or [],
            })

        return books, data.get("numFound", 0), None

    except requests.Timeout:
        return [], 0, "검색 서버 응답 시간이 초과됐어요. 잠시 후 다시 시도해 주세요."
    except requests.RequestException:
        return [], 0, "도서 검색 서버에 연결하지 못했어요. 잠시 후 다시 시도해 주세요."
    except ValueError:
        return [], 0, "검색 결과를 읽지 못했어요. 잠시 후 다시 시도해 주세요."


def show_books(books, section):
    if not books:
        st.info("표시할 도서가 없어요. 검색어를 바꾸거나 다른 분야를 선택해 보세요.")
        return

    for start in range(0, len(books), 3):
        columns = st.columns(3)

        for index, book in enumerate(books[start:start + 3]):
            with columns[index]:
                with st.container(border=True):
                    cover_id = book.get("cover")

                    if cover_id:
                        st.image(
                            f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg",
                            use_container_width=True,
                        )
                    else:
                        st.markdown(
                            "<div style='background:#eee8f8;height:180px;"
                            "display:flex;align-items:center;"
                            "justify-content:center;border-radius:10px;"
                            "font-size:48px;'>📚</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown(f"**{book['title']}**")
                    st.caption(book["author"])

                    if book.get("year"):
                        st.caption(f"출판 연도: {book['year']}")

                    st.markdown(
                        f"[도서 정보 보기](https://openlibrary.org{book['key']})"
                    )

                    favorite_id = book["key"]
                    is_saved = favorite_id in st.session_state.career_favorites

                    if st.button(
                        "💗 찜 취소" if is_saved else "♡ 찜하기",
                        key=f"{section}_{favorite_id}",
                        use_container_width=True,
                    ):
                        if is_saved:
                            st.session_state.career_favorites.remove(favorite_id)
                        else:
                            st.session_state.career_favorites.append(favorite_id)
                        st.rerun()


st.markdown("""
<div class="hero">
    <h1>📚 꿈을 찾는 책장</h1>
    <p>관심 있는 분야의 책을 읽으며 나에게 맞는 진로를 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

tab_search, tab_favorites = st.tabs(["🔎 분야별 도서 검색", "💗 찜한 도서"])

with tab_search:
    field = st.selectbox("관심 분야", list(FIELDS.keys()))
    keyword = st.text_input(
        "검색어 (선택)",
        placeholder="예: 인공지능, 상담, 환경, 저자 이름",
    )

    if "career_page" not in st.session_state:
        st.session_state.career_page = 0

    if st.button("🔎 책 검색하기", type="primary", use_container_width=True):
        st.session_state.career_page = 0
        st.session_state.career_last_field = field
        st.session_state.career_last_keyword = keyword

    chosen_field = st.session_state.get("career_last_field", field)
    chosen_keyword = st.session_state.get("career_last_keyword", keyword)

    st.subheader(f"📖 {chosen_field} 분야 도서")

    with st.spinner("도서를 검색하고 있어요..."):
        books, total, error = search_books(
            FIELDS[chosen_field],
            chosen_keyword,
            st.session_state.career_page,
        )

    if error:
        st.warning(error)
    else:
        st.caption(f"검색 결과 약 {total:,}권 · 한 페이지에 최대 40권")

        if total > 0:
            show_books(books, "search")

            left, middle, right = st.columns([1, 2, 1])

            with left:
                if st.button(
                    "⬅ 이전",
                    disabled=st.session_state.career_page == 0,
                    use_container_width=True,
                ):
                    st.session_state.career_page -= 1
                    st.rerun()

            with middle:
                st.markdown(
                    f"<div style='text-align:center;padding:8px;'>"
                    f"{st.session_state.career_page + 1}페이지</div>",
                    unsafe_allow_html=True,
                )

            with right:
                if st.button(
                    "다음 ➡",
                    disabled=(st.session_state.career_page + 1) * 40 >= total,
                    use_container_width=True,
                ):
                    st.session_state.career_page += 1
                    st.rerun()
        else:
            st.info("검색 결과가 없어요. 다른 분야나 검색어를 선택해 보세요.")

with tab_favorites:
    st.subheader("💗 찜한 도서")

    if not st.session_state.career_favorites:
        st.info("아직 찜한 책이 없어요. 분야별 검색에서 마음에 드는 책을 찜해 보세요.")
    else:
        st.write("찜한 책의 정보 링크를 확인해 보세요.")
        st.caption("찜 목록은 현재 앱 세션에 저장됩니다.")
        st.write("찜한 도서 목록을 보려면 검색 결과에서 해당 책을 다시 확인할 수 있어요.")

st.divider()
st.caption(
    "도서 데이터와 표지는 Open Library에서 제공합니다. "
    "검색 결과 수는 데이터베이스에 따라 달라질 수 있으며, 모든 책에 표지가 있는 것은 아닙니다."
)
