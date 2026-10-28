
import streamlit as st
import requests
from urllib.parse import quote

st.set_page_config(
    page_title="진로백과",
    page_icon="📚",
    layout="wide"
)

API_URL = "https://openlibrary.org/search.json"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff9f2, #f4f2ff);
}
.book-card {
    background: white;
    border: 1px solid #e8e1f3;
    border-radius: 18px;
    padding: 16px;
    min-height: 190px;
    box-shadow: 0 4px 14px rgba(70,50,100,.06);
}
.book-title {
    font-size: 17px;
    font-weight: 700;
    color: #37304b;
    margin: 10px 0 6px 0;
}
.book-info {
    color: #77718b;
    font-size: 13px;
}
.book-desc {
    color: #514d61;
    font-size: 13px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 진로백과")
st.caption("관심 분야의 책을 찾아 나에게 맞는 진로를 탐색해 보세요.")

# 분야별 검색어
FIELDS = {
    "IT·인공지능": (
        "subject:computers OR subject:programming "
        "OR subject:artificial_intelligence "
        "OR subject:machine_learning"
    ),
    "의학·생명과학": (
        "subject:biology OR subject:medicine "
        "OR subject:genetics OR subject:health"
    ),
    "심리·상담": (
        "subject:psychology OR subject:psychiatry "
        "OR subject:counseling"
    ),
    "법·정치·사회": (
        "subject:law OR subject:politics "
        "OR subject:sociology OR subject:social_sciences"
    ),
    "교육·언어": (
        "subject:education OR subject:linguistics "
        "OR subject:language OR subject:writing"
    ),
    "예술·디자인": (
        "subject:art OR subject:design "
        "OR subject:painting OR subject:photography"
    ),
    "환경·공학": (
        "subject:engineering OR subject:environment "
        "OR subject:ecology OR subject:technology"
    ),
    "요리·서비스·체육": (
        "subject:cooking OR subject:food "
        "OR subject:sports OR subject:fitness"
    ),
    "경제·경영": (
        "subject:economics OR subject:business "
        "OR subject:management OR subject:finance"
    )
}

ALL_QUERY = " OR ".join(
    f"({value})" for value in FIELDS.values()
)

# API 호출: 한 페이지에 최대 100권
@st.cache_data(ttl=3600, show_spinner=False)
def search_books(field, keyword, page):
    query = FIELDS.get(field, ALL_QUERY)

    if keyword.strip():
        query = f"({query}) AND ({keyword.strip()})"

    params = {
        "q": query,
        "limit": 100,
        "offset": page * 100,
        "lang": "ko",
        "fields": (
            "key,title,author_name,first_publish_year,"
            "cover_i,subject,edition_count"
        )
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=25,
        headers={
            "User-Agent": "CareerEncyclopedia/1.0 (school project)"
        }
    )
    response.raise_for_status()
    data = response.json()

    return data.get("docs", []), data.get("num_found", 0)


# 관심 도서
if "career_favorites" not in st.session_state:
    st.session_state.career_favorites = {}

if "book_page" not in st.session_state:
    st.session_state.book_page = 0

tab_search, tab_favorites = st.tabs(
    ["🔎 도서 찾기", "💜 관심 도서"]
)

with tab_search:
    st.subheader("나에게 맞는 진로 도서 찾기")

    selected_field = st.selectbox(
        "관심 분야",
        ["전체 분야"] + list(FIELDS.keys())
    )

    keyword = st.text_input(
        "책 제목 또는 저자 검색",
        placeholder="예: 인공지능, 심리학, biology"
    ).strip()

    # 분야나 검색어가 바뀌면 첫 페이지부터 검색
    current_search = (selected_field, keyword)

    if st.session_state.get("last_search") != current_search:
        st.session_state.book_page = 0
        st.session_state.last_search = current_search

    if st.button("🔎 도서 검색", use_container_width=True):
        st.session_state.book_page = 0

    page = st.session_state.book_page

    try:
        with st.spinner("도서 정보를 불러오는 중..."):
            books, total = search_books(
                selected_field,
                keyword,
                page
            )

        # 제목과 저자가 같은 결과 중복 제거
        unique_books = []
        seen = set()

        for book in books:
            title = book.get("title", "").strip()
            authors = book.get("author_name", [])
            author = ", ".join(authors) if authors else "저자 정보 없음"
            identity = (title.casefold(), author.casefold())

            if title and identity not in seen:
                seen.add(identity)
                unique_books.append(book)

        st.caption(
            f"검색 결과 약 {total:,}건 · "
            f"{page + 1}페이지 · 현재 {len(unique_books)}권"
        )

        if not unique_books:
            st.info(
                "검색 결과가 없어요. 다른 검색어나 분야를 선택해 보세요."
            )

        for start in range(0, len(unique_books), 3):
            cols = st.columns(3)

            for col, book in zip(
                cols, unique_books[start:start + 3]
            ):
                title = book.get("title", "제목 없음")
                authors = book.get("author_name", [])
                author = (
                    ", ".join(authors)
                    if authors else "저자 정보 없음"
                )
                year = book.get("first_publish_year")
                cover_id = book.get("cover_i")
                book_key = book.get("key", "")
                subjects = book.get("subject", [])
                description = (
                    ", ".join(subjects[:3])
                    if subjects else "상세 설명이 등록되지 않은 도서입니다."
                )

                # 도서 식별용 키
                identity = book_key or f"{title}|{author}"

                with col:
                    st.markdown('<div class="book-card">',
                                unsafe_allow_html=True)

                    if cover_id:
                        st.image(
                            f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg",
                            width=150
                        )
                    else:
                        st.markdown("📖 표지 이미지 없음")

                    st.markdown(
                        f'<div class="book-title">{title}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="book-info">저자: {author}</div>',
                        unsafe_allow_html=True
                    )

                    if year:
                        st.caption(f"최초 출판 연도: {year}")

                    st.markdown(
                        f'<div class="book-desc">{description}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                    saved = identity in st.session_state.career_favorites

                    if st.button(
                        "💜 저장 해제" if saved else "♡ 관심 도서 저장",
                        key=f"fav_{page}_{start}_{identity}",
                        use_container_width=True
                    ):
                        if saved:
                            del st.session_state.career_favorites[identity]
                        else:
                            st.session_state.career_favorites[identity] = {
                                "title": title,
                                "author": author,
                                "field": selected_field,
                                "year": year,
                                "key": book_key,
                                "cover_id": cover_id,
                                "description": description
                            }
                        st.rerun()

                    if book_key:
                        book_url = "https://openlibrary.org" + book_key
                    else:
                        book_url = (
                            "https://openlibrary.org/search?q="
                            + quote(title)
                        )

                    st.link_button(
                        "🔎 책 정보 보기",
                        book_url,
                        use_container_width=True
                    )

        st.divider()

        previous_col, page_col, next_col = st.columns([1, 2, 1])

        with previous_col:
            if st.button(
                "⬅️ 이전",
                disabled=(page == 0),
                use_container_width=True
            ):
                st.session_state.book_page -= 1
                st.rerun()

        with page_col:
            st.markdown(
                f"<div style='text-align:center;padding:8px'>"
                f"{page + 1} 페이지</div>",
                unsafe_allow_html=True
            )

        with next_col:
            has_next = (page + 1) * 100 < total

            if st.button(
                "다음 ➡️",
                disabled=not has_next,
                use_container_width=True
            ):
                st.session_state.book_page += 1
                st.rerun()

    except requests.RequestException:
        st.error(
            "도서 API에 연결하지 못했어요. "
            "인터넷 연결을 확인하고 잠시 후 다시 시도해 주세요."
        )
    except (ValueError, KeyError):
        st.error("도서 정보를 처리하는 중 문제가 발생했어요.")

with tab_favorites:
    st.subheader("💜 관심 도서 목록")

    favorites = list(st.session_state.career_favorites.items())

    if not favorites:
        st.info(
            "아직 저장한 책이 없어요. "
            "도서 찾기에서 관심 도서를 저장해 보세요."
        )

    for identity, book in favorites:
        with st.container(border=True):
            cover_id = book.get("cover_id")

            if cover_id:
                st.image(
                    f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg",
                    width=100
                )

            st.markdown(f"### 📚 {book['title']}")
            st.write(f"저자: {book['author']}")
            st.write(f"분야: {book['field']}")

            if book.get("year"):
                st.write(f"최초 출판 연도: {book['year']}")

            st.write(book["description"])

            book_key = book.get("key", "")
            if book_key:
                st.link_button(
                    "책 정보 보기",
                    "https://openlibrary.org" + book_key
                )

            if st.button(
                "저장 취소",
                key=f"remove_{identity}"
            ):
                del st.session_state.career_favorites[identity]
                st.rerun()

st.divider()
st.caption(
    "도서 정보 제공: Open Library API · "
    "검색 결과와 표지 제공 여부는 데이터베이스에 따라 달라질 수 있습니다."
)
