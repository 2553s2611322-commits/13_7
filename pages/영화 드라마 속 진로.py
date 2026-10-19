import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화/드라마 속 진로 탐색기",
    page_icon="🎬",
    layout="wide"
)

# 깔끔하고 모던한 미니멀 디자인 CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
        text-align: center;
        letter-spacing: -0.02em;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .poster-frame {
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-text {
        font-size: 0.98rem;
        line-height: 1.7;
        color: #334155;
    }
    .job-badge {
        background-color: #EFF6FF;
        color: #2563EB;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# ---------------------------------------------------------
# 사전 정의된 데이터베이스 (상세하고 긴 설명 적용)
# ---------------------------------------------------------
CAREER_DATABASE = {
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://i.namu.wiki/i/ef_sXHPS0n5WXXPMy_beluYPRxdyU1Xp498X8xSROif2NmttieYaaRYM7WUj8zj71FEdEfyCsxXmjc_d39jWbg.webp",
        "summary": "IQ 164의 천재적인 두뇌와 자폐스펙트럼을 동시에 가진 신입 변호사 우영우가 대형 로펌 '한바다'에 입사하여 다양한 사건들을 자신만의 독창적인 시각으로 해결해 나가는 법정 휴먼 드라마입니다. 사회적 편견과 고정관념에 맞서며 의뢰인의 진심을 끌어내고, 진정한 법조인이자 사회 구성원으로 거듭나는 가슴 따뜻한 성장을 다룹니다.",
        "career_info": "변호사는 법률에 대한 전문적 지식을 바탕으로 의뢰인의 권리를 보호하고 법적 분쟁을 대리하는 전문직입니다. 민사·형사 사건의 소송 수행, 법률 자문, 계약서 검토 등 다양한 법률 서비스를 제공합니다. 철저한 논리적 사고력과 문제 해결 능력, 문서 작성 기술이 필수적이며, 무엇보다 의뢰인의 사정을 깊이 이해하고 공감하면서도 객관적인 판단력을 유지하는 윤리의식과 소통 역량이 중요합니다."
    },
    "요리사": {
        "title": "파스타 (Pasta)",
        "type": "드라마",
        "poster": "https://i.namu.wiki/i/y8WOfzKIiRwC6WM8Z2RvyfZ1eG5qEc1hMi6VvZZ2u10yw5DwulSRrs_lqXJu07BQC38zwvJwVTxcWr4PQK99mw.webp",
        "summary": "이탈리안 레스토랑 '라스페라'를 배경으로, 삼류 주방 보조에서 시작해 일류 셰프를 꿈꾸는 주인공의 치열한 도전과 주방 안에서의 뜨거운 진검승부를 그린 드라마입니다. 완벽주의 셰프와의 갈등과 협력을 통해 음식에 대한 철학과 레스토랑 주방의 리얼한 생태계를 선명하게 보여줍니다.",
        "career_info": "요리사(셰프)는 식재료 선정부터 메뉴 개발, 음식 조리, 그리고 레스토랑 주방 전반의 위생과 팀원들을 관리하는 종합 맛의 아티스트이자 매니저입니다. 미각과 시각을 사로잡는 창의적인 감각은 물론, 고된 조리 과정을 견뎌낼 체력과 신속 정확한 위기 대처 능력이 필요합니다. 또한 대형 주방을 효과적으로 운영하기 위한 리더십과 팀워크가 핵심적인 역량으로 평가받습니다."
    },
    "의사": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcThr8iEUCVGH3KYnd7LGycHt9hvx0J-i4vHVZLvzBKVU1pgosQNmM83JWQHwkjxTiuP3g71DPfgBQFQesg",
        "summary": "누군가는 태어나고 누군가는 삶을 끝내는 인생의 축소판이라 불리는 병원에서, 20년지기 의사 친구 5인방이 펼쳐가는 병원 일상과 환자들과의 가슴 깊은 에피소드를 다룬 드라마입니다. 생사의 갈림길에서 치열하게 분투하는 의료진의 사명감과 인간적인 고민을 진솔하게 담아냈습니다.",
        "career_info": "의사는 인간의 질병을 진단하고 치료하여 생명을 살리는 고도의 전문 의료인입니다. 신체 및 정신적 질환에 관한 학문적 지식을 바탕으로 수술, 처방, 종합 정밀 검사를 시행합니다. 긴급한 상황에서도 신속하고 정확하게 판단할 수 있는 냉철한 집중력과 더불어, 환자와 보호자의 마음을 어루만질 수 있는 따뜻한 공감 능력 및 생명 존중 윤리관이 최우선으로 요구됩니다."
    },
    "과학자": {
        "title": "마션 (The Martian)",
        "type": "영화",
        "poster": "https://i.namu.wiki/i/cXSKxR4Fa1lI-dUFlXVHCPIxpME78sh6WEAAO8Ddj3qodypZ2umRe3pjSV3enB9gwUaAsk-9eP-eVfOR2WZ18g.webp",
        "summary": "화성 탐사 중 뜻밖의 모래폭풍을 만나 고립된 식물학자 겸 탐사원 마크 와트니가 자신의 지식과 과학적 원리를 동원하여 극한의 우주 환경에서 살아남는 생존기를 그린 영화입니다. 식량 제조, 수소 합성, 통신 장비 복구 등 지식 기반의 창의적 생존법이 돋보입니다.",
        "career_info": "과학자는 자연 세계의 원리와 법칙을 관찰·실험·분석하여 새로운 이론을 규명하고 기술을 개발하는 연구자입니다. 관찰력과 가설 검증 능력, 수리·논리적 비판력이 핵심입니다. 문제에 직면했을 때 기존 공식을 넘어서는 창의적인 사고방식과 실패에 굴하지 않고 끊임없이 탐구하는 끈기가 요구됩니다."
    },
    "건축가": {
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQjVg-k3nYJMmfOerIXfYWe1y-cj4YwZMokPH4Guy5Gzl7p2YRAgNEHkWfI77-HsMgvPQhengcTYnKsotA",
        "summary": "건축사사무소에 근무하는 주인공 승민에게 15년 만에 나타난 첫사랑 서연이 자신의 옛 추억이 담긴 제주도 집을 새로 지어달라고 의뢰하면서, 공간을 완성함과 동시에 서로의 마음을 치유해 나가는 감성 휴먼 영화입니다.",
        "career_info": "건축가는 사용자의 필요와 삶의 형태를 반영하여 안전하고 아름다운 공간 구조물을 기획하고 설계하는 전문가입니다. 예술적 미적 감각과 공간 지각력은 물론, 건축 법규와 구조 안전성을 정확히 계산해 내는 공학적 지식이 동시에 필요합니다. 의뢰인의 요구사항을 경청하고 도면으로 구현해내는 경청과 커뮤니케이션 능력이 필수적입니다."
    }
}

OTHER_CAREERS = {
    "국정원 요원 (비밀요원)": "국가의 안보 정보를 수집·분석하며 국가적 위기를 예방하는 직업입니다. 높은 분석력과 판단력, 철저한 보안 의식 및 순발력이 필요합니다. (대표작: 영화 '아저씨', 드라마 '아이리스')",
    "기자 / 언론인": "취재를 통해 사실관계를 검증하고 사회적 이슈를 보도합니다. 비판적 사고, 직업 윤리, 정확한 문장 구성 및 전달력이 핵심입니다. (대표작: 드라마 '피노키오', '뉴스룸')",
    "프로파일러": "범죄 현장의 정황과 행동 패턴을 분석하여 범인의 심리 상태 및 특성을 추정하는 경찰 범죄분석관입니다. 심리학 지식과 논리적 추론 능력이 필수적입니다. (대표작: 드라마 '시그널', '악의 마음을 읽는 자들')",
    "소방관": "화재 진압, 재난 구조, 긴급 구급 활동을 통해 인명과 재산을 보호합니다. 투철한 사명감, 신체적 체력, 순간적인 위기 대처 능력이 필요합니다. (대표작: 영화 '신과함께', 드라마 '소방서 옆 경찰서')",
    "운동선수": "특정 스포츠 종목에서 체력과 기술을 극대화하여 경기에 임하는 전문가입니다. 철저한 자기 관리, 훈련 끈기, 승부욕이 요구됩니다. (대표작: 드라마 '스물다섯 스물하나', 영화 '국가대표')"
}

# ---------------------------------------------------------
# Gemini API 호출 함수 (상세한 내용 생성 프롬프트)
# ---------------------------------------------------------
def get_gemini_recommendation(search_job):
    """Gemini API를 호출하여 데이터베이스에 없는 직업 정보 생성"""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되지 않았습니다. Secrets 설정을 확인해주세요."
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        당신은 진로 및 영화/드라마 미디어 전문가입니다. 입력된 직업 '{search_job}'에 관한 정보를 아래 양식에 맞추어 풍부하고 상세하게 작성해 주세요.
        
        [제목]: (이 직업이 주요 역할로 등장하는 대표 영화 또는 드라마 1개의 정확한 제목)
        [구분]: (영화 또는 드라마)
        [줄거리]: (작품의 핵심 줄거리와 주인공의 활약을 4~5문장 이상으로 구체적이고 깊이 있게 설명)
        [진로소개]: (이 직업이 수행하는 핵심 업무, 작업 환경, 요구되는 핵심 자질 및 필요한 역량을 4~5문장 이상으로 상세히 설명)
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
st.markdown('<div class="main-title">🎬 영화·드라마 속 진로 탐색기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">관심 있는 진로 및 직업을 검색하고 대표 작품과 상세 진로 가이드를 확인해보세요.</div>', unsafe_allow_html=True)

# 인기 진로 추천 태그 영역
st.caption("🔥 인기 진로 추천 (클릭 시 자동 검색)")
rec_cols = st.columns(len(CAREER_DATABASE))
for idx, key in enumerate(CAREER_DATABASE.keys()):
    if rec_cols[idx].button(key, use_container_width=True, key=f"btn_{key}"):
        st.session_state.search_term = key

# 진로 입력창
input_value = st.text_input(
    "탐색할 진로/직업을 입력하세요:", 
    value=st.session_state.search_term,
    placeholder="예: 변호사, 요리사, 의사, 과학자, 건축가, 프로게이머..."
).strip()

st.session_state.search_term = input_value

# ---------------------------------------------------------
# 결과 출력 세션 (진로/직업 입력 후에만 노출)
# ---------------------------------------------------------
if st.session_state.search_term:
    st.divider()
    search_query = st.session_state.search_term
    
    # 1. DB 매칭 확인
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
            st.image(data["poster"], use_container_width=True, caption=f"공식 포스터 | [{data['type']}] {data['title']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f'<span class="job-badge">{data["type"]}</span>', unsafe_allow_html=True)
            st.markdown(f"# {data['title']}")
            
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📖 작품 상세 줄거리</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-text">{data["summary"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">💡 진로/직업 상세 소개 ({matched_key})</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-text">{data["career_info"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # 2. DB에 없는 직업일 경우 Gemini AI 사용
        st.info(f"💡 DB에 등록되지 않은 직업입니다. Gemini AI가 관련 정보를 탐색합니다.")
        with st.spinner("AI가 관련 영화/드라마 포스터와 상세 가이드를 준비하는 중입니다..."):
            ai_result, error = get_gemini_recommendation(search_query)
            
            if error:
                st.error(error)
                st.warning("GEMINI_API_KEY가 등록되어 있는지 확인해주세요.")
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.6])
                with col_poster:
                    st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
                    st.image(
                        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
                        caption=f"{search_query} 관련 대표 작품 추천",
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with col_info:
                    st.markdown(f"# 🤖 AI 분석 결과: {search_query}")
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-text">{ai_result}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ---------------------------------------------------------
    # 하단: 기타 미디어 속 진로 탐색 (검색 후에만 표시)
    # ---------------------------------------------------------
    st.markdown("### 🌟 스크린 속 또 다른 다양한 직업들")
    st.caption("궁금한 직업 카드를 클릭하면 상세 설명과 대표 작품을 볼 수 있습니다.")

    grid_cols = st.columns(3)
    for idx, (job_title, job_desc) in enumerate(OTHER_CAREERS.items()):
        col_idx = idx % 3
        with grid_cols[col_idx]:
            with st.expander(f"📌 **{job_title}**"):
                st.write(job_desc)
