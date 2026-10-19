import json
import streamlit as st
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 모던 Custom CSS (깔끔하고 정돈된 스타일링)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화·드라마 속 진로 탐색",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
    /* 전체 배경 및 폰트 레이아웃 정돈 */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }
    
    /* 타이틀 디자인 */
    .title-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748B;
        font-weight: 400;
    }

    /* 카드 엘리먼트 스타일 */
    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .content-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }
    .content-text {
        font-size: 0.98rem;
        color: #334155;
        line-height: 1.6;
    }
    
    /* 태그 및 구분선 */
    .badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 검증된 실존 작품 및 실제 포스터 DB (오류 방지 및 빠른 응답용)
# -----------------------------------------------------------------------------
BUILTIN_DATA = {
    "요리사": {
        "title": "파스타 (MBC 드라마)",
        "poster": "https://image.yes24.com/momo/TopCate85/MidCate08/8472831.jpg",
        "video_url": "https://www.youtube.com/watch?v=S374IAnM2f8",
        "story": "이탈리안 레스토랑 '라스페라'를 배경으로, 음식에 대한 열정과 사랑을 가진 주방 보조 서유경이 셰프 최현욱 아래에서 완벽한 요리사로 성장해가는 과정을 그린 드라마입니다.",
        "job_desc": "요리사(셰프)는 식재료를 선별하고 미각적·시각적으로 뛰어난 음식을 만듭니다. 주방 위생 및 정교한 조리 기법, 그리고 팀원들과의 신속하고 명확한 소통 능력이 요구됩니다."
    },
    "건축가": {
        "title": "건축학개론 (영화)",
        "poster": "https://i.namu.wiki/i/otf8tOY_lb8MyTzXHsaEVM-NodcB5-JYvwFvZTfu3sdmAd4LkLBDQqiNdTKPMRrxy2n7QwvnDt5j7RqPtLHElw.webp",
        "video_url": "https://www.youtube.com/watch?v=J3mR6b5K_qY",
        "story": "생전 처음 집을 지어달라며 찾아온 대학 시절 첫사랑 서연과, 서연을 위해 제주도에 아름다운 집을 집 설계해 나가는 건축가 승민의 이야기를 담은 로맨스 영화입니다.",
        "job_desc": "건축가는 사용자의 라이프스타일과 니즈를 반영해 건축물을 디자인하고 설계합니다. 공간에 대한 미적 감각, 공학적 지식, 의뢰인과의 커뮤니케이션 능력이 필수적입니다."
    },
    "검사": {
        "title": "비밀의 숲 (tvN 드라마)",
        "poster": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcTOEu5atgSLm4LlHZDCgF3kOW8EP1CD_FSaLBsHCAurkjwUJ6bjMbqHS84PU_Eho_2mwAwos6rbVsbv4zY",
        "video_url": "https://www.youtube.com/watch?v=2e6M6qW93v4",
        "story": "뇌수술로 감정을 잃어버린 외톨이 검사 황시목이 정의롭고 따뜻한 형사 한여진과 함께 검찰 내부의 스폰서 살인사건과 그 뒤에 숨겨진 거대한 비리를 파헤치는 추적극입니다.",
        "job_desc": "검사는 사건 수사, 공소 제기, 재판 진행 등 법적 정의를 실현하는 공무원입니다. 철저한 법률 지식, 논리적 분석력, 도덕성과 공정함이 요구됩니다."
    },
    "프로그래머": {
        "title": "스타트업 (tvN 드라마)",
        "poster": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQEf5utUafLG-gmwX_W7ZL94vyLwDsAfDz6Uy8iOnkrg3t5hVEu-SAvV-Jas8al817dJmdEbJz9lWg1Hks",
        "video_url": "https://www.youtube.com/watch?v=BemKyzbLDkc",
        "story": "한국의 샌드박스에서 성공을 꿈꾸며 스타트업에 뛰어든 청춘들의 시작과 성장을 그린 드라마로, 좌절을 딛고 인공지능 알고리즘을 구현해 나가는 과정을 담고 있습니다.",
        "job_desc": "소프트웨어 개발자/프로그래머는 프로그래밍 언어를 사용하여 소프트웨어나 서비스 시스템을 개발합니다. 문제 해결력, 논리적 사고, 새로운 기술 습득 능력이 핵심입니다."
    }
}

# 검색 전에는 아무것도 보이지 않도록 기본값 초기화
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

def set_query(query_text):
    st.session_state["search_query"] = query_text

# -----------------------------------------------------------------------------
# 3. Gemini AI 연동 함수 (실존 작품 검색 제약 조건 강화)
# -----------------------------------------------------------------------------
def get_job_info_from_gemini(job_name):
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = f"""
        사용자가 입력한 직업/진로: '{job_name}'
        
        반드시 '실제로 존재하고 개봉/방영된' 대한민국 또는 글로벌 유명 영화나 드라마 1편을 선정해주세요.
        가상의 작품이나 실존하지 않는 제목은 절대로 생성하지 마세요.
        
        다음 JSON 형식으로만 정확히 답변해주세요:
        {{
            "title": "실제 작품 제목 (영화/드라마 구분)",
            "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80",
            "video_url": "",
            "story": "해당 실제 작품의 주요 줄거리 (2~3문장)",
            "job_desc": "해당 직업에 대한 설명과 작중 역할, 필요 역량 (2~3문장)"
        }}
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception:
        return None

# -----------------------------------------------------------------------------
# 4. 헤더 영역 (깔끔하고 심플한 디자인)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="title-container">
    <div class="main-title">🎬 영화·드라마 속 진로 탐색</div>
    <div class="sub-title">궁금한 직업이나 진로를 입력하여 스크린 속 직업 세계를 탐색해보세요.</div>
</div>
""", unsafe_allow_html=True)

# 검색창 영역
search_input = st.text_input(
    "직업 입력", 
    value=st.session_state["search_query"],
    placeholder="탐색하고 싶은 직업/진로를 입력하세요 (예: 요리사, 검사, 건축가, 프로그래머...)",
    label_visibility="collapsed"
)

# 추천 키워드 버튼
st.markdown("<p style='font-size: 0.85rem; color: #64748B; margin-bottom: 0.5rem;'>💡 <b>추천 키워드:</b></p>", unsafe_allow_html=True)
c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 2])
if c1.button("🍳 요리사", use_container_width=True): set_query("요리사")
if c2.button("📐 건축가", use_container_width=True): set_query("건축가")
if c3.button("⚖️ 검사", use_container_width=True): set_query("검사")
if c4.button("💻 프로그래머", use_container_width=True): set_query("프로그래머")

current_job = search_input.strip() if search_input else st.session_state["search_query"]

# -----------------------------------------------------------------------------
# 5. 검색 결과 영역 (진로 입력 전에는 아무것도 띄우지 않음)
# -----------------------------------------------------------------------------
if current_job:
    st.markdown("<br>", unsafe_allow_html=True)
    
    data = None
    if current_job in BUILTIN_DATA:
        data = BUILTIN_DATA[current_job]
    else:
        with st.spinner(f"'{current_job}' 관련 실제 작품과 진로 정보 검색 중..."):
            data = get_job_info_from_gemini(current_job)
    
    if data:
        # 좌측: 포스터 & 영상(있는 경우만), 우측: 정보
        col_poster, col_info = st.columns([1, 1.4], gap="large")
        
        with col_poster:
            # 실존 작품 포스터 띄우기
            poster_url = data.get("poster")
            if poster_url:
                try:
                    st.image(poster_url, use_column_width=True)
                except Exception:
                    st.image("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80", use_column_width=True)
            
            # 하이라이트 영상 (유효한 링크가 존재할 경우에만 깔끔하게 출력)
            video_url = data.get("video_url")
            if video_url and ("youtube.com" in video_url or "youtu.be" in video_url):
                st.markdown("<div style='margin-top: 1rem;'><b>🎥 작품 하이라이트</b></div>", unsafe_allow_html=True)
                try:
                    st.video(video_url)
                except Exception:
                    pass  # 에러 발생 시 영상 영역을 완전히 감춤

        with col_info:
            st.markdown(f'<span class="badge">관련 대표 작품</span>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin-top:0; color:#0F172A; font-weight:700;'>{data.get('title', '작품 정보')}</h2>", unsafe_allow_html=True)
            
            # 줄거리 카트
            st.markdown(f"""
            <div class="content-box">
                <div class="content-label">📖 작품 줄거리</div>
                <div class="content-text">{data.get('story', '줄거리 정보가 없습니다.')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 진로/직업 소개 카드
            st.markdown(f"""
            <div class="content-box">
                <div class="content-label">💼 '{current_job}' 진로·직업 소개</div>
                <div class="content-text">{data.get('job_desc', '직업 정보가 없습니다.')}</div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning(f"'{current_job}'에 대한 정보를 찾지 못했습니다. 다른 직업명(예: 요리사, 검사, 건축가 등)으로 검색해보세요.")
