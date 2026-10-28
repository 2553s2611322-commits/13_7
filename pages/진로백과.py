
import re
import requests
import streamlit as st
from html import unescape

st.set_page_config(
    page_title="진로백과",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff9f2, #f4f2ff);
}
.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
.book-card {
    background: white;
    border: 1px solid #e8e1f3;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    min-height: 310px;
    box-shadow: 0 4px 12px rgba(70, 50, 100, 0.05);
}
.book-title {
    font-size: 17px;
    font-weight: 700;
    color: #403451;
    margin-bottom: 8px;
}
.book-info {
    font-size: 13px;
    color: #777080;
    margin-bottom: 8px;
}
.book-desc {
    font-size: 13px;
    color: #514b5b;
    line-height: 1.5;
}
.stButton button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 진로백과")
st.caption("관심 분야의 책을 찾아 나에게 맞는 진로를 탐색해 보세요.")

FIELDS = {
    "IT · 인공지능": ["인공지능", "컴퓨터 프로그래밍", "코딩"],
    "의료 · 생명과학": ["의학", "생명과학", "간호학"],
    "심리 · 상담": ["심리학", "상담심리", "청소년 심리"],
    "법 · 정치 · 사회": ["법학", "정치학", "사회학"],
    "교육 · 언어": ["교육학", "언어학", "국어교육"],
    "예술 · 디자인": ["디자인", "미술", "시각디자인"],
    "환경 · 공학": ["환경공학", "공학", "기후변화"],
    "경제 · 경영": ["경제학", "경영학", "마케팅"],
    "요리 · 서비스 · 스포츠": ["요리", "호텔관광", "스포츠과학"],
}

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "results" not in st.session_state:
    st.session_state.results = []

if "last_search" not in st.session_state:
    st.session_state.last_search = ""

def has_korean(text):
    return bool(re.search(r"[가-힣]", text or ""))

def clean_text(text):
    text = re.sub(r"<[^>]*>", "", text or "")
    return unescape(text).strip()

@st.cache_data(ttl=3600, show_spinner=False)
def search_google_books(search_term, max_books=100):
    """Google Books에서 한국어 도서 정보를 검색한다."""
    url = "https://www.googleapis.com/books/v1/volumes"
    found = []
    seen = set()

    # Google Books는 한 요청에 최대 40개까지 반환한다.
    for start in range(0, 120, 40):
        params = {
            "q": search_term,
            "langRestrict": "ko",
            "printType": "books",
            "maxResults": 40,
            "startIndex": start,
            "orderBy": "relevance",
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            if not found:
                raise RuntimeError(
                    "도서 검색 서버에 연결하지 못했어요. "
                    "잠시 후 다시 시도해 주세요."
                )
            break
        except ValueError:
            if not found:
                raise RuntimeError(
                    "도서 검색 결과를 읽지 못했어요. 다시 시도해 주세요."
                )
            break

        items = data.get("items", [])
        if not items:
            break

        for item in items:
            info = item.get("volumeInfo", {})
            title = clean_text(info.get("title", ""))

            # 실제 검색 결과 중 한국어 제목이 있는 책만 표시
            if not title or not has_korean(title):
                continue

            if info.get("language") not in (None, "ko"):
                continue

            book_id = item.get("id", "")
            isbn = ""
            for identifier in info.get("industryIdentifiers", []):
                if identifier.get("type") in ("ISBN_13", "ISBN_10"):
                    isbn = identifier.get("identifier", "")
                    break

            unique_key = isbn or book_id or title
            if unique_key in seen:
                continue
            seen.add(unique_key)

            image = info.get("imageLinks", {}).get("thumbnail", "")
            if image:
                image = image.replace("http://", "https://")

            description = clean_text(info.get("description", ""))
            if len(description) > 220:
                description = description[:220] + "..."

            found.append({
                "id": book_id or unique_key,
                "title": title,
                "authors": ", ".join(info.get("authors", [])) or "저자 정보 없음",
                "publisher": info.get("publisher", "출판사 정보 없음"),
                "published": info.get("publishedDate", ""),
                "description": description or "책 소개가 등록되어 있지 않습니다.",
                "image": image,
                "link": info.get(
                    "infoLink",
                    "https://books.google.com/"
                ),
                "isbn": isbn,
            })

            if len(found) >= max_books:
                return found

        if len(items) < 40:
            break

    return found


def show_book(book, index, prefix):
    with st.container(border=True):
        left, right = st.columns([1, 2])

        with left:
            if book.get("image"):
                st.image(book["image"], use_container_width=True)
            else:
                st.markdown("📖 **표지 이미지 없음**")

        with right:
            st.markdown(f"**{book['title']}**")
            st.caption(f"저자: {book['authors']}")
            st.caption(f"출판사: {book['publisher']}")

            if book.get("published"):
                st.caption(f"출판일: {book['published']}")

            st.write(book["description"])

            st.link_button(
                "도서 정보 보기",
                book["link"],
                use_container_width=True
            )

            book_id = book["id"]
            is_saved = book_id in st.session_state.favorites

            if is_saved:
                if st.button(
                    "💜 찜 목록에서 삭제",
                    key=f"{prefix}_remove_{index}_{book_id}",
                    use_container_width=True
                ):
                    del st.session_state.favorites[book_id]
                    st.rerun()
            else:
                if st.button(
                    "🤍 찜하기",
                    key=f"{prefix}_save_{index}_{book_id}",
                    use_container_width=True
                ):
                    st.session_state.favorites[book_id] = book
                    st.rerun()


search_tab, favorite_tab = st.tabs(["🔎 분야별 책 찾기", "💜 찜한 책"])

with search_tab:
    selected_field = st.selectbox(
        "진로 분야를 선택하세요",
        list(FIELDS.keys())
    )

    keyword = st.text_input(
        "검색어 (선택)",
        placeholder="예: 인공지능, 간호사, 심리학"
    )

    st.caption("검색 결과는 실제 도서 데이터에 따라 달라질 수 있어요.")

    if st.button("📚 책 검색하기", type="primary", use_container_width=True):
        st.session_state.results = []
        st.session_state.last_search = ""

        try:
            with st.spinner("한국어 도서를 찾고 있어요..."):
                if keyword.strip():
                    # 입력한 검색어로 한국어 도서를 검색
                    results = search_google_books(keyword.strip(), 100)
                    search_label = keyword.strip()
                else:
                    # 분야별 여러 검색어로 검색한 뒤 중복 제거
                    results = []
                    seen_ids = set()

                    for term in FIELDS[selected_field]:
                        remaining = 100 - len(results)
                        if remaining <= 0:
                            break

                        books = search_google_books(term, remaining)
                        for book in books:
                            if book["id"] not in seen_ids:
                                seen_ids.add(book["id"])
                                results.append(book)

                            if len(results) >= 100:
                                break

                    search_label = selected_field

                st.session_state.results = results
                st.session_state.last_search = search_label

        except RuntimeError as error:
            st.error(str(error))
        except Exception:
            st.error(
                "검색 중 예상하지 못한 문제가 생겼어요. "
                "잠시 후 다시 시도해 주세요."
            )

    results = st.session_state.results

    if results:
        st.success(f"검색 결과 {len(results)}권")
        for i in range(0, len(results), 2):
            cols = st.columns(2)
            for col, book_index in zip(cols, range(i, min(i + 2, len(results)))):
                with col:
                    show_book(results[book_index], book_index, "search")

    elif st.session_state.last_search:
        st.info(
            "조건에 맞는 한국어 책을 찾지 못했어요. "
            "다른 검색어를 입력해 보세요."
        )
    else:
        st.info(
            "분야를 선택하고 '책 검색하기'를 눌러 주세요. "
            "검색어를 직접 입력해도 돼요."
        )

with favorite_tab:
    favorites = list(st.session_state.favorites.values())

    if not favorites:
        st.info("아직 찜한 책이 없어요. 마음에 드는 책을 찜해 보세요!")
    else:
        st.write(f"💜 찜한 책 {len(favorites)}권")

        for i in range(0, len(favorites), 2):
            cols = st.columns(2)
            for col, book_index in zip(cols, range(i, min(i + 2, len(favorites)))):
                with col:
                    show_book(favorites[book_index], book_index, "favorite")
