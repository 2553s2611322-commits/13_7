import streamlit as st
import requests
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="진로상담센터 찾기",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: #f4f7fb;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

.app-header {
    background: white;
    border: 1px solid #e8edf3;
    border-radius: 20px;
    padding: 18px 22px;
    margin-bottom: 16px;
}

.brand {
    color: #203b5c;
    font-weight: 800;
    font-size: 1.2rem;
}

.brand-sub {
    color: #7b8ca1;
    font-size: .78rem;
    margin-top: 3px;
}

.hero {
    background: linear-gradient(120deg, #1689e8, #42c7b5);
    border-radius: 22px;
    padding: 24px;
    color: white;
    margin-bottom: 18px;
}

.hero h1 {
    color: white;
    font-size: 1.65rem;
}

.hero p {
    color: #f3ffff;
}

.section-title {
    color: #263a52;
    font-size: 1.15rem;
    font-weight: 800;
    margin: 18px 0 10px;
}

.metric {
    background: white;
    border: 1px solid #e5ebf2;
    border-radius: 15px;
    padding: 14px;
    text-align: center;
}

.metric-number {
    font-size: 1.3rem;
    font-weight: 800;
    color: #217bd0;
}

.metric-label {
    color: #7d8da0;
    font-size: .78rem;
}

div.stButton > button {
    border-radius: 12px;
    border: 0;
    font-weight: 700;
    min-height: 2.7rem;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #2785e6, #31bcae);
    color: white;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #e5ebf2;
    border-radius: 12px;
}

@media (max-width: 650px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 19px;
    }

    .hero h1 {
        font-size: 1.4rem;
    }
}
</style>
""", unsafe_allow_html=True)


# 지역 정보
REGIONS = {
    "서울특별시": [
        "종로구", "중구", "용산구", "성동구", "광진구",
        "동대문구", "중랑구", "성북구", "강북구", "도봉구",
        "노원구", "은평구", "서대문구", "마포구", "양천구",
        "강서구", "구로구", "금천구", "영등포구", "동작구",
        "관악구", "서초구", "강남구", "송파구", "강동구"
    ],
    "부산광역시": [
        "중구", "서구", "동구", "영도구", "부산진구",
        "동래구", "남구", "북구", "해운대구", "사하구",
        "금정구", "강서구", "연제구", "수영구", "사상구", "기장군"
    ],
    "대구광역시": [
        "중구", "동구", "서구", "남구", "북구",
        "수성구", "달서구", "달성군", "군위군"
    ],
    "인천광역시": [
        "중구", "동구", "미추홀구", "연수구", "남동구",
        "부평구", "계양구", "서구", "강화군", "옹진군"
    ],
    "광주광역시": ["동구", "서구", "남구", "북구", "광산구"],
    "대전광역시": ["동구", "중구", "서구", "유성구", "대덕구"],
    "울산광역시": ["중구", "남구", "동구", "북구", "울주군"],
    "세종특별자치시": ["세종시"],
    "경기도": [
        "수원시", "성남시", "고양시", "용인시", "부천시",
        "안산시", "안양시", "남양주시", "화성시", "평택시",
        "의정부시", "파주시", "김포시", "광명시", "군포시",
        "오산시", "이천시", "양주시", "구리시", "안성시",
        "포천시", "하남시", "의왕시", "여주시", "양평군",
        "가평군", "연천군", "동두천시", "과천시", "시흥시", "광주시"
    ],
    "강원특별자치도": [
        "춘천시", "원주시", "강릉시", "동해시", "태백시",
        "속초시", "삼척시", "홍천군", "횡성군"
    ],
    "충청북도": [
        "청주시", "충주시", "제천시", "보은군", "옥천군",
        "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"
    ],
    "충청남도": [
        "천안시", "공주시", "보령시", "아산시", "서산시",
        "논산시", "계룡시", "당진시", "홍성군", "예산군"
    ],
    "전북특별자치도": [
        "전주시", "군산시", "익산시", "정읍시", "남원시",
        "김제시", "완주군", "고창군", "부안군"
    ],
    "전라남도": [
        "목포시", "여수시", "순천시", "나주시", "광양시",
        "담양군", "고흥군", "보성군", "화순군", "해남군", "무안군"
    ],
    "경상북도": [
        "포항시", "경주시", "김천시", "안동시", "구미시",
        "영주시", "영천시", "상주시", "문경시", "경산시"
    ],
    "경상남도": [
        "창원시", "진주시", "통영시", "사천시",
        "김해시", "밀양시", "거제시", "양산시"
    ],
    "제주특별자치도": ["제주시", "서귀포시"]
}

CATEGORY_QUERIES = {
    "진로진학지원센터": [
        "진로진학지원센터",
        "진로진학센터"
    ],
    "진로교육지원센터": [
        "진로교육지원센터",
        "진로교육센터"
    ],
    "진로체험지원센터": [
        "진로체험지원센터",
        "진로체험센터"
    ],
    "직업진로기관": [
        "직업진로상담",
        "직업상담센터",
        "고용복지플러스센터"
    ]
}

HEADERS = {
    "User-Agent": "CareerCenterGuide/1.0 educational project"
}


def get_location():
    try:
        from streamlit_geolocation import streamlit_geolocation

        location = streamlit_geolocation()

        if not isinstance(location, dict):
            return None

        lat = location.get("latitude")
        lon = location.get("longitude")

        if lat is None or lon is None:
            return None

        lat = float(lat)
        lon = float(lon)

        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon

    except Exception:
        return None

    return None


def reverse_geocode(lat, lon):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "jsonv2",
                "accept-language": "ko"
            },
            headers=HEADERS,
            timeout=8
        )

        response.raise_for_status()
        address = response.json().get("address", {})

        return (
            address.get("city")
            or address.get("town")
            or address.get("county")
            or address.get("state")
            or "현재 위치"
        )

    except (
        requests.RequestException,
        ValueError,
        TypeError
    ):
        return "현재 위치"


def search_places(query, lat=None, lon=None, limit=8):
    params = {
        "q": query,
        "format": "jsonv2",
        "limit": limit,
        "addressdetails": 1,
        "accept-language": "ko"
    }

    if lat is not None and lon is not None:
        params.update({
            "lat": lat,
            "lon": lon
        })

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers=HEADERS,
            timeout=12
        )

        response.raise_for_status()
        data = response.json()

        places = []
        seen = set()

        if not isinstance(data, list):
            return []

        for item in data:
            name = (item.get("name") or "").strip()
            address = (item.get("display_name") or "").strip()

            if not name:
                continue

            if item.get("lat") is None or item.get("lon") is None:
                continue

            key = (name.lower(), address.lower())

            if key in seen:
                continue

            seen.add(key)

            try:
                latitude = float(item["lat"])
                longitude = float(item["lon"])
            except (TypeError, ValueError):
                continue

            places.append({
                "name": name,
                "address": address or "주소 정보 없음",
                "lat": latitude,
                "lon": longitude,
                "map": (
                    "https://www.openstreetmap.org/?mlat="
                    + str(latitude)
                    + "&mlon="
                    + str(longitude)
                    + "#map=16/"
                    + str(latitude)
                    + "/"
                    + str(longitude)
                )
            })

        return places

    except (
        requests.RequestException,
        ValueError,
        TypeError
    ):
        return []


def search_centers(area, category, location=None):
    if location:
        lat, lon = location
    else:
        lat, lon = None, None

    results = []
    seen = set()

    for keyword in CATEGORY_QUERIES[category]:
        found = search_places(
            f"{area} {keyword}",
            lat,
            lon
        )

        for place in found:
            name = place["name"].lower()

            if not any(
                word in name
                for word in ("진로", "진학", "직업", "고용")
            ):
                continue

            if any(
                word in name
                for word in ("심리상담", "정신건강", "청소년상담복지")
            ):
                continue

            key = (place["name"], place["address"])

            if key not in seen:
                seen.add(key)
                results.append(place)

            if len(results) >= 10:
                return results

    return results


def map_link(area, category="진로진학센터"):
    query = quote(f"{area} {category}")
    return f"https://www.google.com/maps/search/{query}"


# ---------- 상단 헤더 ----------
st.markdown("""
<div class="app-header">
    <div class="brand">🧭 진로상담센터 찾기</div>
    <div class="brand-sub">나의 꿈을 향한 첫 번째 길찾기</div>
</div>
""", unsafe_allow_html=True)


# ---------- 메뉴 ----------
home_tab, booking_tab, finder_tab, my_tab, community_tab = st.tabs([
    "🏠 홈",
    "📅 예약",
    "🔎 센터 찾기",
    "👤 마이페이지",
    "💬 커뮤니티"
])


# ---------- 홈 ----------
with home_tab:
    st.markdown("""
    <div class="hero">
        <h1>내 꿈에 가까워지는<br>진로상담센터 찾기</h1>
        <p>내 주변의 진로·진학 전문 기관을 찾아보세요.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 📍 내 주변 진로상담센터 검색")

        col1, col2 = st.columns(2)

        with col1:
            province = st.selectbox(
                "시·도",
                list(REGIONS.keys()),
                key="home_province"
            )

        with col2:
            district = st.selectbox(
                "시·군·구",
                REGIONS[province],
                key="home_district"
            )

        category = st.selectbox(
            "기관 유형",
            list(CATEGORY_QUERIES.keys()),
            key="home_category"
        )

        col3, col4 = st.columns([1, 2])

        with col3:
            if st.button(
                "📍 현재 위치 사용",
                use_container_width=True
            ):
                location = get_location()

                if location:
                    st.session_state["my_location"] = location
                    st.session_state["my_area"] = reverse_geocode(
                        *location
                    )
                    st.success(
                        f"위치를 확인했어요: "
                        f"{st.session_state['my_area']}"
                    )
                else:
                    st.warning(
                        "위치 권한을 확인하거나 지역을 직접 선택해 주세요."
                    )

        with col4:
            if st.session_state.get("my_location"):
                st.caption("현재 위치를 검색에 활용할 수 있어요.")
            else:
                st.caption(
                    "위치 권한은 선택 사항이에요. "
                    "지역을 직접 선택해도 됩니다."
                )

        area = f"{province} {district}"

        if st.button(
            "🔎 진로상담센터 검색하기",
            type="primary",
            use_container_width=True
        ):
            with st.spinner("진로 관련 기관을 찾고 있어요..."):
                results = search_centers(
                    area,
                    category,
                    st.session_state.get("my_location")
                )

            st.session_state["centers"] = results
            st.session_state["search_area"] = area
            st.session_state["search_category"] = category

    st.markdown(
        '<div class="section-title">✨ 이런 서비스를 이용할 수 있어요</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric">
            <div class="metric-number">📍</div>
            <div class="metric-label">주변 센터 찾기</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric">
            <div class="metric-number">🎓</div>
            <div class="metric-label">진로·진학 정보</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric">
            <div class="metric-number">🗓️</div>
            <div class="metric-label">상담 준비하기</div>
        </div>
        """, unsafe_allow_html=True)

    if "centers" in st.session_state:
        results = st.session_state["centers"]
        area = st.session_state.get("search_area", "선택 지역")
        category = st.session_state.get(
            "search_category",
            "진로진학지원센터"
        )

        st.markdown(
            '<div class="section-title">📌 검색 결과</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"[🗺️ 지도에서 더 찾아보기]({map_link(area, category)})"
        )

        if results:
            st.success(f"진로 관련 검색 결과 {len(results)}곳")

            st.map(pd.DataFrame([
                {"lat": place["lat"], "lon": place["lon"]}
                for place in results
            ]))

            for index, place in enumerate(results):
                with st.container(border=True):
                    st.markdown("**🧭 진로·진학 관련 기관 후보**")
                    st.markdown(f"### 🏫 {place['name']}")
                    st.write(f"📍 {place['address']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.link_button(
                            "위치 보기",
                            place["map"],
                            use_container_width=True
                        )

                    with col2:
                        if st.button(
                            "♡ 관심 센터 저장",
                            key=f"fav_{index}",
                            use_container_width=True
                        ):
                            favorites = st.session_state.get(
                                "favorites", []
                            )

                            if place not in favorites:
                                favorites.append(place)

                            st.session_state["favorites"] = favorites
                            st.success("관심 센터에 저장했어요.")

                    with st.expander("센터 이용 전 확인하기"):
                        st.write(
                            "상담 대상, 상담 분야, 운영 시간, 예약 방법은 "
                            "해당 기관의 공식 홈페이지나 전화로 확인하세요."
                        )

        else:
            st.warning(
                "조건에 맞는 기관을 지도 데이터에서 찾지 못했어요. "
                "기관이 없다는 뜻은 아닙니다."
            )

            st.markdown(
                f"[Google 지도에서 다시 검색하기]"
                f"({map_link(area, category)})"
            )


# ---------- 예약 ----------
with booking_tab:
    st.markdown(
        '<div class="section-title">📅 상담 예약 준비</div>',
        unsafe_allow_html=True
    )

    st.write(
        "상담 예약 전에 관심 분야와 가능한 날짜를 정리해 보세요."
    )

    with st.container(border=True):
        topic = st.selectbox(
            "상담하고 싶은 주제",
            [
                "진로 탐색",
                "학과 선택",
                "고등학교·대학교 진학",
                "직업 정보",
                "진로 변경"
            ]
        )

        preferred_date = st.date_input("희망 상담 날짜")

        note = st.text_area(
            "상담 때 물어보고 싶은 내용",
            placeholder="예: 관심 있는 학과와 관련 직업을 알고 싶어요."
        )

        if st.button(
            "예약 메모 저장",
            type="primary",
            use_container_width=True
        ):
            st.session_state["booking_note"] = {
                "topic": topic,
                "date": str(preferred_date),
                "note": note
            }

            st.success(
                "예약 준비 메모를 저장했어요. "
                "실제 예약은 기관의 공식 채널에서 진행해야 해요."
            )

    if "booking_note" in st.session_state:
        booking = st.session_state["booking_note"]

        st.markdown("#### 저장한 예약 메모")
        st.write(f"**주제:** {booking['topic']}")
        st.write(f"**희망 날짜:** {booking['date']}")
        st.write(f"**질문:** {booking['note'] or '작성한 내용 없음'}")

    st.info(
        "이 앱은 예약 메모 기능을 제공하며, "
        "실제 상담 예약을 접수하거나 확정하지는 않습니다."
    )


# ---------- 센터 찾기 ----------
with finder_tab:
    st.markdown(
        '<div class="section-title">🔎 진로 전문 기관 찾기</div>',
        unsafe_allow_html=True
    )

    st.write(
        "지역과 기관 유형을 선택해 진로·진학 관련 기관을 검색하세요."
    )

    col1, col2 = st.columns(2)

    with col1:
        province2 = st.selectbox(
            "시·도 선택",
            list(REGIONS.keys()),
            key="finder_province"
        )

    with col2:
        district2 = st.selectbox(
            "시·군·구 선택",
            REGIONS[province2],
            key="finder_district"
        )

    category2 = st.selectbox(
        "기관 유형 선택",
        list(CATEGORY_QUERIES.keys()),
        key="finder_category"
    )

    if st.button(
        "센터 검색",
        key="finder_search",
        type="primary",
        use_container_width=True
    ):
        area2 = f"{province2} {district2}"

        with st.spinner("검색 중..."):
            results2 = search_centers(
                area2,
                category2,
                st.session_state.get("my_location")
            )

        st.session_state["finder_results"] = results2
        st.session_state["finder_area"] = area2
        st.session_state["finder_category_result"] = category2

    if "finder_results" in st.session_state:
        results2 = st.session_state["finder_results"]
        area2 = st.session_state.get(
            "finder_area",
            f"{province2} {district2}"
        )
        category2 = st.session_state.get(
            "finder_category_result",
            category2
        )

        st.markdown(
            f"[Google 지도에서 추가 검색하기]"
            f"({map_link(area2, category2)})"
        )

        if results2:
            st.map(pd.DataFrame([
                {"lat": place["lat"], "lon": place["lon"]}
                for place in results2
            ]))

            for place in results2:
                with st.container(border=True):
                    st.markdown(f"### 🧭 {place['name']}")
                    st.write(place["address"])
                    st.link_button("지도에서 위치 보기", place["map"])

        else:
            st.warning(
                "검색 결과가 없어요. 지도 데이터에 정보가 없을 수 있어요."
            )

            st.markdown(
                f"[지도에서 다시 검색하기]({map_link(area2, category2)})"
            )


# ---------- 마이페이지 ----------
with my_tab:
    st.markdown(
        '<div class="section-title">👤 마이페이지</div>',
        unsafe_allow_html=True
    )

    st.write(
        "저장한 관심 센터와 상담 준비 메모를 확인할 수 있어요."
    )

    with st.container(border=True):
        st.markdown("### 🙋 사용자 정보")

        nickname = st.text_input(
            "닉네임",
            value=st.session_state.get("nickname", ""),
            placeholder="닉네임을 입력하세요"
        )

        if st.button("닉네임 저장"):
            st.session_state["nickname"] = nickname
            st.success("닉네임을 저장했어요.")

    st.markdown("### ♡ 관심 센터")

    favorites = st.session_state.get("favorites", [])

    if favorites:
        for place in favorites:
            with st.container(border=True):
                st.markdown(f"**{place['name']}**")
                st.caption(place["address"])
                st.markdown(f"[지도 보기]({place['map']})")
    else:
        st.info(
            "아직 저장한 관심 센터가 없어요. "
            "홈의 검색 결과에서 저장할 수 있어요."
        )

    st.markdown("### 📋 상담 메모")

    if "booking_note" in st.session_state:
        booking = st.session_state["booking_note"]

        st.write(
            f"주제: {booking['topic']} · "
            f"희망 날짜: {booking['date']}"
        )

        st.write(booking["note"] or "추가 질문 없음")
    else:
        st.info("아직 저장한 상담 메모가 없어요.")


# ---------- 커뮤니티 ----------
with community_tab:
    st.markdown(
        '<div class="section-title">💬 진로 커뮤니티</div>',
        unsafe_allow_html=True
    )

    st.write(
        "진로 고민과 정보를 나누는 공간입니다. "
        "아래 게시글은 예시이며 실제 이용자 게시글이 아닙니다."
    )

    with st.container(border=True):
        st.markdown("### 🌱 어떤 학과가 나에게 맞을까요?")
        st.caption("진로 고민 · 예시 게시글")

        st.write(
            "관심 있는 과목과 좋아하는 활동을 정리한 뒤, "
            "관련 학과의 수업과 진출 분야를 찾아보면 도움이 돼요."
        )

    with st.container(border=True):
        st.markdown("### 🎓 진로상담을 받기 전에 준비할 것")
        st.caption("상담 준비 · 예시 게시글")

        st.write(
            "궁금한 점을 2~3개 적고 관심 직업이나 학과를 정리해 가면 "
            "상담 시간을 더 잘 활용할 수 있어요."
        )

    st.markdown("### ✍️ 나의 진로 고민 작성")

    post_title = st.text_input(
        "제목",
        placeholder="진로 고민을 적어 주세요"
    )

    post_body = st.text_area(
        "내용",
        placeholder="어떤 점이 고민인가요?"
    )

    if st.button(
        "게시글 등록",
        type="primary",
        use_container_width=True
    ):
        if post_title.strip() and post_body.strip():
            posts = st.session_state.get("community_posts", [])

            posts.insert(0, {
                "title": post_title.strip(),
                "body": post_body.strip()
            })

            st.session_state["community_posts"] = posts

            st.success(
                "게시글을 등록했어요. 현재 세션에서만 보관됩니다."
            )
        else:
            st.warning("제목과 내용을 모두 입력해 주세요.")

    for post in st.session_state.get("community_posts", []):
        with st.container(border=True):
            st.markdown(f"### {post['title']}")
            st.write(post["body"])


st.divider()

st.caption(
    "진로상담센터 찾기 · 지도 데이터 기반 검색 서비스. "
    "검색 결과는 전체 기관 목록이 아니며, 실제 상담 제공 여부와 "
    "운영 정보는 공식 채널에서 확인하세요."
)
