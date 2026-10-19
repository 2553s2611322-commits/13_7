import os
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ==========================================
# 1. 페이지 설정 및 디자인 스타일 (CSS)
# ==========================================
st.set_page_config(
    page_title="AI 진로 상담 - 너의 고민, AI와 함께",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - 버튼 크기 고정 및 디자인 개선
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #EEF2FF;
        border-right: 1px solid #E2E8F0;
    }
    
    /* 메인 타이틀 */
    .app-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
        padding-bottom: 5px;
    }
    .app-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 20px;
    }

    /* AI 인사말 박스 */
    .ai-welcome-box {
        background-color: #EFF6FF;
        border: 1px solid #DBEAFE;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        color: #1E3A8A;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 🔥 카드 버튼 크기 완전 통일 (CSS 핵심 수정 부분) */
    div[data-testid="stColumn"] {
        display: flex;
        justify-content: center;
    }
    
    div[data-testid="stColumn"] > div {
        width: 100%;
    }

    .stButton > button {
        width:
