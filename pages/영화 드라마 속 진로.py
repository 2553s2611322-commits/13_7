import json
import streamlit as st
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 모던 Custom CSS (깔끔한 UI 레이아웃)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화·드라마 속 진로 탐색기",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
    /* 전체 메인 컨테이너 최대 너비 및 여백 설정 */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3.5rem;
        max-width: 1050px;
    }
    
    /* 헤더 스타일링 */
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
        font-size: 1.05rem;
        color: #64748B;
        font-weight: 400;
    }

    /* 카드 스타일링 */
    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.3rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .content-label {
        font-size: 0.88rem;
        font-weight: 700;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .content-text {
        font-size: 0.98rem;
        color: #334155;
        line-height: 1.65;
    }
    
    /* 태그 배지 */
    .badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        margin-bottom: 0.75rem;
    }
    
    /* 이미지 둥근 테두리 처리 */
    img {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 검증된 내장 DB (이미지/영상 불러오기 안전 처리)
# -----------------------------------------------------------------------------
BUILTIN_DATA = {
    "요리사": {
        "title": "파스타 (MBC 드라마)",
        "poster": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=700&q=80",
        "video_url": "https://www.youtube.com/watch?v=S374IAnM2f8",
        "story": "이탈리안 레스토랑 '라스페라'를 배경으로, 음식에 대한 뜨거운 열정과 사랑을 가진 주방 보조 서유경이 까다로운 셰프 최현욱 아래에서 완벽한 요리사로 성장해가는 과정을 그린 일류 주방의 생생한 이야기입니다.",
        "job_desc": "요리사(셰프)는 신선한 식재료를 선별하고 창의적인 조리법으로 최고의 요리를 만듭니다. 고도의 집중력과 미각, 청결한 주방 위생 관리, 그리고 압박감이 큰 주방 환경 속에서 팀원들과 신속히 협업하는 리더십이 요구됩니다.",
        "skills": "식재료 이해도, 메뉴 기획, 주방 위생 관리, 팀 커뮤니케이션, 미각적·시각적 감각",
        "related_jobs": "푸드스타일리스트, 메뉴 개발자, 외식업 컨설턴트, 소믈리에"
    },
    "건축가": {
        "title": "건축학개론 (영화)",
        "poster": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=700&q=80",
        "video_url": "https://www.youtube.com/watch?v=J3mR6b5K_qY",
        "story": "생전 처음 집을 지어달라며 찾아온 대학 시절 첫사랑 서연과, 서연을 위해 제주도에 아름다운 집을 설계해 나가는 건축가 승민의 공간 완성 및 감성적인 기억 재생 이야기입니다.",
        "job_desc": "건축가는 사용자의 삶의 방식과 니즈를 다각도로 분석하여 건축물을 기획하고 설계합니다. 공간에 대한 미적 감각, 공학적/구조적 안전 지식, 그리고 의뢰인의 요청을 설계도로 도출해내는 원활한 소통 능력이 필수적입니다.",
        "skills": "공간 디자인 및 캐드(CAD) 설계를 위한 툴 활용, 건축 법규 및 구조 이해, 사용자 니즈 파악력, 현장 감리",
        "related_jobs": "인테리어 디자이너, 도시계획가, 조경설계사, 건축시공기술자"
    },
    "검사": {
        "title": "비밀의 숲 (tvN 드라마)",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=700&q=80",
        "video_url": "https://www.youtube.com/watch?v=2e6M6qW93v4",
        "story": "뇌수술로 감정을 잃어버린 외톨이 검사 황시목이 정의롭고 따뜻한 형사 한여진과 함께 검찰 내부의 스폰서 살인사건과 그 뒤에 숨겨진 거대한 조직 비리를 파헤치는 긴장감 넘치는 추적극입니다.",
        "job_desc": "검사는 사건을 수사하고 공소를 제기하며 재판 과정에 참여하여 법적 정의를 실현합니다. 방대한 수사 기록을 엄밀히 분석하는 논리력, 흔들리지 않는 공정함, 도덕성 및 강한 법률 지식이 요구됩니다.",
        "skills": "형사법률 지식, 증거 분석 및 수사력, 논리적 논증 및 변론, 공정성 및 직업 윤리",
        "related_jobs": "변호사, 판사, 경찰 수사관, 법률 자문위원"
    },
    "프로그래머": {
        "title": "스타트업 (tvN 드라마)",
        "poster": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=700&q=80",
        "video_url": "https://www.youtube.com/watch?v=BemKyzbLDkc",
        "story": "한국의 샌드박스에서 성공을 꿈꾸며 스타트업에 뛰어든 청춘들의 시작과 성장을 그린 드라마로, AI 알고리즘을 개발하며 다양한 기술적 난관과 한계를 극복해가는 과정을 담고 있습니다.",
        "job_desc": "소프트웨어 개발자/프로그래머는 아이디어를 프로그래밍 언어를 통해 실제 구동되는 시스템이나 앱 서비스로 실체화합니다. 문제 해결 능력, 복잡한 알고리즘 설계 능력, 최신 기술 트렌드 학습 의지가 핵심입니다.",
        "skills": "프로그래밍 언어(Python, Java 등), 데이터구조 및 알고리즘, 시스템 아키텍처 설계, 디버깅 및 문제해결",
        "related_jobs": "AI 연구원, 데이터 엔지니어, 보안 전문가, 시스템 아키텍트"
    }
}

# 검색 세션 상태 관리
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

def set_query(query_text):
    st.session_state["search_query"] = query_text

# -----------------------------------------------------------------------------
# 3. Gemini API 연동 (풍부한 데이터 구조 반환)
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
        
        반드시 실제로 개봉/방영된 대한민국 또는 글로벌 유명 영화나 드라마 1편을 선정해주세요.
        가상의 작품이나 실존하지 않는 제목은 절대 금지합니다.
        
        다음 JSON 구조로만 정확히 답변하세요. 부연설명은 포함하지 마세요.
        {{
            "title": "실제 작품 제목 (영화 또는 드라마 구분)",
            "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=700&q=80",
            "video_url": "",
            "story": "해당 실제 작품의 주요 줄거리 (3~4문장으로 상세히)",
            "job_desc": "해당 직업의 역할, 작업 방식, 현장 모습 및 의미 (3~4문장으로 상세히)",
            "skills": "해당 직업을 위해 필요한 핵심 역량 및 기술 (쉼표로 구분)",
            "related_jobs": "연관되거나 발전시킬 수 있는 확장 진로 분야 (쉼표로 구분)"
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
# 4. 헤더 영역 (깔끔한 UI)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="title-container">
    <div class="main-title">🎬 영화·드라마 속 진로 탐색기</div>
    <div class="sub-title">궁금한 직업이나 진로를 입력하여 스크린 속 직업의 세계와 세부 정보를 확인해보세요.</div>
</div>
""", unsafe_allow_html=True)

# 검색 입력창
search_input = st.text_input(
    "직업 입력", 
    value=st.session_state["search_query"],
    placeholder="진로 또는 직업명을 입력하세요 (예: 요리사, 검사, 건축가, 프로그래머...)",
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
# 5. 검색 결과 영역 (입력 전에는 아무것도 출력하지 않음)
# -----------------------------------------------------------------------------
if current_job:
    st.markdown("<br>", unsafe_allow_html=True)
    
    data = None
    if current_job in BUILTIN_DATA:
        data = BUILTIN_DATA[current_job]
    else:
        with st.spinner(f"'{current_job}' 관련 작품과 진로 상세 정보를 분석 중입니다..."):
            data = get_job_info_from_gemini(current_job)
    
    if data:
        col_poster, col_info = st.columns([1, 1.35], gap="large")
        
        with col_poster:
            # 이미지 출력 예외 처리
            poster_url = data.get("poster")
            fallback_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=700&q=80"
            
            try:
                st.image(poster_url if poster_url else fallback_img, use_column_width=True)
            except Exception:
                st.image(fallback_img, use_column_width=True)
            
            # 하이라이트 영상 (유효한 경우에만 안전하게 표시)
            video_url = data.get("video_url")
            if video_url and ("youtube.com" in video_url or "youtu.be" in video_url):
                st.markdown("<div style='margin-top: 1.2rem; font-weight:700; color:#1E293B;'>🎥 작품 하이라이트 / 영상</div>", unsafe_allow_html=True)
                try:
                    st.video(video_url)
                except Exception:
                    pass  # 에러 발생 시 영상 창을 표시하지 않음

        with col_info:
            st.markdown(f'<span class="badge">관련 대표 작품</span>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin-top:0; color:#0F172A; font-weight:700;'>{data.get('title', '작품 정보')}</h2>", unsafe_allow_html=True)
            
            # 1. 줄거리
            st.markdown(f"""
            <div class="content-box">
                <div class="content-label">📖 작품 줄거리</div>
                <div class="content-text">{data.get('story', '줄거리 정보가 제공되지 않습니다.')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. 직업 상세 정보
            st.markdown(f"""
            <div class="content-box">
                <div class="content-label">💼 '{current_job}' 진로 및 직업 분석</div>
                <div class="content-text">{data.get('job_desc', '직업 상세 설명이 제공되지 않습니다.')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 3. 핵심 필요 역량
            if data.get("skills"):
                st.markdown(f"""
                <div class="content-box">
                    <div class="content-label">🛠️ 핵심 필요 역량</div>
                    <div class="content-text">{data.get('skills')}</div>
                </div>
                """, unsafe_allow_html=True)
                
            # 4. 연관 진로 분야
            if data.get("related_jobs"):
                st.markdown(f"""
                <div class="content-box">
                    <div class="content-label">🌱 확장 가능한 연관 진로</div>
                    <div class="content-text">{data.get('related_jobs')}</div>
                </div>
                """, unsafe_allow_html=True)
            
    else:
        st.warning(f"'{current_job}'에 대한 정보를 찾지 못했습니다. 다른 직업명(예: 요리사, 검사, 건축가 등)으로 검색해 주세요.")
