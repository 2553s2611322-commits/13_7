import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="🎬 영화·드라마 속 아기자기 진로 탐색기 팝!",
    page_icon="✨",
    layout="wide"
)

# ---------------------------------------------------------
# 아기자기하고 따뜻한 파스텔 톤 CSS 스타일링
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }
    
    .stApp {
        background-color: #FFFDF9;
    }
    
    /* 메인 타이틀 디자인 */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #FF6B81;
        text-align: center;
        letter-spacing: -0.02em;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
        text-shadow: 2px 2px 0px #FFE0E6;
    }
    
    .sub-title {
        font-size: 1.05rem;
        color: #70A1FF;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* 포스터 이미지 테두리 및 그림자 */
    .poster-frame img {
        border-radius: 20px !important;
        box-shadow: 0 12px 24px rgba(255, 107, 129, 0.15) !important;
        border: 4px solid #FFFFFF;
    }
    
    /* 아기자기한 카드 디자인 */
    .info-card {
        background-color: #FFFFFF;
        border: 2px solid #FFEAA7;
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 6px 15px rgba(255, 234, 167, 0.3);
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FF6B6B;
        margin-bottom: 8px;
        border-bottom: 2px dashed #FFEAA7;
        padding-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .card-text {
        font-size: 0.96rem;
        line-height: 1.7;
        color: #2F3542;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Streamlit 기본 버튼 파스텔 스타일 개선 */
    .stButton>button {
        background-color: #FFF;
        color: #FF4757;
        border: 2px solid #FF7888;
        border-radius: 14px;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #FF7888;
        color: #FFF;
        border-color: #FF7888;
        transform: translateY(-2px);
    }
    
    /* 제목 및 공백 오류 방지 */
    h1 {
        margin-top: 0px !important;
        padding-top: 0px !important;
        margin-bottom: 10px !important;
        color: #2F3542;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# ---------------------------------------------------------
# 이미지 로딩 오류가 없는 고화질 포스터 & 풍부한 20가지 직업 DB
# ---------------------------------------------------------
CAREER_DATABASE = {
    "제빵사": {
        "title": "제빵왕 김탁구",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&auto=format&fit=crop&q=80",
        "summary": "주인공 김탁구가 온갖 역경을 이겨내고 진정한 제빵 명인으로 성장해 나가는 이야기를 다룬 따뜻한 성장 드라마입니다. 빵 한 조각에 온기와 희망을 담아내는 제빵사들의 정성과 치열한 기술 경쟁을 깊이 있게 그려냅니다.",
        "career_info": "제빵사는 밀가루, 효모 등을 발효시키고 구워 맛있는 빵을 만드는 기술 전문가입니다. 반죽의 온도, 발효 시간 조절 등 섬세한 과학적 계산과 미각, 디자인 감각, 정성이 모두 요구됩니다.",
        "co_careers": {
            "디저트 파티시에": "케이크, 타르트 등 달콤한 고급 디저트를 전문적으로 기획하고 디자인하는 전문가입니다.",
            "식품 연구원": "빵과 과자류의 유통기한과 신메뉴 원료를 과학적으로 연구 개발하는 전문가입니다."
        }
    },
    "바리스타": {
        "title": "커피프린스 1호점",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80",
        "summary": "청춘들이 모여 커피 향 가득한 카페를 만들며 커피를 배우고 경험하며 성장해가는 클래식 청춘 드라마입니다. 원두 추출과 향미 평가 등 전문적인 커피의 세계를 다룹니다.",
        "career_info": "바리스타는 커피 원두의 특성을 파악하고 고객 취향에 맞는 다양한 커피 음료를 추출해 제공하는 음료 전문가입니다. 섬세한 미각과 라떼 아트 등 표현력이 중요합니다.",
        "co_careers": {
            "커피 로스터": "생두를 볶아 커피 원두 특유의 고유한 맛과 향을 끌어내는 테크니션입니다.",
            "카페 디렉터": "인테리어, 원두 선택, 브랜딩 등 카페 전반을 총괄 기획하는 매니저입니다."
        }
    },
    "수의사": {
        "title": "어쩌다 전원일기",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1532712938310-34cb3982ef74?w=600&auto=format&fit=crop&q=80",
        "summary": "시골 마을에 온 서울 출신 수의사가 다양한 동물들을 치료하며 마을 사람들과 교감하고 성장해나가는 마음 따뜻해지는 전원 로맨스 드라마입니다.",
        "career_info": "수의사는 동물의 질병 예방과 진단, 치료, 수술을 담당하는 전문가입니다. 동물을 사랑하는 마음은 물론 생물학적 지식, 정확한 판단력과 생명을 다루는 책임감이 필요합니다.",
        "co_careers": {
            "동물보건사": "수의사의 진료와 수술을 보조하고 동물의 간호를 전담하는 동물 보건 전문가입니다.",
            "반려동물 행동교정사": "동물의 행동 문제 원인을 분석하고 올바른 습관을 길러주는 훈련 전문가입니다."
        }
    },
    "교사": {
        "title": "블랙독 (Black Dog)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&auto=format&fit=crop&q=80",
        "summary": "학교 현장에 첫 부임한 신입 교사가 학생들의 성장을 돕고, 교육적 사명감을 지키며 진정한 선생님으로 거듭나는 감동 스토리를 다룹니다.",
        "career_info": "교사는 교과 지식을 가르칠 뿐만 아니라 학생들의 인성 지도, 진로 상담, 올바른 사회화를 돕는 멘토 역할을 수행하는 교육 전문가입니다.",
        "co_careers": {
            "진로 진학 상담교사": "학생 적성과 직업 탐색, 대학 진학 경로를 전담 상담해주는 상담 선생님입니다.",
            "교육 콘텐츠 기획자": "학생들이 쉽게 공부할 수 있도록 교재와 교육용 앱을 기획하는 전문가입니다."
        }
    },
    "요리사": {
        "title": "이태원 클라쓰",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&auto=format&fit=crop&q=80",
        "summary": "이태원 작은 요리 주점에서 시작해 대형 푸드 기업으로 성장해나가는 청춘들의 치열한 레시피 개발과 레스토랑 성공 스토리를 다룹니다.",
        "career_info": "요리사(셰프)는 다양한 식재료를 활용하여 맛과 미적 감각을 갖춘 음식을 기획하고 조리하는 전문가입니다. 위생관념과 손끝 감각, 주방 팀워크가 핵심입니다.",
        "co_careers": {
            "푸드 스타일리스트": "음식이 미디어에 예쁘게 나오도록 연출하고 디스플레이하는 스타일링 전문가입니다.",
            "메뉴 개발자": "외식 브랜드의 신메뉴 개발 및 맛의 밸런스를 연구하는 전문가입니다."
        }
    },
    "변호사": {
        "title": "이상한 변호사 우영우",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=80",
        "summary": "천재적인 두뇌를 가진 신입 변호사 우영우가 따뜻한 시선으로 법적 사건들을 해결해나가며 성장하는 힐링 법정 드라마입니다.",
        "career_info": "변호사는 법률 지식을 바탕으로 의뢰인의 권리를 지키고 분쟁을 해결하는 법률 전문가입니다. 공정한 마음과 논리적 분석력, 경청하는 자세가 매우 중요합니다.",
        "co_careers": {
            "변리사": "특허나 상표권 등 지식재산권을 보호하고 관리하는 지식재산 법률 전문가입니다.",
            "법률 사무원": "소송 서류 작성 및 법원 제출 업무를 보조하는 법률 지원 전문가입니다."
        }
    },
    "프로그래머": {
        "title": "스타트업 (Start-Up)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop&q=80",
        "summary": "혁신적인 아이디어와 인공지능 코딩 기술로 스타트업을 창업한 청춘들이 세상을 바꿔나가는 거침없는 도전과 성공을 담았습니다.",
        "career_info": "프로그래머(개발자)는 컴퓨터 언어를 사용해 앱, 웹사이트, 게임, AI 프로그램을 만드는 소프트웨어 기술자입니다. 논리적 사고와 문제 해결력이 핵심입니다.",
        "co_careers": {
            "UI/UX 디자이너": "사용자가 앱이나 웹사이트를 편리하고 예쁘게 쓸 수 있도록 화면을 설계하는 디자이너입니다.",
            "데이터 분석가": "빅데이터 속에서 유용한 정보와 패턴을 찾아내는 데이터 전문가입니다."
        }
    },
    "경찰": {
        "title": "베테랑",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=600&auto=format&fit=crop&q=80",
        "summary": "사건 현장을 누비는 베테랑 형사들이 사회적 정의를 지키기 위해 불굴의 집념으로 범죄를 추적하는 통쾌한 액션 영화입니다.",
        "career_info": "경찰관은 국민의 생명과 안전을 보호하고 사회 질서를 유지하기 위해 범죄 예방과 수사, 치안 활동을 펼치는 공무원입니다. 체력과 강한 정의감이 필요합니다.",
        "co_careers": {
            "프로파일러": "범죄 현장 정황을 토대로 심리를 분석해 범인을 추정하는 범죄 심리 분석관입니다.",
            "과학수사관": "현장 증거물을 과학적 기법으로 정밀 분석하여 증거를 확보하는 수사관입니다."
        }
    },
    "소방관": {
        "title": "소방서 옆 경찰서",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80",
        "summary": "화재 현장과 재난 현장에 누구보다 빠르게 달려가 타인의 생명을 구해내는 소방관들의 뜨거운 현장 대응 일지입니다.",
        "career_info": "소방관은 화재 진압, 인명 구조, 응급 환자 이송 등 위급한 상황에서 생명을 구하는 영웅적인 전문가입니다. 순발력과 체력, 사명감이 필수입니다.",
        "co_careers": {
            "응급구조사": "현장에서 즉시 응급 처치를 수행하고 안전하게 병원으로 이송하는 의료 전문가입니다.",
            "화재조사관": "화재 발원지와 원인을 과학적으로 파악해 재발을 막는 안전 전문가입니다."
        }
    },
    "외과의사": {
        "title": "슬기로운 의사생활",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&auto=format&fit=crop&q=80",
        "summary": "환자들의 생명을 살리기 위해 고군분투하는 의사 친구들의 진솔한 일상과 생명의 소중함을 그려내는 가슴 따뜻한 메디컬 드라마입니다.",
        "career_info": "외과의사는 수술을 통해 질병과 부상을 치료하는 의료 전문가입니다. 고도의 집중력, 섬세한 손기술, 그리고 생명을 아끼는 마음이 요구됩니다.",
        "co_careers": {
            "수술실 간호사": "수술이 안전하게 진행되도록 도구를 관리하고 의사를 보조하는 전문 간호사입니다.",
            "임상병리사": "혈액이나 세포 조직을 검사해 질병의 정확한 원인을 진단하는 검사 전문가입니다."
        }
    },
    "건축가": {
        "title": "건축학개론",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600&auto=format&fit=crop&q=80",
        "summary": "누군가의 추억과 공간을 담아 정성껏 집을 설계하고 지어주는 건축가의 아름다운 공간 연출 이야기입니다.",
        "career_info": "건축가는 사람이 보금자리로 삼을 건물의 구조와 미관을 아름답고 안전하게 설계하는 공간 창작 전문가입니다. 예술적 감각과 공학적 지식이 균형을 이뤄야 합니다.",
        "co_careers": {
            "인테리어 디자이너": "실내 공간을 콘셉트에 맞게 조명, 가구, 색채로 꾸미는 공간 연출가입니다.",
            "조경가": "건물 주변에 정원, 공원, 자원 생태 공간을 기획하고 연출하는 자연 디자이너입니다."
        }
    },
    "웹툰 작가": {
        "title": "W (더블유)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop&q=80",
        "summary": "상상 속 웹툰 세계와 현실 세계가 연결되며 일어나는 흥미진진한 이야기로, 작가의 창의적인 스토리텔링과 그림의 힘을 보여줍니다.",
        "career_info": "웹툰 작가는 풍부한 상상력으로 이야기(콘티)를 짜고 개성 있는 그림체로 만화를 연재하는 디지털 아티스트입니다. 독창적인 그림체와 연출력이 핵심입니다.",
        "co_careers": {
            "웹툰 기획자(PD)": "작가의 연재 일정을 관리하고 작품 브랜딩과 유통을 돕는 매니저입니다.",
            "스토리 작가": "만화의 흥미진진한 줄거리와 대사를 집중적으로 집필하는 문학 전문가입니다."
        }
    },
    "파일럿": {
        "title": "탑건: 매버릭",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1519074069444-1ba4fff16be3?w=600&auto=format&fit=crop&q=80",
        "summary": "하늘을 가르며 승객과 기체를 안전하게 조종하는 조종사들의 꿈, 열정, 그리고 비행에 대한 열정을 다룬 상공 액션 영화입니다.",
        "career_info": "파일럿(항공기 조종사)은 비행기를 안전하게 운항하는 항공 전문가입니다. 신속한 상황 판단력, 비행 제어 기술, 그리고 철저한 책임감이 필요합니다.",
        "co_careers": {
            "항공 승무원": "기내에서 승객의 안전을 지키고 쾌적한 서비스를 제공하는 승무원입니다.",
            "항공 정비사": "항공기의 엔진과 장비를 정밀 점검하여 안전한 비행을 돕는 기계 전문가입니다."
        }
    },
    "패션 디자이너": {
        "title": "악마는 프라다를 입는다",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600&auto=format&fit=crop&q=80",
        "summary": "화려한 패션 업계 뒤에서 새로운 트렌드를 만들어내기 위해 밤낮으로 고민하는 패션 디자이너와 에디터들의 치열한 열정을 보여줍니다.",
        "career_info": "패션 디자이너는 의류, 잡화의 원단과 디자인을 기획하여 새로운 스타일을 창조하는 아티스트입니다. 색채 감각과 트렌드 캐치 능력이 핵심입니다.",
        "co_careers": {
            "패션 에디터": "패션 잡지와 미디어에서 최신 트렌드 기사를 작성하고 화보를 기획하는 에디터입니다.",
            "패션 스타일리스트": "연예인이나 모델의 스타일을 콘셉트에 맞춰 완성해주는 스타일 전문가입니다."
        }
    },
    "운동선수": {
        "title": "스물다섯 스물하나",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop&q=80",
        "summary": "펜싱 꿈나무 주인공이 땀 흘려 훈련하며 꿈을 향해 달리는 청춘과 스포츠맨십을 싱그럽게 그려낸 드라마입니다.",
        "career_info": "운동선수는 꾸준한 신체 훈련을 통해 스포츠 경기에서 최고의 기량을 발휘하는 체육 전문가입니다. 강한 자기 관리와 승부욕이 필요합니다.",
        "co_careers": {
            "스포츠 트레이너": "선수들의 신체 조건과 근육을 관리해 부상을 예방해주는 전문가입니다.",
            "스포츠 에이전트": "선수의 계약과 광고, 연봉 협상을 전문적으로 관리해주는 매니저입니다."
        }
    },
    "래퍼 / 뮤지션": {
        "title": "8 마일 (8 Mile)",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600&auto=format&fit=crop&q=80",
        "summary": "힘든 현실 속에서도 음악과 랩에 대한 뜨거운 passion으로 무대 위에서 자신의 이야기를 펼쳐내는 힙합 아티스트의 이야기입니다.",
        "career_info": "래퍼 및 뮤지션은 자신만의 감성과 메시지를 가사와 멜로디로 표현하는 음악가입니다. 라임 구성과 박자감, 독창적 음색이 무기입니다.",
        "co_careers": {
            "음악 프로듀서": "곡의 비트를 만들고 전체 앨범의 사운드를 디렉팅하는 음악 총괄 기획자입니다.",
            "사운드 엔지니어": "녹음된 소리의 음량과 톤을 깔끔하게 조율해 완벽한 음원을 만드는 기술자입니다."
        }
    },
    "메이크업 아티스트": {
        "title": "청춘기록",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&auto=format&fit=crop&q=80",
        "summary": "메이크업 아티스트를 꿈꾸는 주인공이 보조부터 시작해 멋진 뷰티 아티스트로 성장해가는 반짝이는 청춘 이야기입니다.",
        "career_info": "메이크업 아티스트는 얼굴형과 분위기에 맞게 화장품으로 아름다움을 연출하는 뷰티 전문가입니다. 색감 센스와 트렌드 감각이 요구됩니다.",
        "co_careers": {
            "뷰티 크리에이터": "화장법과 뷰티 팁을 영상으로 제작하여 독자들과 소통하는 미디어 전문가입니다.",
            "특수분장사": "영화나 드라마 캐릭터에 맞게 상처나 기괴한 분장을 연출하는 표현 전문가입니다."
        }
    },
    "피아니스트": {
        "title": "피아니스트",
        "type": "영화",
        "poster": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=600&auto=format&fit=crop&q=80",
        "summary": "어려운 상황 속에서도 피아노 건반 위에서 솔직한 영혼의 연주를 펼치는 예술가의 아름다운 감동 영화입니다.",
        "career_info": "피아니스트는 정교한 건반 연주 기술과 풍부한 표현력으로 음악을 완성해 사람들에게 감동을 전하는 악기 연주자입니다.",
        "co_careers": {
            "음악치료사": "피아노 및 음악 연주를 통해 마음이 아픈 사람들을 치유하는 전문가입니다.",
            "공연 기획자": "음악회와 콘서트 무대를 정성껏 기획하고 총괄하는 무대 기획자입니다."
        }
    },
    "기자": {
        "title": "피노키오",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop&q=80",
        "summary": "진실을 밝히기 위해 사건 현장을 발로 뛰는 젊은 기자들의 솔직하고 흥미진진한 취재 이야기입니다.",
        "career_info": "기자는 사회적 이슈나 사건을 취재해 정확한 기사로 전달하는 언론인입니다. 관찰력과 공정한 시선, 정확한 문장력이 필요합니다.",
        "co_careers": {
            "방송 PD": "뉴스 및 다큐멘터리 영상을 기획하고 촬영을 연출하는 영상 전문가입니다.",
            "미디어 평론가": "사회 언론 및 뉴스 콘텐츠의 공정성을 분석하고 진단하는 분석가입니다."
        }
    },
    "프로게이머": {
        "title": "취시광연적니 (너를 만난 날)",
        "type": "드라마",
        "poster": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&auto=format&fit=crop&q=80",
        "summary": "e스포츠 무대에서 우승을 목표로 팀원들과 피나는 연습을 하며 우정을 쌓아가는 프로게이머 청춘들의 스릴 넘치는 이야기입니다.",
        "career_info": "프로게이머는 e스포츠 대회에 참가해 정교한 컨트롤과 전략으로 승리를 거두는 정식 스포츠 선수입니다. 반응 속도와 팀 피드백 능력이 중요합니다.",
        "co_careers": {
            "e스포츠 코치": "선수들의 경기 전략을 연구하고 멘탈 관리를 돕는 지휘관입니다.",
            "게임 캐스터": "박진감 넘치게 경기를 중계하고 관객에게 전달하는 전문 해설가입니다."
        }
    }
}

# ---------------------------------------------------------
# Gemini AI 호출 함수
# ---------------------------------------------------------
def get_gemini_recommendation(search_job):
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되지 않았습니다. Secrets 구성을 확인해 주세요."
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        당신은 상스롭고 친절한 진로 전문가입니다. 직업 '{search_job}'에 대한 정보를 아래 형식으로 귀엽고 친근한 말투로 작성해 주세요.
        
        [대표 작품]: (이 직업이 나오는 영화 또는 드라마 제목)
        [작품 구분]: (영화 또는 드라마)
        [작품 줄거리]: (작품 전체의 핵심 줄거리를 상세히 작성)
        [진로 상세 소개]: (해당 직업이 하는 일, 필요 역량, 진로 전망을 친절히 작성)
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return response.text, None
    except Exception as e:
        return None, f"AI 정보 생성 중 오류가 발생했습니다: {str(e)}"

# ---------------------------------------------------------
# UI 메인 화면 구성 (아기자기한 파스텔 콘셉트)
# ---------------------------------------------------------
st.markdown('<div class="main-title">✨ 🎬 영화·드라마 속 진로 탐색기 💖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">궁금한 직업을 콕! 집어 버튼을 누르거나 검색해 보세요 🌸</div>', unsafe_allow_html=True)

# 인기 직업 선택 태그 (4개씩 예쁘게 배치)
st.caption("✨ 탐색하고 싶은 직업을 선택해 보세요! (클릭 시 자동 검색)")
rec_keys = list(CAREER_DATABASE.keys())

cols_per_row = 5
for i in range(0, len(rec_keys), cols_per_row):
    row_keys = rec_keys[i:i + cols_per_row]
    rec_cols = st.columns(cols_per_row)
    for idx, key in enumerate(row_keys):
        if rec_cols[idx].button(f"✨ {key}", use_container_width=True, key=f"btn_{key}"):
            st.session_state.search_term = key

st.write("")

# 검색어 입력창
input_value = st.text_input(
    "🔍 직접 궁금한 직업명을 입력해 보세요:",
    value=st.session_state.search_term,
    placeholder="예: 수의사, 제빵사, 파일럿, 변호사, 프로그래머..."
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
        
        col_poster, col_info = st.columns([1, 1.5])
        
        with col_poster:
            st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
            st.image(data["poster"], use_container_width=True, caption=f"[{data['type']}] {data['title']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"<h1 style='color:#FF6B81;'>🎬 {data['title']}</h1>", unsafe_allow_html=True)
            
            # 줄거리 카드
            st.markdown(f"""
            <div class="info-card">
                <div class="card-title">🎀 작품 속 상세 이야기</div>
                <div class="card-text">{data["summary"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 진로 소개 카드
            st.markdown(f"""
            <div class="info-card">
                <div class="card-title">💡 {matched_key} 직업 탐구 가이드</div>
                <div class="card-text">{data["career_info"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # 작품 속 또 다른 직업 카드
        if "co_careers" in data and data["co_careers"]:
            st.write("")
            st.markdown(f"### 🤝 [{data['title']}]에 함께 나오는 관련 직업들")
            
            co_cols = st.columns(len(data["co_careers"]))
            for idx, (co_job, co_desc) in enumerate(data["co_careers"].items()):
                with co_cols[idx]:
                    with st.expander(f"✨ **{co_job}**", expanded=True):
                        st.write(co_desc)

    else:
        # DB 미등록 시 AI 호출
        st.info(f"💡 기본 목록에 없는 직업이에요! Gemini AI 친구가 탐색해 줄게요 ⭐")
        with st.spinner("AI가 예쁜 추천 가이드를 만들고 있어요..."):
            ai_result, error = get_gemini_recommendation(search_query)
            if error:
                st.error(error)
            elif ai_result:
                col_poster, col_info = st.columns([1, 1.5])
                with col_poster:
                    st.image(
                        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
                        caption=f"{search_query} 관련 미디어 추천",
                        use_container_width=True
                    )
                with col_info:
                    st.markdown(f"<h1>🤖 AI 가이드: {search_query}</h1>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="card-text">{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
