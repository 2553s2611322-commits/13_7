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

.center-card {
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
# 3. 실제 서울 진로직업체험지원센터 데이터
# ==========================================

CENTERS = [
    {
        "district": "강남구",
        "name": "나래꿈터",
        "address": "서울 강남구 논현로64길 7 역삼청소년센터 2층",
        "phone": "02-550-3629"
    },
    {
        "district": "강동구",
        "name": "강동 미래온(ON)",
        "address": "서울 강동구 구천면로 395 2층",
        "phone": "02-481-7088"
    },
    {
        "district": "강북구",
        "name": "강북구 진로직업체험지원센터",
        "address": "서울 강북구 삼양로51가길 22",
        "phone": "02-6265-7640"
    },
    {
        "district": "강서구",
        "name": "강서 진로직업체험지원센터",
        "address": "서울 강서구 양천로 542 기아 강서서비스센터 2층",
        "phone": "02-2699-8724"
    },
    {
        "district": "관악구",
        "name": "관악 진로직업체험지원센터",
        "address": "서울 관악구 남부순환로234길 73 싱글벙글교육센터 3층",
        "phone": "02-873-8815"
    },
    {
        "district": "광진구",
        "name": "광진해봄",
        "address": "서울 광진구 구천면로 2 시립광진청소년센터",
        "phone": "02-2204-3135"
    },
    {
        "district": "구로구",
        "name": "구로 진로직업체험지원센터",
        "address": "서울 구로구 가마산로25길 21 구로구민회관 2층",
        "phone": "02-860-2881"
    },
    {
        "district": "금천구",
        "name": "금천진로진학지원센터",
        "address": "서울 금천구 문성로 38",
        "phone": "02-2627-2823"
    },
    {
        "district": "노원구",
        "name": "상상이룸센터",
        "address": "서울 노원구 노해로 502 노원KT 신관 4층",
        "phone": "02-936-3326"
    },
    {
        "district": "도봉구",
        "name": "꿈여울",
        "address": "서울 도봉구 도봉로 552 도봉구민회관 3층",
        "phone": "02-2091-2343"
    },
    {
        "district": "동대문구",
        "name": "와락",
        "address": "서울 동대문구 답십리로38길 19 A동 3층",
        "phone": "02-6238-2020"
    },
    {
        "district": "동작구",
        "name": "동작구 진로직업체험지원센터",
        "address": "서울 동작구 장승배기로 161 4층",
        "phone": "02-815-3371"
    },
    {
        "district": "마포구",
        "name": "희망나래",
        "address": "서울 마포구 성산로 128 마포중앙도서관 5층",
        "phone": "02-322-2660"
    },
    {
        "district": "서대문구",
        "name": "서대문 진로직업체험지원센터",
        "address": "서울 서대문구 포방터길 110 홍은청소년문화의집",
        "phone": "02-395-1318"
    },
    {
        "district": "서초구",
        "name": "양재내곡교육지원센터",
        "address": "서울 서초구 강남대로 190 대관빌딩 1층",
        "phone": "02-574-0304"
    },
    {
        "district": "성동구",
        "name": "성동구 진로직업체험지원센터",
        "address": "서울 성동구 고산자로 270 성동구청 2층",
        "phone": "02-2286-6675"
    },
    {
        "district": "성북구",
        "name": "성북청소년미래지원센터",
        "address": "서울 성북구 오패산로3길 87",
        "phone": "02-2241-2400"
    },
    {
        "district": "송파구",
        "name": "꿈마루",
        "address": "서울 송파구 마천로35길 12 송파구 평생학습원 1층",
        "phone": "02-6713-2394"
    },
    {
        "district": "양천구",
        "name": "진로드림",
        "address": "서울 양천구 목동동로 375 1층",
        "phone": "02-2084-5414"
    },
    {
        "district": "영등포구",
        "name": "영등포 진로직업체험지원센터",
        "address": "서울 영등포구 국회대로 596 영등포구민회관 3층",
        "phone": "02-2636-6521"
    },
    {
        "district": "용산구",
        "name": "용산구 진로직업체험지원센터 미래야",
        "address": "서울 용산구 한강대로 255 시립청소년미디어센터",
        "phone": "070-7165-1023"
    },
    {
        "district": "은평구",
        "name": "은평구 진로직업체험지원센터",
        "address": "서울 은평구 백련산로4길 16 은평청소년센터",
        "phone": "070-7113-4994"
    },
    {
        "district": "종로구",
        "name": "종로구 진로직업체험지원센터",
        "address": "서울 종로구 이화장길 81 한국방송통신대학교 열린관 3층",
        "phone": "02-6956-1152"
    },
    {
        "district": "중구",
        "name": "중구 진로직업체험지원센터",
        "address": "서울 중구 다산로33길 3 신당누리센터 4층",
        "phone": "02-2250-0580"
    },
    {
        "district": "중랑구",
        "name": "중랑드림하이",
        "address": "서울 중랑구 망우로325 방정환교육지원센터 4층",
        "phone": "070-4304-4057"
    }
]

# ==========================================
# 4. 메인 화면
# ==========================================

st.markdown("""
<div class="header-box">
    <h2>내 꿈에 가까워지는<br>진로상담센터 찾기</h2>
    <p>내 주변의 진로·진학 전문 기관을 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📍 내 주변 진로상담센터 검색")

# ==========================================
# 5. 지역 선택
# ==========================================

districts = ["전체"] + sorted(
    [center["district"] for center in CENTERS]
)

col1, col2 = st.columns(2)

with col1:
    selected_region = st.selectbox(
        "시·도",
        ["서울특별시"],
        key="region_select"
    )

with col2:
    selected_district = st.selectbox(
        "시·군·구",
        districts,
        key="district_select"
    )

institution_type = st.selectbox(
    "기관 유형",
    [
        "전체 진로상담기관",
        "진로직업체험지원센터",
        "진로진학지원센터"
    ],
    key="institution_type"
)

st.caption(
    "서울시 25개 자치구의 진로·진학 관련 기관 정보를 제공합니다."
)

# ==========================================
# 6. 검색
# ==========================================

if st.button(
    "🔎 진로상담센터 검색하기",
    type="primary",
    use_container_width=True
):

    if selected_district == "전체":
        results = CENTERS
    else:
        results = [
            center for center in CENTERS
            if center["district"] == selected_district
        ]

    st.session_state["search_results"] = results
    st.session_state["search_district"] = selected_district

# ==========================================
# 7. 검색 결과
# ==========================================

if "search_results" in st.session_state:

    results = st.session_state["search_results"]

    if results:

        st.success(
            f"총 {len(results)}개의 진로상담센터를 찾았습니다."
        )

        for center in results:

            st.markdown(
                f"""
                <div class="center-card">
                    <h3>🏫 {center["name"]}</h3>
                    <p><b>지역:</b> {center["district"]}</p>
                    <p><b>주소:</b> {center["address"]}</p>
                    <p><b>전화번호:</b> {center["phone"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.link_button(
                "📍 지도에서 위치 확인하기",
                "https://map.kakao.com/?q="
                + center["address"],
                use_container_width=True
            )

            st.markdown("")

    else:

        st.warning(
            "선택한 지역에서 진로상담센터를 찾지 못했습니다."
        )

# ==========================================
# 8. 공식 자료 출처
# ==========================================

st.markdown("---")

st.markdown("### 📚 공식 기관 정보")

st.markdown("""
센터의 주소와 전화번호는 서울 진로직업체험지원센터협의회의
기관 안내를 참고하여 구성했습니다.
""")

st.link_button(
    "서울 진로직업체험지원센터 공식 목록",
    "https://seouljinro.or.kr/centers",
    use_container_width=True
)

st.caption(
    "※ 주소와 전화번호는 변경될 수 있습니다. "
    "방문 전 기관에 연락하여 상담 가능 여부를 확인해 주세요."
)
