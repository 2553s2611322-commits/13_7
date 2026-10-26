
import streamlit as st
import html
from urllib.parse import quote_plus

st.title("📚 진로백과")
st.caption("관심 분야의 책을 찾아보며 나에게 맞는 진로를 탐색해 보세요.")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff9f2, #f4f2ff);
}
.book-card {
    background: white;
    border: 1px solid #e8e1f3;
    border-radius: 18px;
    padding: 15px;
    min-height: 370px;
    box-shadow: 0 4px 14px rgba(70, 50, 100, 0.07);
}
.cover {
    height: 190px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    background: #f8f4ff;
    border-radius: 12px;
}
.cover img {
    max-height: 190px;
    max-width: 100%;
    object-fit: contain;
}
.book-title {
    font-size: 17px;
    font-weight: 700;
    color: #37304b;
    margin-top: 12px;
}
.book-author {
    font-size: 13px;
    color: #77718b;
    margin-top: 5px;
}
.book-desc {
    font-size: 13px;
    color: #514d61;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# 앱 내부 데이터만 검색하므로 도서 검색 API 호출이 없습니다.
BOOKS = [
    ("AI 최강의 수업", "김진형", "IT·인공지능", "인공지능의 핵심 개념과 활용"),
    ("혼자 공부하는 머신러닝+딥러닝", "박해선", "IT·인공지능", "머신러닝과 딥러닝 입문"),
    ("Do it! 점프 투 파이썬", "박응용", "IT·인공지능", "파이썬 프로그래밍 입문"),
    ("클린 코드", "로버트 C. 마틴", "IT·인공지능", "읽기 쉬운 코드를 작성하는 방법"),
    ("밑바닥부터 시작하는 딥러닝", "사이토 고키", "IT·인공지능", "딥러닝의 작동 원리"),
    ("이기적 유전자", "리처드 도킨스", "의학·생명과학", "유전자와 진화"),
    ("랩 걸", "호프 자런", "의학·생명과학", "식물학자의 연구와 성장"),
    ("생명이란 무엇인가", "폴 너스", "의학·생명과학", "생명의 원리"),
    ("코스모스", "칼 세이건", "의학·생명과학", "우주와 과학의 역사"),
    ("세포의 노래", "싯다르타 무케르지", "의학·생명과학", "세포 연구의 역사"),
    ("생각에 관한 생각", "대니얼 카너먼", "심리·상담", "인간의 판단과 의사결정"),
    ("미움받을 용기", "기시미 이치로·고가 후미타케", "심리·상담", "아들러 심리학"),
    ("설득의 심리학", "로버트 치알디니", "심리·상담", "설득과 행동의 원리"),
    ("콰이어트", "수전 케인", "심리·상담", "내향적인 성향의 이해"),
    ("몰입", "황농문", "심리·상담", "집중과 몰입"),
    ("정의란 무엇인가", "마이클 샌델", "법·정치·사회", "정의와 공정성"),
    ("팩트풀니스", "한스 로슬링 외", "법·정치·사회", "데이터로 이해하는 세계"),
    ("사피엔스", "유발 하라리", "법·정치·사회", "인류의 역사"),
    ("공정하다는 착각", "마이클 샌델", "법·정치·사회", "능력주의와 공정성"),
    ("왜 세계의 절반은 굶주리는가?", "장 지글러", "법·정치·사회", "기아 문제와 사회 구조"),
    ("공부머리 독서법", "최승필", "교육·언어", "독서를 활용한 학습"),
    ("완벽한 공부법", "고영성·신영준", "교육·언어", "학습 습관과 공부 방법"),
    ("유시민의 글쓰기 특강", "유시민", "교육·언어", "논리적인 글쓰기"),
    ("언어의 온도", "이기주", "교육·언어", "말과 글의 영향"),
    ("말의 품격", "이기주", "교육·언어", "소통과 말하기"),
    ("방구석 미술관", "조원재", "예술·디자인", "미술 작품과 예술가"),
    ("디자인의 디자인", "하라 켄야", "예술·디자인", "디자인의 본질"),
    ("미술관에 간 화학자", "전창림", "예술·디자인", "미술과 과학의 만남"),
    ("생각의 탄생", "로버트 루트번스타인·미셸 루트번스타인", "예술·디자인", "창조적 사고"),
    ("침묵의 봄", "레이첼 카슨", "환경·공학", "환경오염과 생태계"),
    ("거의 모든 것의 역사", "빌 브라이슨", "환경·공학", "과학의 여러 분야"),
    ("과학 콘서트", "정재승", "환경·공학", "일상 속 과학"),
    ("사소한 것들의 과학", "마크 미오도닉", "환경·공학", "재료와 공학"),
    ("음식의 언어", "댄 주래프스키", "요리·서비스·체육", "음식과 문화"),
    ("운동화 신은 뇌", "존 레이티·에릭 헤이거먼", "요리·서비스·체육", "운동과 뇌의 관계"),
    ("아웃라이어", "말콤 글래드웰", "요리·서비스·체육", "성공에 영향을 미치는 조건"),
    ("경제학 콘서트", "팀 하포드", "경제·경영", "일상생활 속 경제"),
    ("넛지", "리처드 탈러·캐스 선스타인", "경제·경영", "선택과 행동경제학"),
    ("린 스타트업", "에릭 리스", "경제·경영", "아이디어와 사업 개발"),
    ("원칙", "레이 달리오", "경제·경영", "의사결정과 조직 운영"),
]

FIELDS = sorted({book[2] for book in BOOKS})

if "career_favorites" not in st.session_state:
    st.session_state.career_favorites = []

tab_search, tab_favorites = st.tabs(["🔎 도서 찾기", "💜 관심 도서"])

with tab_search:
    selected_field = st.selectbox("관심 분야", ["전체 분야"] + FIELDS)
    query = st.text_input("책 제목 또는 저자 검색", placeholder="예: 인공지능, 심리학")

    results = []
    for book in BOOKS:
        title, author, field, desc = book
        if selected_field != "전체 분야" and field != selected_field:
            continue
        if query.strip() and query.strip().casefold() not in (
            title + " " + author + " " + field + " " + desc
        ).casefold():
            continue
        results.append(book)

    st.caption(f"검색 결과 {len(results)}권")

    if not results:
        st.info("검색 결과가 없어요. 다른 검색어나 분야를 선택해 보세요.")

    for start in range(0, len(results), 3):
        cols = st.columns(3)
        for col, book in zip(cols, results[start:start + 3]):
            title, author, field, desc = book

            # 제목으로 표지를 조회합니다. 검색 API를 호출하지 않습니다.
            cover_url = (
                "https://covers.openlibrary.org/b/title/"
                + quote_plus(title)
                + "-M.jpg?default=false"
            )
            safe_title = html.escape(title)
            safe_author = html.escape(author)
            safe_field = html.escape(field)
            safe_desc = html.escape(desc)

            with col:
                st.markdown(
                    f"""
                    <div class="book-card">
                      <div class="cover">
                        <img src="{cover_url}" alt="{safe_title} 표지">
                      </div>
                      <div style="color:#9076ba;font-size:12px;margin-top:10px">
                        📖 {safe_field}
                      </div>
                      <div class="book-title">{safe_title}</div>
                      <div class="book-author">저자: {safe_author}</div>
                      <div class="book-desc">{safe_desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                key = title + "|" + author
                saved = key in st.session_state.career_favorites

                if st.button(
                    "💜 저장 해제" if saved else "♡ 관심 도서 저장",
                    key="favorite_" + str(start) + "_" + key,
                    use_container_width=True,
                ):
                    if saved:
                        st.session_state.career_favorites.remove(key)
                    else:
                        st.session_state.career_favorites.append(key)
                    st.rerun()

                st.link_button(
                    "🔗 책 정보 보기",
                    "https://www.google.com/search?q="
                    + quote_plus(title + " " + author + " 책"),
                    use_container_width=True,
                )

with tab_favorites:
    st.subheader("💜 관심 도서 목록")
    saved_books = [
        book for book in BOOKS
        if book[0] + "|" + book[1] in st.session_state.career_favorites
    ]

    if not saved_books:
        st.info("아직 저장한 책이 없어요. 도서 찾기에서 관심 도서를 저장해 보세요.")
    else:
        for title, author, field, desc in saved_books:
            with st.container(border=True):
                st.markdown(f"### 📚 {title}")
                st.write(f"저자: {author} · 분야: {field}")
                st.write(desc)

                if st.button("저장 취소", key="remove_" + title + author):
                    st.session_state.career_favorites.remove(title + "|" + author)
                    st.rerun()

st.divider()
st.caption(
    "도서 검색은 앱 내부 목록에서 실행됩니다. "
    "표지는 외부 이미지 서비스에 등록된 경우에만 표시될 수 있습니다."
)
