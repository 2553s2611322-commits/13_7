import os
import json
import urllib.request
import urllib.error
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 & 커스텀 CSS
# ==========================================
st.set_page_config(
    page_title="영화·드라마 속 진로 탐색",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .job-tag {
        display: inline-block;
        background-color: #3B82F6;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 내장 데이터베이스 (기본 데이터)
# ==========================================
DEFAULT_JOBS = {
    "의사": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/watch?v=NlAR8EOn1f0",
        "synopsis": "누군가는 떠나고 누군가는 태어나는 인생의 축소판이라 불리는 병원에서 평범한 듯 특별한 하루하루를 살아가는 사람들과 눈빛만 봐도 알 수 있는 20년지기 친구들의 케미스토리를 담은 드라마입니다.",
        "job_desc": "의사는 환자의 질병을 진단하고 치료하여 생명을 구하는 전문가입니다. 뛰어난 전문 지식뿐만 아니라 환자에 대한 공감 능력과 철저한 책임감이 요구됩니다.",
        "skills": ["질병 진단 및 치료", "의학적 판단력", "공감 및 소통 능력", "스트레스 조절력"]
    },
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/watch?v=9L9jY_M342E",
        "synopsis": "천재적인 두뇌와 자폐스펙트럼을 동시에 가진 신입 변호사 우영우가 대형 로펌에서 사건들을 해결하며 진정한 법조인으로 성장해 나가는 법정 휴먼 드라마입니다.",
        "job_desc": "변호사는 법률적 분쟁에서 의뢰인을 대리하여 권리를 보호하고 법적 자문을 제공합니다. 논리적 사고력과 엄밀한 법률 지식이 핵심 요구 역량입니다.",
        "skills": ["법률 분석 및 논리력", "변론 및 설득력", "의뢰인 상담", "비판적 사고"]
    },
    "요리사": {
        "title": "파스타 (Pasta)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/watch?v=W09-OBy2O_k",
        "synopsis": "이탈리안 레스토랑 '라스페라'를 배경으로 음식과 사랑을 만들어가는 젊은 요리사들의 열정과 성공 스토리를 다룬 미식 드라마입니다.",
        "job_desc": "요리사는 식재료의 특성을 이해하고 미각적·시각적으로 훌륭한 음식을 창조합니다. 창의력과 더불어 주방이라는 격렬한 환경에서의 팀워크와 체력이 필수적입니다.",
        "skills": ["조리 기술 및 메뉴 개발", "위생 및 안전 관리", "팀워크 및 리더십", "체력 관리"]
    },
    "경찰": {
        "title": "시그널 (Signal)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1582139329536-e7284fece509?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/watch?v=2eIs2I0cEIs",
        "synopsis": "무전기로 연결된 과거와 현재의 형사들이 오랜 미제 사건들을 파헤치는 수사극으로, 정의 실현을 위해 헌신하는 경찰들의 모습을 생생하게 보여줍니다.",
        "job_desc": "경찰은 사회의 치안을 유지하고 범죄를 예방 및 수사하여 국민의 안전을 지킵니다. 투철한 사명감과 준법정신, 순발력이 중요합니다.",
        "skills": ["범죄 수사 및 정보 수집", "위기 대응 능력", "사명감 및 윤리의식", "체력"]
    },
    "개발자": {
        "title": "스타트업 (Start-Up)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/watch?v=BemKyzbLDDc",
        "synopsis": "한국의 실리콘 밸리에서 성공을 꿈꾸며 스타트업에 도전한 젊은이들의 시작(START)과 성장(UP)을 그린 인공지능/소프트웨어 개발 관련 드라마입니다.",
        "job_desc": "소프트웨어 개발자는 컴퓨팅 프로그래밍 언어를 활용하여 서비스 및 시스템을 개발합니다. 문제 해결 능력과 끊임없이 새로운 기술을 학습하는 자세가 요구됩니다.",
        "skills": ["프로그래밍 / 코딩", "논리적 문제 해결력", "협업 및 커뮤니케이션", "지속적 학습력"]
    },
    "아나운서": {
        "title": "질투의 화신",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/watch?v=pAnK1xThM9Y",
        "synopsis": "방송국 뉴스를 무대로 기상캐스터와 아나운서, 기자 간의 치열한 경쟁과 사랑을 다룬 치열한 언론 미디어 현장의 이야기입니다.",
        "job_desc": "아나운서는 뉴스나 프로그램을 진행하며 신뢰성 있게 정보를 전달합니다. 정확한 발음, 전달력, 순간 대응 능력이 매우 핵심적입니다.",
        "skills": ["스피치 및 정확한 발음", "순발력 및 순응력", "정보 분석 능력", "신뢰감 있는 태도"]
    }
}

# ==========================================
# 3. Gemini REST API 직접 호출 함수 (외부 패키지 미사용)
# ==========================================
def fetch_job_info_from_gemini_rest(query_job):
    """라이브러리 없이 urllib로 Gemini API를 직접 호출하여 정보 생성"""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되어 있지 않습니다."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    
    prompt = f"""
    당신은 영화/드라마 및 진로 정보 전문가입니다.
    직업/진로 이름: "{query_job}"

    다음 직업이 주요 역할로 나타나는 대표적인 영화나 드라마 1개를 선정하고, 아래 JSON 형식으로만 응답해 주세요. 다른 텍스트는 포함하지 마세요.

    {{
        "title": "작품 제목",
        "type": "영화 또는 드라마",
        "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80",
        "video_url": "https://www.youtube.com/results?search_query=작품제목+하이라이트",
        "synopsis": "작품의 줄거리 2-3문장 요약",
        "job_desc": "해당 직업이 하는 일과 직무 특성 2문장 설명",
        "skills": ["필요 역량1", "필요 역량2", "필요 역량3", "필요 역량4"]
    }}
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    try:
        data_json = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, 
            data=data_json, 
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_data = json.loads(res_body)
            
            # API 응답 결과 파싱
            text_result = res_data["candidates"][0]["content"]["parts"][0]["text"]
            parsed_result = json.loads(text_result)
            return parsed_result, None

    except urllib.error.HTTPError as e:
        return None, f"API 호출 실패 (HTTP Error {e.code})"
    except Exception as e:
        return None, f"오류 발생: {str(e)}"

# ==========================================
# 4. 앱 헤더 및 검색 섹션
# ==========================================
st.markdown("<div class='main-header'>🎬 영화·드라마 속 진로 탐색기</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>관심 있는 직업을 검색하고 미디어 속 주인공의 실제 역할과 직무를 탐색해보세요!</div>", unsafe_allow_html=True)

search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    user_input = st.text_input(
        "탐색하고 싶은 진로/직업을 입력하세요", 
        placeholder="예: 의사, 변호사, 요리사, 개발자, 경찰, 아나운서, 건축가 등",
        label_visibility="collapsed"
    )
with search_col2:
    search_button = st.button("🔍 진로 탐색", use_container_width=True)

if "selected_job" not in st.session_state:
    st.session_state["selected_job"] = "의사"

if search_button and user_input.strip():
    st.session_state["selected_job"] = user_input.strip()

current_job = st.session_state["selected_job"]

# ==========================================
# 5. 메인 컨텐츠 영역
# ==========================================
st.divider()

job_data = None
error_msg = None

if current_job in DEFAULT_JOBS:
    job_data = DEFAULT_JOBS[current_job]
else:
    with st.spinner(f"'{current_job}' 관련 영화/드라마 및 진로 정보를 분석 중입니다..."):
        job_data, error_msg = fetch_job_info_from_gemini_rest(current_job)
        if error_msg or not job_data:
            st.info(f"💡 AI 조회 참고: 기본 데이터베이스 결과로 안내합니다.")
            job_data = DEFAULT_JOBS["의사"]
            current_job = "의사 (기본 추천)"

if job_data:
    st.subheader(f"📌 '{current_job}' 직업이 빛나는 추천 작품")
    
    col_left, col_right = st.columns([1, 1.2], gap="medium")
    
    with col_left:
        st.image(job_data.get("poster"), use_container_width=True, caption=f"[{job_data.get('type')}] {job_data.get('title')}")
        
        video_url = job_data.get("video_url", "")
        if video_url:
            st.markdown("##### 🎥 작품 하이라이트 / 예고편")
            try:
                st.video(video_url)
            except Exception:
                st.markdown(f"[👉 YouTube에서 예고편 보기]({video_url})")

    with col_right:
        st.markdown(f"### **{job_data.get('title')}**")
        st.markdown(f"<span class='job-tag'>{job_data.get('type')}</span>", unsafe_allow_html=True)
        
        st.markdown("#### 📖 작품 줄거리")
        st.info(job_data.get("synopsis"))
        
        st.markdown(f"#### 💼 '{current_job}' 직무 상세 소개")
        st.write(job_data.get("job_desc"))
        
        st.markdown("#### 🔑 핵심 필요 역량")
        skills = job_data.get("skills", [])
        if skills:
            cols = st.columns(len(skills))
            for idx, skill in enumerate(skills):
                cols[idx % len(cols)].metric(label=f"역량 {idx+1}", value=skill)

# ==========================================
# 6. 하단: 타 진로/직업 탐색
# ==========================================
st.divider()
st.subheader("💡 영화·드라마에 나오는 다양한 타 진로/직업 둘러보기")
st.caption("아래 버튼을 클릭하면 해당 직업의 주요 설명과 추천 작품을 바로 확인할 수 있습니다.")

other_jobs = [j for j in DEFAULT_JOBS.keys() if j != current_job]

grid_cols = st.columns(3)
for idx, job_name in enumerate(other_jobs):
    col = grid_cols[idx % 3]
    with col:
        if st.button(f"🎭 {job_name}", key=f"other_btn_{job_name}", use_container_width=True):
            st.session_state["selected_job"] = job_name
            st.rerun()

with st.expander("ℹ️ 전체 등록 직업 한눈에 알아보기"):
    for key, info in DEFAULT_JOBS.items():
        st.markdown(f"**• {key}** ({info['title']}): {info['job_desc']}")
