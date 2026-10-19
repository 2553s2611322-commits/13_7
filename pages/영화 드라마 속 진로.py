import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화/드라마 속 진로 탐색기",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS로 깔끔하고 현대적인 디자인 연출
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .career-card {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 20px;
        color: #1E293B;
    }
    .job-badge {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화 (검색어 유지용)
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# ---------------------------------------------------------
# 사전 정의된 데이터베이스 (기본 안정적 데이터)
# ---------------------------------------------------------
CAREER_DATABASE = {
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=80",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 동시에 가진 신입 변호사 우영우가 다양한 사건을 해결하며 진정한 로펌 변호사로 성장하는 과정을 그린 법정 휴먼 드라마입니다.",
        "career_info": "변호사는 법률 사건에 대한 자문과 소송을 대리하는 법률 전문가입니다. 의뢰인의 입장을 대변하면서도 공정성과 논리적 사고력, 법률 지식, 세심한 관찰력이 필요합니다.",
        "video_url": "https://www.youtube.com/watch?v=9S3U-4o_25A"
    },
    "요리사": {
        "title": "파스타 (Pasta)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&auto=format&fit=crop&q=80",
        "summary": "이탈리안 레스토랑을 배경으로, 일류 요리사를 꿈꾸는 주인공의 성장과 주방 내부의 뜨거운 진검승부를 다룬 리얼 키친 드라마입니다.",
        "career_info": "요리사(셰프)는 메뉴를 기획하고 식재료를 관리하며 레스토랑의 주방을 총괄합니다. 체력, 미각, 창의성과 더불어 바쁜 주방을 지휘하는 리더십과 팀워크가 핵심 요구됩니다.",
        "video_url": "https://www.youtube.com/watch?v=W3A4_3wD4Yg"
    },
    "의사": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&auto=format&fit=crop&q=80",
        "summary": "병원에서 하루하루를 살아가는 사람들과 20년지기 의사 친구들의 휴머니즘과 우정을 담은 드라마입니다.",
        "career_info": "의사는 환자의 질병을 진단하고 치료하는 의료 전문가입니다. 높은 전문 지식과 빠른 판단력, 그리고 환자의 아픔에 공감할 수 있는 따뜻한 생명 존중 정신이 중요합니다.",
        "video_url": "https://www.youtube.com/watch?v=NInS-9IvdW8"
    },
    "과학자": {
        "title": "마션 (The Martian)",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80",
        "summary": "화성에 고립된 식물학자가 과학적 지식과 기발한 응용력을 발휘하여 극한의 환경에서 생존해 나가는 우주 생존 영화입니다.",
        "career_info": "과학자는 자연 법칙과 기술적 원리를 연구하는 전문가입니다. 논리적 비판 사고력, 가설 검증 능력, 문제 발생 시 창의적인 원인 분석 능력이 필수적입니다.",
        "video_url": "https://www.youtube.com/watch?v=ej3ioOneTy8"
    },
    "건축가": {
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&auto=format&fit=crop&q=80",
        "summary": "건축사사무소에 근무하는 주인공이 옛 추억이 담긴 공간과 집을 새로 지어주며 펼쳐지는 이야기를 다룬 휴먼 로맨스 영화입니다.",
        "career_info": "건축가는 사람들의 보금자리와 공간을 기획하고 설계하는 창의적 분야입니다. 공간 감각과 예술성, 그리고 안전한 건축 구조를 고려하는 공학적 설계 능력이 종합적으로 요구됩니다.",
        "video_url": "https://www.youtube.com/watch?v=2n5qCj0M144"
    }
}

OTHER_CAREERS = {
    "국정원 요원 (비밀요원)": "국가의 안보 정보를 수집하고 분석하는 직업으로 통찰력, 순간 판단력, 철저한 사명감과 보안 의식이 요구됩니다. (대표작: 영화 '아저씨', 드라마 '아이리스')",
    "기자 / 언론인": "취재를 통해 사실을 보도하고 사회적 이슈를 공론화합니다. 비판적 사고, 직업 윤리, 정확한 전달력이 중요합니다. (대표작: 드라마 '피노키오', '뉴스룸')",
    "프로파일러": "범죄자의 행동과 심리를 과학적으로 분석하여 수사를 돕는 직업입니다. 심리학 지식과 철저한 논리 분석력이 핵심입니다. (대표작: 드라마 '시그널', '악의 마음을 읽는 자들')",
    "소방관": "화재 진압과 긴급 재난 상황에서 인명을 구조합니다. 강한 사명감, 신체적 체력, 위기 대응 능력이 필요합니다. (대표작: 영화 '신과함께', 드라마 '소방서 옆 경찰서')",
    "운동선수": "특정 스포츠 종목에서 신체 기량을 극대화하여 경쟁합니다. 절제력, 꾸준한 훈련, 강한 승부욕이 필수적입니다. (대표작: 드라마 '스물다섯 스물하나', 영화 '국가대표')"
}

# ---------------------------------------------------------
# Gemini API 호출 함수 (오류 예외처리 강화)
# ---------------------------------------------------------
def get_gemini_recommendation(search_job):
    """Gemini API를 활용해 데이터베이스에 없는 직업 정보 즉석 생성"""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되지 않았습니다. Secrets 구성을 확인해주세요."
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        당신은 진로 및 미디어 콘텐츠 전문가입니다. 입력된 직업 '{search_job}'에 대한 정보를 아래 작성 형식에 맞춰 정확히 작성해 주세요.
        
        **[대표 작품]**: (이 직업이 주요 역할로 등장하는 영화 또는 드라마 1개 제목)
        **[작품 구분]**: (영화 또는 드라마)
        **[간단 줄거리]**: (작품의 줄거리 2~3문장)
        **[진로/직업 소개]**: (이 직업이 하는 일과 필요한 핵심 역량 2~3문장)
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
st.markdown('<div class="main-header">🎬 영화·드라마 속 진로 탐색기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">궁금한 진로/직업을 입력하고 관련 미디어 작품과 진로 가이드, 하이라이트를 확인해 보세요!</div>', unsafe_allow_html=True)

# 추천 키워드 버튼 영역
st.caption("💡 인기 직업 빠른 탐색 (아래 버튼 클릭)")
rec_cols = st.columns(len(CAREER_DATABASE))
for idx, key in enumerate(CAREER_DATABASE.keys()):
    if rec_cols[idx].button(key, use_container_width=True, key=f"btn_{key}"):
        st.session_state.search_term = key

# 입력 창
input_value = st.text_input(
    "탐색하고 싶은 진로/직업을 입력하거나 선택하세요:", 
    value=st.session_state.search_term,
    placeholder="예: 변호사, 요리사, 의사, 과학자, 건축가, 우주비행사..."
).strip()

st.session_state.search_term = input_value

st.divider()

# ---------------------------------------------------------
# 결과 출력 세션
# ---------------------------------------------------------
if st.session_state.search_term:
    search_query = st.session_state.search_term
    
    # 1. DB 일치 여부 확인
    matched_key = None
    for key in CAREER_DATABASE.keys():
        if key in search_query or search_query in key:
            matched_key = key
            break

    if matched_key:
        data = CAREER_DATABASE[matched_key]
        st.subheader(f"🔍 '{matched_key}' 관련 추천 작품")
        
        col_left, col_right = st.columns([1, 1.2])
        
        with col_left:
            st.image(data["poster"], use_container_width=True, caption=f"[{data['type']}] {data['title']}")
            st.markdown("#### 🍿 영상 하이라이트")
            try:
                st.video(data["video_url"])
            except Exception:
                st.info("영상 링크를 불러올 수 없습니다.")
            
        with col_right:
            st.markdown(f'<span class="job-badge">{data["type"]}</span>', unsafe_allow_html=True)
            st.markdown(f"## {data['title']}")
            
            st.markdown('<div class="career-card">', unsafe_allow_html=True)
            st.markdown("### 📖 간단 줄거리")
            st.write(data["summary"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="career-card" style="border-left-color: #10B981;">', unsafe_allow_html=True)
            st.markdown(f"### 💡 진로 소개: {matched_key}")
            st.write(data["career_info"])
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # 2. DB에 없을 경우 Gemini AI 활용
        st.info(f"💡 기본 DB에 없는 직업입니다. AI(Gemini 2.5 Flash Lite)가 정보를 즉석 생성합니다.")
        with st.spinner("AI가 관련 영화/드라마 및 진로 가이드를 생성 중입니다..."):
            ai_result, error = get_gemini_recommendation(search_query)
            
            if error:
                st.error(error)
                st.warning("AI 키 설정을 확인하거나 기본 데이터('변호사', '요리사', '의사', '과학자', '건축가')를 입력해 보세요.")
            elif ai_result:
                col_left, col_right = st.columns([1, 1.2])
                with col_left:
                    st.image(
                        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
                        caption="AI 가이드 추천",
                        use_container_width=True
                    )
                with col_right:
                    st.markdown(f"## 🤖 AI 탐색 결과: {search_query}")
                    st.markdown('<div class="career-card">', unsafe_allow_html=True)
                    st.markdown(ai_result)
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👆 위 입력창에 직업을 입력하거나 빠른 탐색 버튼을 누르면 해당 진로의 영화/드라마 정보가 나타납니다.")

st.divider()

# ---------------------------------------------------------
# 하단: 기타 미디어 속 다양한 진로 탐색 (클릭 시 설명)
# ---------------------------------------------------------
st.subheader("🌟 스크린 속 또 다른 다양한 직업들")
st.caption("아래 직업 카드를 클릭하면 간단한 설명과 대표 작품을 확인할 수 있습니다.")

grid_cols = st.columns(3)
for idx, (job_title, job_desc) in enumerate(OTHER_CAREERS.items()):
    col_idx = idx % 3
    with grid_cols[col_idx]:
        with st.expander(f"📌 **{job_title}**"):
            st.write(job_desc)
