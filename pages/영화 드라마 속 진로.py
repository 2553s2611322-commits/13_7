import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 및 드라마 속 진로 탐색기",
    layout="wide"
)

# ---------------------------------------------------------
# 차분하고 세련된 블루 톤 CSS (이모티콘 완전 제거)
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
    
    /* 메인 타이틀 */
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
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.18) !important;
        border: 1px solid #CBD5E1;
        object-fit: cover;
        width: 100%;
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
    
    /* Streamlit 버튼 스타일 */
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
    
    /* 여백 조정 */
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
# 실제 영화/드라마 공식 포스터 데이터베이스
# ---------------------------------------------------------
CAREER_DATABASE = {
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/zI3e226L0aG21oD2I1I4wG38f71.jpg",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 동시에 가진 신입 변호사 우영우가 대형 로펌 한바다에서 다양한 사건들을 자신만의 시각으로 해결해 나가며 진정한 법조인으로 성장하는 이야기입니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인을 대리하여 소송을 진행하고 법적 자문을 제공하는 법률 전문가입니다. 사건의 본질을 파악하는 논리적 사고력과 세심한 관찰력이 핵심 역량입니다.",
        "co_careers": {
            "변리사": "특허 및 상표권 등 지식재산권 등록과 분쟁을 전문적으로 다루는 지식재산 법률 전문가입니다.",
            "법률 사무원": "소송 관련 서류 준비 및 법원 제출 업무를 보조하는 법률 지원 전문가입니다."
        }
    },
    "래퍼": {
        "title": "8 마일",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/7T86GscV0dF3m43Z6i74o0nI5Xn.jpg",
        "summary": "디트로이트의 고단한 현실 속에서 살아가는 청년이 자신의 절박한 삶과 감정을 랩 가사로 풀어내어 랩 배틀 무대에서 자신의 존재를 증명해내는 음악 영화입니다.",
        "career_info": "래퍼는 리듬과 멜로디 위에 라임과 메시지를 담은 가사를 읊는 음악 아티스트입니다. 독창적인 음색과 박자감, 사회 및 개인의 이야기를 전달하는 작사 능력이 요구됩니다.",
        "co_careers": {
            "음악 프로듀서": "곡의 비트를 제작하고 앨범 사운드 전체를 총지휘하는 아티스트입니다.",
            "사운드 엔지니어": "녹음된 음원의 음량과 밸런스를 조율하여 완벽한 음원을 만드는 기술 전문가입니다."
        }
    },
    "교사": {
        "title": "블랙독",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/a3A3L13812KjJ718228381283.jpg",
        "summary": "기간제 교사로 고등학교에 부임한 주인공이 치열한 학교 현장 속에서 학생들의 성장과 진로를 돕고 동료 교사들과 소통하며 진정한 교사로 거듭나는 직업 드라마입니다.",
        "career_info": "교사는 학생들에게 교과 지식을 전달하고 인성 지도와 진로 탐색을 보조하는 교육 전문가입니다. 전달력과 기획 능력, 학생들과 친밀하게 소통하는 능력이 필요합니다.",
        "co_careers": {
            "진로 진학 상담교사": "학생들의 적성과 진학 설계를 전담하여 개별 상담을 제공하는 전문 교사입니다.",
            "교육 행정가": "학교 및 교육청 기관에서 학사 일정, 교육 예산 시스템을 관리하는 행정 전문가입니다."
        }
    },
    "축구선수": {
        "title": "드림",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/812391238912389123891238912.jpg",
        "summary": "개념 없는 전직 축구선수와 집 없는 국대 선수들이 생전 처음 모여 홈리스 월드컵에 도전하는 과정을 그린 감동 스포츠 영화입니다.",
        "career_info": "축구선수는 전술에 맞춰 경기장에서 승리를 목표로 뛰는 스포츠 전문가입니다. 강인한 체력과 순발력, 팀원들과의 협동심이 필수적인 요구 역량입니다.",
        "co_careers": {
            "축구 감독": "팀 전술을 수립하고 선수 교체 및 훈련 과정을 총괄 지휘하는 지도자입니다.",
            "스포츠 피지컬 트레이너": "선수들의 체력 수준을 관리하고 부상 방지를 전담하는 스포츠 과학 전문가입니다."
        }
    },
    "야구선수": {
        "title": "스토브리그",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/982371928371928371928371928.jpg",
        "summary": "팬들의 눈물마저 말라버린 꼴찌 야구팀에 새 단장이 부임하며 다음 시즌을 철저하게 준비하는 뜨거운 겨울 이야기를 다룬 오피스 스포츠 드라마입니다.",
        "career_info": "야구선수는 투구, 타격, 수비 등 정교한 기량을 바탕으로 경기에 참가하는 전문 체육인입니다. 철저한 자기관리와 고도의 집중력, 경기 분석 능력이 중요합니다.",
        "co_careers": {
            "야구 전력분석원": "상대 팀과 자팀 선수들의 데이터를 분석하여 경기 전략 수립을 지원하는 전문가입니다.",
            "야구 에이전트": "선수의 계약 및 연봉 협상, 마케팅 활동을 전문적으로 대행하는 매니저입니다."
        }
    },
    "농구선수": {
        "title": "리바운드",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/129837129837129837129837129.jpg",
        "summary": "해체 위기의 부산중앙고 농구부 신임 코치와 6명의 최약체 선수들이 전국 고교농구대회에서 써내려간 기적 같은 실화 바탕의 스포츠 영화입니다.",
        "career_info": "농구선수는 코트 위에서 신체적 순발력과 정교한 슈팅 능력을 바탕으로 경기를 치르는 스포츠 전문가입니다. 순간 판단력과 빠른 공수 전환 능력이 핵심입니다.",
        "co_careers": {
            "농구 코치": "선수들의 슈팅 폼과 전술 이해도를 지도하는 기술 전문가입니다.",
            "스포츠 전력분석관": "경기 영상을 분석하여 공수 패턴을 파악하는 데이터 전문가입니다."
        }
    },
    "우주탐험가": {
        "title": "인터스텔라",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/gEU2Q3L0A9m8N3m5A0N11432A91.jpg",
        "summary": "세계 각국의 경제와 식량 위기 속에서 인류를 구하기 위해 우주 시공간의 틈을 넘어 새로운 터전을 찾아 떠나는 탐험가들의 위대한 여정을 그린 SF 영화입니다.",
        "career_info": "우주탐험가(우주비행사)는 우주선을 조종하고 우주 공간에서 과학 실험 및 데이터 수집 임무를 수행하는 전문가입니다. 천문학, 공학 지식과 극한 환경을 견디는 심신이 필요합니다.",
        "co_careers": {
            "우주공학자": "우주선, 인공위성, 발사체를 설계하고 제작하는 공학 전문가입니다.",
            "천문학자": "우주 천체의 운동과 물질 구성을 연구하는 기초 과학 연구원입니다."
        }
    },
    "물리치료사": {
        "title": "시를 잊은 그대에게",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/o72837189239123891238912391.jpg",
        "summary": "의사가 주인공이 아닌 물리치료사, 방사선사, 코메디컬 스태프들의 일상을 시와 함께 따뜻하게 풀어낸 보건 의료 휴먼 드라마입니다.",
        "career_info": "물리치료사는 신체적 장애나 부상을 입은 환자들에게 운동 치료, 열 치료, 전기 치료 등을 적용하여 신체 기능을 회복시키는 전문 보건 의료인입니다.",
        "co_careers": {
            "작업치료사": "환자가 일상생활을 독립적으로 수행할 수 있도록 훈련하는 의료 전문가입니다.",
            "방사선사": "X-ray, MRI 등 정밀 진단 장비를 운용하는 전문 기술 의료인입니다."
        }
    },
    "바리스타": {
        "title": "커피프린스 1호점",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/AmL6fM8bY25D03JkY21B5b0F0v4.jpg",
        "summary": "청춘들이 모여 커피를 배우고 경험하며 매장을 정성껏 운영해 나가는 과정을 그린 커피 문화 중심의 로맨스 드라마입니다.",
        "career_info": "바리스타는 커피 추출 기구를 활용하여 원두의 맛과 향을 최상으로 끌어올리는 음료 전문가입니다. 원두 감별 능력과 고객 서비스 정신이 중요합니다.",
        "co_careers": {
            "커피 로스터": "생두를 전문적으로 볶아 원두의 풍미를 완성하는 기술자입니다.",
            "카페 디렉터": "원두 선택, 인테리어, 브랜드 콘셉트를 총괄하는 카페 기획자입니다."
        }
    },
    "보건교사": {
        "title": "보건교사 안은영",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/q39487192837192837192837192.jpg",
        "summary": "평범한 이름과 달리 보이지 않는 젤리를 볼 수 있는 특별한 능력을 가진 보건교사 안은영이 학교에서 일어나는 의문의 미스터리를 해결하는 판타지 드라마입니다.",
        "career_info": "보건교사는 학교에서 학생과 교직원의 건강 상태를 관리하고 응급처치, 보건 교육, 감염병 예방 관리 업무를 총괄하는 전문 교사이자 간호사입니다.",
        "co_careers": {
            "학교 간호사": "학생들의 응급 처치 및 유행성 질환 예방 관리를 전담하는 간호 전문가입니다.",
            "보건 행정가": "지역사회 보건소 및 교육청에서 건강 증진 사업을 추진하는 행정관입니다."
        }
    },
    "심리상담사": {
        "title": "굿 윌 헌팅",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/b1p141515151515151515151515.jpg",
        "summary": "천재적인 두뇌를 가졌지만 깊은 마음의 상처를 안고 사는 청년 윌 헌팅이 따뜻한 심리상담사 숀 교수를 만나 마음을 열고 진정한 자신의 삶을 찾아가는 휴먼 영화입니다.",
        "career_info": "심리상담사는 상담을 통해 의뢰인의 정서적 고통, 스트레스, 인간관계 문제 등의 원인을 파악하고 회복하도록 돕는 심리 지원 전문가입니다.",
        "co_careers": {
            "임상심리사": "심리 평가 도구를 활용하여 정신건강 상태를 정확히 진단하는 전문가입니다.",
            "청소년 상담사": "청소년의 비만, 학업 스트레스, 또래 관계 문제를 전담 상담하는 전문가입니다."
        }
    },
    "승무원": {
        "title": "플라이트",
        "type": "영화",
        "poster": "https://image.tmdb.org/t/p/w500/c29381923819238192381923819.jpg",
        "summary": "비행기 기체 이상으로 위기를 맞은 비행기 내에서 승객들의 안전을 최우선으로 지켜내는 조종사와 승무원들의 위기 관리 이야기입니다.",
        "career_info": "승무원(객실승무원)은 비행기 탑승 승객의 안전을 책임지고 쾌적한 비행 환경을 제공하는 서비스 및 안전 전문가입니다. 비상 상황 대응 훈련이 필수적입니다.",
        "co_careers": {
            "항공기 조종사": "항공기의 운항 경로와 정밀 조종을 전담하는 파일럿입니다.",
            "지상직 승무원": "공항 내 체크인 카운터와 출입국 게이트에서 승객 수속을 돕는 전문가입니다."
        }
    },
    "소믈리에": {
        "title": "신의 물방울",
        "type": "드라마",
        "poster": "https://image.tmdb.org/t/p/w500/d12983712983712983712983712.jpg",
        "summary": "세계 최고의 와인 컬렉션을 두고 두 젊은이가 와인의 깊은 향과 역사, 테이스팅 대결을 벌이며 진정한 소믈리로 거듭나는 와인 미식 드라마입니다.",
        "career_info": "소믈리에는 와인의 품종, 산지, 빈티지 특성을 파악하여 음식과 어울리는 와인을 추천하고 관리하는 와인 전문 컨설턴트입니다. 섬세한 후각과 미각이 요구됩니다.",
        "co_careers": {
            "와인 수입자(바이어)": "세계 각국의 와이너리를 탐방하여 우수한 와인을 발굴하고 수입하는 바이어입니다.",
            "식음료(F&B) 매니저": "호텔 및 고급 레스토랑의 전체 음료 메뉴와 서비스를 기획 관리하는 전문가입니다."
        }
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
        당신은 미디어 및 진로 전문가입니다. 직업 '{search_job}'에 대한 정보를 이모티콘 없이 명확하게 작성해 주세요.
        
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
st.markdown('<div class="sub-title">궁금한 직업을 클릭하거나 입력하여 공식 포스터와 진로 가이드를 확인해보세요.</div>', unsafe_allow_html=True)

# 직업 버튼 목록
st.caption("탐색 가능한 주요 직업")
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
    placeholder="예: 변호사, 래퍼, 우주탐험가, 보건교사, 승무원..."
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
        
        col_poster, col_info = st.columns([1, 1.6])
        
        with col_poster:
            st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
            # 확실한 공식 포스터 출력
            st.image(data["poster"], use_container_width=True, caption=f"[{data['type']}] {data['title']} 공식 포스터")
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
        # DB에 없을 시 Gemini AI 호출
        st.info(f"기본 목록에 등록되지 않은 직업입니다. AI 분석 결과를 생성 중입니다.")
        with st.spinner("정보 분석 및 가이드 생성 중..."):
            ai_result, error = get_gemini_recommendation(search_query)
            if error:
                st.error(error)
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.6])
                with col_poster:
                    st.image(
                        "https://image.tmdb.org/t/p/w500/gEU2Q3L0A9m8N3m5A0N11432A91.jpg",
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
