import streamlit as st
import requests

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="내 주변 진로상담센터 찾기",
    page_icon="📍",
    layout="centered"
)

# ==========================================
# 2. 디자인 CSS
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

.search-box {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #DDE3EC;
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
# 3. 지역 데이터
# ==========================================

REGIONS = {
    "서울특별시": [
        "전체", "강남구", "강동구", "강북구", "강서구",
        "관악구", "광진구", "구로구", "금천구", "노원구",
        "도봉구", "동대문구", "동작구", "마포구", "서대문구",
        "서초구", "성동구", "성북구", "송파구", "양천구",
        "영등포구", "용산구", "은평구", "종로구", "중구",
        "중랑구"
    ],

    "부산광역시": [
        "전체", "중구", "서구", "동구", "영도구",
        "부산진구", "동래구", "남구", "북구", "해운대구",
        "사하구", "금정구", "강서구", "연제구", "수영구",
        "사상구", "기장군"
    ],

    "대구광역시": [
        "전체", "중구", "동구", "서구", "남구",
        "북구", "수성구", "달서구", "달성군", "군위군"
    ],

    "인천광역시": [
        "전체", "중구", "동구", "미추홀구", "연수구",
        "남동구", "부평구", "계양구", "서구", "강화군",
        "옹진군"
    ],

    "광주광역시": [
        "전체", "동구", "서구", "남구", "북구", "광산구"
    ],

    "대전광역시": [
        "전체", "동구", "중구", "서구", "유성구", "대덕구"
    ],

    "울산광역시": [
        "전체", "중구", "남구", "동구", "북구", "울주군"
    ],

    "세종특별자치시": [
        "전체"
    ],

    "경기도": [
        "전체", "수원시", "성남시", "의정부시", "안양시",
        "부천시", "광명시", "평택시", "동두천시", "안산시",
        "고양시", "과천시", "구리시", "남양주시", "오산시",
        "시흥시", "군포시", "의왕시", "하남시", "용인시",
        "파주시", "이천시", "안성시", "김포시", "화성시",
        "광주시", "양주시", "포천시", "여주시", "연천군",
        "가평군", "양평군"
    ],

    "강원특별자치도": [
        "전체", "춘천시", "원주시", "강릉시", "동해시",
        "태백시", "속초시", "삼척시", "홍천군", "횡성군",
        "영월군", "평창군", "정선군", "철원군", "화천군",
        "양구군", "인제군", "고성군", "양양군"
    ],

    "충청북도": [
        "전체", "청주시", "충주시", "제천시", "보은군",
        "옥천군", "영동군", "증평군", "진천군", "괴산군",
        "음성군", "단양군"
    ],

    "충청남도": [
        "전체", "천안시", "공주시", "보령시", "아산시",
        "서산시", "논산시", "계룡시", "당진시", "금산군",
        "부여군", "서천군", "청양군", "홍성군", "예산군",
        "태안군"
    ],

    "전북특별자치도": [
        "전체", "전주시", "군산시", "익산시", "정읍시",
        "남원시", "김제시", "완주군", "진안군", "무주군",
        "장수군", "임실군", "순창군", "고창군", "부안군"
    ],

    "전라남도": [
        "전체", "목포시", "여수시", "순천시", "나주시",
        "광양시", "담양군", "곡성군", "구례군", "고흥군",
        "보성군", "화순군", "장흥군", "강진군", "해남군",
        "영암군", "무안군", "함평군", "영광군", "장성군",
        "완도군", "진도군", "신안군"
    ],

    "경상북도": [
        "전체", "포항시", "경주시", "김천시", "안동시",
        "구미시", "영주시", "영천시", "상주시", "문경시",
        "경산시", "의성군", "청송군", "영양군", "영덕군",
        "청도군", "고령군", "성주군", "칠곡군", "예천군",
        "봉화군", "울진군", "울릉군"
    ],

    "경상남도": [
        "전체", "창원시", "진주시", "통영시", "사천시",
        "김해시", "밀양시", "거제시", "양산시", "의령군",
        "함안군", "창녕군", "고성군", "남해군", "하동군",
        "산청군", "함양군", "거창군", "합천군"
    ],

    "제주특별자치도": [
        "전체", "제주시", "서귀포시"
    ]
}


# ==========================================
# 4. 카카오 API 키 확인
# ==========================================

def get_api_key():
    try:
        return st.secrets.get("KAKAO_REST_API_KEY", "")
    except Exception:
        return ""


# ==========================================
# 5. 실제 진로상담센터 검색
# ==========================================

def search_centers(region, district, api_key):

    search_words = [
        "진로진학지원센터",
        "진로상담센터",
        "진로교육지원센터"
    ]

    results = []
    seen_ids = set()

    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }

    if district == "전체":
        location = region
    else:
        location = f"{region} {district}"

    for word in search_words:

        query = f"{location} {word}"

        try:
            response = requests.get(
                "https://dapi.kakao.com/v2/local/search/keyword.json",
                headers=headers,
                params={
                    "query": query,
                    "size": 15,
                    "page": 1
                },
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            for item in data.get("documents", []):

                place_id = item.get("id")

                if place_id in seen_ids:
                    continue

                name = item.get("place_name", "")

                category = item.get("category_name", "")

                # 진로·진학 관련 기관 위주로 표시
                if not any(
                    keyword in name + category
                    for keyword in [
                        "진로",
                        "진학",
                        "교육지원청"
                    ]
                ):
                    continue

                seen_ids.add(place_id)

                results.append({
                    "name": name,
                    "address": (
                        item.get("road_address_name")
                        or item.get("address_name")
                        or "주소 정보 없음"
                    ),
                    "phone": (
                        item.get("phone")
                        or "전화번호 정보 없음"
                    ),
                    "category": category,
                    "url": item.get("place_url", "")
                })

        except requests.exceptions.Timeout:
            st.warning("검색 시간이 초과되었습니다. 다시 시도해 주세요.")

        except requests.exceptions.HTTPError:
            st.error(
                "카카오 API 인증에 실패했습니다. "
                "REST API 키를 확인해 주세요."
            )
            return []

        except requests.exceptions.RequestException:
            st.error(
                "인터넷 연결 또는 검색 서버에 문제가 발생했습니다."
            )
            return []

        except ValueError:
            st.error("검색 결과를 읽을 수 없습니다.")
            return []

    return results


# ==========================================
# 6. 메인 화면
# ==========================================

st.markdown("""
<div class="header-box">
    <h2>내 꿈에 가까워지는<br>진로상담센터 찾기</h2>
    <p>내 주변의 진로·진학 전문 기관을 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. 검색 화면
# ==========================================

st.markdown("### 📍 내 주변 진로상담센터 검색")

col1, col2 = st.columns(2)

with col1:
    selected_region = st.selectbox(
        "시·도",
        list(REGIONS.keys()),
        key="region_select"
    )

with col2:
    selected_district = st.selectbox(
        "시·군·구",
        REGIONS[selected_region],
        key="district_select"
    )

institution_type = st.selectbox(
    "기관 유형",
    [
        "진로진학지원센터",
        "진로상담센터",
        "진로교육지원센터",
        "전체 진로상담기관"
    ],
    key="institution_type"
)

st.caption(
    "※ 현재 위치 기능 대신 지역을 직접 선택하도록 구성했습니다. "
    "검색 결과는 앱 안에서 확인할 수 있습니다."
)

search_button = st.button(
    "🔎 진로상담센터 검색하기",
    type="primary",
    use_container_width=True
)


# ==========================================
# 8. 검색 결과 출력
# ==========================================

if search_button:

    api_key = get_api_key()

    if not api_key:

        st.error(
            "카카오 REST API 키가 설정되지 않았습니다."
        )

        st.info(
            "Streamlit Cloud의 앱 설정에서 "
            "KAKAO_REST_API_KEY를 등록해 주세요."
        )

    else:

        with st.spinner("실제 진로상담센터를 검색하고 있습니다..."):

            centers = search_centers(
                selected_region,
                selected_district,
                api_key
            )

        if centers:

            st.success(
                f"총 {len(centers)}개의 검색 결과를 찾았습니다."
            )

            for center in centers:

                with st.container():

                    st.markdown(
                        f"""
                        <div class="result-box">
                            <h4>🏫 {center["name"]}</h4>
                            <p>
                                <b>주소:</b> {center["address"]}
                            </p>
                            <p>
                                <b>전화번호:</b> {center["phone"]}
                            </p>
                            <p>
                                <b>기관 유형:</b> {center["category"]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if center["url"]:

                        st.link_button(
                            "기관 상세 정보 확인하기",
                            center["url"],
                            use_container_width=True
                        )

                    st.markdown("")

        else:

            st.warning(
                "선택한 지역에서 진로상담센터를 찾지 못했습니다."
            )

            st.info(
                "다른 지역을 선택하거나 "
                "시·도 전체 검색을 이용해 주세요."
            )


# ==========================================
# 9. 하단 안내
# ==========================================

st.markdown("---")

st.caption(
    "본 서비스는 카카오 로컬 API를 활용하여 "
    "진로·진학 관련 기관의 장소 정보를 검색합니다."
)

st.caption(
    "검색 결과가 실제 상담 운영 여부를 보장하지는 않습니다. "
    "방문 전 기관에 전화하여 상담 가능 여부를 확인해 주세요."
)
