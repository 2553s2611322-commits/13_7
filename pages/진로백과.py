
import streamlit as st

st.title("📚 진로백과")
st.caption("관심 있는 분야의 책을 찾아보고 나에게 맞는 진로를 탐색해 보세요.")

# 외부 API 없이 작동하는 도서 목록
# 검색과 분야 필터는 로컬 데이터에서 처리합니다.
BOOKS = [
    # IT · 인공지능
    {"title": "AI 시대, 문과생은 이렇게 일합니다", "author": "노구치 류타", "field": "IT·인공지능", "desc": "AI 시대에 필요한 역량과 일하는 방법을 살펴보는 책"},
    {"title": "AI 최강의 수업", "author": "김진형", "field": "IT·인공지능", "desc": "인공지능의 핵심 개념과 활용을 이해하는 책"},
    {"title": "혼자 공부하는 머신러닝+딥러닝", "author": "박해선", "field": "IT·인공지능", "desc": "머신러닝과 딥러닝의 기초를 배우는 책"},
    {"title": "밑바닥부터 시작하는 딥러닝", "author": "사이토 고키", "field": "IT·인공지능", "desc": "딥러닝의 작동 원리를 단계별로 알아보는 책"},
    {"title": "클린 코드", "author": "로버트 C. 마틴", "field": "IT·인공지능", "desc": "읽기 쉽고 유지하기 좋은 코드를 배우는 책"},
    {"title": "Do it! 점프 투 파이썬", "author": "박응용", "field": "IT·인공지능", "desc": "파이썬 프로그래밍 입문서"},
    {"title": "처음 배우는 데이터 과학", "author": "관련 분야 입문서", "field": "IT·인공지능", "desc": "데이터를 분석하고 활용하는 분야를 알아보기"},
    {"title": "세상을 바꾸는 데이터 과학", "author": "데이터 과학 분야", "field": "IT·인공지능", "desc": "데이터 분석과 사회의 변화를 살펴보기"},

    # 의학 · 생명과학
    {"title": "이기적 유전자", "author": "리처드 도킨스", "field": "의학·생명과학", "desc": "진화와 유전자를 새로운 관점에서 이해하는 책"},
    {"title": "코스모스", "author": "칼 세이건", "field": "의학·생명과학", "desc": "과학과 우주를 폭넓게 탐구하는 책"},
    {"title": "아내를 모자로 착각한 남자", "author": "올리버 색스", "field": "의학·생명과학", "desc": "신경학 사례를 통해 뇌와 인간을 살펴보는 책"},
    {"title": "랩 걸", "author": "호프 자런", "field": "의학·생명과학", "desc": "식물학자의 연구와 성장 이야기"},
    {"title": "생명이란 무엇인가", "author": "폴 너스", "field": "의학·생명과학", "desc": "생명의 원리를 이해하는 과학 교양서"},
    {"title": "침묵의 봄", "author": "레이첼 카슨", "field": "의학·생명과학", "desc": "환경과 생태계의 관계를 살펴보는 책"},
    {"title": "세포의 노래", "author": "싯다르타 무케르지", "field": "의학·생명과학", "desc": "세포 연구의 역사와 생명과학을 알아보는 책"},
    {"title": "유전자의 내밀한 역사", "author": "싯다르타 무케르지", "field": "의학·생명과학", "desc": "유전학의 발전과 윤리적 쟁점을 살펴보는 책"},

    # 심리 · 상담
    {"title": "생각에 관한 생각", "author": "대니얼 카너먼", "field": "심리·상담", "desc": "인간의 판단과 의사결정 과정을 이해하는 책"},
    {"title": "미움받을 용기", "author": "기시미 이치로·고가 후미타케", "field": "심리·상담", "desc": "아들러 심리학을 대화 형식으로 소개하는 책"},
    {"title": "죽음의 수용소에서", "author": "빅터 프랭클", "field": "심리·상담", "desc": "삶의 의미와 인간의 내면을 탐구하는 책"},
    {"title": "감정은 어떻게 만들어지는가", "author": "리사 펠드먼 배럿", "field": "심리·상담", "desc": "감정과 뇌의 관계를 살펴보는 책"},
    {"title": "설득의 심리학", "author": "로버트 치알디니", "field": "심리·상담", "desc": "사람의 판단과 설득 원리를 이해하는 책"},
    {"title": "아직도 가야 할 길", "author": "M. 스캇 펙", "field": "심리·상담", "desc": "성장과 책임, 인간관계를 생각해 보는 책"},
    {"title": "콰이어트", "author": "수전 케인", "field": "심리·상담", "desc": "내향적인 성향과 사회의 관계를 다루는 책"},
    {"title": "몰입", "author": "황농문", "field": "심리·상담", "desc": "집중과 몰입의 원리를 살펴보는 책"},

    # 경제 · 경영
    {"title": "부자 아빠 가난한 아빠", "author": "로버트 기요사키", "field": "경제·경영", "desc": "돈과 자산에 대한 관점을 소개하는 책"},
    {"title": "넛지", "author": "리처드 탈러·캐스 선스타인", "field": "경제·경영", "desc": "선택과 행동경제학을 이해하는 책"},
    {"title": "죽은 경제학자의 살아있는 아이디어", "author": "토드 부크홀츠", "field": "경제·경영", "desc": "경제학자들의 주요 이론을 살펴보는 책"},
    {"title": "경제학 콘서트", "author": "팀 하포드", "field": "경제·경영", "desc": "일상생활 속 경제 원리를 설명하는 책"},
    {"title": "생각의 지도", "author": "리처드 니스벳", "field": "경제·경영", "desc": "문화에 따른 사고방식의 차이를 살펴보는 책"},
    {"title": "원칙", "author": "레이 달리오", "field": "경제·경영", "desc": "의사결정과 조직 운영의 원칙을 다루는 책"},
    {"title": "린 스타트업", "author": "에릭 리스", "field": "경제·경영", "desc": "아이디어를 실험하고 사업을 발전시키는 방법"},
    {"title": "마케팅 불변의 법칙", "author": "알 리스·잭 트라우트", "field": "경제·경영", "desc": "브랜드와 마케팅의 기본 원리를 소개하는 책"},

    # 법 · 정치 · 사회
    {"title": "정의란 무엇인가", "author": "마이클 샌델", "field": "법·정치·사회", "desc": "정의와 공정성에 관한 여러 관점을 탐구하는 책"},
    {"title": "왜 세계의 절반은 굶주리는가?", "author": "장 지글러", "field": "법·정치·사회", "desc": "기아 문제의 원인과 사회 구조를 살펴보는 책"},
    {"title": "팩트풀니스", "author": "한스 로슬링 외", "field": "법·정치·사회", "desc": "세계의 실제 모습을 데이터로 이해하는 책"},
    {"title": "사피엔스", "author": "유발 하라리", "field": "법·정치·사회", "desc": "인류의 역사와 사회의 변화를 살펴보는 책"},
    {"title": "공정하다는 착각", "author": "마이클 샌델", "field": "법·정치·사회", "desc": "능력주의와 공정성에 대해 질문하는 책"},
    {"title": "침묵의 봄", "author": "레이첼 카슨", "field": "법·정치·사회", "desc": "환경 문제와 사회적 책임을 생각해 보는 책"},
    {"title": "감시와 처벌", "author": "미셸 푸코", "field": "법·정치·사회", "desc": "권력과 사회 제도의 관계를 분석하는 책"},
    {"title": "불평등의 대가", "author": "조지프 스티글리츠", "field": "법·정치·사회", "desc": "경제적 불평등의 원인과 영향을 다루는 책"},

    # 교육 · 언어
    {"title": "왜 공부하는가", "author": "마스다 무네아키", "field": "교육·언어", "desc": "배움의 의미와 공부하는 태도를 생각하는 책"},
    {"title": "공부머리 독서법", "author": "최승필", "field": "교육·언어", "desc": "독서를 활용한 학습 방법을 소개하는 책"},
    {"title": "완벽한 공부법", "author": "고영성·신영준", "field": "교육·언어", "desc": "학습과 습관을 개선하는 방법을 다루는 책"},
    {"title": "메타인지 학습법", "author": "리사 손", "field": "교육·언어", "desc": "자신의 학습 과정을 점검하는 방법을 소개하는 책"},
    {"title": "언어의 온도", "author": "이기주", "field": "교육·언어", "desc": "말과 글이 사람에게 미치는 영향을 생각하는 책"},
    {"title": "유시민의 글쓰기 특강", "author": "유시민", "field": "교육·언어", "desc": "논리적인 글쓰기 방법을 설명하는 책"},
    {"title": "말의 품격", "author": "이기주", "field": "교육·언어", "desc": "말하기와 소통의 태도를 돌아보는 책"},
    {"title": "어른의 문해력", "author": "김선영", "field": "교육·언어", "desc": "읽고 이해하고 표현하는 능력을 키우는 책"},

    # 예술 · 디자인
    {"title": "미술관에 간 화학자", "author": "전창림", "field": "예술·디자인", "desc": "미술 작품을 과학의 관점에서 살펴보는 책"},
    {"title": "방구석 미술관", "author": "조원재", "field": "예술·디자인", "desc": "미술 작품과 예술가의 이야기를 소개하는 책"},
    {"title": "디자인의 디자인", "author": "하라 켄야", "field": "예술·디자인", "desc": "디자인의 본질과 역할을 탐구하는 책"},
    {"title": "예술가의 일", "author": "조성준", "field": "예술·디자인", "desc": "창작과 예술 활동의 세계를 살펴보는 책"},
    {"title": "창조적 행위", "author": "릭 루빈", "field": "예술·디자인", "desc": "창작 과정과 예술적 태도를 다루는 책"},
    {"title": "그림의 힘", "author": "김선현", "field": "예술·디자인", "desc": "그림과 감정의 관계를 살펴보는 책"},
    {"title": "오리지널스", "author": "애덤 그랜트", "field": "예술·디자인", "desc": "새로운 아이디어와 창의성을 탐구하는 책"},
    {"title": "생각의 탄생", "author": "로버트 루트번스타인·미셸 루트번스타인", "field": "예술·디자인", "desc": "창조적 사고의 여러 방법을 살펴보는 책"},

    # 환경 · 공학
    {"title": "엔트로피", "author": "제레미 리프킨", "field": "환경·공학", "desc": "에너지와 문명의 관계를 다루는 책"},
    {"title": "침묵의 봄", "author": "레이첼 카슨", "field": "환경·공학", "desc": "환경오염이 생태계에 미치는 영향을 다루는 책"},
    {"title": "기후변화의 과학", "author": "기후과학 분야", "field": "환경·공학", "desc": "기후 변화의 과학적 원리를 알아보는 주제 도서"},
    {"title": "거의 모든 것의 역사", "author": "빌 브라이슨", "field": "환경·공학", "desc": "과학의 여러 분야와 발견을 소개하는 책"},
    {"title": "사소한 것들의 과학", "author": "마크 미오도닉", "field": "환경·공학", "desc": "일상 속 재료와 공학의 원리를 알아보는 책"},
    {"title": "세상을 바꾼 물리", "author": "물리학 교양 분야", "field": "환경·공학", "desc": "물리학의 발전과 기술의 관계를 살펴보는 주제 도서"},
    {"title": "공학이란 무엇인가", "author": "서울대학교 공과대학", "field": "환경·공학", "desc": "다양한 공학 분야와 진로를 소개하는 책"},
    {"title": "과학 콘서트", "author": "정재승", "field": "환경·공학", "desc": "일상에서 발견하는 과학 원리를 설명하는 책"},

    # 요리 · 서비스 · 체육
    {"title": "요리는 감이여", "author": "51명의 충청도 할매들", "field": "요리·서비스·체육", "desc": "생활 속 요리 경험과 조리법을 담은 책"},
    {"title": "식탁 위의 과학", "author": "식품과학 분야", "field": "요리·서비스·체육", "desc": "음식과 조리의 과학적 원리를 살펴보는 주제 도서"},
    {"title": "음식의 언어", "author": "댄 주래프스키", "field": "요리·서비스·체육", "desc": "음식 이름과 문화의 관계를 탐구하는 책"},
    {"title": "운동화 신은 뇌", "author": "존 레이티·에릭 헤이거먼", "field": "요리·서비스·체육", "desc": "운동과 뇌 건강의 관계를 설명하는 책"},
    {"title": "스포츠 심리학", "author": "스포츠 심리학 분야", "field": "요리·서비스·체육", "desc": "운동 수행과 심리의 관계를 살펴보는 주제 도서"},
    {"title": "아웃라이어", "author": "말콤 글래드웰", "field": "요리·서비스·체육", "desc": "성공에 영향을 미치는 여러 조건을 분석하는 책"},
]

FIELDS = sorted(set(book["field"] for book in BOOKS))

# 세션 상태 초기화
if "career_favorites" not in st.session_state:
    st.session_state.career_favorites = []

if "career_query" not in st.session_state:
    st.session_state.career_query = ""

# 디자인
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff9f2 0%, #f4f5ff 100%);
}
.book-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid #e9e5f5;
    border-radius: 18px;
    padding: 17px;
    min-height: 150px;
    box-shadow: 0 4px 15px rgba(80,70,120,0.06);
}
.book-title {
    font-size: 17px;
    font-weight: 700;
    color: #34304a;
    margin-bottom: 8px;
}
.book-author {
    color: #77718b;
    font-size: 13px;
}
.book-desc {
    color: #514d61;
    font-size: 14px;
    margin-top: 12px;
}
div.stButton > button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# 메뉴
tab1, tab2 = st.tabs(["🔎 도서 찾기", "💜 관심 도서"])

with tab1:
    st.subheader("나에게 맞는 진로 도서 찾기")
    st.write("분야를 선택하거나 책 제목과 저자를 검색해 보세요.")

    selected_field = st.selectbox("관심 분야", ["전체 분야"] + FIELDS)
    query = st.text_input(
        "책 제목 또는 저자 검색",
        placeholder="예: 인공지능, 심리학, 김진형"
    ).strip().lower()

    filtered = BOOKS.copy()

    if selected_field != "전체 분야":
        filtered = [
            book for book in filtered
            if book["field"] == selected_field
        ]

    if query:
        filtered = [
            book for book in filtered
            if query in book["title"].lower()
            or query in book["author"].lower()
            or query in book["desc"].lower()
        ]

    st.caption(f"검색 결과 {len(filtered)}권")

    if not filtered:
        st.info("검색 결과가 없어요. 다른 검색어나 분야를 선택해 보세요.")
    else:
        cols_per_row = 3

        for start in range(0, len(filtered), cols_per_row):
            cols = st.columns(cols_per_row)

            for col, book in zip(
                cols, filtered[start:start + cols_per_row]
            ):
                with col:
                    st.markdown(
                        f"""
                        <div class="book-card">
                            <div style="font-size:12px;color:#8d79bd;">
                                📖 {book["field"]}
                            </div>
                            <div class="book-title">
                                {book["title"]}
                            </div>
                            <div class="book-author">
                                저자: {book["author"]}
                            </div>
                            <div class="book-desc">
                                {book["desc"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    favorite_key = (
                        book["title"] + "|" + book["author"]
                    )
                    is_favorite = favorite_key in st.session_state.career_favorites

                    if st.button(
                        "💜 관심 도서 해제" if is_favorite else "♡ 관심 도서 저장",
                        key="fav_" + str(start) + "_" + favorite_key
                    ):
                        if is_favorite:
                            st.session_state.career_favorites.remove(
                                favorite_key
                            )
                        else:
                            st.session_state.career_favorites.append(
                                favorite_key
                            )
                        st.rerun()

                    search_url = (
                        "https://www.google.com/search?q="
                        + book["title"].replace(" ", "+")
                        + "+책"
                    )
                    st.link_button("🔗 책 정보 찾아보기", search_url)

                    st.write("")

with tab2:
    st.subheader("💜 내가 저장한 도서")

    favorites = [
        book for book in BOOKS
        if book["title"] + "|" + book["author"]
        in st.session_state.career_favorites
    ]

    if not favorites:
        st.info("아직 저장한 책이 없어요. 도서 찾기에서 관심 도서를 저장해 보세요.")
    else:
        for book in favorites:
            with st.container(border=True):
                st.markdown(f"### 📚 {book['title']}")
                st.write(f"**저자:** {book['author']}")
                st.write(f"**분야:** {book['field']}")
                st.write(book["desc"])

                if st.button(
                    "저장 취소",
                    key="remove_" + book["title"] + book["author"]
                ):
                    st.session_state.career_favorites.remove(
                        book["title"] + "|" + book["author"]
                    )
                    st.rerun()

st.divider()
st.caption(
    "현재 도서 목록은 앱 내부 데이터로 검색합니다. "
    "외부 도서 검색 API를 호출하지 않으므로 API 요청 한도 오류가 발생하지 않습니다."
)
