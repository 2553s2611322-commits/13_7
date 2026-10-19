import os
import json
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# 1. 페이지 기본 설정 & 커스텀 CSS (깔끔한 UI)
# ==========================================
st.set_page_config(
    page_title="영화·드라마 속 진로 탐색",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# UI 스타일링
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
# 2. 내장 데이터베이스 (Fallback 및 기본 추천)
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
        "job_desc": "소프트웨어 개발자는 컴퓨팅 프로그래밍 언어를 활용하여 서비스 및 시스템을 개발합니다
