
import streamlit as st
import requests
import pandas as pd
from urllib.parse import quote

# -----------------------------------
# 기본 설정
# -----------------------------------
st.set_page_config(
    page_title="진로상담센터 안내",
    page_icon="🧭",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }
    .hero {
        background: linear-gradient(120deg, #dceaff, #e7f5ed);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .hero h1 {
        color: #24476b;
        margin-bottom: 8px;
    }
    .info-card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e4eaf0;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# 지역 정보
# -----------------------------------
REGIONS = {
    "서울특별시": ["종로구", "중구", "용산구", "성동구", "광진구",
                 "동대문구", "중랑구", "성북구", "강북구", "도봉구",
                 "노원구", "은평구", "서대문구", "마포구", "양천구",
                 "강서구", "구로구", "금천구", "영등포구", "동작구",
                 "관악구", "서초구", "강남구", "송파구", "강동구"],
    "부산광역시": ["중구", "서구", "동구", "영도구", "부산진구",
                 "동래구", "남구", "북구", "해운대구", "사하구",
                 "금정구", "강서구", "연제구", "수영구", "사상구",
                 "기장군"],
    "대구광역시": ["중구", "동구", "서구", "남구", "북구",
                 "수성구", "달서구", "달성군", "군위군"],
    "인천광역시": ["중구", "동구", "미추홀구", "연수구", "남동구",
                 "부평구", "계양구", "서구", "강화군", "옹진군"],
    "광주광역시": ["동구", "서구", "남구", "북구", "광산구"],
    "대전광역시": ["동구", "중구", "서구", "유성구", "대덕구"],
    "울산광역시": ["중구", "남구", "동구", "북구", "울주군"],
    "세종특별자치시": ["세종시"],
    "경기도": ["수원시", "성남시", "고양시", "용인시", "부천시",
              "안산시", "안양시", "남양주시", "화성시", "평택시",
              "의정부시", "파주시", "김포시", "광명시", "군포시",
              "오산시", "이천시", "양주시", "구리시", "안성시",
              "포천시", "하남시", "의왕시", "여주시", "양평군",
              "가평군", "연천군", "동두천시", "과천시", "시흥시",
              "광주시"],
    "강원특별자치도": ["춘천시", "원주시", "강릉시", "동해시",
                    "태백시", "속초시", "삼척시", "홍천군",
                    "횡성군", "영월군", "평창군", "정선군",
                    "철원군", "화천군", "양구군", "인제군",
                    "고성군", "양양군"],
    "충청북도": ["청주시", "충주시", "제천시", "보은군", "옥천군",
               "영동군", "증평군", "진천군", "괴산군", "음성군",
               "단양군"],
    "충청남도": ["천안시", "공주시", "보령시", "아산시", "서산시",
               "논산시", "계룡시", "당진시", "금산군", "부여군",
               "서천군", "청양군", "홍성군", "예산군", "태안군"],
    "전북특별자치도": ["전주시", "군산시", "익산시", "정읍시",
                    "남원시", "김제시", "완주군", "진안군",
                    "무주군", "장수군", "임실군", "순창군",
                    "고창군", "부안군"],
    "전라남도": ["목포시", "여수시", "순천시", "나주시", "광양시",
               "담양군", "곡성군", "구례군", "고흥군", "보성군",
               "화순군", "장흥군", "강진군", "해남군", "영암군",
               "무안군", "함평군", "영광군", "장성군", "완도군",
               "진도군", "신안군"],
    "경상북도": ["포항시", "경주시", "김천시", "안동시", "구미시",
               "영주시", "영천시", "상주시", "문경시", "경산시",
               "의성군", "청송군", "영양군", "영덕군", "청도군",
               "고령군", "성주군", "칠곡군", "예천군", "봉화군",
               "울진군", "울릉군"],
    "경상남도": ["창원시", "진주시", "통영시", "사천시", "김해시",
               "밀양시", "거제시", "양산시", "의령군", "함안군",
               "창녕군", "고성군", "남해군", "하동군", "산청군",
               "함양군", "거창군", "합천군"],
    "제주특별자치도": ["제주시", "서귀포시"]
}


# -----------------------------------
# 위치 정보 가져오기
# -----------------------------------
def get_location():
    """브라우저 위치 정보를 요청한다."""
    try:
        from streamlit_geolocation import streamlit_geolocation
        location = streamlit_geolocation()

        if not isinstance(location, dict):
            return None

        lat = location.get("latitude")
        lon = location.get("longitude")

        if lat is None or lon is None:
            return None

        lat, lon = float(lat), float(lon)

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return None

        return lat, lon

    except Exception:
        return None


def reverse_geocode(lat, lon):
    """좌표를 대략적인 주소로 변환한다."""
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "jsonv2",
                "accept-language": "ko"
            },
            headers={"User-Agent": "CareerCenterGuide/1.0"},
            timeout=8
        )
        response.raise_for_status()
        data = response.json()
        address = data.get("address", {})

        return (
            address.get("city")
            or address.get("county")
            or address.get("state")
            or "현재 위치"
        )
    except (requests.RequestException, ValueError, TypeError):
        return "현재 위치"


# -----------------------------------
# 상담센터 검색
# -----------------------------------
def search_centers(query, lat=None, lon=None):
    """OpenStreetMap에서 관련 장소를 검색한다."""
    try:
        params = {
            "q": query,
            "format": "jsonv2",
            "limit": 8,
            "addressdetails": 1,
            "accept-language": "ko"
        }

        # 현재 위치가 있으면 해당 좌표 주변을 우선 검색
        if lat is not None and lon is not None:
            params.update({
                "lat": lat,
                "lon": lon
            })

        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers={"User-Agent": "CareerCenterGuide/1.0"},
            timeout=10
        )
        response.raise_for_status()
        results = response.json()

        centers = []
        for item in results:
            name = item.get("name") or item.get("display_name", "")
            address = item.get("display_name", "")
            if not name:
                continue

            centers.append({
                "센터명": name,
                "주소": address,
                "위도": float(item["lat"]),
                "경도": float(item["lon"]),
                "지도": (
                    "https://www.openstreetmap.org/?mlat="
                    + str(item["lat"])
                    + "&mlon="
                    + str(item["lon"])
                    + "#map=16/"
                    + str(item["lat"])
                    + "/"
                    + str(item["lon"])
                )
            })

        return centers

    except (requests.RequestException, ValueError, TypeError, KeyError):
        return []


# -----------------------------------
# 화면 구성
# -----------------------------------
st.markdown("""
<div class="hero">
    <h1>🧭 나의 진로 길찾기</h1>
    <p>진로가 고민될 때, 가까운 상담센터를 찾아보세요.</p>
    <p>내 주변의 상담 기관부터 온라인 진로상담까지 한곳에서!</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📍 주변 센터 찾기",
    "💬 온라인 진로상담",
    "❓ 이용 안내"
])

with tab1:
    st.subheader("어디에 있는 상담센터를 찾나요?")
    st.caption("현재 위치는 권한을 허용한 경우에만 확인합니다.")

    if st.button("📍 현재 위치 확인하기", use_container_width=True):
        location = get_location()
        if location:
            st.session_state["my_location"] = location
            st.session_state["my_area"] = reverse_geocode(*location)
            st.success(
                "위치를 확인했어요: "
                + st.session_state["my_area"]
            )
        else:
            st.warning(
                "위치를 가져오지 못했어요. 브라우저 위치 권한을 확인하거나 "
                "아래에서 지역을 직접 선택해 주세요."
            )

    provinces = list(REGIONS.keys())
    default_index = provinces.index("서울특별시")

    province = st.selectbox(
        "시·도 선택",
        provinces,
        index=default_index
    )
    district = st.selectbox(
        "시·군·구 선택",
        REGIONS[province]
    )

    search_keyword = st.selectbox(
        "찾고 싶은 기관",
        [
            "진로상담센터",
            "청소년상담복지센터",
            "진로진학지원센터",
            "진로체험지원센터"
        ]
    )

    area = f"{province} {district}"
    st.info(f"검색 지역: {area}")

    if st.button("🔎 상담센터 검색하기", type="primary",
                 use_container_width=True):
        search_text = f"{area} {search_keyword}"
        with st.spinner("주변 기관 정보를 검색하고 있어요..."):
            results = search_centers(search_text)

        st.session_state["search_results"] = results
        st.session_state["search_area"] = area
        st.session_state["search_keyword"] = search_keyword

    if "search_results" in st.session_state:
        results = st.session_state["search_results"]
        area = st.session_state.get("search_area", area)
        keyword = st.session_state.get("search_keyword", search_keyword)

        map_query = quote(f"{area} {keyword}")
        st.markdown(
            f"[🗺️ 지도에서 더 많은 상담센터 찾아보기]"
            f"(https://www.google.com/maps/search/{map_query})"
        )

        if results:
            st.success(f"검색 결과 {len(results)}곳")
            st.map(pd.DataFrame([
                {"lat": c["위도"], "lon": c["경도"]}
                for c in results
            ]))

            for center in results:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown(f"### 🏫 {center['센터명']}")
                st.write(f"📍 주소: {center['주소']}")
                st.markdown(f"[지도에서 위치 보기]({center['지도']})")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning(
                "등록된 장소를 찾지 못했어요. 검색어가 다르거나 "
                "지도 데이터에 정보가 없을 수 있어요."
            )
            st.write(
                "아래 지도 검색에서 지역과 기관명을 바꾸어 확인해 보세요."
            )

with tab2:
    st.subheader("온라인으로 진로 고민 상담하기")
    st.write(
        "직업 선택, 학과 고민, 진학 방향 등 다양한 진로 고민을 "
        "온라인으로 상담할 수 있어요."
    )

    st.markdown("""
    <div class="info-card">
        <h3>🌱 커리어넷</h3>
        <p>직업 정보, 진로심리검사, 진로상담 서비스를 이용할 수 있어요.</p>
        <a href="https://www.career.go.kr/" target="_blank">
            커리어넷 바로가기 ↗
        </a>
    </div>
    <div class="info-card">
        <h3>🌼 주니어 커리어넷</h3>
        <p>청소년을 위한 진로 탐색과 진로상담 정보를 확인할 수 있어요.</p>
        <a href="https://www.career.go.kr/cloud/jm/main/home" target="_blank">
            주니어 커리어넷 바로가기 ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("자주 묻는 질문")
    with st.expander("현재 위치는 어떻게 확인하나요?"):
        st.write(
            "현재 위치 확인 버튼을 누른 뒤 브라우저에서 위치 권한을 "
            "허용하면 됩니다. 허용하지 않아도 지역을 직접 선택할 수 있어요."
        )

    with st.expander("검색 결과가 나오지 않아요."):
        st.write(
            "지도 데이터에 해당 기관이 등록되지 않았을 수 있어요. "
            "지도에서 더 많은 상담센터 찾아보기를 이용해 보세요."
        )

    with st.expander("방문 전에 무엇을 확인해야 하나요?"):
        st.write(
            "운영 시간, 상담 대상, 예약 방법 및 연락처를 해당 기관의 "
            "공식 홈페이지에서 확인한 후 방문하세요."
        )

    st.caption(
        "안내: 지도 검색 결과는 기관의 전체 목록이 아니며, "
        "주소·운영 여부·상담 가능 여부는 방문 전에 확인해야 합니다."
    )

st.divider()
st.caption(
    "진로상담센터 안내 | 지역별 상담 기관을 찾기 위한 정보 서비스"
)
