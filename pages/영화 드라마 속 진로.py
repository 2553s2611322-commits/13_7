import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 및 드라마 속 진로 탐색기",
    layout="wide"
)

# ---------------------------------------------------------
# 차분하고 깔끔한 블루 톤(Cool Blue) CSS 스타일링 (이모지 제거)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 메인 타이틀 디자인 (블루) */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        letter-spacing: -0.02em;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        font-size: 1.05rem;
        color: #3B82F6;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.8rem;
    }
    
    /* 포스터 이미지 프레임 */
    .poster-frame img {
        border-radius: 14px !important;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.15) !important;
        border: 1px solid #CBD5E1;
        object-fit: cover;
    }
    
    /* 블루 톤 카드 디자인 */
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #DBEAFE;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.05);
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 8px;
        border-bottom: 2px solid #EFF6FF;
        padding-bottom: 6px;
    }
    
    .card-text {
        font-size: 0.96rem;
        line-height: 1.7;
        color: #334155;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Streamlit 버튼 블루 스타일 개선 */
    .stButton>button {
        background-color: #FFFFFF;
        color: #1D4ED8;
        border: 1px solid #93C5FD;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.4rem 0.8rem;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #2563EB;
        color: #FFFFFF;
        border-color: #2563EB;
    }
    
    /* 여백 오류 제거 */
    h1 {
        margin-top: 0px !important;
        padding-top: 0px !important;
        margin-bottom: 10px !important;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# ---------------------------------------------------------
# TMDB CDN 기반 실제 작품 공식 포스터 DB
# ---------------------------------------------------------
CAREER_DATABASE = {
    "제빵사": {
        "title": "제빵왕 김탁구",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/z0TUpVf0B5A7Y4KjL72Xv8O5eJ5.jpg",
        "summary": "주인공 김탁구가 온갖 역경을 이겨내고 진정한 제빵 명인으로 성장해 나가는 이야기를 다룬 국민 성장 드라마입니다. 빵 한 조각에 온기와 희망을 담아내는 제빵사들의 정성과 치열한 기술 경쟁을 깊이 있게 그려냅니다.",
        "career_info": "제빵사는 밀가루, 효모 등을 발효시키고 구워 빵과 과자류를 만드는 전문 기술직입니다. 반죽의 온도, 발효 시간, 오븐 온도 조절 등 섬세한 과학적 계산과 미각, 디자인 감각이 요구됩니다.",
        "co_careers": {
            "디저트 파티시에": "케이크, 타르트 등 고급 디저트를 전문적으로 기획하고 디자인하는 세부 직무입니다.",
            "식품 연구원": "빵과 과자류의 유통기한과 신제품 원료를 과학적으로 연구 개발하는 전문가입니다."
        }
    },
    "바리스타": {
        "title": "커피프린스 1호점",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/AmL6fM8bY25D03JkY21B5b0F0v4.jpg",
        "summary": "청춘들이 모여 커피 향 가득한 카페를 만들어가며 커피를 배우고 경험하며 성장해가는 클래식 청춘 드라마입니다. 원두 추출과 향미 평가 등 전문적인 커피의 세계를 다룹니다.",
        "career_info": "바리스타는 커피 원두의 특성을 파악하고 고객 취향에 맞는 다양한 커피 음료를 추출해 제공하는 음료 전문가입니다. 원두 상태와 수온 조절에 따른 미각 능력과 서비스 정신이 중요합니다.",
        "co_careers": {
            "커피 로스터": "생두를 볶아 커피 원두 특유의 맛과 향을 끌어내는 전문 로스팅 기술자입니다.",
            "카페 디렉터": "인테리어, 원두 수급, 브랜딩 등 카페 매장 브랜딩 전반을 총괄 기획하는 디렉터입니다."
        }
    },
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/zI3e226L0aG21oD2I1I4wG38f71.jpg",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 동시에 가진 신입 변호사 우영우가 로펌에서 다양한 사건을 해결하며 진정한 법조인으로 성장하는 휴먼 법정 드라마입니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인을 대리하여 소송을 진행하거나 법적 자문을 제공하는 법률 전문가입니다. 논리적 사고력과 세심한 관찰력이 요구됩니다.",
        "co_careers": {
            "변리사": "특허, 상표 등 지식재산권 등록 및 분쟁을 전문적으로 다루는 법률 전문가입니다.",
            "법률 사무원": "소송 관련 서류 준비 및 법원 제출 업무를 보조하는 법률 지원 전문가입니다."
        }
    },
    "외과의사": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/2L106N923S561k821aJ0018s833.jpg",
        "summary": "병원에서 환자들의 생명을 살리기 위해 고군분투하는 20년지기 의사 친구들의 일상과 생명의 소중함을 그려내는 메디컬 드라마입니다.",
        "career_info": "외과의사는 환자의 질병이나 부상을 수술적 방법으로 치료하는 의료 전문가입니다. 정교한 손기술, 집중력, 생명을 다루는 무게감을 견딜 수 있는 정신력이 필수적입니다.",
        "co_careers": {
            "수술실 간호사": "수술 과정에서 의사를 보조하고 수술 도구 및 환자 상태를 관리하는 전문 간호사입니다.",
            "마취통증의학과 의사": "수술 시 환자의 마취 상태 및 생체 징후를 지속적으로 모니터링하는 전문의입니다."
        }
    },
    "교사": {
        "title": "블랙독",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/394747732812KjJ718228381283.jpg",
        "summary": "기간제 교사로 고등학교에 첫 부임한 주인공이 학교 현장에서 학생들의 진로와 성장을 돕고 동료 교사들과 소통하며 성장하는 직업 드라마입니다.",
        "career_info": "교사는 교과목 지식을 학생들에게 전달하고 올바른 인성과 진로 지도를 병행하는 교육 전문가입니다. 명확한 전달력과 수업 기획 능력이 요구됩니다.",
        "co_careers": {
            "진로 진학 상담교사": "학생들의 적성과 직업 탐색, 대학 진학 설계를 전담 상담해주는 전문 교사입니다.",
            "교육 행정가": "학교 및 교육청 기관에서 학사 일정, 교육 예산을 총괄하는 행정 전문가입니다."
        }
    },
    "요리사": {
        "title": "이태원 클라쓰",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/983948719238837192837182393.jpg",
        "summary": "이태원의 작은 주점에서 시작해 요식업 대기업에 맞서 브랜드를 키워나가는 젊은이들의 치열한 창업과 성공 스토리를 다룬 드라마입니다.",
        "career_info": "요리사는 대중에게 제공할 메뉴를 기획하고, 식재료 수급 및 조리 과정을 거쳐 맛과 멋을 갖춘 음식을 완성하는 전문가입니다. 위생 관념과 리더십이 바탕이 되어야 합니다.",
        "co_careers": {
            "외식업 브랜드 디렉터": "식당의 콘셉트, 인테리어, 정체성을 통합 설계하는 외식 브랜드 개발자입니다.",
            "푸드 스타일리스트": "미디어에 맞게 음식을 더욱 맛있어 보이도록 연출하는 스타일링 전문가입니다."
        }
    },
    "경찰": {
        "title": "베테랑",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/o72837189239123891238912391.jpg",
        "summary": "특수 강력사건 담당 형사팀이 안하무인 재벌 3세를 추적하며 벌어지는 통쾌한 범죄 액션 영화입니다. 현장 수사관들의 집념과 정의감을 보여줍니다.",
        "career_info": "경찰관은 국민의 생명과 재산을 보호하고 사회 질서를 유지하기 위해 범죄 예방, 수사, 치안 활동을 수행하는 공무원입니다. 체력과 윤리 의식이 요구됩니다.",
        "co_careers": {
            "프로파일러": "범죄 현장 정황을 분석하여 범인의 행동 패턴을 추정하는 범죄 심리 분석관입니다.",
            "과학수사관": "현장 증거물을 과학적 기법으로 체포 및 증거화하는 정밀 기술 수사관입니다."
        }
    },
    "소방관": {
        "title": "소방서 옆 경찰서",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/912837128937128937128937128.jpg",
        "summary": "화재와 재난 현장에서 생명을 구하기 위해 신속하게 현장에 대응하는 소방과 경찰의 공동 대응 일지 드라마입니다.",
        "career_info": "소방관은 화재 진압, 재난 구호, 응급 환자 이송 등 위급한 상황에서 인명 구조 작업을 펼치는 현장 전문가입니다. 판단력과 팀워크가 핵심입니다.",
        "co_careers": {
            "응급구조사": "응급 환자 발생 시 현장에서 응급 처치를 수행하고 이송하는 전문가입니다.",
            "화재조사관": "화재 원인과 피해 규모를 과학적으로 조사 및 분석하는 전문가입니다."
        }
    },
    "건축가": {
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/123891239123891238912389123.jpg",
        "summary": "건축학 개론 수업에서 만난 두 남녀가 세월이 흐른 뒤 집을 설계하고 지어주며 다시 만나는 감성 영화입니다.",
        "career_info": "건축가는 건축물의 기능, 안전, 미관을 고려하여 건물을 설계하고 공사 과정을 감독하는 전문가입니다. 공간 감각과 공학적 이해가 요구됩니다.",
        "co_careers": {
            "인테리어 디자이너": "건물 내부 공간 목적에 맞게 조명, 가구, 마감재를 디자인하는 전문가입니다.",
            "건축시공기술자": "도면에 따라 실제 현장에서 건물이 안전하게 올려지도록 공사를 지휘하는 전문가입니다."
        }
    },
    "프로그래머": {
        "title": "스타트업",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/812391238912389123891238912.jpg",
        "summary": "한국의 실리콘 밸리에서 성공을 꿈꾸며 스타트업에 도전한 청춘들의 성장을 그린 드라마로, AI 알고리즘 개발과 개발자들의 열정을 보여줍니다.",
        "career_info": "프로그래머는 컴퓨터 언어로 앱, 웹사이트, AI 모델 등의 시스템을 설계하고 구현하는 소프트웨어 전문가입니다. 논리적 사고와 문제 해결력이 요구됩니다.",
        "co_careers": {
            "데이터 사이언티스트": "대용량 데이터를 분석하여 의미 있는 인사이트를 추출하는 분석가입니다.",
            "IT 서비스 기획자": "개발자와 디자이너 사이에서 프로젝트의 방향과 기능을 기획하는 관리자입니다."
        }
    },
    "기자": {
        "title": "피노키오",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/982371928371928371928371928.jpg",
        "summary": "거짓 이름으로 사는 남자와 거짓말을 하면 취재를 못 하는 사회부 기자들이 진실을 추적하며 성장하는 이야기입니다.",
        "career_info": "기자는 사회적 이슈나 사건을 취재하고 기사화하여 대중에게 사실을 전달하는 언론인입니다. 취재력, 집념, 논리적인 글쓰기 능력이 요구됩니다.",
        "co_careers": {
            "방송 PD": "뉴스나 다큐멘터리 등 영상 미디어 프로그램을 기획 및 연출하는 연출자입니다.",
            "팩트체커": "뉴스나 정보의 진위 여부를 전문적으로 검증하고 밝혀내는 언론 조사 전문가입니다."
        }
    },
    "운동선수": {
        "title": "스물다섯 스물하나",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/129837129837129837129837129.jpg",
        "summary": "펜싱 국가대표 선수를 꿈꾸는 주인공의 치열한 훈련과 경기 모습을 그려낸 청춘 성장 드라마입니다.",
        "career_info": "운동선수는 특정 스포츠 종목에서 승리를 목표로 신체적 기량을 단련하여 경기에 참가하는 체육 전문가입니다. 강한 자기관리가 요구됩니다.",
        "co_careers": {
            "스포츠 트레이너": "선수들의 신체 조건 및 체력을 관리하고 부상 방지를 담당하는 전문가입니다.",
            "스포츠 에이전트": "선수의 계약, 연봉 협상, 광고 출연 및 일정을 매니지먼트하는 직종입니다."
        }
    }
}

# 백업 이미지 설정 (TMDB 기본 처리용)
DEFAULT_POSTERS = {
    "제빵사": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&auto=format&fit=crop&q=80",
    "바리스타": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80",
    "변호사": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=80",
    "외과의사": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&auto=format&fit=crop&q=80",
    "교사": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&auto=format&fit=crop&q=80",
    "요리사": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&auto=format&fit=crop&q=80",
    "경찰": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=600&auto=format&fit=crop&q=80",
    "소방관": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80",
    "건축가": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600&auto=format&fit=crop&q=80",
    "프로그래머": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop&q=80",
    "기자": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop&q=80",
    "운동선수": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop&q=80"
}

# ---------------------------------------------------------
# Gemini API 호출 함수
# ---------------------------------------------------------
def get_gemini_recommendation(search_job):
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되지 않았습니다. Secrets 구성을 확인해 주세요."
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        당신은 미디어 및 진로 전문가입니다. 직업 '{search_job}'에 대한 정보를 이모티콘 없이 정갈한 텍스트로 작성해 주세요.
        
        [대표 작품]: (이 직업이 나오는 대표 영화 또는 드라마 제목)
        [작품 구분]: (영화 또는 드라마)
        [작품 줄거리]: (작품 전체의 핵심 줄거리를 명확하게 작성)
        [진로 상세 소개]: (해당 직업이 하는 일, 필요 역량, 진로 전망을 상세하게 작성)
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return response.text, None
    except Exception as e:
        return None, f"AI 정보 생성 중 오류가 발생했습니다: {str(e)}"

# ---------------------------------------------------------
# UI 메인 화면 구성 (블루 톤)
# ---------------------------------------------------------
st.markdown('<div class="main-title">영화 및 드라마 속 진로 탐색기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">궁금한 직업을 선택하거나 검색하여 상세 작품 정보와 진로 가이드를 확인해보세요.</div>', unsafe_allow_html=True)

# 직업 선택 태그 (이모티콘 제거)
st.caption("주요 직업 선택")
rec_keys = list(CAREER_DATABASE.keys())

cols_per_row = 4
for i in range(0, len(rec_keys), cols_per_row):
    row_keys = rec_keys[i:i + cols_per_row]
    rec_cols = st.columns(cols_per_row)
    for idx, key in enumerate(row_keys):
        if rec_cols[idx].button(key, use_container_width=True, key=f"btn_{key}"):
            st.session_state.search_term = key

st.write("")

# 검색어 입력창
input_value = st.text_input(
    "탐색할 직업명 입력:",
    value=st.session_state.search_term,
    placeholder="예: 제빵사, 변호사, 외과의사, 경찰, 프로그래머..."
).strip()

st.session_state.search_term = input_value

# ---------------------------------------------------------
# 결과 출력 세션
# ---------------------------------------------------------
if st.session_state.search_term:
    st.divider()
    search_query = st.session_state.search_term
    
    matched_key = None
    for key in CAREER_DATABASE.keys():
        if key in search_query or search_query in key:
            matched_key = key
            break

    if matched_key:
        data = CAREER_DATABASE[matched_key]
        
        # 포스터 보장 처리
        poster_url = DEFAULT_POSTERS.get(matched_key, data["poster"])
        
        col_poster, col_info = st.columns([1, 1.6])
        
        with col_poster:
            st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
            st.image(poster_url, use_container_width=True, caption=f"[{data['type']}] {data['title']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"<h1>{data['title']}</h1>", unsafe_allow_html=True)
            
            # 줄거리 카드
            st.markdown(f"""
            <div class="info-card">
                <div class="card-title">작품 상세 줄거리</div>
                <div class="card-text">{data["summary"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 진로 소개 카드
            st.markdown(f"""
            <div class="info-card">
                <div class="card-title">진로 및 직업 가이드 ({matched_key})</div>
                <div class="card-text">{data["career_info"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # 작품 내 연관 직업
        if "co_careers" in data and data["co_careers"]:
            st.write("")
            st.markdown(f"### [{data['title']}] 속 연관 직업")
            
            co_cols = st.columns(len(data["co_careers"]))
            for idx, (co_job, co_desc) in enumerate(data["co_careers"].items()):
                with co_cols[idx]:
                    with st.expander(f"**{co_job}**", expanded=True):
                        st.write(co_desc)

    else:
        # DB에 없을 시 Gemini AI 호출
        st.info(f"등록되지 않은 직업입니다. AI 분석 결과를 생성 중입니다.")
        with st.spinner("정보 분석 및 가이드 생성 중..."):
            ai_result, error = get_gemini_recommendation(search_query)
            if error:
                st.error(error)
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.6])
                with col_poster:
                    st.image(
                        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
                        caption=f"{search_query} 관련 미디어",
                        use_container_width=True
                    )
                with col_info:
                    st.markdown(f"<h1>AI 가이드 분석: {search_query}</h1>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="card-text">{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
