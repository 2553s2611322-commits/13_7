import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 및 드라마 속 진로 탐색기",
    layout="wide"
)

# ---------------------------------------------------------
# 차분하고 세련된 블루 톤 CSS (이모티콘 완벽 제거)
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
    
    .poster-frame img {
        border-radius: 14px !important;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.18) !important;
        border: 1px solid #CBD5E1;
        object-fit: cover;
        width: 100%;
        max-height: 520px;
    }
    
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
        margin-bottom: 10px !important;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# ---------------------------------------------------------
# 상단에 노출할 인기 대표 직업 5개
# ---------------------------------------------------------
POPULAR_JOBS = ["변호사", "의사", "경찰관", "소방관", "소프트웨어 개발자"]

# ---------------------------------------------------------
# 방대한 전체 직업 데이터베이스 (안정적인 CDN 이미지 포스터 URL)
# ---------------------------------------------------------
CAREER_DATABASE = {
    # 1. 법률 / 행정 / 공공
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&auto=format&fit=crop&q=80",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 가진 신입 변호사 우영우가 대형 로펌 한바다에서 다양한 사건들을 자신만의 차별화된 시각으로 해결해 나가며 성장하는 휴먼 법정 드라마입니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인을 대리하여 소송을 진행하고 법적 자문을 제공하는 전문가입니다. 논리적 사고와 사건 분석력이 필수적입니다.",
        "co_careers": {"변리사": "특허 및 지식재산권 전문 법률가", "법률 사무원": "소송 서류 및 행정 지원 전문가"}
    },
    "검사": {
        "title": "비밀의 숲",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?w=800&auto=format&fit=crop&q=80",
        "summary": "감정을 잃은 외톨이 검사 황시목이 정의로운 형사 한여진과 함께 검찰 내부의 비리와 숨겨진 범죄를 파헤치는 스릴러 드라마입니다.",
        "career_info": "검사는 범죄 사건을 수사하고 법원에 공소를 제기하며 형벌 집행을 감독하는 국가 사법 기관입니다.",
        "co_careers": {"검찰 수사관": "검사의 명을 받아 현장을 수사하는 전문가", "변호사": "피의자의 권리를 변호하는 법률가"}
    },
    "판사": {
        "title": "소년심판",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1436450412740-6b988f486c6b?w=800&auto=format&fit=crop&q=80",
        "summary": "소년범을 혐오하는 판사가 지방법원 소년부에 부임하여 소년범죄와 그 뒤에 숨겨진 사회적 문제를 마주하는 법정 드라마입니다.",
        "career_info": "판사는 재판을 진행하고 법률과 양심에 따라 중립적인 입장에서 판결을 내리는 사법부의 핵심 법률가입니다.",
        "co_careers": {"법원 서기관": "재판 기록 작성 법원 공무원", "소년 분류심사원": "소년범 환경 조사 분석 전문가"}
    },
    "경찰관": {
        "title": "베테랑",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=800&auto=format&fit=crop&q=80",
        "summary": "광역수사대 베테랑 형사가 안하무인 재벌 3세를 추적하며 벌어지는 범죄 액션 영화입니다.",
        "career_info": "경찰관은 국민의 생명과 재산을 보호하고 범죄 예방, 수사, 사회 치안을 담당하는 공무원입니다.",
        "co_careers": {"프로파일러": "범죄 심리 분석관", "과학수사관": "현장 증거 과학 분석 전문가"}
    },
    "소방관": {
        "title": "소방서 옆 경찰서",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80",
        "summary": "화재 진압과 인명 구조를 담당하는 소방과 범죄를 수사하는 경찰이 신속하게 공동 대응하는 현장 드라마입니다.",
        "career_info": "소방관은 화재 진압, 재난 구호, 응급 환자 이송 작업을 펼치는 인명 구조 전문가입니다.",
        "co_careers": {"응급구조사": "현장 응급처치 전문가", "화재조사관": "화재 원인 정밀 분석관"}
    },
    "일반행정 공무원": {
        "title": "청춘기록",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&auto=format&fit=crop&q=80",
        "summary": "현실의 벽에 부딪혀도 스스로의 힘으로 꿈과 사랑을 이루기 위해 노력하는 청춘들의 일상과 성장을 그린 드라마입니다.",
        "career_info": "일반행정 공무원은 정부 및 지방자치단체에서 국가 정책 수립, 주민 복지 제공, 행정 절차 관리 업무를 수행합니다.",
        "co_careers": {"사회복지 전담 공무원": "취약계층 복지 지원 전문가", "정책 기획관": "공공 정책 수립 전문가"}
    },
    "직업군인": {
        "title": "태양의 후예",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=800&auto=format&fit=crop&q=80",
        "summary": "낯선 땅 극한의 환경 속에서 사랑과 성공을 꿈꾸는 젊은 군인과 의사들을 통해 삶의 가치를 담아낸 휴먼 멜로 드라마입니다.",
        "career_info": "직업군인은 국가의 안전 보장과 국방의 의무를 전업으로 수행하며 부대를 지휘하고 군사 작전을 집행하는 전문가입니다.",
        "co_careers": {"군의관": "군부대 내 의료 전담 의사", "부사관": "부대 실무 기술 및 대원 지휘 전문가"}
    },
    "외교관": {
        "title": "교섭",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=800&auto=format&fit=crop&q=80",
        "summary": "분쟁지역에서 인질 극이 발생하자 인질을 구하기 위해 현지로 파견된 외교관과 국정원 요원의 협상 작전을 그린 영화입니다.",
        "career_info": "외교관은 해외에서 자국의 이익을 대변하고 재외국민을 보호하며 국제 교류 및 조약 체결 업무를 수행하는 국가 대표입니다.",
        "co_careers": {"국제기구 활동가": "UN 등 국제기구 정책 전문가", "외교 통역사": "정상 회담 전문 통역관"}
    },

    # 2. 의료 / 보건 / 복지
    "의사": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&auto=format&fit=crop&q=80",
        "summary": "병원에서 환자들의 생명을 살리기 위해 노력하는 의사 친구들의 진솔한 일상을 그려낸 드라마입니다.",
        "career_info": "의사는 질병을 진단하고 약물 및 수술적 치료를 통해 환자의 건강을 회복시키는 의료 전문가입니다.",
        "co_careers": {"수술실 간호사": "수술 보조 전문 간호사", "임상병리사": "검사 및 혈액 진단 전문가"}
    },
    "간호사": {
        "title": "정신병동에도 아침이 와요",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&auto=format&fit=crop&q=80",
        "summary": "정신건강의학과 근무를 처음 하게 된 간호사가 정신병동 안에서 만나는 사람들의 마음을 따뜻하게 돌보는 이야기입니다.",
        "career_info": "간호사는 환자의 상태를 관찰하고 의사의 진료를 보조하며 환자의 신체적, 정서적 회복을 다각도로 돕는 의료인입니다.",
        "co_careers": {"정신건강 간호사": "마음 건강 전담 간호사", "보건교사": "학교 보건 책임 교사"}
    },
    "약사": {
        "title": "봄밤",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=800&auto=format&fit=crop&q=80",
        "summary": "조용하고 평범한 일상을 살아가던 약사와 도서관 관수가 어느 날 갑자기 찾아온 감정의 파동을 겪는 잔잔한 로맨스 드라마입니다.",
        "career_info": "약사는 의사의 처방전에 따라 의약품을 조제하고 환자에게 복약 지도와 약물 오남용 예방을 제공하는 전문 보건인입니다.",
        "co_careers": {"제약 연구원": "신약 개발 및 성분 분석가", "한약사": "한약 조제 전문가"}
    },
    "수의사": {
        "title": "어쩌다 전원일기",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1532712938310-34cb3982ef74?w=800&auto=format&fit=crop&q=80",
        "summary": "시골 마을로 내려온 수의사가 농장 동물과 반려동물을 치료하며 마을 사람들과 소통하는 힐링 드라마입니다.",
        "career_info": "수의사는 동물의 질병 예방, 진단, 수술 치료 및 동물 방역 관리를 전담하는 전문 의료인입니다.",
        "co_careers": {"동물보건사": "수의 진료 보조 및 간호인", "반려동물 훈련사": "행동 교정 전문가"}
    },
    "물리치료사": {
        "title": "시를 잊은 그대에게",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&auto=format&fit=crop&q=80",
        "summary": "물리치료사, 방사선사 등 병원 코메디컬 스태프들의 일상을 시와 함께 풀어낸 보건 의료 휴먼 드라마입니다.",
        "career_info": "물리치료사는 부상이나 질환으로 신체 기능이 저하된 환자에게 운동, 열, 전기 치료를 적용하여 회복시키는 보건인입니다.",
        "co_careers": {"작업치료사": "일상생활 적응 훈련가", "재활운동전문가": "맞춤형 운동 처방사"}
    },
    "임상심리사": {
        "title": "굿 윌 헌팅",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&auto=format&fit=crop&q=80",
        "summary": "마음의 상처를 안고 사는 천재 청년이 따뜻한 심리 상담 치료사를 만나며 상처를 치유하고 성장하는 영화입니다.",
        "career_info": "임상심리사는 심리 검사 및 평가 도구를 활용하여 정서적, 행동적 문제를 진단하고 심리 치료를 수행하는 전문가입니다.",
        "co_careers": {"아동심리상담사": "아동 행동 심리 치료가", "정신건강의학과 의사": "정신 질환 전문의"}
    },
    "아동심리상담사": {
        "title": "우리들의 블루스",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=800&auto=format&fit=crop&q=80",
        "summary": "제주를 배경으로 다양한 인물들의 삶과 아픔, 그리고 가족과 아이들의 심리적 회복을 따뜻하게 담아낸 드라마입니다.",
        "career_info": "아동심리상담사는 아동의 정서 불안, 행동 문제, 발달 상의 고충을 심리 상담과 놀이 치료를 통해 회복시키는 전문가입니다.",
        "co_careers": {"놀이치료사": "매개체 활용 치료 전문가", "특수교사": "발달 지원 교사"}
    },
    "사회복지사": {
        "title": "나의 아저씨",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?w=800&auto=format&fit=crop&q=80",
        "summary": "삶의 무게를 버텨내는 아저씨 삼형제와 거칠게 살아온 한 여성이 서로를 통해 삶을 치유해가는 휴먼 드라마입니다.",
        "career_info": "사회복지사는 아동, 노인, 장애인 등 사회적 도움이 필요한 사람들의 복지 지원 제도를 연결하고 생활을 돕는 전문가입니다.",
        "co_careers": {"요양보호사": "돌봄 전담 전문가", "직업재활사": "장애인 취업 지원가"}
    },
    "응급구조사": {
        "title": "골든타임",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&auto=format&fit=crop&q=80",
        "summary": "중증 외상 환자를 살리기 위해 생사의 갈림길에서 사투를 벌이는 응급외상센터 사람들의 이야기입니다.",
        "career_info": "응급구조사는 응급 환자가 발생한 현장에서 신속히 응급 처치를 시행하고 안전하게 병원으로 이송하는 전문가입니다.",
        "co_careers": {"소방관": "인명 구조 전담 공무원", "응급의학과 의사": "응급 치료 전담의"}
    },
    "치과위생사": {
        "title": "갯마을 차차차",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800&auto=format&fit=crop&q=80",
        "summary": "바닷가 마을 공진에서 치과의사와 만능 백수가 펼치는 티키타카 힐링 로맨스 드라마입니다.",
        "career_info": "치과위생사는 치과 진료 보조, 스케일링, 구강 보건 교육을 제공하여 환자의 구강 건강을 지키는 전문 보건인입니다.",
        "co_careers": {"치과의사": "치과 전문의", "치기공사": "보철물 제작 기술자"}
    },

    # 3. IT / 공학 / 과학
    "소프트웨어 개발자": {
        "title": "스타트업",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop&q=80",
        "summary": "혁신적인 인공지능 프로그래밍 기술과 아이디어로 스타트업에 도전하는 청춘들의 성장을 그린 드라마입니다.",
        "career_info": "소프트웨어 개발자는 프로그래밍 언어로 어플리케이션, 시스템, 웹 서비스를 기획하고 구현하는 기술자입니다.",
        "co_careers": {"UI/UX 디자이너": "화면 설계 전문가", "데이터 엔지니어": "데이터 파이프라인 구축가"}
    },
    "인공지능 전문가": {
        "title": "시지프스",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80",
        "summary": "세상에 정체를 숨기고 살아가는 존재를 밝혀내려는 천재 공학자와 그를 위해 먼 길을 거슬러온 구원자의 판타지 드라마입니다.",
        "career_info": "인공지능 전문가는 딥러닝, 머신러닝 알고리즘을 설계하여 데이터 학습 알고리즘을 구축하는 미래 기술 전문가입니다.",
        "co_careers": {"빅데이터 전문가": "대용량 데이터 분석가", "로봇공학자": "AI 로봇 개발자"}
    },
    "데이터 분석가": {
        "title": "머니게임",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&auto=format&fit=crop&q=80",
        "summary": "국가적 금융 위기 상황 속에서 최선의 데이터 분석과 정책으로 금융 부실을 막으려는 기획재정부 공무원들의 이야기입니다.",
        "career_info": "데이터 분석가는 대용량 수치 데이터를 수집, 정제하여 수치 속에 숨겨진 의미와 트렌드를 도출하는 전문가입니다.",
        "co_careers": {"데이터 사이언티스트": "예측 모델 개발자", "경영컨설턴트": "기업 전략 자문가"}
    },
    "화이트해커": {
        "title": "유령",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80",
        "summary": "인터넷 및 사이버 공간 속 은폐된 범죄를 파헤치는 사이버 수사대원들의 고군분투를 다룬 첨단 범죄 드라마입니다.",
        "career_info": "화이트해커(보안 전문가)는 시스템의 취약점을 선제적으로 탐지하고 사이버 공격으로부터 정보 자산을 지키는 보안관입니다.",
        "co_careers": {"사이버 수사관": "디지털 범죄 수사관", "모의침투 전문가": "취약점 진단 전문가"}
    },
    "게임 프로그래머": {
        "title": "알함브라 궁전의 추억",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800&auto=format&fit=crop&q=80",
        "summary": "AR 게임 개발자가 스페인 그라나다에 방문했다가 기묘한 증강현실 게임 사건에 휘말리게 되는 판타지 드라마입니다.",
        "career_info": "게임 프로그래머는 게임 엔진을 활용하여 게임 캐릭터의 물리 엔진, 시스템, 네트워크 인터페이스를 개발하는 프로그래머입니다.",
        "co_careers": {"게임 기획자": "게임 규칙 및 세계관 설계자", "게임 그래픽 디자이너": "3D 모델링 전문가"}
    },
    "로봇공학자": {
        "title": "너도 인간이니?",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&auto=format&fit=crop&q=80",
        "summary": "혼수상태에 빠진 아들을 대신해 만들어진 인공지능 로봇이 인간 세상에 투입되며 벌어지는 SF 로맨스 드라마입니다.",
        "career_info": "로봇공학자는 로봇의 제어 메커니즘, 인공지능, 감지 센서 및 프레임을 기획하고 설계하는 차세대 공학자입니다.",
        "co_careers": {"제어공학자": "자동화 시스템 개발자", "임베디드 개발자": "하드웨어 칩 프로그래머"}
    },
    "반도체 엔지니어": {
        "title": "코리아",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
        "summary": "세계 최고를 목표로 집념과 정밀한 기술을 단련하여 결실을 맺는 도전을 그린 감동 영화입니다.",
        "career_info": "반도체 엔지니어는 초미세 집적 회로를 설계하고 반도체 제조 공정 및 수율을 개선하는 전자공학 전문가입니다.",
        "co_careers": {"공정기술 엔지니어": "제조 수율 관리자", "회로설계 연구원": "IC 칩 설계자"}
    },
    "자동차공학 기술자": {
        "title": "포드 V 페라리",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&auto=format&fit=crop&q=80",
        "summary": "불가능을 가능으로 바꾸기 위해 엔진 성능을 극한으로 끌어올리는 혁신적인 자동차 엔지니어와 레이서의 이야기입니다.",
        "career_info": "자동차공학 기술자는 차량의 파워트레인, 차체, 내연 및 전기 배터리 시스템을 연구 개발하는 기술자입니다.",
        "co_careers": {"전기차 배터리 연구원": "차세대 배터리 개발자", "차량 디자이너": "외형 외관 디자이너"}
    },
    "화장품 연구원": {
        "title": "뷰티 인사이드",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&auto=format&fit=crop&q=80",
        "summary": "얼굴이 바뀌는 특별한 조건 속에서도 아름다움과 피부 가치를 연구하고 완성해 나가는 패션 뷰티 로맨스 드라마입니다.",
        "career_info": "화장품 연구원은 피부에 안전하고 유용한 성분을 수집, 화학 합성하여 화장품 신제품 제형을 개발하는 연구원입니다.",
        "co_careers": {"조향사": "화장품 향료 개발자", "피부과학 연구원": "피부 장벽 세포 연구자"}
    },
    "식품공학 연구원": {
        "title": "제빵왕 김탁구",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&auto=format&fit=crop&q=80",
        "summary": "발효균 연구와 식재료 조화를 통해 맛있는 빵의 표준을 만들어내는 식품 기술자들의 성장 드라마입니다.",
        "career_info": "식품공학 연구원은 식재료의 영양 성분, 유통기한, 발효공학 기법을 분석하여 안전한 신품목 식품을 개발합니다.",
        "co_careers": {"식품위생검사원": "식품 안전 진단관", "메뉴 개발자": "외식 신제품 연구원"}
    },
    "신약 개발자": {
        "title": "킹덤",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&auto=format&fit=crop&q=80",
        "summary": "원인을 알 수 없는 의문의 역병 성분을 조사하고 이를 치료하기 위한 약초와 역병의 비밀을 밝혀내는 역사 스릴러입니다.",
        "career_info": "신약 개발자는 질병을 치료하는 새로운 화학 성분 및 바이오 신약을 개발하여 임상 시험을 검증하는 바이오 전문가입니다.",
        "co_careers": {"임상시험 코디네이터": "약물 시험 관리자", "바이오 연구원": "유전자 분석 연구원"}
    },
    "생명과학 연구원": {
        "title": "설국열차",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=800&auto=format&fit=crop&q=80",
        "summary": "기후 변화 속 폐쇄된 공간에서 인공 생태계 유지를 위해 자원과 유전자를 관리하는 미래 생명 과학 과학자들의 이야기입니다.",
        "career_info": "생명과학 연구원은 동식물, 미생물, 유전체 세포의 생명 현상을 연구하여 바이오 기술에 응용하는 과학자입니다.",
        "co_careers": {"유전공학자": "유전자 편집 연구원", "줄기세포 연구원": "재생 의학 기술자"}
    },
    "환경 엔지니어": {
        "title": "승리호",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop&q=80",
        "summary": "우주 쓰레기를 청소하며 오염된 지구 환경을 회복하기 위해 노력하는 2092년 우주 청소선 청춘들의 이야기입니다.",
        "career_info": "환경 엔지니어는 대기, 수질, 폐기물 오염을 방지하고 친환경 재생 에너지 시스템을 설계하는 공학 전문가입니다.",
        "co_careers": {"탄소배출권 컨설턴트": "친환경 규제 전문가", "신재생에너지 개발자": "태양광 수소 에너지 연구원"}
    },

    # 4. 문화 / 예술 / 미디어 / 연예
    "래퍼": {
        "title": "8 마일",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&auto=format&fit=crop&q=80",
        "summary": "디트로이트의 고단한 삶 속에서 힙합 가사와 박자감으로 무대 위에서 자신을 증명해내는 래퍼의 음악 영화입니다.",
        "career_info": "래퍼는 라임과 리듬을 바탕으로 독창적인 가사와 음색을 선보이는 대중음악 아티스트입니다.",
        "co_careers": {"음악 프로듀서": "트랙 제작자", "사운드 엔지니어": "음향 믹싱 전문가"}
    },
    "보컬리스트": {
        "title": "비긴 어게인",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800&auto=format&fit=crop&q=80",
        "summary": "상처받은 보컬리스트와 음반 프로듀서가 뉴욕 거리 곳곳을 무대 삼아 노래하며 상처를 치유하는 음악 영화입니다.",
        "career_info": "보컬리스트는 풍부한 가창력과 감정 전달력으로 곡을 해석하여 노래하는 전문 음악가입니다.",
        "co_careers": {"보컬 트레이너": "발성 지도 전문가", "작곡가": "멜로디 창작자"}
    },
    "아이돌 가수": {
        "title": "최애의 아이",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&auto=format&fit=crop&q=80",
        "summary": "화려한 엔터테인먼트 무대 뒤에서 대중의 사랑을 받기 위해 피나게 노력하는 아이돌들과 연예계의 실제 모습을 담아낸 이야기입니다.",
        "career_info": "아이돌 가수는 가창, 댄스, 무대 매너를 결합하여 음악 및 팬들과 소통하는 아티스트입니다.",
        "co_careers": {"안무가": "댄스 동선 기획자", "A&R 매니저": "음반 기획 총괄자"}
    },
    "작곡가": {
        "title": "드림하이",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800&auto=format&fit=crop&q=80",
        "summary": "예술고등학교에서 음악 작곡과 노래를 배우며 세계적인 아티스트로 성장해가는 사관학교 청춘 성장 드라마입니다.",
        "career_info": "작곡가는 악상과 화성을 조합하여 새로운 멜로디와 곡 구조를 창작하는 음악 창작자입니다.",
        "co_careers": {"편곡가": "악기 세션 배치 전문가", "작사가는": "노래 가사 집필자"}
    },
    "싱어송라이터": {
        "title": "유열의 음악앨범",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=800&auto=format&fit=crop&q=80",
        "summary": "라디오에서 흘러나오는 노래처럼 엇갈림 속에서도 자신들의 이야기를 노래로 담아내는 싱어송라이터의 아날로그 로맨스입니다.",
        "career_info": "싱어송라이터는 직접 곡을 작사, 작곡하고 직접 가창하여 본인의 음악 정체성을 표현하는 뮤지션입니다.",
        "co_careers": {"음반 제작자": "레이블 대표", "세션 연주자": "기타 및 피아노 연주자"}
    },
    "음악 프로듀서": {
        "title": "비긴 어게인",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800&auto=format&fit=crop&q=80",
        "summary": "음반 기획자가 새로운 원석 아티스트를 발굴하여 차별화된 사운드로 앨범을 프로듀싱하는 과정을 다룹니다.",
        "career_info": "음악 프로듀서는 앨범 콘셉트 기획부터 작곡, 편곡, 믹싱 등 음악 제작 전체 과정을 지휘하는 총괄자입니다.",
        "co_careers": {"A&R 디렉터": "아티스트 발굴자", "믹싱 엔지니어": "음향 디렉터"}
    },
    "안무가": {
        "title": "스텝 업",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1547153760-18fc86324498?w=800&auto=format&fit=crop&q=80",
        "summary": "스트릿 댄서와 스트릿 안무가가 무대 연출 안무를 개발하여 격렬한 댄스 콘테스트에 도전하는 무대 영화입니다.",
        "career_info": "안무가는 음악 분위기에 맞춰 신체 움직임 동선과 댄스 동작을 창작하고 무대를 총지휘하는 아티스트입니다.",
        "co_careers": {"댄서": "무대 수행 연주자", "무대 연출가": "조명 및 무대 디자인 전문가"}
    },
    "댄서": {
        "title": "스트릿 우먼 파이터",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=800&auto=format&fit=crop&q=80",
        "summary": "대한민국 최고의 스트릿 댄스 크루들이 자존심을 걸고 펼치는 솔직하고 강렬한 댄스 배틀 무대입니다.",
        "career_info": "댄서는 안무를 습득하고 뛰어난 신체 표현력으로 무대 위에서 춤을 완성하는 전문 무용인입니다.",
        "co_careers": {"백업 댄서": "아티스트 보조 댄서", "댄스 트레이너": "실기 지도 교사"}
    },
    "뮤지컬 배우": {
        "title": "라라랜드",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?w=800&auto=format&fit=crop&q=80",
        "summary": "꿈을 꾸는 사람들을 위한 별들의 도시에서 배우를 꿈꾸는 지망생과 재즈 피아니스트의 열정과 사랑을 담은 뮤지컬 영화입니다.",
        "career_info": "뮤지컬 배우는 연기, 가창, 무대 댄스를 동시에 수행하여 라이브 무대에서 감동을 전하는 공연 예술가입니다.",
        "co_careers": {"음악 감독": "공연 라이브 세션 지휘자", "보컬 코치": "노래 지도 전문가"}
    },
    "연극배우": {
        "title": "드라이브 마이 카",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=800&auto=format&fit=crop&q=80",
        "summary": "상처를 가진 연극 연출가와 배우가 무대 연극을 준비하며 대사를 주고받고 서로의 상처를 들여다보는 휴먼 영화입니다.",
        "career_info": "연극배우는 관객과 직접 호흡하는 소극장 및 관객 무대 위에서 대사 및 신체 연기를 선보이는 연기자입니다.",
        "co_careers": {"연극 연출가": "무대 극본 연출자", "극작가": "연극 대본 집필가"}
    },
    "영화감독": {
        "title": "파벨만스",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800&auto=format&fit=crop&q=80",
        "summary": "영화와 사랑에 빠진 소년이 필름 카메라를 들고 자신만의 영상 세계를 구축하며 거장 감독으로 성장해가는 실화 영화입니다.",
        "career_info": "영화감독은 시나리오 선정, 배우 캐스팅, 촬영 현장 지휘, 편집을 총괄하는 영상 예술의 총지휘자입니다.",
        "co_careers": {"촬영 감독": "카메라 앵글 설계자", "영화 프로듀서": "제작 예산 및 기획자"}
    },
    "방송 PD": {
        "title": "프로듀사",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=800&auto=format&fit=crop&q=80",
        "summary": "KBS 예능국 예능 PD들의 리얼한 편집실 일상과 프로그램 기획 현장을 그린 예능 드라마입니다.",
        "career_info": "방송 PD는 뉴스, 예능, 교양 프로그램을 기획하고 구성 및 현장 촬영을 총괄 연출하는 미디어 기획자입니다.",
        "co_careers": {"방송 작가": "대본 스크립터", "FD": "현장 진행 보조 연출가"}
    },
    "드라마 작가": {
        "title": "멜로가 체질",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&auto=format&fit=crop&q=80",
        "summary": "서른 살 여자 친구들의 고민과 연애, 그리고 신인 드라마 작가가 대본을 완성해가는 코미디 드라마입니다.",
        "career_info": "드라마 작가는 회차별 대본, 캐릭터 설정, 스토리를 창작하여 방송 영상의 뼈대를 만드는 작가입니다.",
        "co_careers": {"보조 작가": "자료 조사원", "드라마 제작사 대표": "기획 유통 책임자"}
    },
    "웹툰 작가": {
        "title": "W (더블유)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80",
        "summary": "현실 세계의 의사가 자신이 읽던 웹툰 속으로 들어가 캐릭터와 소통하는 판타지 드라마입니다.",
        "career_info": "웹툰 작가는 디지털 기기로 스토리 콘티를 구성하고 만화 작화를 통해 인터넷 플랫폼에 연재하는 아티스트입니다.",
        "co_careers": {"웹툰 PD": "연재 일정 관리 매니저", "채색 작가": "컬러 분업 작가"}
    },
    "일러스트레이터": {
        "title": "그 해 우리는",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800&auto=format&fit=crop&q=80",
        "summary": "얼굴 없는 건물 전문 일러스트레이터로 성공한 주인공이 학창 시절 청춘을 다시 마주하는 청춘 로맨스입니다.",
        "career_info": "일러스트레이터는 책, 광고, 캐릭터에 들어가는 그림 시각 요소를 독창적으로 그리는 미술 전문가입니다.",
        "co_careers": {"북 디자이너": "책 표지 기획자", "콘셉트 아티스트": "캐릭터 기획 디자이너"}
    },

    # 5. 미용 / 패션 / 스타일
    "네일아티스트": {
        "title": "달콤한 원수",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1604654894610-df63bc536371?w=800&auto=format&fit=crop&q=80",
        "summary": "손끝에 아름다운 색채를 입히고 정성을 다해 네일 케어를 완성하는 네일 숍 전문가들의 이야기입니다.",
        "career_info": "네일아티스트는 고객의 손톱 건강 케어 및 네일 아트 디자인을 시술하는 뷰티 전문가입니다.",
        "co_careers": {"뷰티 숍 매니저": "매장 경영자", "손톱 위생 관리사": "네일케어 전담원"}
    },
    "메이크업 아티스트": {
        "title": "청춘기록",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=800&auto=format&fit=crop&q=80",
        "summary": "메이크업 스태프에서 시작해 본인 브랜드를 갖춘 메이크업 아티스트로 성장해가는 감동 드라마입니다.",
        "career_info": "메이크업 아티스트는 고객 피부와 의상 콘셉트에 맞게 화장품으로 이목구비를 미적으로 표현하는 전문가입니다.",
        "co_careers": {"뷰티 크리에이터": "화장법 콘텐츠 제작자", "특수분장사": "캐릭터 분장가"}
    },
    "헤어 디자이너": {
        "title": "닥터스",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=800&auto=format&fit=crop&q=80",
        "summary": "세련된 헤어 스타일링과 깔끔한 이미지로 인물의 분위기를 변화시켜주는 전문가들의 세련된 일상을 보여줍니다.",
        "career_info": "헤어 디자이너는 고객 두상과 모발 특성을 분석하여 헤어 커트, 파마, 염색 스타일을 연출하는 전문가입니다.",
        "co_careers": {"두피 관리사": "두피 케어 스파 전문가", "헤어 컬러리스트": "염색 전문 디자이너"}
    },
    "패션 디자이너": {
        "title": "패션왕",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&auto=format&fit=crop&q=80",
        "summary": "동대문 시장에서 시작해 세계적인 패션 디자이너를 꿈꾸는 젊은이들의 열정과 사랑을 다룬 드라마입니다.",
        "career_info": "패션 디자이너는 의류 및 잡화의 패브릭 원단 선택, 패턴, 디자인 스타일을 독창적으로 창작하는 디자이너입니다.",
        "co_careers": {"패셔니스타 모델": "의상 표현자", "패션 MD": "의류 상품 기획자"}
    },
    "스타일리스트": {
        "title": "악마는 프라다를 입는다",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&auto=format&fit=crop&q=80",
        "summary": "패션 잡지사와 스타 배우들의 분위기에 맞게 완벽한 스타일링 조합을 만드는 패션 전문가들의 이야기입니다.",
        "career_info": "스타일리스트는 연예인, 모델, 광고 인물의 의상, 신발, 액세서리를 기획하여 통합 룩을 완성하는 전문가입니다.",
        "co_careers": {"패션 에디터": "잡지 화보 기획자", "쇼핑 호스트": "의류 디스플레이어"}
    },
    "모델": {
        "title": "청춘기록",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=800&auto=format&fit=crop&q=80",
        "summary": "런웨이 무대 위에서 의상을 빛내는 런웨이 패션 모델들의 치열한 도전기를 그려낸 드라마입니다.",
        "career_info": "모델은 런웨이, 화보, 광고 촬영에서 의류 및 브랜드 제품을 신체 포즈와 표현력으로 돋보이게 하는 모델입니다.",
        "co_careers": {"패션 사진작가": "화보 찍는 작가", "에이전시 매니저": "모델 일정 매니저"}
    },
    "사진작가": {
        "title": "8월의 크리스마스",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1554048612-b6a482bc67e5?w=800&auto=format&fit=crop&q=80",
        "summary": "작은 사진관에서 카메라 렌즈 너머 사람들의 가장 소중하고 반짝이는 순간을 담아내는 사진작가의 이야기입니다.",
        "career_info": "사진작가는 조명, 카메라 앵글, 조리개를 조절하여 인물, 풍경, 광고 이미지를 찍는 시각 예술가입니다.",
        "co_careers": {"리터처": "사진 후보정 전문가", "스튜디오 실장": "촬영 조명 감독"}
    },

    # 6. 식음료 / 외식
    "제과제빵사(파티시에)": {
        "title": "내 이름은 김삼순",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&auto=format&fit=crop&q=80",
        "summary": "프랑스 유학파 전문 파티시에 삼순이가 맛있는 디저트와 케이크를 만들며 사랑을 이어가는 로맨스 코미디입니다.",
        "career_info": "제과제빵사(파티시에)는 빵, 케이크, 타르트 등 고급 과자류와 디저트를 기획하고 구워내는 전문가입니다.",
        "co_careers": {"쇼콜라티에": "초콜릿 공예가", "베이커리 매니저": "디저트 카페 경영자"}
    },
    "쇼콜라티에": {
        "title": "초콜릿",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=800&auto=format&fit=crop&q=80",
        "summary": "정성스럽게 만든 초콜릿 한 조각으로 상처받은 사람들의 마음을 따뜻하게 위로하는 쇼콜라티에의 잔잔한 이야기입니다.",
        "career_info": "쇼콜라티에는 카카오 원두 선정부터 템퍼링 과정을 거쳐 아름답고 맛있는 수제 초콜릿을 가공하는 예술가입니다.",
        "co_careers": {"디저트 연구원": "초콜릿 성분 개발자", "파티시에": "제과 기술자"}
    },
    "바리스타": {
        "title": "커피프린스 1호점",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&auto=format&fit=crop&q=80",
        "summary": "카페를 살아있는 공간으로 탈바꿈시키기 위해 청춘들이 모여 원두 향 가득한 커피를 만드는 청춘 드라마입니다.",
        "career_info": "바리스타는 원두의 추출 상태와 분쇄도를 조율하여 고객의 취향에 맞는 고품질 커피를 제공하는 음료 전문가입니다.",
        "co_careers": {"커피 로스터": "원두 로스팅 전문가", "카페 디렉터": "카페 공간 브랜딩 기획자"}
    },
    "소믈리에": {
        "title": "신의 물방울",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80",
        "summary": "세계 최고 와인들을 블라인드 테이스팅하며 와인의 역사와 맛을 전달하는 와인 소믈리에들의 이야기입니다.",
        "career_info": "소믈리에는 와인의 빈티지, 산지, 품종을 분석하여 음식과 어울리는 와인을 추천 및 관리하는 와인 전문가입니다.",
        "co_careers": {"와인 바이어": "와인 수입 유통 전문가", "F&B 매니저": "식음료 서비스 관리자"}
    },
    "요리사(셰프)": {
        "title": "파스타",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800&auto=format&fit=crop&q=80",
        "summary": "이탈리안 레스토랑 주방에서 최고 요리사가 되기 위해 불과 칼을 다루며 정성을 쏟는 셰프들의 치열한 요리 드라마입니다.",
        "career_info": "요리사는 최상급 식재료를 수급하여 맛과 멋을 갖춘 음식을 기획하고 주방을 이끄는 조리 전문가입니다.",
        "co_careers": {"수셰프": "부주방장", "푸드 스타일리스트": "음식 디스플레이 연출가"}
    },
    "푸드 스타일리스트": {
        "title": "식샤를 합시다",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800&auto=format&fit=crop&q=80",
        "summary": "음식이 수록되는 촬영 현장에서 음식을 더욱 맛깔나고 먹음직스럽게 디스플레이하는 스타일리스트들의 이야기입니다.",
        "career_info": "푸드 스타일리스트는 미디어 화보 및 광고 촬영 시 음식을 시각적으로 더욱 아름답게 코디하는 전문가입니다.",
        "co_careers": {"테이블 코디네이터": "식기 배치 연출가", "메뉴 컨설턴트": "식당 연출 컨설턴트"}
    },

    # 7. 콘텐츠 / 디자인 / 마케팅
    "유튜브 크리에이터": {
        "title": "빅마우스",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&auto=format&fit=crop&q=80",
        "summary": "미디어를 적극적으로 활용해 대중에게 트렌디한 정보와 흥미로운 비디오 영상을 전달하는 디지털 크리에이터 이야기입니다.",
        "career_info": "유튜브 크리에이터는 영상 기획, 촬영, 소통을 주도하여 자신만의 창의적인 비디오 콘텐츠를 제작하는 1인 미디어입니다.",
        "co_careers": {"영상 편집자": "컷 편집 전문 기술자", "채널 매니저": "유튜브 알고리즘 관리자"}
    },
    "영상 편집자": {
        "title": "기생충",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&auto=format&fit=crop&q=80",
        "summary": "촬영된 영상 원본 조각들을 리듬감 있게 컷 편집하고 색보정을 더해 완벽한 하나의 영화 스토리를 완성하는 편집실 이야기입니다.",
        "career_info": "영상 편집자는 촬영된 비디오 소스에 자막, 효과음, 컷 편집, 색보정(CG)을 적용하여 몰입감을 높이는 기술자입니다.",
        "co_careers": {"모션 그래픽 디자이너": "자막 모션 연출가", "컬러리스트": "영상 색보정 전문가"}
    },
    "웹디자이너": {
        "title": "검색어를 입력하세요 WWW",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800&auto=format&fit=crop&q=80",
        "summary": "포털 사이트 메인 웹 페이지 레이아웃과 배너 디자인을 깔끔하게 바꾸며 포털 경쟁을 이끄는 디자이너들의 이야기입니다.",
        "career_info": "웹디자이너는 인터넷 홈페이지 및 디지털 레이아웃의 비주얼 이미지와 인포그래픽을 시각화하는 디자이너입니다.",
        "co_careers": {"UI 디자이너": "사용자 인터페이스 설계자", "퍼블리셔": "웹 표준 코딩 기술자"}
    },
    "게임 그래픽 디자이너": {
        "title": "알함브라 궁전의 추억",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80",
        "summary": "증강현실 속 입체적인 게임 캐릭터와 아이템, 몬스터 그래픽 요소를 세밀하게 디자인하는 아티스트 이야기입니다.",
        "career_info": "게임 그래픽 디자이너는 3D 모델링 및 2D 원화 작업을 통해 게임 세계관 캐릭터, 배경 그래픽을 연출하는 디자이너입니다.",
        "co_careers": {"3D 모델러": "입체 객체 제작자", "원화가": "캐릭터 컨셉 원화 디자이너"}
    },
    "인테리어 디자이너": {
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&auto=format&fit=crop&q=80",
        "summary": "낡은 단독주택 실내 공간을 따뜻한 조명과 목재 가구로 리모델링하여 아름다운 집으로 바꿔주는 내부 디자이너 이야기입니다.",
        "career_info": "인테리어 디자이너는 건물 내부의 동선, 마감재, 가구 배치, 조명을 콘셉트에 맞춰 실내 공간을 연출하는 전문가입니다.",
        "co_careers": {"조명 디자이너": "실내 조명 설계자", "공간 컨설턴트": "동선 설계 전문가"}
    },
    "시각 디자이너": {
        "title": "뷰티 인사이드",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=800&auto=format&fit=crop&q=80",
        "summary": "가구 브랜드의 고유한 브랜드 로고와 포장 패키지를 세련되게 디자인하여 브랜드 가치를 다지는 디자이너 이야기입니다.",
        "career_info": "시각 디자이너는 포스터, 브랜드 로고(CI/BI), 패키지 그래픽을 디자인하여 메시지를 전달하는 전문가입니다.",
        "co_careers": {"브랜드 디자이너": "기업 로고 기획자", "패키지 디자이너": "제품 포장 디자이너"}
    },
    "광고 기획자": {
        "title": "대행사",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&auto=format&fit=crop&q=80",
        "summary": "최고 경쟁 PT를 승리로 이끌기 위해 차별화된 광고 캠페인을 전파하는 미디어 광고 대행사 오피스 드라마입니다.",
        "career_info": "광고 기획자(AE)는 광고주 요구사항을 토대로 광고 전략을 수립하고 제작, 카피, 매체 집행 전 과정을 관리하는 전문가입니다.",
        "co_careers": {"카피라이터": "광고 슬로건 창작자", "미디어 바이어": "광고 지면 매체 집행자"}
    },
    "카피라이터": {
        "title": "대행사",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&auto=format&fit=crop&q=80",
        "summary": "짧은 한 줄의 광고 문구로 소비자 마음을 사로잡기 위해 밤낮으로 단어를 조합하는 카피라이터들의 치열한 일상입니다.",
        "career_info": "카피라이터는 광고의 핵심 슬로건, 영상 콘티의 대사, 헤드라인 핵심문구를 독창적으로 집필하는 문학자입니다.",
        "co_careers": {"광고 기획자": "광고 총괄 AE", "크리에이티브 디렉터": "광고 제작 총감독"}
    },
    "아나운서": {
        "title": "질투의 화신",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800&auto=format&fit=crop&q=80",
        "summary": "뉴스 앵커 자리를 놓고 벌어지는 베테랑 아나운서와 기상캐스터의 치열한 방송국 보도국 이야기입니다.",
        "career_info": "아나운서는 정확한 발음과 전달력으로 뉴스를 진행하고 각종 프로그램을 정돈되게 이끄는 방송 언론인입니다.",
        "co_careers": {"뉴스 앵커": "메인 보도 진행자", "기상캐스터": "날씨 정보 전달자"}
    },
    "쇼호스트": {
        "title": "킬힐",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1511556532299-8f662fc26c06?w=800&auto=format&fit=crop&q=80",
        "summary": "홈쇼핑 방송에서 완판을 목표로 수백만 시청자 앞에서 상품의 매력을 몰입감 있게 설명하는 패션 쇼호스트 이야기입니다.",
        "career_info": "쇼호스트는 생방송 중 상품의 기능과 가치를 공감대 있게 소개해 구매를 유도하는 커머스 전문가입니다.",
        "co_careers": {"홈쇼핑 PD": "라이브 커머스 연출자", "라이브 커머스 진행자": "모바일 완판 진행자"}
    },
    "성우": {
        "title": "유미의 세포들",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=800&auto=format&fit=crop&q=80",
        "summary": "애니메이션 세포 캐릭터들의 다채로운 목소리를 실감 나게 더빙하여 생동감을 불어넣는 성우들의 연기 이야기입니다.",
        "career_info": "성우는 목소리만으로 애니메이션, 다큐멘터리, 외화, 게임 캐릭터의 감정을 연기하는 전문 음성 연기자입니다.",
        "co_careers": {"오디오북 내레이터": "책 읽어주는 내레이터", "더빙 연출가": "음성 연출 감독"}
    },

    # 8. 스포츠 / 레저
    "스포츠 트레이너": {
        "title": "오 마이 비너스",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&auto=format&fit=crop&q=80",
        "summary": "세계적인 헬스 트레이너가 건강을 잃은 주인공의 맞춤 운동과 식단을 관리하며 체력 증진을 돕는 로맨틱 헬스 드라마입니다.",
        "career_info": "스포츠 트레이너는 고객의 신체 측정 결과에 맞춰 운동 루틴과 영양 관리를 컨설팅해 주는 운동 전문가입니다.",
        "co_careers": {"퍼스널 트레이너(PT)": "개인 맞춤 피트니스 지도자", "스포츠 영양사": "식단 설계 전문가"}
    },
    "필라테스 강사": {
        "title": "술꾼도시여자들",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&auto=format&fit=crop&q=80",
        "summary": "퇴근 후 삶을 즐기는 청춘들이 낮에는 필라테스 기구를 활용해 유연성과 체형 교정을 지도하는 기구 운동 이야기입니다.",
        "career_info": "필라테스 강사는 리포머 등 전용 기구를 활용해 코어 근육 강화, 코어 정렬 및 체형 교정을 지도하는 강사입니다.",
        "co_careers": {"체형 교정 전문가": "자세 분석 강사", "요가 강사": "호흡 수련 강사"}
    },
    "요가 강사": {
        "title": "서른, 아홉",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=800&auto=format&fit=crop&q=80",
        "summary": "마음의 평온과 유연성을 기르기 위해 매트 위에서 호흡하고 몸을 정렬하는 요가 강사의 따뜻한 휴먼 드라마입니다.",
        "career_info": "요가 강사는 다양한 동작(아사나)과 호흡법, 명상을 통해 수련자의 신체적 유연성과 정신적 평온을 지도하는 강사입니다.",
        "co_careers": {"명상 지도사": "마음 수련가", "플라잉요가 강사": "해먹 운동 전문가"}
    },
    "프로게이머": {
        "title": "취시광연적니",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&auto=format&fit=crop&q=80",
        "summary": "e스포츠 대회 우승을 위해 정교한 피지컬 컨트롤과 팀 플레이로 피나는 연마를 하는 프로게이머 이야기입니다.",
        "career_info": "프로게이머는 e스포츠 정식 종목 대회에 참가해 전략과 빠른 피지컬 반응 속도로 경쟁하는 스포츠 선수입니다.",
        "co_careers": {"e스포츠 코치": "전략 코치", "게임 캐스터": "e스포츠 전문 중계진"}
    },
    "e스포츠 감독": {
        "title": "취시광연적니",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800&auto=format&fit=crop&q=80",
        "summary": "선수들의 밴픽 전략을 수립하고 멘탈 케어와 구단 운영을 지휘하는 e스포츠 지도자들의 이야기입니다.",
        "career_info": "e스포츠 감독은 구단 게임단 전략 수립, 선수 픽업, 경기 피드백 및 구단 스폰서십을 총괄 지휘하는 최고 지도자입니다.",
        "co_careers": {"전력분석관": "데이터 패턴 분석가", "선수 트레이너": "피지컬 케어 담당자"}
    },
    "스포츠 마케터": {
        "title": "스토브리그",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&auto=format&fit=crop&q=80",
        "summary": "구단 유니폼 스폰서십을 유치하고 팬 마케팅 이벤트를 펼쳐 구단 가치를 높이는 스포츠 마케팅 이야기입니다.",
        "career_info": "스포츠 마케터는 스포츠 구단, 선수 스폰서십, 티켓 판매, 스포츠 용품 브랜딩 기획을 담당하는 전문가입니다.",
        "co_careers": {"구단 홍보팀장": "미디어 언론 담당자", "스포츠 에이전트": "선수 매니지먼트가"}
    },
    "축구 코치": {
        "title": "드림",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&auto=format&fit=crop&q=80",
        "summary": "축구 전술에 생소한 선수들에게 패스, 슈팅 전술 포메이션을 직접 지도하며 팀을 만들어가는 코치의 이야기입니다.",
        "career_info": "축구 코치는 선수들의 개인 기량 향상을 위해 훈련 프로그램을 설계하고 감독의 전술 구상을 보조하는 전문가입니다.",
        "co_careers": {"축구 감독": "팀 최고 지도자", "축구 분석관": "경기 영상 분석가"}
    },
    "재활 운동 전문가": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&auto=format&fit=crop&q=80",
        "summary": "수술 후 운동 기능이 떨어진 환자들에게 단계별 재활 체조를 시켜 일상 복귀를 돕는 운동 치료 이야기입니다.",
        "career_info": "재활 운동 전문가는 관절 및 근육 부상 후 일상 운동 능력을 회복하도록 맞춤 운동 처방을 지도하는 전문가입니다.",
        "co_careers": {"물리치료사": "도수 및 물리치료사", "선수 재활 트레이너": "운동선수 재활 담당자"}
    },
    "치어리더": {
        "title": "치얼업",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&auto=format&fit=crop&q=80",
        "summary": "대학 응원단에 모여 신나는 안무와 응원가로 관객을 매료시키는 치어리더들의 청춘 이야기입니다.",
        "career_info": "치어리더는 경기장이나 응원 무대에서 열정적인 안무와 구호로 관객의 응원을 유도하고 사기를 북돋우는 전문가입니다.",
        "co_careers": {"응원단장": "관객 응원 구호 리더", "무대 안무가": "응원 동작 창작자"}
    },
    "경호원": {
        "title": "더 케이투 (THE K2)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=800&auto=format&fit=crop&q=80",
        "summary": "전직 특수부대 출신 경호원이 VIP 경호 임무를 맡아 위급한 위협으로부터 의뢰인을 완벽히 보호하는 액션 드라마입니다.",
        "career_info": "경호원은 요인 및 의뢰인의 신변을 신체적 위험으로부터 경계하고 안전하게 보호하는 보안 전문 인력입니다.",
        "co_careers": {"신변보호원": "VIP 전담 경호원", "경비 지도사": "보안 시스템 관리자"}
    },

    # 9. 교육
    "초등학교 교사": {
        "title": "동백꽃 필 무렵",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&auto=format&fit=crop&q=80",
        "summary": "어린 초등학생들의 자라나는 마음을 어루만져주고 기초 학습 능력을 따뜻하게 지도해주는 교사들의 이야기입니다.",
        "career_info": "초등학교 교사는 초등학생을 대상으로 전 교과목의 기초 학습 지도, 생활 지도, 바른 인성 형성을 담당하는 교육인입니다.",
        "co_careers": {"돌봄교사": "방과후 돌봄 교사", "초등학습 교재 기획자": "초등 교육 출판 전문가"}
    },
    "고등학교 교사": {
        "title": "블랙독",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&auto=format&fit=crop&q=80",
        "summary": "기간제 교사로 고등학교에 부임해 입시 스트레스 속 학생들의 진로 설계와 과목 수업을 열정적으로 펼치는 드라마입니다.",
        "career_info": "고등학교 교사는 전공 과목의 심화 지식을 가르치고 학생들의 대학 진학 및 사회 진출 진로 설계를 지도하는 교육인입니다.",
        "co_careers": {"진로진학 상담교사": "진학 전담 상담 교사", "EBS 강사": "방송 교과 강사"}
    },
    "유치원 교사": {
        "title": "안녕, 나야!",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=800&auto=format&fit=crop&q=80",
        "summary": "유아들의 눈높이에 맞춰 유아 발달에 필요한 신체 놀이와 표현 활동을 정성껏 이끄는 유아 교육 이야기입니다.",
        "career_info": "유치원 교사는 유아의 신체, 언어, 정서, 사회성 발달을 돕기 위해 놀이 중심 교육과정을 운영하는 교사입니다.",
        "co_careers": {"보육교사": "어린이집 보육 전문가", "유아 교구 개발자": "유아 교구 연구원"}
    },
    "상담교사": {
        "title": "소년심판",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1436450412740-6b988f486c6b?w=800&auto=format&fit=crop&q=80",
        "summary": "학교 폭력이나 교우 관계, 가정 고충으로 방황하는 학생들의 마음을 들어주고 따뜻한 위로와 상담을 건네는 상담실 이야기입니다.",
        "career_info": "상담교사(전문상담교사)는 학교 상담실에서 학생들의 정서 불안, 학업 스트레스, 또래 관계 상담을 집행하는 교사입니다.",
        "co_careers": {"청소년 상담사": "청소년 전문 상담가", "임상심리사": "정서 진단 평가사"}
    },
    "특수교사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&auto=format&fit=crop&q=80",
        "summary": "발달 장애나 신체적 장애를 가진 학생들의 특성에 맞춰 개별 맞춤 교육을 지원하고 사회 자립을 돕는 교육 드라마입니다.",
        "career_info": "특수교사는 시각, 청각, 지적 장애 등 특수교육 대상 학생들에게 맞춤형 교육과 일상 자립 훈련을 제공하는 전문가입니다.",
        "co_careers": {"언어치료사": "언어 발달 치료사", "특수교육 보조인": "학습 지원 보조원"}
    },
    "학원 강사": {
        "title": "일타 스캔들",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&auto=format&fit=crop&q=80",
        "summary": "대한민국 사교육 1번지에서 수천 명의 수강생을 끌어모으는 수학 일타강사의 로맨스 스캔들 드라마입니다.",
        "career_info": "학원 강사는 교과목 명확한 핵심 개념 전달과 시험 문제 분석을 통해 수강생들의 성적 향상을 이끄는 교육 전문가입니다.",
        "co_careers": {"학원 원장": "사교육 학원 경영자", "입시 컨설턴트": "수시 정시 진학 분석가"}
    },

    # 10. 전문직 / 경영 / 금융
    "변리사": {
        "title": "스타트업",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&auto=format&fit=crop&q=80",
        "summary": "기술 특허 등록과 특허 침해 분쟁으로부터 기술 스타트업의 핵심 기술 권리를 지켜주는 특허 전문가 이야기입니다.",
        "career_info": "변리사는 발명, 특허, 상표, 디자인 등 지식재산권의 등록 권리화 및 특허 소송을 대리하는 전문 법률가입니다.",
        "co_careers": {"특허심사관": "특허청 특허 심사 공무원", "기술가치평가사": "기술 가치 평가원"}
    },
    "회계사": {
        "title": "넘버스: 빌딩숲의 감시자들",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&auto=format&fit=crop&q=80",
        "summary": "회계법인의 부조리에 맞서 기업 회계 장부를 검증하고 정의를 구현해 나가는 오피스 드라마입니다.",
        "career_info": "공인회계사(CPA)는 기업 재무제표의 회계 감사, 세무 자문, 재무 컨설팅을 집행하여 금융 투명성을 지키는 전문가입니다.",
        "co_careers": {"세무사": "세금 납부 전문 대리인", "CFO": "기업 최고 재무 책임자"}
    },
    "세무사": {
        "title": "트레이서",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1554224154-26032ffc0d07?w=800&auto=format&fit=crop&q=80",
        "summary": "국세청 팀원들과 납세자의 복잡한 세금을 정확히 계산하고 소명하는 세무 전문가들의 드라마입니다.",
        "career_info": "세무사는 개인 및 기업의 세금 신고 대리, 세무 조사 소명, 절세 방안을 자문해 주는 세법 전문가입니다.",
        "co_careers": {"국세청 공무원": "세금 징수 조사관", "손해사정사": "보험 손해액 산정가"}
    },
    "노무사": {
        "title": "송곳",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800&auto=format&fit=crop&q=80",
        "summary": "부당해고에 직면한 노동자들을 위해 법률 지식과 노동법으로 부조리에 맞서는 노무 상담소 이야기입니다.",
        "career_info": "공인노무사는 노동관계 법령 자문, 부당해고 구제 신청, 임금체불 해결, 부당 노동 행위 중재를 전담하는 전문가입니다.",
        "co_careers": {"근로감독관": "고용노동부 노동 법규 감독관", "인사담당자": "기업 채용 관리자"}
    },
    "건축가": {
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&auto=format&fit=crop&q=80",
        "summary": "집을 설계해 달라는 의뢰를 받아 도면을 그리고 감성적인 건축물을 지어 올리는 건축가의 공간 이야기입니다.",
        "career_info": "건축가는 건축물의 공간 기능, 구조적 안전, 미관을 감안하여 도면을 설계하고 시공을 감독하는 공학 예술가입니다.",
        "co_careers": {"건축시공기술자": "현장 공사 책임자", "인테리어 디자이너": "실내 공간 연출가"}
    },
    "경영컨설턴트": {
        "title": "야망의 전설",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&auto=format&fit=crop&q=80",
        "summary": "기업의 경영 비효율 원인을 진단하고 사업 구조 조정과 마케팅 방향을 제시하는 컨설턴트들의 비즈니스 드라마입니다.",
        "career_info": "경영컨설턴트는 기업의 자원 배분, 마케팅, 조직 구조 문제를 진단하여 경영 효율 개선 솔루션을 제안하는 전문가입니다.",
        "co_careers": {"전략기획자": "기업 성장 전략 수립자", "데이터 분석가": "경영 수치 분석가"}
    },
    "마케팅 전문가": {
        "title": "대행사",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=800&auto=format&fit=crop&q=80",
        "summary": "소비자 니즈를 타겟팅하여 제품 매출을 수십 배 끌어올리는 마케팅 전략가들의 성장 이야기입니다.",
        "career_info": "마케팅 전문가는 타겟 소비자를 분석하고 브랜드 인지도 향상 및 매출 증대를 위한 기획, 프로모션을 집행하는 전문가입니다.",
        "co_careers": {"퍼포먼스 마케터": "디지털 광고 효율 분석가", "브랜드 매니저": "브랜드 총괄 관리자"}
    },
    "인사담당자": {
        "title": "김비서가 왜 그럴까",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800&auto=format&fit=crop&q=80",
        "summary": "임직원들의 인적 자원 관리, 복리후생, 채용 면접을 정돈되게 이끄는 기업 HR 인사팀 이야기입니다.",
        "career_info": "인사담당자(HR)는 우수 인재 채용, 임직원 평가, 조직 문화 개선, 급여 보상 체계를 기획 운영하는 전문가입니다.",
        "co_careers": {"헤드헌터": "인재 추천 매칭 전문가", "노무사": "노동법 자문가"}
    },
    "자산관리사": {
        "title": "국가부도의 날",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&auto=format&fit=crop&q=80",
        "summary": "금융 위기 속에서 고객들의 자산 손실을 막기 위해 리스크 포트폴리오를 빠르게 재구성하는 금융 자산관리사의 이야기입니다.",
        "career_info": "자산관리사(FP)는 고객의 재무 상태를 분석하여 주식, 채권, 부동산 등 맞춤형 금융 투자 포트폴리오를 제시하는 전문가입니다.",
        "co_careers": {"펀드매니저": "펀드 자산 운용가", "PB (프라이빗 뱅커)": "고액 자산가 전담 금융인"}
    },
    "펀드매니저": {
        "title": "작전",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&auto=format&fit=crop&q=80",
        "summary": "수백억 원의 주식 펀드를 운용하며 차트 분석과 기업 가치 평가로 막대한 수익을 내기 위해 사투를 벌이는 주식 영화입니다.",
        "career_info": "펀드매니저는 투자자들로부터 모은 자금을 가치 있는 자산에 투자하여 투자 수익률을 극대화하는 투자 운용 전문가입니다.",
        "co_careers": {"애널리스트": "기업 주가 분석 연구원", "주식 트레이더": "매수 매도 전문 매매인"}
    },

    # 11. 서비스 / 항공 / 관광
    "호텔리어": {
        "title": "호텔 델루나",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&auto=format&fit=crop&q=80",
        "summary": "엘리트 호텔리어가 최고급 룸서비스와 컨시어지 서비스를 정성을 다해 제공하는 드라마입니다.",
        "career_info": "호텔리어는 객실 예약, 고객 체크인 컨시어지, 식음료 서비스를 종합적으로 관장하는 객실 및 서비스 전문가입니다.",
        "co_careers": {"컨시어지": "고객 맞춤 안내 전문가", "호텔 지배인": "호텔 서비스 총괄 운영자"}
    },
    "항공기 승무원": {
        "title": "플라이트",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1540339832862-47459980783b?w=800&auto=format&fit=crop&q=80",
        "summary": "항공기 기내 비상 상황 속에서도 침착함을 잃지 않고 승객들의 인명 안전을 도모하는 객실 승무원들의 이야기입니다.",
        "career_info": "항공기 승무원은 기내 탑승객의 비상 안전 관리를 전담하고 쾌적한 승객 서비스를 제공하는 서비스 안전 전문가입니다.",
        "co_careers": {"지상직 승무원": "공항 수속 전담인", "항공기 조종사": "기장 및 부기장"}
    },
    "항공기 조종사": {
        "title": "탑건: 매버릭",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1519074069444-1ba4fff16be3?w=800&auto=format&fit=crop&q=80",
        "summary": "하늘 위에서 항공기 계기를 조종하며 안전하게 목표 지점까지 도착하는 파일럿 이야기입니다.",
        "career_info": "항공기 조종사(파일럿)는 항공기의 비행 경로를 정밀 조종하고 기상 변화에 신속히 대응하여 승객과 화물을 이송합니다.",
        "co_careers": {"항공관제사": "이착륙 경로 통제관", "항공정비사": "항공기 정밀 정비사"}
    },
    "여행 기획자": {
        "title": "더 패키지",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&auto=format&fit=crop&q=80",
        "summary": "패키지 여행 코스를 직접 기획하고 손님들과 함께 투어를 다니며 추억을 담아내는 여행 이야기입니다.",
        "career_info": "여행 기획자(투어 플래너)는 현지 관광 코스, 숙박, 교통 인프라를 조합하여 창의적인 여행 상품을 설계하는 전문가입니다.",
        "co_careers": {"관광 통역 안내사": "현지 가이드", "항공권 예약 발권 전문가": "투어 티케팅 담당자"}
    },
    "파티플래너": {
        "title": "위대한 개츠비",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&auto=format&fit=crop&q=80",
        "summary": "특별한 파티 콘셉트와 음악, 연회를 완벽히 세팅하여 잊지 못할 밤을 만들어내는 파티 기획자 이야기입니다.",
        "career_info": "파티플래너는 파티의 주제 선정, 장소 대관, 테마 장식, 음향, 케이터링 코디를 총괄하여 행사를 이끄는 연출가입니다.",
        "co_careers": {"웨딩플래너": "결혼식 기획자", "케이터링 셰프": "연회 음식 연출가"}
    }
}

# 기본 처리 이미지
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&auto=format&fit=crop&q=80"

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
        당신은 미디어 및 진로 전문가입니다. 직업 '{search_job}'에 대한 정보를 이모티콘 없이 명확하고 정갈하게 작성해 주세요.
        
        [대표 작품]: (이 직업이 대표적으로 등장하는 영화 또는 드라마 제목)
        [작품 구분]: (영화 또는 드라마)
        [작품 줄거리]: (작품 전체의 핵심 줄거리를 상세히 작성)
        [진로 상세 소개]: (해당 직업이 하는 일, 필요 역량, 진로 전망을 상세히 작성)
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
st.markdown('<div class="sub-title">인기 대표 직업을 클릭하거나 검색창에 원하는 직업을 입력해보세요.</div>', unsafe_allow_html=True)

# 1. 인기 직업 5개만 깔끔히 노출
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
    placeholder="예: 래퍼, 변호사, 소프트웨어 개발자, 패션 디자이너, 항공기 조종사..."
).strip()

st.session_state.search_term = input_value

# ---------------------------------------------------------
# 결과 출력 세션
# ---------------------------------------------------------
if st.session_state.search_term:
    st.divider()
    search_query = st.session_state.search_term
    
    # DB 매칭
    matched_key = None
    for key in CAREER_DATABASE.keys():
        if key in search_query or search_query in key:
            matched_key = key
            break

    if matched_key:
        data = CAREER_DATABASE[matched_key]
        
        col_poster, col_info = st.columns([1, 1.6])
        
        with col_poster:
            st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
            st.image(
                data["poster"],
                use_container_width=True,
                caption=f"[{data['type']}] {data['title']} 공식 연출 및 장면"
            )
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
                <div class="card-title">진로 및 직업 상세 가이드 ({matched_key})</div>
                <div class="card-text">{data["career_info"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # 작품 내 연관 직업
        if "co_careers" in data and data["co_careers"]:
            st.write("")
            st.markdown(f"### [{data['title']}] 속 연관 직업 정보")
            
            co_cols = st.columns(len(data["co_careers"]))
            for idx, (co_job, co_desc) in enumerate(data["co_careers"].items()):
                with co_cols[idx]:
                    with st.expander(f"**{co_job}**", expanded=True):
                        st.write(co_desc)

    else:
        # DB 미등록 검색어일 경우 Gemini AI 호출
        st.info(f"등록된 미디어 데이터를 기반으로 분석 가이드를 생성 중입니다.")
        with st.spinner("정보 분석 및 가이드 생성 중..."):
            ai_result, error = get_gemini_recommendation(search_query)
            if error:
                st.error(error)
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.6])
                with col_poster:
                    st.image(
                        DEFAULT_IMAGE,
                        caption=f"{search_query} 관련 미디어 추천",
                        use_container_width=True
                    )
                with col_info:
                    st.markdown(f"<h1>AI 가이드 분석: {search_query}</h1>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="card-text">{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
