import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화/드라마 속 진로 탐색기",
    page_icon="🎬",
    layout="wide"
)

# 깔끔하고 정돈된 스타일링
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
        margin-bottom: 2rem;
    }
    .poster-frame img {
        border-radius: 14px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.12);
    }
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.02);
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 12px;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 8px;
    }
    .card-text {
        font-size: 0.98rem;
        line-height: 1.75;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# ---------------------------------------------------------
# 풍부하고 다양한 직업 데이터베이스 (작품 내 연관 직업 포함)
# ---------------------------------------------------------
CAREER_DATABASE = {
    "제빵사": {
        "title": "제빵왕 김탁구",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&auto=format&fit=crop&q=80",
        "summary": "70~80년대 한국 식품 산업의 성장기를 배경으로, 주인공 김탁구가 온갖 역경을 이겨내고 진정한 제빵 명인으로 성장해 나가는 이야기를 다룬 국민 드라마입니다. 빵 한 조각에 온기와 희망을 담아내는 제빵사들의 정성과 치열한 기술 경쟁, 그리고 기술에 대한 명장 정신을 깊이 있게 그려냅니다.",
        "career_info": "제빵사는 밀가루, 효모, 물 등 식재료를 발효시키고 구워 다양한 빵과 과자류를 만드는 전문 기술직입니다. 단순히 빵을 만드는 것을 넘어 반죽의 온도, 발효 시간, 오븐 온도 조절 등 섬세한 과학적 계산과 미각, 시각적 디자인 감각이 모두 요구됩니다. 위생 관념과 더불어 장시간 서서 일하는 체력, 독창적인 레시피를 개발하는 창의성이 중요한 역량입니다.",
        "co_careers": {
            "제과 경영자 / 브랜딩 매니저": "베이커리 매장의 경영 전략을 수립하고 신제품 출시 및 브랜드 이미지를 구축하는 마케팅 중심의 직업입니다.",
            "식품 연구원": "빵과 제과 제품의 유통기한, 발효균, 원료 구성을 과학적으로 연구하여 제품의 품질을 향상시키는 연구 직무입니다."
        }
    },
    "바리스타": {
        "title": "커피프린스 1호점",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80",
        "summary": "정체된 카페를 살아있는 공간으로 탈바꿈시키기 위해 청춘들이 모여 커피를 배우고 경험하며 성장하는 이야기를 담은 클래식 로맨스 드라마입니다. 원두의 추출 과정과 향미 평가, 카페 문화의 정착 과정을 세련되게 담아내어 커피 산업과 바리스타라는 직업을 대중에게 크게 알렸습니다.",
        "career_info": "바리스타는 커피 추출 기구를 다루며 원두의 특성을 파악하고 고객의 취향에 맞는 다양한 커피 음료를 전문적으로 만드는 전문가입니다. 원두의 로스팅 상태와 분쇄도, 수온 조절에 따른 맛의 변화를 감별하는 미각 능력과 서비스 정신이 핵심입니다. 또한 카페 공간 운영과 신메뉴 개발 능력을 갖추어 전문 음료 컨설턴트로 성장할 수도 있습니다.",
        "co_careers": {
            "커피 로스터": "생두를 볶아 커피 원두 특유의 맛과 향을 끌어내는 전문 로스팅 기술자입니다.",
            "카페 디렉터": "인테리어, 원두 수급, 브랜딩, 고객 경험을 총괄 기획하는 카페 브랜드 기획자입니다."
        }
    },
    "교사": {
        "title": "블랙독 (Black Dog)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&auto=format&fit=crop&q=80",
        "summary": "기간제 교사로 고등학교에 첫 부임한 주인공이 학교라는 작은 사회 속에서 학생들의 진로와 성장을 돕고, 동료 교사들과 호흡하며 리얼한 학교 현장의 일상과 고민을 헤쳐 나가는 직업 드라마입니다. 교사의 행정적 고충과 교육적 사명감 사이에서의 성찰을 진솔하게 다룹니다.",
        "career_info": "교사는 교과목 지식을 학생들에게 효과적으로 전달하고, 올바른 인성과 진로 지도, 생활 지도를 병행하는 교육 전문가입니다. 명확한 전달력과 수업 기획 능력은 물론, 학생 개개인의 성향과 고민에 귀 기울일 수 있는 따뜻한 소통 능력이 필수적입니다. 교육 과정의 변화에 능동적으로 대처하며 교재 연구를 지속하는 열정이 중요합니다.",
        "co_careers": {
            "진로 진학 상담교사": "학생들의 적성과 직업 탐색, 대학 진학 설계를 전담하여 개별 상담을 제공하는 전문 교사입니다.",
            "교육 행정가": "학교 및 교육청 기관에서 학사 일정, 교육 예산, 시스템 관리를 총괄하는 행정 전문가입니다."
        }
    },
    "래퍼": {
        "title": "8 마일 (8 Mile)",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600&auto=format&fit=crop&q=80",
        "summary": "디트로이트의 빈민가에서 밤낮으로 노동하며 살아가는 청년이 자신의 절박한 삶과 감정을 힙합 랩으로 풀어내어, 마침내 랩 배틀 무대에서 자신의 존재를 입증해내는 뜨거운 음악 영화입니다. 자신의 현실과 솔직한 이야기를 가사로 담아내는 힙합 아티스트의 고뇌와 성장을 보여줍니다.",
        "career_info": "래퍼는 리듬과 멜로디에 맞춰 라임과 메시지를 담은 가사를 읊는 대중음악 아티스트입니다. 라임 구성 능력, 언어 구사력, 박자감이 핵심이며, 자신만의 독창적인 음색과 스타일을 구축하는 것이 성공의 열쇠입니다. 본인의 삶과 사회적 메시지를 음악으로 표현하는 작사/작곡 능력이 필수적으로 요구됩니다.",
        "co_careers": {
            "음악 프로듀서": "트랙을 비트메이킹하고 전체 곡의 사운드와 앨범 컨셉을 총지휘하는 아티스트입니다.",
            "사운드 엔지니어": "녹음된 음원의 음량, 밸런스, 톤을 정교하게 조율하고 믹싱/마스터링하는 기술 전문가입니다."
        }
    },
    "피아니스트": {
        "title": "피아니스트 (The Pianist)",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=600&auto=format&fit=crop&q=80",
        "summary": "2차 세계대전 당시 전쟁의 참상 속에서도 음악에 대한 열정과 피아노에 대한 집념으로 절망적인 생존을 이어나간 천재 피아니스트 스필만의 실화를 다룬 영화입니다. 음악이 주는 깊은 위로와 한 예술가의 기교 너머의 혼을 담은 연주를 그려냅니다.",
        "career_info": "피아니스트는 악보에 명시된 곡을 정교한 테크닉과 감성으로 해석하여 관객에게 전달하는 건반 악기 연주자입니다. 수십 년간 지속되는 끊임없는 연습과 단련이 필수적이며, 악곡의 역사적 배경을 이해하는 해석력이 중요합니다. 독주회, 협연, 음악 교육 등 다양한 분야에서 활동할 수 있습니다.",
        "co_careers": {
            "음악 음악치료사": "음악적 자극과 연주 활동을 통해 환자의 심리적/신체적 회복을 돕는 전문가입니다.",
            "클래식 기획자": "연주회 공연 일정을 기획하고 연주자와 홀을 매칭하여 무대를 조성하는 공연 기획자입니다."
        }
    },
    "메이크업 아티스트": {
        "title": "청춘기록",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&auto=format&fit=crop&q=80",
        "summary": "현실의 벽에 부딪혀도 스스로의 힘으로 꿈을 향해 나아가는 청춘들의 성장을 담은 드라마로, 메이크업 아티스트를 꿈꾸는 주인공이 뷰티 샵 스태프부터 시작해 브랜드 아티스트로 성장하는 치열한 현장을 보여줍니다.",
        "career_info": "메이크업 아티스트는 고객의 얼굴형, 피부 톤, 의상, 행사 성격에 맞춰 화장품과 도구를 활용해 미적 연출을 시행하는 전문가입니다. 색채 감각과 최신 트렌드 분석력이 필수적이며, 패션쇼, 방송, 영화, 웨딩 등 다양한 스튜디오 환경에서 빠른 시간 내 완성도 높은 스타일링을 완성해야 합니다.",
        "co_careers": {
            "헤어 디자이너": "헤어 스타일링과 커트, 염색을 맡아 전체적 스타일에 어울리는 헤어 룩을 완성하는 아티스트입니다.",
            "뷰티 크리에이터": "화장법과 제품 리뷰를 기획해 영상 콘텐츠로 제작하여 대중과 소통하는 미디어 전문가입니다."
        }
    },
    "요리사": {
        "title": "이태원 클라쓰",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&auto=format&fit=crop&q=80",
        "summary": "이태원의 작은 포차에서 시작해 대한민국 요식업계 대기업에 맞서 주점 브랜드를 키워나가는 젊은이들의 치열한 창업과 성공 스토리를 다룬 드라마입니다. 메뉴의 창의성과 매장 운영, 요리사의 레시피 개발 현장을 사실적으로 담아냈습니다.",
        "career_info": "요리사는 대중에게 제공할 메뉴를 기획하고, 식재료 수급 및 손질, 조리 과정을 거쳐 맛과 멋을 갖춘 음식을 완성하는 전문가입니다. 위생 관념과 미각적 센스는 물론, 최적의 맛을 일정하게 유지하는 끈기 및 주방 전체의 호흡을 이끄는 커뮤니케이션 능력이 바탕이 되어야 합니다.",
        "co_careers": {
            "외식업 브랜드 디렉터": "식당의 콘셉트, 인테리어, 정체성을 통합 설계하는 외식 브랜드 개발자입니다.",
            "푸드 스타일리스트": "음식이 수록되는 미디어에 맞게 음식을 더욱 맛있어 보이도록 연출하는 스타일링 전문가입니다."
        }
    },
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=80",
        "summary": "천재적인 두뇌와 자폐스펙트럼을 동시에 가진 신입 변호사 우영우가 로펌 한바다에서 다양한 법적 사건을 해결하며 진정한 변호사로 성장하는 법정 휴먼 드라마입니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인을 대리하여 소송을 진행하거나 법적 자문을 제공하는 법률 전문가입니다. 공정성과 논리적 사고력, 세심한 사건 관찰력과 더불어 의뢰인과의 두터운 신뢰 형성이 핵심 역량입니다.",
        "co_careers": {
            "법률 사무원": "소송 관련 서류 준비 및 법원 제출, 서면 작성을 보조하는 법률 행정 지원 전문가입니다.",
            "변리사": "특허, 상표 등 지식재산권 등록 및 분쟁을 전문적으로 다루는 지식재산권 법률 전문가입니다."
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
        당신은 진로 및 미디어 전문가입니다. 직업 '{search_job}'에 대한 정보를 아래 형식으로 길고 자세하게 작성하세요.
        
        [대표 작품]: (이 직업이 나오는 영화/드라마 제목)
        [작품 구분]: (영화 또는 드라마)
        [작품 줄거리]: (작품 전체의 핵심 줄거리를 4~5문장 이상 상세히 작성)
        [진로 상세 소개]: (해당 직업이 하는 일, 필요 역량, 진로 전망을 4~5문장 이상 상세히 작성)
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
st.markdown('<div class="sub-title">궁금한 직업을 검색하거나 클릭하여 해당 작품의 상세 설명과 진로 가이드를 확인해보세요.</div>', unsafe_allow_html=True)

# 인기 직업 선택 태그
st.caption("🔥 직업 선택하기 (버튼 클릭 시 바로 탐색)")
rec_keys = list(CAREER_DATABASE.keys())
rec_cols = st.columns(len(rec_keys))
for idx, key in enumerate(rec_keys):
    if rec_cols[idx].button(key, use_container_width=True, key=f"btn_{key}"):
        st.session_state.search_term = key

# 검색어 입력창
input_value = st.text_input(
    "탐색할 직업명을 입력하세요:",
    value=st.session_state.search_term,
    placeholder="예: 제빵사, 바리스타, 교사, 래퍼, 피아니스트, 메이크업 아티스트, 요리사..."
).strip()

st.session_state.search_term = input_value

# ---------------------------------------------------------
# 결과 출력 세션 (검색 또는 버튼 클릭 시에만 표시됨)
# ---------------------------------------------------------
if st.session_state.search_term:
    st.divider()
    search_query = st.session_state.search_term
    
    # DB 내 매칭되는 직업 찾기
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
            st.image(data["poster"], use_container_width=True, caption=f"[{data['type']}] {data['title']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"# {data['title']}")
            
            # 줄거리 카드
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📖 작품 상세 줄거리</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-text">{data["summary"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 진로 소개 카드
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">💡 진로/직업 상세 가이드 ({matched_key})</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-text">{data["career_info"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 작품 내 함께 나오는 타 직업 소개 (검색 후 하단에 나타남)
        if "co_careers" in data and data["co_careers"]:
            st.write("")
            st.markdown(f"### 🤝 [{data['title']}] 속 또 다른 다양한 직업들")
            st.caption("해당 작품 안에서 주인공과 함께 등장하는 관련 직업 정보입니다.")
            
            co_cols = st.columns(len(data["co_careers"]))
            for idx, (co_job, co_desc) in enumerate(data["co_careers"].items()):
                with co_cols[idx]:
                    with st.expander(f"📌 **{co_job}**", expanded=True):
                        st.write(co_desc)

    else:
        # DB에 없을 시 Gemini AI 호출
        st.info(f"💡 기본 데이터베이스에 등록되지 않은 직업입니다. Gemini AI가 정보를 탐색 중입니다.")
        with st.spinner("AI가 작품 추천 및 상세 진로 가이드를 생성 중입니다..."):
            ai_result, error = get_gemini_recommendation(search_query)
            if error:
                st.error(error)
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.6])
                with col_poster:
                    st.image(
                        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
                        caption=f"{search_query} 관련 미디어 추천",
                        use_container_width=True
                    )
                with col_info:
                    st.markdown(f"# 🤖 AI 분석 가이드: {search_query}")
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-text">{ai_result}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
