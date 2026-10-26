import os
import streamlit as st

# ---------------------------------------------------------
# 페이지 기본 설정
# ---------------------------------------------------------
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
    
    /* 포스터 이미지 프레임 (세로형 포스터 비율 최적화) */
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
# 데이터베이스 (TMDB CDN 공식 포스터 & 상세 가이드)
# ---------------------------------------------------------
CAREER_DATABASE = {
    # --- 교사 계열 ---
    "유치원 교사": {
        "group": "교사",
        "title": "안녕, 나야!",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/yA3I879S9D1829431872918239.jpg",
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

    # --- 의사 계열 ---
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

    # --- 대표 주요 직업군 ---
    "변호사": {
        "group": "변호사",
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/zI3e226L0aG21oD2I1I4wG38f71.jpg",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 가진 신입 변호사 우영우가 대형 로펌 한바다에서 다양한 법적 사건들을 판례와 차별화된 시각으로 해결해 나가는 휴먼 법정 드라마입니다. 의뢰인의 진심을 듣고 법적 입증을 거쳐 정의를 구현해 나가는 변호사들의 삶을 입체적으로 다룹니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인의 권리를 대리하여 소송을 진행하거나 법적 자문을 제공하는 전문 법률가입니다. 사건 정황을 철저히 조사하고 관련 법률과 판례를 분석하여 법원에서 논리적인 서면과 변론을 펼칩니다. 세심한 관찰력, 공정한 윤리의식, 의뢰인과의 두터운 신뢰 형성 능력이 핵심 역량입니다.",
        "co_careers": {"변리사": "특허 및 지식재산권 등록/분쟁 전문 법률가", "법률 사무원": "소송 관련 서류 작성 및 법원 제출 업무 보조 전문가"}
    },
    "경찰관": {
        "group": "경찰관",
        "title": "베테랑",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/o72837189239123891238912391.jpg",
        "summary": "광역수사대 형사팀이 안하무인 재벌 3세를 추적하며 끝까지 범죄를 파헤치는 범죄 액션 영화입니다. 현장 수사관들의 집념과 사회 정의를 지키려는 불굴의 의지를 사실적으로 그려냅니다.",
        "career_info": "경찰관은 국민의 생명과 재산을 보호하고 사회 질서를 유지하기 위해 범죄 예방, 수사, 치안 활동을 수행하는 공무원입니다. 사건 현장을 조사하고 범인을 체포하며 사회 치안 환경을 다집니다. 강인한 체력과 순발력, 강한 정의감과 공직 윤리가 필요합니다.",
        "co_careers": {"프로파일러": "범죄 현장 정황을 분석해 행동 패턴을 추정하는 전문가", "과학수사관": "현장 증거물을 정밀 과학 분석하는 수사관"}
    },
    "소방관": {
        "group": "소방관",
        "title": "소방서 옆 경찰서",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/912837128937128937128937128.jpg",
        "summary": "화재 현장과 재난 현장에 누구보다 빠르게 진입하여 생명을 구해내는 소방관들과 경찰의 치열한 현장 대응 현장을 그려낸 드라마입니다.",
        "career_info": "소방관은 화재 진압, 재난 구호, 응급 환자 이송 작업을 펼치는 인명 구조 전문가입니다. 위급 상황에서 신속한 구조 판단과 팀워크를 발휘합니다. 사명감, 체력, 위험 상황 대처 능력이 요구됩니다.",
        "co_careers": {"응급구조사": "현장 응급처치 전문가", "화재조사관": "화재 원인 정밀 분석관"}
    },
    "래퍼": {
        "group": "래퍼",
        "title": "8 마일",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/7T86GscV0dF3m43Z6i74o0nI5Xn.jpg",
        "summary": "디트로이트의 빈민가에서 밤낮으로 일하며 절박한 삶을 사는 청년이 힙합 랩 가사와 라임으로 자신의 마음을 담아 무대에서 존재를 입증하는 음악 영화입니다.",
        "career_info": "래퍼는 라임과 메시지를 담은 가사를 읊어 감정을 전달하는 대중음악 아티스트입니다. 독창적인 음색과 언어 구사력, 작사 능력이 성공의 열쇠입니다.",
        "co_careers": {"음악 프로듀서": "트랙 비트를 제작하고 곡 사운드를 총지휘하는 아티스트", "사운드 엔지니어": "녹음된 음원의 음량과 톤을 조율하는 전문가"}
    },
    "소프트웨어 개발자": {
        "group": "소프트웨어 개발자",
        "title": "스타트업",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/812391238912389123891238912.jpg",
        "summary": "혁신적인 인공지능 프로그래밍 기술과 아이디어로 스타트업을 창업한 청춘들이 세상을 바꿔나가는 거침없는 도전을 그린 드라마입니다.",
        "career_info": "소프트웨어 개발자는 프로그래밍 언어로 어플리케이션, 시스템, 웹 서비스를 기획하고 구현하는 기술자입니다. 논리적 사고와 지속적인 학습 능력이 필요합니다.",
        "co_careers": {"UI/UX 디자이너": "화면 인터페이스 설계자", "데이터 엔지니어": "데이터 파이프라인 구축 전문가"}
    },
    "건축가": {
        "group": "건축가",
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/123891239123891238912389123.jpg",
        "summary": "건축학 개론 수업에서 만난 두 남녀가 세월이 흐른 뒤 집을 설계하고 지어주며 다시 만나는 감성 영화입니다. 삶의 기억과 공간을 함께 지어 올리는 건축가의 작업과 진솔한 감정을 그려냅니다.",
        "career_info": "건축가는 건물의 안전, 기능, 미관을 고려하여 최적의 건축 도면을 설계하고 시공 과정을 감독하는 전문가입니다. 공간에 대한 예술적 센스, 공학적 지식, 건축 법규에 대한 이해가 요구됩니다.",
        "co_careers": {"인테리어 디자이너": "실내 공간을 콘셉트에 맞게 연출하는 전문가", "건축시공기술자": "현장에서 공사를 지휘하는 기술자"}
    },
    "요리사": {
        "group": "요리사",
        "title": "이태원 클라쓰",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/983948719238837192837182393.jpg",
        "summary": "이태원의 작은 주점에서 시작해 요식업 대기업에 맞서 브랜드를 키워나가는 젊은이들의 치열한 창업과 성공 스토리를 다룬 드라마입니다. 메뉴의 창의성과 매장 운영, 요리사의 레시피 개발 현장을 생생히 보여줍니다.",
        "career_info": "요리사는 대중에게 제공할 메뉴를 기획하고, 식재료 수급 및 손질, 조리 과정을 거쳐 맛과 멋을 갖춘 음식을 완성하는 조리 전문가입니다. 미각적 센스, 위생 관념, 주방 리더십이 바탕이 되어야 합니다.",
        "co_careers": {"외식업 브랜드 디렉터": "식당 콘셉트 및 브랜딩을 개발하는 전문가", "푸드 스타일리스트": "음식을 맛있어 보이도록 연출하는 스타일링 전문가"}
    },
    "바리스타": {
        "group": "바리스타",
        "title": "커피프린스 1호점",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/AmL6fM8bY25D03JkY21B5b0F0v4.jpg",
        "summary": "정체된 카페를 살아있는 공간으로 탈바꿈시키기 위해 청춘들이 모여 커피를 배우고 경험하며 성장해가는 로맨스 청춘 드라마입니다. 원두 추출 과정과 향미 평가 등 커피 전문가의 세계를 다룹니다.",
        "career_info": "바리스타는 커피 추출 기구를 다루며 원두의 특성을 파악하고 고객 취향에 맞는 다양한 커피 음료를 만드는 음료 전문가입니다. 원두 상태, 분쇄도, 수온 조절에 따른 맛의 변화를 감별하는 섬세함이 핵심 역량입니다.",
        "co_careers": {"커피 로스터": "생두를 볶아 맛과 향을 끌어내는 기술자", "카페 디렉터": "카페 브랜드 및 공간을 총괄 기획하는 매니저"}
    },
    "기자": {
        "group": "기자",
        "title": "피노키오",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/982371928371928371928371928.jpg",
        "summary": "거짓 이름으로 사는 남자와 거짓말을 하면 취재를 못 하는 사회부 기자들이 진실을 추적하며 진정한 언론인으로 성장해가는 청춘 성찰 드라마입니다.",
        "career_info": "기자는 사회적 이슈나 사건을 취재하고 기사화하여 대중에게 사실을 알리는 언론인입니다. 집요한 취재력, 공정한 시각, 논리적인 글쓰기 능력과 언론 윤리가 요구됩니다.",
        "co_careers": {"방송 PD": "뉴스나 다큐멘터리 프로그램을 연출하는 방송 기획자", "팩트체커": "뉴스 및 정보의 진위를 검증하는 조사 전문가"}
    },
    "수의사": {
        "group": "수의사",
        "title": "어쩌다 전원일기",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/53271293831034cb3982ef74.jpg",
        "summary": "시골 마을로 오게 된 서울 출신 수의사가 다양한 동물들을 치료하며 마을 사람들과 소통하고 성장해나가는 힐링 전원 드라마입니다.",
        "career_info": "수의사는 동물의 질병 예방, 진단, 치료, 수술을 담당하는 전문 의료인입니다. 생명존중 의식, 동물을 사랑하는 마음, 세심한 관찰력과 책임감이 요구됩니다.",
        "co_careers": {"동물보건사": "진료 보조 및 동물의 간호를 전담하는 보건인", "반려동물 행동교정사": "동물 행동 문제를 교정하는 훈련 전문가"}
    },
    "항공기 조종사": {
        "group": "조종사",
        "title": "탑건: 매버릭",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/5190740694441ba4fff16be3.jpg",
        "summary": "최고의 기량을 가진 파일럿들이 극한의 상황에서도 안전하게 기체를 조종하고 미션을 완수하기 위해 사투를 벌이는 항공 액션 영화입니다.",
        "career_info": "항공기 조종사(파일럿)는 승객과 화물을 안전하게 이송하기 위해 항공기를 운항하는 조종 전문가입니다. 신속한 상황 판단력, 정밀한 계기 조종 능력, 강한 책임감이 필요합니다.",
        "co_careers": {"항공관제사": "이착륙 경로와 비행 안전을 통제하는 관제관", "항공정비사": "항공기 기체를 정밀 점검하는 정비 기술자"}
    },
    "항공기 승무원": {
        "group": "승무원",
        "title": "플라이트",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/54033983286247459980783b.jpg",
        "summary": "비행기 기체 비상 상황에서도 침착함을 유지하며 승객의 안전과 기내 질서를 지키는 승무원과 기장의 위기 관리 이야기입니다.",
        "career_info": "항공기 승무원은 비행기 기내에서 승객의 비상 인명 안전을 관리하고 쾌적한 서비스를 제공하는 전문가입니다. 비상 상황 대응 능력, 외국어 소통 능력, 배려심이 중요합니다.",
        "co_careers": {"지상직 승무원": "공항 내 체크인 카운터 업무를 담당하는 수속 전문가", "기내식 기획자": "기내식을 개발하고 연출하는 푸드 전문가"}
    },
    "프로게이머": {
        "group": "프로게이머",
        "title": "취시광연적니",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/542751371adc38448a05e.jpg",
        "summary": "e스포츠 무대에서 우승을 목표로 정교한 컨트롤과 팀 플레이로 피나는 연습을 하며 우정을 쌓아가는 프로게이머들의 이야기입니다.",
        "career_info": "프로게이머는 정식 e스포츠 종목 대회에 참가하여 빠른 피지컬 반응 속도와 전술 전략으로 경기를 치르는 스포츠 선수입니다. 강한 집중력과 순발력, 팀원 간의 협동심이 필수적입니다.",
        "co_careers": {"e스포츠 코치": "경기 전략을 수립하고 선수를 지도하는 전략가", "게임 캐스터": "경기를 박진감 넘치게 중계하는 전문 해설가"}
    },
    "웹툰 작가": {
        "group": "웹툰 작가",
        "title": "W (더블유)",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/618005182384a83a8bd57fbe.jpg",
        "summary": "현실 세계의 여의사가 인기 웹툰 'W' 속으로 들어가 캐릭터와 소통하며 벌어지는 판타지 드라마로, 작가의 창의력과 작화의 힘을 보여줍니다.",
        "career_info": "웹툰 작가는 스토리 구상부터 콘티, 그림, 채색까지 거쳐 인터넷 플랫폼에 만화를 연재하는 디지털 아티스트입니다. 독창적인 스토리텔링, 연출력, 작화 실력이 핵심입니다.",
        "co_careers": {"웹툰 프로듀서(PD)": "작가의 일정과 유통 플랫폼 계약을 담당하는 기획자", "웹툰 채색 작가": "작화 과정 중 컬러링을 전담하는 기술 아티스트"}
    },
    "약사": {
        "group": "약사",
        "title": "봄밤",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/587854692152cbe660dbde88.jpg",
        "summary": "평범한 일상을 살아가던 약사와 도서관 관수가 어느 날 찾아온 감정의 파동을 겪는 잔잔한 감성 로맨스 드라마입니다.",
        "career_info": "약사는 의사의 처방전에 따라 약품을 조제하고 환자에게 복약 지도 및 의약품 오남용 방지 자문을 제공하는 전문 보건인입니다. 세심한 정확성과 약학 전문 지식이 요구됩니다.",
        "co_careers": {"제약 연구원": "신약 개발 및 성분을 분석하는 과학자", "한약사": "한약을 전문적으로 조제하는 보건인"}
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
    placeholder="예: 교사, 의사, 변호사, 요리사, 건축가, 기자, 수의사..."
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
