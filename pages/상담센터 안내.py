
import html
import json
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="진로상담센터 찾기",
    page_icon="🧭",
    layout="wide",
)

# -------------------- 디자인 --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Noto Sans KR',sans-serif;}
.stApp {background:#f4f7fb;}
.block-container {max-width:1100px;padding-top:1.2rem;padding-bottom:3rem;}
.app-header {background:white;border:1px solid #e8edf3;border-radius:20px;padding:18px 22px;margin-bottom:16px;}
.brand {color:#203b5c;font-weight:800;font-size:1.2rem;}
.brand-sub {color:#7b8ca1;font-size:.82rem;margin-top:3px;}
.hero {background:linear-gradient(120deg,#1689e8,#42c7b5);border-radius:22px;padding:24px;color:white;margin-bottom:18px;}
.hero h1 {color:white;font-size:1.65rem;}
.hero p {color:#f3ffff;}
.section-title {color:#263a52;font-size:1.15rem;font-weight:800;margin:18px 0 10px;}
div.stButton>button {border-radius:12px;font-weight:700;min-height:2.7rem;}
div.stButton>button[kind="primary"] {background:linear-gradient(90deg,#2785e6,#31bcae);color:white;border:0;}
</style>
""", unsafe_allow_html=True)


# -------------------- 지역 데이터 --------------------
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
        "춘천시", "원주시", "강릉시", "동해시",
        "태백시", "속초시", "삼척시", "홍천군", "횡성군"
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
        "전주시", "군산시", "익산시", "정읍시",
        "남원시", "김제시", "완주군", "고창군", "부안군"
    ],
    "전라남도": [
        "목포시", "여수시", "순천시", "나주시",
        "광양시", "담양군", "고흥군", "보성군",
        "화순군", "해남군", "무안군"
    ],
    "경상북도": [
        "포항시", "경주시", "김천시", "안동시", "구미시",
        "영주시", "영천시", "상주시", "문경시", "경산시"
    ],
    "경상남도": [
        "창원시", "진주시", "통영시", "사천시",
        "김해시", "밀양시", "거제시", "양산시"
    ],
    "제주특별자치도": ["제주시", "서귀포시"],
}

CATEGORY_QUERIES = {
    "진로진학지원센터": ["진로진학지원센터", "진로진학센터"],
    "진로교육지원센터": ["진로교육지원센터", "진로교육센터"],
    "진로체험지원센터": ["진로체험지원센터", "진로체험센터"],
    "직업진로기관": ["직업진로상담", "직업상담센터", "고용복지플러스센터"],
}

HEADERS = {
    "User-Agent": "CareerCenterGuide/1.0 educational project"
}


# -------------------- 현재 위치 --------------------
def get_browser_location():
    """사용자가 허용한 경우에만 브라우저 위치를 가져옵니다."""
    try:
        from streamlit_geolocation import streamlit_geolocation

        loc = streamlit_geolocation()

        if not isinstance(loc, dict):
            return None

        lat = loc.get("latitude")
        lon = loc.get("longitude")

        if lat is None or lon is None:
            return None

        lat = float(lat)
        lon = float(lon)

        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon

    except Exception:
        return None

    return None


# -------------------- 장소 검색 --------------------
def search_places(query, limit=8, near=None):
    params = {
        "q": query,
        "format": "jsonv2",
        "limit": limit,
        "addressdetails": 1,
        "accept-language": "ko",
    }

    if near:
        params["lat"] = near[0]
        params["lon"] = near[1]

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers=HEADERS,
            timeout=12,
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError):
        return []

    results = []
    seen = set()

    if not isinstance(data, list):
        return results

    for item in data:
        name = (item.get("name") or "").strip()
        address = (item.get("display_name") or "").strip()

        if not name or item.get("lat") is None or item.get("lon") is None:
            continue

        searchable = f"{name} {address}".lower()

        # 진로·진학·직업 관련 기관만 후보로 표시
        if not any(word in searchable for word in (
            "진로", "진학", "직업", "고용"
        )):
            continue

        # 심리상담 기관과 혼동할 수 있는 결과 제외
        if any(word in searchable for word in (
            "심리상담", "정신건강", "청소년상담복지센터"
        )):
            continue

        key = (name.lower(), address.lower())

        if key in seen:
            continue

        seen.add(key)

        try:
            lat = float(item["lat"])
            lon = float(item["lon"])
        except (TypeError, ValueError):
            continue

        results.append({
            "name": name,
            "address": address or "주소 정보 없음",
            "lat": lat,
            "lon": lon,
            "map": (
                "https://www.google.com/maps/dir/?api=1"
                f"&destination={lat},{lon}"
            ),
        })

    return results


def search_centers(area, category, near=None):
    results = []
    seen = set()

    for keyword in CATEGORY_QUERIES.get(category, []):
        places = search_places(
            f"{area} {keyword}",
            limit=10,
            near=near,
        )

        for place in places:
            key = (place["name"], place["address"])

            if key not in seen:
                seen.add(key)
                results.append(place)

            if len(results) >= 10:
                return results

    return results


# -------------------- 앱 안의 지도 --------------------
def render_map(places, height=390):
    """검색된 센터들의 위치를 앱 내부 대화형 지도에 표시합니다."""
    valid = []

    for place in places:
        try:
            valid.append({
                "name": str(place["name"]),
                "address": str(place["address"]),
                "lat": float(place["lat"]),
                "lon": float(place["lon"]),
                "map": str(place["map"]),
            })
        except (KeyError, TypeError, ValueError):
            continue

    if not valid:
        st.info("지도에 표시할 위치가 없습니다.")
        return

    payload = json.dumps(
        valid,
        ensure_ascii=False
    ).replace("</", "<\\/")

    map_html = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <link rel="stylesheet"
       href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
      <style>
        html,body,#map {
          height:100%;
          margin:0;
          font-family:Arial,sans-serif;
        }
        .leaflet-popup-content {
          font-size:13px;
          line-height:1.5;
          max-width:230px;
        }
        .go {
          display:inline-block;
          margin-top:7px;
          padding:7px 10px;
          background:#2185e6;
          color:white!important;
          border-radius:8px;
          text-decoration:none;
          font-weight:bold;
        }
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <script>
        const places = __PLACES__;
        const map = L.map('map');

        L.tileLayer(
          'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          {
            maxZoom:19,
            attribution:'&copy; OpenStreetMap contributors'
          }
        ).addTo(map);

        const bounds = [];

        places.forEach(p => {
          const marker = L.marker([p.lat,p.lon]).addTo(map);

          const name = String(p.name)
            .replace(/&/g,'&amp;')
            .replace(/</g,'&lt;')
            .replace(/>/g,'&gt;');

          const address = String(p.address)
            .replace(/&/g,'&amp;')
            .replace(/</g,'&lt;')
            .replace(/>/g,'&gt;');

          marker.bindPopup(
            '<b>'+name+'</b><br>'+address+
            '<br><a class="go" href="'+p.map+
            '" target="_blank" rel="noopener">길찾기</a>'
          );

          bounds.push([p.lat,p.lon]);
        });

        if (bounds.length === 1) {
          map.setView(bounds[0],15);
        } else if (bounds.length > 1) {
          map.fitBounds(bounds,{padding:[25,25]});
        }
      </script>
    </body>
    </html>
    """.replace("__PLACES__", payload)

    components.html(
        map_html,
        height=height,
        scrolling=False,
    )


# -------------------- 검색 결과 표시 --------------------
def show_results(results, key_prefix="result"):
    if not results:
        st.warning(
            "검색 결과가 없어요. 지도 데이터에 정보가 없을 수 있습니다. "
            "다른 기관 유형이나 주변 지역도 검색해 보세요."
        )
        return

    st.success(f"진로·진학 관련 기관 후보 {len(results)}곳을 찾았어요.")

    st.markdown("#### 🗺️ 센터 위치 지도")
    render_map(results)

    for i, place in enumerate(results):
        with st.container(border=True):
            st.markdown(f"### 🏫 {place['name']}")
            st.write(f"📍 {place['address']}")

            col1, col2 = st.columns(2)

            with col1:
                st.link_button(
                    "길찾기",
                    place["map"],
                    use_container_width=True,
                )

            with col2:
                if st.button(
                    "♡ 관심 센터 저장",
                    key=f"{key_prefix}_fav_{i}",
                    use_container_width=True,
                ):
                    favorites = st.session_state.get("favorites", [])

                    exists = any(
                        f["name"] == place["name"]
                        and f["address"] == place["address"]
                        for f in favorites
                    )

                    if not exists:
                        favorites.append(place)

                    st.session_state["favorites"] = favorites
                    st.success("관심 센터에 저장했어요.")

            with st.expander("방문 전 확인 사항"):
                st.write(
                    "검색 결과는 지도 데이터 기반 후보입니다. "
                    "실제 진로상담 제공 여부, 대상 연령, 운영 시간과 "
                    "예약 방법은 기관 공식 홈페이지나 전화로 확인하세요."
                )


# -------------------- 상단 헤더 --------------------
st.markdown("""
<div class="app-header">
  <div class="brand">🧭 진로상담센터 찾기</div>
  <div class="brand-sub">나의 꿈을 향한 첫 번째 길찾기</div>
</div>
""", unsafe_allow_html=True)


home_tab, booking_tab, finder_tab, my_tab, community_tab = st.tabs([
    "🏠 홈",
    "📅 예약 준비",
    "🔎 센터 찾기",
    "👤 마이페이지",
    "💬 커뮤니티",
])


# ==================== 홈 ====================
with home_tab:
    st.markdown("""
    <div class="hero">
      <h1>내 꿈에 가까워지는<br>진로상담센터 찾기</h1>
      <p>내 주변의 진로·진학 전문 기관을 찾아보세요.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 📍 내 주변 진로상담센터 검색")

        c1, c2 = st.columns(2)

        with c1:
            province = st.selectbox(
                "시·도",
                list(REGIONS.keys()),
                key="home_province",
            )

        with c2:
            district = st.selectbox(
                "시·군·구",
                REGIONS[province],
                key="home_district",
            )

        category = st.selectbox(
            "기관 유형",
            list(CATEGORY_QUERIES.keys()),
            key="home_category",
        )

        if st.button("📍 현재 위치 사용", use_container_width=True):
            location = get_browser_location()

            if location:
                st.session_state["my_location"] = location
                st.success(
                    "현재 위치를 확인했어요. "
                    "검색할 때 주변 결과를 우선 참고합니다."
                )
            else:
                st.info(
                    "위치 정보를 받지 못했어요. "
                    "브라우저 위치 권한을 허용하거나 지역을 직접 선택해 주세요."
                )

        st.caption(
            "현재 위치 사용은 선택 사항입니다. "
            "위치 권한이 거부되거나 지원되지 않으면 지역을 직접 선택하세요."
        )

        if st.button(
            "🔎 진로상담센터 검색하기",
            type="primary",
            use_container_width=True,
        ):
            area = f"{province} {district}"

            with st.spinner("진로 관련 기관을 찾고 있어요..."):
                results = search_centers(
                    area,
                    category,
                    st.session_state.get("my_location"),
                )

            st.session_state["home_results"] = results
            st.session_state["home_area"] = area
            st.session_state["home_category"] = category

    st.markdown(
        '<div class="section-title">✨ 이용할 수 있는 기능</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    for col, emoji, label in [
        (c1, "📍", "지역별 센터 검색"),
        (c2, "🎓", "진로·진학 기관 정보"),
        (c3, "🗓️", "상담 준비 메모"),
    ]:
        with col:
            st.markdown(
                f'<div style="background:white;border:1px solid #e5ebf2;'
                f'border-radius:15px;padding:16px;text-align:center">'
                f'<div style="font-size:1.5rem">{emoji}</div>'
                f'<b>{label}</b></div>',
                unsafe_allow_html=True,
            )

    if "home_results" in st.session_state:
        st.markdown(
            '<div class="section-title">📌 검색 결과</div>',
            unsafe_allow_html=True,
        )
        show_results(st.session_state["home_results"], "home")


# ==================== 예약 준비 ====================
with booking_tab:
    st.markdown(
        '<div class="section-title">📅 상담 예약 준비</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "실제 예약을 접수하는 기능은 아니며, "
        "상담 전에 필요한 내용을 메모할 수 있어요."
    )

    with st.container(border=True):
        topic = st.selectbox(
            "상담 주제",
            [
                "진로 탐색",
                "학과 선택",
                "고등학교·대학교 진학",
                "직업 정보",
                "진로 변경",
            ],
        )

        preferred_date = st.date_input("희망 상담 날짜")

        note = st.text_area(
            "상담 때 물어보고 싶은 내용",
            placeholder="예: 관심 있는 학과와 관련 직업을 알고 싶어요.",
        )

        if st.button(
            "상담 준비 메모 저장",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["booking_note"] = {
                "topic": topic,
                "date": str(preferred_date),
                "note": note.strip(),
            }
            st.success("상담 준비 메모를 저장했어요.")

    if "booking_note" in st.session_state:
        memo = st.session_state["booking_note"]

        st.markdown("#### 저장한 메모")
        st.write(f"**주제:** {memo['topic']}")
        st.write(f"**희망 날짜:** {memo['date']}")
        st.write(f"**질문:** {memo['note'] or '작성한 내용 없음'}")


# ==================== 센터 찾기 ====================
with finder_tab:
    st.markdown(
        '<div class="section-title">🔎 지역별 진로 전문 기관</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        province2 = st.selectbox(
            "시·도",
            list(REGIONS.keys()),
            key="finder_province",
        )

    with c2:
        district2 = st.selectbox(
            "시·군·구",
            REGIONS[province2],
            key="finder_district",
        )

    category2 = st.selectbox(
        "기관 유형",
        list(CATEGORY_QUERIES.keys()),
        key="finder_category",
    )

    if st.button(
        "센터 검색",
        key="finder_search",
        type="primary",
        use_container_width=True,
    ):
        area2 = f"{province2} {district2}"

        with st.spinner("검색 중..."):
            st.session_state["finder_results"] = search_centers(
                area2,
                category2,
                st.session_state.get("my_location"),
            )

        st.session_state["finder_area"] = area2
        st.session_state["finder_category_saved"] = category2

    if "finder_results" in st.session_state:
        show_results(st.session_state["finder_results"], "finder")


# ==================== 마이페이지 ====================
with my_tab:
    st.markdown(
        '<div class="section-title">👤 마이페이지</div>',
        unsafe_allow_html=True,
    )

    nickname = st.text_input(
        "닉네임",
        value=st.session_state.get("nickname", ""),
        placeholder="닉네임을 입력하세요",
    )

    if st.button("닉네임 저장"):
        st.session_state["nickname"] = nickname.strip()
        st.success("닉네임을 저장했어요.")

    st.markdown("### ♡ 관심 센터")

    favorites = st.session_state.get("favorites", [])

    if favorites:
        for i, place in enumerate(favorites):
            with st.container(border=True):
                st.markdown(f"**🏫 {place['name']}**")
                st.caption(place["address"])
                st.link_button(
                    "길찾기",
                    place["map"],
                    key=f"favorite_map_{i}",
                )

        if st.button("관심 센터 전체 삭제"):
            st.session_state["favorites"] = []
            st.rerun()
    else:
        st.info(
            "아직 저장한 관심 센터가 없어요. "
            "검색 결과에서 저장할 수 있습니다."
        )

    st.markdown("### 📋 상담 준비 메모")

    if "booking_note" in st.session_state:
        memo = st.session_state["booking_note"]
        st.write(f"**주제:** {memo['topic']} · **희망 날짜:** {memo['date']}")
        st.write(memo["note"] or "추가 질문 없음")
    else:
        st.info("아직 저장한 상담 준비 메모가 없습니다.")


# ==================== 커뮤니티 ====================
with community_tab:
    st.markdown(
        '<div class="section-title">💬 진로 커뮤니티</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "예시 글과 직접 작성한 글은 현재 세션에서만 보관됩니다."
    )

    with st.container(border=True):
        st.markdown("### 🌱 어떤 학과가 나에게 맞을까요?")
        st.write(
            "관심 있는 과목과 좋아하는 활동을 정리하고, "
            "관련 학과의 수업과 진출 분야를 찾아보세요."
        )

    with st.container(border=True):
        st.markdown("### 🎓 상담 전에 준비하면 좋은 것")
        st.write(
            "궁금한 점을 2~3개 적고 관심 직업이나 학과를 정리해 가면 "
            "상담 시간을 더 잘 활용할 수 있어요."
        )

    title = st.text_input(
        "게시글 제목",
        placeholder="진로 고민을 적어 주세요",
    )

    body = st.text_area(
        "게시글 내용",
        placeholder="어떤 점이 고민인가요?",
    )

    if st.button(
        "게시글 등록",
        type="primary",
        use_container_width=True,
    ):
        if title.strip() and body.strip():
            posts = st.session_state.get("community_posts", [])

            posts.insert(0, {
                "title": title.strip(),
                "body": body.strip(),
            })

            st.session_state["community_posts"] = posts
            st.success("게시글을 등록했어요. 현재 세션에서만 보관됩니다.")
        else:
            st.warning("제목과 내용을 모두 입력해 주세요.")

    for post in st.session_state.get("community_posts", []):
        with st.container(border=True):
            st.markdown(f"### {html.escape(post['title'])}")
            st.write(post["body"])


# ==================== 하단 안내 ====================
st.divider()

st.caption(
    "진로상담센터 찾기 · 지도 데이터 기반 검색 서비스입니다. "
    "검색 결과는 전체 기관 목록이 아니며, 실제 진로상담 제공 여부와 "
    "운영 정보는 공식 채널에서 확인하세요."
)
