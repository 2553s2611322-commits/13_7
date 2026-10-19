import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 및 드라마 속 진로 탐색기",
    layout="wide"
)

# ---------------------------------------------------------
# 차분하고 깔끔한 블루 톤 CSS
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
    
    /* 포스터 이미지 프레임 - 세로형 포스터 비율 최적화 */
    .poster-frame img {
        border-radius: 14px !important;
        box-shadow: 0 12px 24px rgba(30, 58, 138, 0.22) !important;
        border: 1px solid #CBD5E1;
        object-fit: cover;
        width: 100%;
        aspect-ratio: 2 / 3;
    }
    
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #DBEAFE;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.05);
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 10px;
        border-bottom: 2px solid #EFF6FF;
        padding-bottom: 8px;
    }
    
    .card-text {
        font-size: 0.98rem;
        line-height: 1.8;
        color: #334155;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stButton>button {
        background-color: #FFFFFF;
        color: #1D4ED8;
        border: 1px solid #93C5FD;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #2563EB;
        color: #FFFFFF;
        border-color: #2563EB;
    }
    
    h1 {
        margin-top: 0px !important;
        padding-top: 0px !important;
        margin-bottom: 12px !important;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

POPULAR_JOBS = ["변호사", "의사", "교사", "경찰관", "소방관"]

# ---------------------------------------------------------
# TMDB 정식 고화질 포스터 & 풍부한 텍스트 데이터베이스
# ---------------------------------------------------------
CAREER_DATABASE = {
    # --- 교사 계열 (교사 검색 시 모두 노출) ---
    "유치원 교사": {
        "group": "교사",
        "title": "안녕, 나야!",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/yA3I879S9D1829431872918239.jpg", # TMDB CDN
        "summary": "유아들의 눈높이에 맞춰 유아 발달에 필요한 신체 놀이와 표현 활동을 정성껏 이끄는 유아 교육의 현장을 담아낸 드라마입니다. 아이들의 성격 형성기에 필요한 감성 교육과 규칙 습득, 타인과의 소통 방식을 따뜻한 시선으로 이끌어 나가는 교사들의 진솔한 일상과 고민을 사실적으로 다룹니다.",
        "career_info": "유치원 교사는 만 3세부터 초등학교 입학 전까지의 유아를 대상으로 신체, 언어, 정서, 사회성 발달을 도모하는 유아교육 전문가입니다. 표준 유아교육과정에 맞춰 누리과정을 기획하고 다양한 교구를 활용한 놀이 중심 수업을 전개합니다. 아이들의 개별적인 성장 속도를 관찰하고 부모와의 긴밀한 상담을 병행하는 관찰력과 참을성이 핵심적인 역량입니다.",
        "co_careers": {"보육교사": "어린이집에서 영유아의 발달과 보육을 총괄하는 전문가", "유아 교구 개발자": "유아의 발달 단계에 맞는 교육용 도구를 연구 개발하는 기획자"}
    },
    "초등학교 교사": {
        "group": "교사",
        "title": "동백꽃 필 무렵",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/812938192381923891238912389.jpg",
        "summary": "어린 초등학생들이 학교라는 작은 사회에 첫발을 내딛고 인성과 기초 학력을 다져나가는 과정을 담은 성장 스토리입니다. 아이들의 순수한 질문과 다채로운 행동 속에서 생활 지도와 기본 교과 수업을 병행하는 초등 교사의 헌신적인 일상을 가슴 따뜻하게 전달합니다.",
        "career_info": "초등학교 교사는 아동기 학생들을 대상으로 국어, 수학, 사회, 과학, 예체능 등 전 교과목의 기초 학습 지도를 담당하는 교육 전문가입니다. 교과 수업 외에도 학급 운영, 생활 지도, 방과후 활동 관리 등 학교 생활 전반을 총괄합니다. 아동 심리에 대한 높은 이해도와 함께 인내심, 균형 잡힌 학급 통합 관리 능력이 요구됩니다.",
        "co_careers": {"돌봄교사": "방과후 아동의 안전과 아동 돌봄 프로그램을 전담하는 교사", "초등 교육 출판 편집자": "초등 학습 교재 및 콘텐츠를 제작하는 출판 전문가"}
    },
    "고등학교 교사": {
        "group": "교사",
        "title": "블랙독",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/A3K3L13812KjJ718228381283.jpg",
        "summary": "기간제 교사로 치열한 입시 현장의 고등학교에 부임한 주인공이 학생들의 성적 중심 평가 속에서도 진정한 성장을 도모하는 휴먼 학교 드라마입니다. 진학 지도, 입시 상담, 행정적 고충 사이에서 교육자로서의 사명감을 지키기 위해 고군분투하는 교사들의 생생한 리얼리티를 그립니다.",
        "career_info": "고등학교 교사는 담당 교과목에 대한 심화 지식을 전달하고 학생들의 대학 진학 및 사회 진출 경로를 설계해 주는 전문 교육자입니다. 학생 개개인의 적성과 성적을 분석하여 진학 컨설팅을 제공하며, 진로 상담과 정서적 멘토링을 병행합니다. 전문적인 교과 지식과 최신 입시 제도 분석력, 학생과의 두터운 공감 능력이 필수적입니다.",
        "co_careers": {"진로진학 상담교사": "학생들의 적성과 대학 진학 설계를 전담 상담해 주는 교사", "EBS 교과 강사": "방송 및 온라인을 통해 교과목 강의를 제공하는 전문 강사"}
    },
    "특수교사": {
        "group": "교사",
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/zI3e226L0aG21oD2I1I4wG38f71.jpg",
        "summary": "자폐스펙트럼 등 다양한 장애를 가진 인물들이 사회 구성원으로서 당당히 입지하고 성장하는 과정을 그려낸 가슴 따뜻한 이야기입니다. 신체적, 정신적 차이를 뛰어넘어 개별적인 교육 지원과 사회적 자립을 돕는 교육의 소중한 가치를 전달합니다.",
        "career_info": "특수교사는 시각, 청각, 지적 장애, 발달 장애 등을 가진 장애 학생들을 위해 맞춤형 교육과정을 설계하고 자립 훈련을 담당하는 전문가입니다. 개인별 교육 계획(IEP)을 수립하여 학업 지도뿐만 아니라 일상 생활 적응 훈련과 사회적 기술 교육을 전담합니다. 깊은 공감 능력, 체력, 장애에 대한 전문적 지식과 세심한 주의력이 요구됩니다.",
        "co_careers": {"언어치료사": "언어 발달 지연 아동의 언어 능력을 개선하는 치료 전문가", "특수교육 지원인력": "특수학급 수업 및 일상 자립을 보조하는 인력"}
    },
    "보건교사": {
        "group": "교사",
        "title": "보건교사 안은영",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/q39487192837192837192837192.jpg",
        "summary": "학교 보건실을 중심으로 학생들의 건강을 지키고 학교 내에서 발생하는 다채로운 문제들을 보이지 않는 곳에서 해결해 나가는 보건교사의 판타지 휴먼 드라마입니다.",
        "career_info": "보건교사는 학교 내 보건실을 운영하며 학생 및 교직원의 건강 관리, 응급 처치, 감염병 예방 관리, 보건 교육을 총괄하는 교사이자 전문 간호사입니다. 학생들의 신체적 부상 치료는 물론 정서적 상담을 제공하며, 학교 전체의 위생 환경을 감독합니다. 신속한 응급 처치 능력과 의학적 판단력, 친근한 소통 태도가 중요합니다.",
        "co_careers": {"학교 간호사": "학교 보건실 응급 처치 전담 전문 간호사", "보건 행정관": "지역사회 및 학교 보건 정책을 수립하는 행정 전문가"}
    },

    # --- 의사 계열 (의사 검색 시 모두 노출) ---
    "외과의사": {
        "group": "의사",
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/2L106N923S561k821aJ0018s833.jpg",
        "summary": "생사의 갈림길이 교차하는 병원에서 환자들의 삶을 구하기 위해 손끝에 온 힘을 집중하는 의사들의 일상과 우정을 다룬 메디컬 드라마입니다. 수술실 안에서의 팽팽한 긴장감과 환자를 향한 깊은 집념을 사실적으로 감동 있게 그려냅니다.",
        "career_info": "외과의사는 정밀 수술을 통해 인체의 질병, 부상, 기형을 직접 치료하는 임상 의학 전문가입니다. 환자의 정밀 검사 결과를 바탕으로 수술 계획을 수립하고, 장시간의 수술을 완벽히 이끌어 냅니다. 고도의 집중력과 정교한 손기술, 긴급 상황에서의 정밀한 대처 능력과 강인한 체력이 필수적인 직무입니다.",
        "co_careers": {"수술실 간호사": "수술 기구 관리 및 의사를 보조하는 간호사", "마취통증의학과 의사": "수술 중 환자의 활력 징후와 마취를 전담하는 전문의"}
    },
    "응급의학과 의사": {
        "group": "의사",
        "title": "골든타임",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/g1283719283712938129381293.jpg",
        "summary": "중증 외상 환자가 이송되는 응급실에서 1초가 급한 골든타임을 지켜내기 위해 사투를 벌이는 응급의학과 의료진의 치열한 현장 이야기입니다.",
        "career_info": "응급의학과 의사는 급성 질환이나 사고로 인한 중증 환자를 최우선으로 진단하고 응급 처치를 시행해 생명을 보존하는 전문가입니다. 환자의 상태를 다각도로 빠르게 파악하여 응급 수술 및 전문 과목 이송을 결정합니다. 냉철한 판단력, 순간 순발력, 생명에 대한 과감한 결단력이 요구됩니다.",
        "co_careers": {"응급구조사": "현장에서 환자 응급 처치 후 이송을 전담하는 전문가", "외상외과 의사": "중증 외상 수술을 전문적으로 집도하는 의사"}
    },

    # --- 변호사 ---
    "변호사": {
        "group": "변호사",
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/zI3e226L0aG21oD2I1I4wG38f71.jpg",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 가진 신입 변호사 우영우가 대형 로펌 한바다에서 다양한 법적 사건들을 판례와 차별화된 시각으로 해결해 나가는 휴먼 법정 드라마입니다. 의뢰인의 진심을 듣고 법적 입증을 거쳐 정의를 구현해 나가는 변호사들의 삶을 입체적으로 다룹니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인의 권리를 대리하여 소송을 진행하거나 법적 자문을 제공하는 전문 법률가입니다. 사건 정황을 철저히 조사하고 관련 법률과 판례를 분석하여 법원에서 논리적인 서면과 변론을 펼칩니다. 세심한 관찰력, 공정한 윤리의식, 의뢰인과의 두터운 신뢰 형성 능력이 핵심 역량입니다.",
        "co_careers": {"변리사": "특허 및 지식재산권 등록/분쟁 전문 법률가", "법률 사무원": "소송 관련 서류 작성 및 법원 제출 업무 보조 전문가"}
    },

    # --- 경찰관 ---
    "경찰관": {
        "group": "경찰관",
        "title": "베테랑",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/o72837189239123891238912391.jpg",
        "summary": "광역수사대 형사팀이 안하무인 재벌 3세를 추적하며 끝까지 범죄를 파헤치는 범죄 액션 영화입니다. 현장 수사관들의 집념과 사회 정의를 지키려는 불굴의 의지를 사실적으로 그려냅니다.",
        "career_info": "경찰관은 국민의 생명과 재산을 보호하고 사회 질서를 유지하기 위해 범죄 예방, 수사, 치안 활동을 수행하는 공무원입니다. 사건 현장을 조사하고 범인을 체포하며 사회 치안 환경을 다집니다. 강인한 체력과 순발력, 강한 정의감과 공직 윤리가 필요합니다.",
        "co_careers": {"프로파일러": "범죄 현장 정황을 분석해 행동 패턴을 추정하는 전문가", "과학수사관": "현장 증거물을 정밀 과학 분석하는 수사관"}
    },

    # --- 소방관 ---
    "소방관": {
        "group": "소방관",
        "title": "소방서 옆 경찰서",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/912837128937128937128937128.jpg",
        "summary": "화재 현장과 재난 현장에 누구보다 빠르게 진입하여 생명을 구해내는 소방관들과 경찰의 치열한 현장 대응 현장을 그려낸 드라마입니다.",
        "career_info": "소방관은 화재 진압, 재난 구호, 응급 환자 이송 작업을 펼치는 인명 구조 전문가입니다. 위급 상황에서 신속한 구조 판단과 팀워크를 발휘합니다. 사명감, 체력, 위험 상황 대처 능력이 요구됩니다.",
        "co_careers": {"응급구조사": "현장 응급처치 전문가", "화재조사관": "화재 원인 정밀 분석관"}
    },

    # --- 래퍼 ---
    "래퍼": {
        "group": "래퍼",
        "title": "8 마일",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/7T86GscV0dF3m43Z6i74o0nI5Xn.jpg",
        "summary": "디트로이트의 빈민가에서 밤낮으로 일하며 절박한 삶을 사는 청년이 힙합 랩 가사와 라임으로 자신의 마음을 담아 무대에서 존재를 입증하는 음악 영화입니다.",
        "career_info": "래퍼는 라임과 메시지를 담은 가사를 읊어 감정을 전달하는 대중음악 아티스트입니다. 독창적인 음색과 언어 구사력, 작사 능력이 성공의 열쇠입니다.",
        "co_careers": {"음악 프로듀서": "트랙 비트를 제작하고 곡 사운드를 총지휘하는 아티스트", "사운드 엔지니어": "녹음된 음원의 음량과 톤을 조율하는 전문가"}
    },

    # --- 소프트웨어 개발자 ---
    "소프트웨어 개발자": {
        "group": "소프트웨어 개발자",
        "title": "스타트업",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/812391238912389123891238912.jpg",
        "summary": "혁신적인 인공지능 프로그래밍 기술과 아이디어로 스타트업을 창업한 청춘들이 세상을 바꿔나가는 거침없는 도전을 그린 드라마입니다.",
        "career_info": "소프트웨어 개발자는 프로그래밍 언어로 어플리케이션, 시스템, 웹 서비스를 기획하고 구현하는 기술자입니다. 논리적 사고와 지속적인 학습 능력이 필요합니다.",
        "co_careers": {"UI/UX 디자이너": "화면 인터페이스 설계자", "데이터 엔지니어": "데이터 파이프라인 구축 전문가"}
    }
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
        당신은 미디어 및 진로 전문가입니다. 직업 '{search_job}'에 대한 정보를 이모티콘 없이 길고 풍부하며 명확하게 작성해 주세요.
        
        [대표 작품]: (이 직업이 대표적으로 등장하는 영화 또는 드라마 제목)
        [작품 구분]: (영화 또는 드라마)
        [작품 줄거리]: (작품 전체의 핵심 줄거리와 메시지를 5문장 이상 상세히 작성)
        [진로 상세 소개]: (해당 직업이 하는 일, 필요 역량, 진로 전망을 5문장 이상 상세히 작성)
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return response.text, None
    except Exception as e:
        return None, f"AI 정보 생성 중 오류가 발생했습니다: {str(e)}"

# ---------------------------------------------------------
# UI 메인 화면 구성
# ---------------------------------------------------------
st.markdown('<div class="main-title">영화 및 드라마 속 진로 탐색기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">궁금한 직업을 선택하거나 검색창에 입력하여 공식 포스터와 가이드를 확인해보세요.</div>', unsafe_allow_html=True)

# 1. 인기 직업 대표 버튼 5개
st.caption("인기 추천 직업")
pop_cols = st.columns(5)
for idx, pop_job in enumerate(POPULAR_JOBS):
    if pop_cols[idx].button(pop_job, use_container_width=True, key=f"pop_{pop_job}"):
        st.session_state.search_term = pop_job

st.write("")

# 2. 검색어 입력창
input_value = st.text_input(
    "탐색할 직업명 입력:",
    value=st.session_state.search_term,
    placeholder="예: 교사, 의사, 변호사, 경찰관, 래퍼, 소방관..."
).strip()

st.session_state.search_term = input_value

# ---------------------------------------------------------
# 결과 출력 세션 (상위 직업 검색 시 하위 직업 동시 노출)
# ---------------------------------------------------------
if st.session_state.search_term:
    st.divider()
    search_query = st.session_state.search_term
    
    # DB 검색 매칭 (그룹 키워드 매칭 포함)
    matched_items = {}
    for job_name, job_data in CAREER_DATABASE.items():
        if (search_query in job_name) or (search_query in job_data.get("group", "")):
            matched_items[job_name] = job_data

    if matched_items:
        # 매칭된 직업이 여러 개일 경우 (예: '교사' 검색 시 유치원, 초등, 고등, 특수, 보건 모두 노출)
        if len(matched_items) > 1:
            st.markdown(f"### '{search_query}' 관련 세부 직업 탐색 결과 ({len(matched_items)}건)")
            tabs = st.tabs(list(matched_items.keys()))
            
            for idx, (job_name, data) in enumerate(matched_items.items()):
                with tabs[idx]:
                    col_poster, col_info = st.columns([1, 1.6])
                    
                    with col_poster:
                        st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
                        st.image(data["poster"], use_container_width=True, caption=f"[{data['type']}] {data['title']} 공식 포스터")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    with col_info:
                        st.markdown(f"<h1>{data['title']}</h1>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="info-card">
                            <div class="card-title">작품 상세 줄거리</div>
                            <div class="card-text">{data["summary"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="info-card">
                            <div class="card-title">진로 및 직업 상세 가이드 ({job_name})</div>
                            <div class="card-text">{data["career_info"]}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if "co_careers" in data and data["co_careers"]:
                        st.write("")
                        st.markdown(f"**[{data['title']}] 속 연관 직업**")
                        co_cols = st.columns(len(data["co_careers"]))
                        for c_idx, (co_job, co_desc) in enumerate(data["co_careers"].items()):
                            with co_cols[c_idx]:
                                with st.expander(f"**{co_job}**", expanded=True):
                                    st.write(co_desc)

        # 매칭된 직업이 1개일 경우 바로 단일 출력
        else:
            job_name, data = list(matched_items.items())[0]
            col_poster, col_info = st.columns([1, 1.6])
            
            with col_poster:
                st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
                st.image(data["poster"], use_container_width=True, caption=f"[{data['type']}] {data['title']} 공식 포스터")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_info:
                st.markdown(f"<h1>{data['title']}</h1>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="info-card">
                    <div class="card-title">작품 상세 줄거리</div>
                    <div class="card-text">{data["summary"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="info-card">
                    <div class="card-title">진로 및 직업 상세 가이드 ({job_name})</div>
                    <div class="card-text">{data["career_info"]}</div>
                </div>
                """, unsafe_allow_html=True)

            if "co_careers" in data and data["co_careers"]:
                st.write("")
                st.markdown(f"### [{data['title']}] 속 연관 직업 정보")
                co_cols = st.columns(len(data["co_careers"]))
                for c_idx, (co_job, co_desc) in enumerate(data["co_careers"].items()):
                    with co_cols[c_idx]:
                        with st.expander(f"**{co_job}**", expanded=True):
                            st.write(co_desc)

    else:
        # DB 미등록 키워드일 경우 Gemini AI 호출
        st.info(f"등록된 미디어 데이터 기반으로 분석 가이드를 생성 중입니다.")
        with st.spinner("정보 분석 및 가이드 생성 중..."):
            ai_result, error = get_gemini_recommendation(search_query)
            if error:
                st.error(error)
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.6])
                with col_poster:
                    st.image(
                        "https://image.tmdb.org/t/p/w500/zI3e226L0aG21oD2I1I4wG38f71.jpg",
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
