import streamlit as st
import google.generativeai as genai
import json

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 Custom CSS (깔끔한 UI 구성)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화·드라마 속 진로 탐색기",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
    /* 메인 배경 및 타이틀 스타일 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* 카드 컨테이너 스타일 */
    .info-card {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .job-badge {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 내장 기본 데이터베이스 (Gemini API 미설정/오류 시 또는 빠른 반응을 위한 샘플)
# -----------------------------------------------------------------------------
BUILTIN_DATA = {
    "요리사": {
        "title": "파스타 (Drama)",
        "poster": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500&q=80",
        "video_url": "https://www.youtube.com/watch?v=S374IAnM2f8",
        "story": "레스토랑 '라스페라'를 배경으로 음식이라는 하나의 공통점으로 묶인 요리사들의 사랑과 성공을 그린 드라마다.",
        "job_desc": "요리사(셰프)는 식재료를 선별하고 음식을 조리하여 고객에게 제공합니다. 메뉴 개발, 주방 위생 관리, 팀원과의 협업 능력 및 맛에 대한 감각이 핵심 역량입니다."
    },
    "건축가": {
        "title": "건축학개론 (Movie)",
        "poster": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=500&q=80",
        "video_url": "https://www.youtube.com/watch?v=J3mR6b5K_qY",
        "story": "생전 처음 집을 지어달라며 나타난 첫사랑 승민과 서연이 함께 집을 완성해 가는 과정을 담은 로맨스 영화다.",
        "job_desc": "건축가는 공간을 기획하고 사용자의 니즈에 맞는 건물을 설계합니다. 공간감, 디자인적 미감, 공학적 이해 및 의뢰인과의 소통 능력이 요구됩니다."
    },
    "검사": {
        "title": "비밀의 숲 (Drama)",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=500&q=80",
        "video_url": "https://www.youtube.com/watch?v=2e6M6qW93v4",
        "story": "감정을 잃어버린 외톨이 검사 황시목이 정의롭고 따뜻한 형사 한여진과 함께 검찰 스폰서 살인사건과 그 뒤에 숨겨진 진실을 파헤치는 추적극이다.",
        "job_desc": "검사는 범죄 사건을 수사하고 공소를 제기하며 재판을 진행합니다. 법률 지식, 논리적 분석력, 공정함 및 윤리의식이 핵심인 법조 직업입니다."
    },
    "프로그래머": {
        "title": "스타트업 (Drama)",
        "poster": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=500&q=80",
        "video_url": "https://www.youtube.com/watch?v=BemKyzbLDkc",
        "story": "한국의 Silicon Valley에서 성공을 꿈꾸며 스타트업에 뛰어든 청춘들의 시작(START)과 성장(UP)을 그린 드라마다.",
        "job_desc": "소프트웨어 개발자/프로그래머는 아이디어를 코드 구현으로 실체화합니다. 문제 해결 능력, 논리적 사고, 최신 기술 트렌드 학습 열정이 필요합니다."
    }
}

OTHER_JOBS = {
    "법의학자 (드라마 '싸인')": "시신을 부검하여 사망 원인을 밝혀내고 사건 해결의 결정적 단서를 제공하는 법의학 전문 의사입니다.",
    "항공기 조종사 (영화 '탑건')", "항공기를 안전하게 운항하며 승객과 화물을 목적지까지 수송하는 직업으로, 높은 책임감과 기상/기계 지식이 필요합니다.",
    "응급의학과 의사 (드라마 '슬기로운 의사생활')": "응급실에서 최전선으로 환자의 생명을 구하며, 빠른 판단력과 응급 처치 기술이 요구되는 의료 분야입니다.",
    "특수효과 감독 (영화 'SFX 분야')": "영화, 드라마에 가상 효과 및 CG를 가공하여 현실감 있는 비주얼을 완성하는 비주얼 아티스트입니다."
}

# -----------------------------------------------------------------------------
# 3. Gemini API 연동 함수 (실시간 AI 검색기)
# -----------------------------------------------------------------------------
def get_job_info_from_gemini(job_name):
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = f"""
        당신은 영화 및 드라마 속 직업/진로 전문가입니다.
        사용자가 입력한 직업: '{job_name}'
        
        이 직업이 주요하게 나오는 대표적인 한국 또는 유명 зарубе 영화/드라마 1편을 선정하여 다음 JSON 형식으로만 정확히 답변해주세요. 다른 부연설명은 절대로 붙이지 마세요.
        
        JSON 포맷:
        {{
            "title": "작품 제목 (영화 또는 드라마 구분)",
            "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80",
            "video_url": "https://www.youtube.com/watch?v=J3mR6b5K_qY",
            "story": "작품의 주요 줄거리 2~3문장",
            "job_desc": "해당 직업에 대한 설명과 작중 역할, 핵심 필요 역량 2~3문장"
        }}
        """
        response = model.generate_content(prompt)
        # JSON 문자열 정제
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        return None

# -----------------------------------------------------------------------------
# 4. 헤더 및 메인 화면 구현
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">🎬 영화·드라마 속 진로 탐색기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">궁금한 직업/진로를 입력하면 스크린 속 해당 직업의 세계를 소개해 드립니다!</div>', unsafe_allow_html=True)

# 검색 입력창 및 연관 키워드
col_search, col_btn = st.columns([4, 1])

with col_search:
    user_input = st.text_input("직업 또는 진로를 입력하세요", placeholder="예: 요리사, 검사, 건축가, 프로그래머...", label_visibility="collapsed")

st.markdown("**💡 추천 키워드:**")
quick_cols = st.columns(4)
selected_job = user_input.strip() if user_input else ""

if quick_cols[0].button("🍳 요리사"):
    selected_job = "요리사"
if quick_cols[1].button("📐 건축가"):
    selected_job = "건축가"
if quick_cols[2].button("⚖️ 검사"):
    selected_job = "검사"
if quick_cols[3].button("💻 프로그래머"):
    selected_job = "프로그래머"

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. 검색 결과 출력 영역
# -----------------------------------------------------------------------------
if selected_job:
    st.subheader(f"🔍 '{selected_job}' 관련 영화/드라마 진로 탐색")
    
    data = None
    # 1. 내장 데이터 확인
    if selected_job in BUILTIN_DATA:
        data = BUILTIN_DATA[selected_job]
    else:
        # 2. Gemini API 호출
        with st.spinner(f"AI가 '{selected_job}' 관련 추천 작품과 진로 정보를 분석 중입니다..."):
            data = get_job_info_from_gemini(selected_job)
    
    if data:
        # 2열 레이아웃: [왼쪽: 포스터 & 하이라이트, 오른쪽: 줄거리 & 직업소개]
        col_left, col_right = st.columns([1, 1.3])
        
        with col_left:
            st.image(data.get("poster", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80"), use_column_width=True)
            
            st.markdown("##### 🎥 작품 하이라이트 / 트레일러")
            video_url = data.get("video_url")
            if video_url:
                try:
                    st.video(video_url)
                except Exception:
                    st.info("영상을 불러올 수 없습니다.")
            else:
                st.info("제공되는 하이라이트 영상이 없습니다.")
                
        with col_right:
            st.markdown(f'<span class="job-badge">대표 작품</span>', unsafe_allow_html=True)
            st.markdown(f"### {data.get('title', '작품 정보')}")
            
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("#### 📖 작품 줄거리")
            st.write(data.get("story", "줄거리 정보가 없습니다."))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown(f"#### 💼 '{selected_job}' 진로/직업 소개")
            st.write(data.get("job_desc", "직업 정보가 없습니다."))
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"'{selected_job}'에 대한 정보를 불러오지 못했습니다. 다른 직업명(예: 요리사, 검사 등)으로 시도해 주세요.")

else:
    st.info("👆 위 검색창에 직업을 입력하거나 추천 키워드 버튼을 눌러보세요.")

st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. 하단: 타 진로/직업 둘러보기 (아코디언 방식)
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("📌 스크린 속 다른 진로/직업 탐색하기")
st.caption("아래 직업명을 클릭하면 간단한 설명과 미디어 속 모습을 볼 수 있습니다.")

for job_title, job_info in OTHER_JOBS.items():
    with st.expander(f"✨ {job_title}"):
        st.write(job_info)
