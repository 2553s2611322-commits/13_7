
import streamlit as st

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="내 주변 진로상담센터 찾기",
    page_icon="📍",
    layout="centered"
)

# ==========================================
# 2. 디자인
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}

.main .block-container {
    max-width: 900px;
    padding-top: 2rem;
}

.header-box {
    background: linear-gradient(120deg, #4388E8, #61C2B3);
    padding: 35px 25px;
    border-radius: 18px;
    color: white;
    margin-bottom: 20px;
}

.header-box h2 {
    color: white;
    font-size: 27px;
}

.header-box p {
    color: white;
    font-size: 16px;
}

.result-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #DDE3EC;
    margin-bottom: 12px;
}

.stButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 600;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(120deg, #4388E8, #61C2B3);
    border: none;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 전국 공식 진로진학지원센터 정보
# ==========================================

CENTERS = {
    "서울특별시": {
        "name": "서울 진로진학정보센터",
        "url": "https://www.jinhak.or.kr",
        "description": "서울 지역 진로 및 진학 정보 제공"
    },

    "부산광역시": {
        "name": "부산 진로진학지원센터",
        "url": "https://dream.pen.go.kr",
        "description": "부산 지역 진로 및 진학 상담 지원"
    },

    "대구광역시": {
        "name": "대구 진로진학지원센터",
        "url": "https://www.dge.go.kr/jinhak/main.do",
        "description": "대구 지역 진로 및 진학 정보 제공"
    },

    "인천광역시": {
        "name": "인천 진로진학지원센터",
        "url": "https://cyberjinro.ice.go.kr/main",
        "description": "인천 지역 진로 및 진학 정보 제공"
    },

    "광주광역시": {
        "name": "광주 진로진학지원센터",
        "url": "http://jinhak.gen.go.kr",
        "description": "광주 지역 진로 및 진학 상담 지원"
    },

    "대전광역시": {
        "name": "대전 진로진학지원센터",
        "url": "http://www.edurang.net/main.do?s=course",
        "description": "대전 지역 진로 및 진학 정보 제공"
    },

    "울산광역시": {
        "name": "울산 진로진학지원센터",
        "url": "https://use.go.kr/jinhak/index.do",
        "description": "울산 지역 진로 및 진학 상담 지원"
    },

    "세종특별자치시": {
        "name": "세종 진로진학지원센터",
        "url": "https://jinro.sje.go.kr/home/main.do",
        "description": "세종 지역 진로 및 진학 정보 제공"
    },

    "경기도": {
        "name": "경기 진로진학지원센터",
        "url": "https://more.goe.go.kr/jinhak/index.do",
        "description": "경기도 지역 진로 및 진학 상담 지원"
    },

    "강원특별자치도": {
        "name": "강원 진로진학지원센터",
        "url": "https://jinhak.gwe.go.kr",
        "description": "강원 지역 진로 및 진학 정보 제공"
    },

    "충청북도": {
        "name": "충북 진로진학지원센터",
        "url": "https://jinro.cbe.go.kr/home/main.php",
        "description": "충북 지역 진로 및 진학 상담 지원"
    },

    "충청남도": {
        "name": "충남 진로진학지원센터",
        "url": "https://icec.cne.go.kr/home/main.do?screenTp=USER",
        "description": "충남 지역 진로 및 진학 정보 제공"
    },

    "전북특별자치도": {
        "name": "전북 진로진학지원센터",
        "url": "https://www.jbe.go.kr/jinro/index.jbe",
        "description": "전북 지역 진로 및 진학 상담 지원"
    },

    "전라남도": {
        "name": "전남 진로진학지원센터",
        "url": "https://www.jne.go.kr/jinro/main.do",
        "description": "전남 지역 진로 및 진학 정보 제공"
    },

    "경상북도": {
        "name": "경북 진로진학지원센터",
        "url": "https://www.gbe.kr/cheerup/main.do",
        "description": "경북 지역 진로 및 진학 상담 지원"
    },

    "경상남도": {
        "name": "경남 진로진학지원센터",
        "url": "https://gnce.gne.go.kr/gnce/main.do",
        "description": "경남 지역 진로 및 진학 정보 제공"
    },

    "제주특별자치도": {
        "name": "제주 진로진학지원센터",
        "url": "https://jinhak.jje.go.kr",
        "description": "제주 지역 진로 및 진학 상담 지원"
    }
}

# ==========================================
# 4. 메인 화면
# ==========================================

st.markdown("""
<div class="header-box">
    <h2>내 꿈에 가까워지는<br>진로상담센터 찾기</h2>
    <p>내 주변의 진로·진학 전문 기관을 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 지역 선택
# ==========================================

st.markdown("### 📍 내 주변 진로상담센터 검색")

selected_region = st.selectbox(
    "시·도",
    list(CENTERS.keys()),
    key="region_select"
)

st.info(
    "지역을 선택하면 해당 지역의 공식 진로진학지원센터를 안내합니다."
)

# ==========================================
# 6. 검색 버튼
# ==========================================

if st.button(
    "🔎 진로상담센터 검색하기",
    type="primary",
    use_container_width=True
):

    st.session_state["search_region"] = selected_region

# ==========================================
# 7. 검색 결과
# ==========================================

if "search_region" in st.session_state:

    region = st.session_state["search_region"]

    center = CENTERS.get(region)

    if center:

        st.success("공식 진로진학지원센터를 찾았습니다!")

        st.markdown(
            f"""
            <div class="result-box">
                <h3>🏫 {center["name"]}</h3>
                <p><b>지역:</b> {region}</p>
                <p><b>기관 유형:</b> 진로진학지원센터</p>
                <p>{center["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "🌐 공식 홈페이지 방문하기",
            center["url"],
            use_container_width=True
        )

        st.caption(
            "※ 홈페이지에서 상담 신청 방법과 운영 시간을 확인하세요."
        )

# ==========================================
# 8. 전국 센터 목록
# ==========================================

with st.expander("📚 전국 진로진학지원센터 목록 보기"):

    for region, center in CENTERS.items():

        st.markdown(
            f"**{region}** — {center['name']}"
        )

        st.markdown(
            f"[공식 홈페이지 바로가기]({center['url']})"
        )

        st.markdown("---")

# ==========================================
# 9. 추가 진로상담 안내
# ==========================================

st.markdown("### 💬 추가 진로상담 안내")

st.markdown("""
전국의 진로·진학 관련 상담을 알아보고 싶다면
아래 공식 서비스를 이용할 수 있습니다.
""")

st.link_button(
    "🌱 커리어넷 진로정보",
    "https://www.career.go.kr",
    use_container_width=True
)

st.link_button(
    "🎓 전국 진로진학지원센터 안내",
    "https://hischool.go.kr/site/02/index.do",
    use_container_width=True
)

st.markdown("---")

st.caption(
    "본 서비스는 전국 시·도교육청의 공식 진로진학지원센터 정보를 안내합니다."
)

st.caption(
    "센터별 상담 운영 여부와 신청 방법은 공식 홈페이지에서 확인해 주세요."
)
