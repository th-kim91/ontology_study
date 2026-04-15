import streamlit as st
import anthropic
import json
import time

st.set_page_config(
    page_title="Enhans 기술 학습 퀴즈",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #EEF0F4; }
  .main .block-container { padding-top: 2rem; max-width: 960px; }

  /* ════════════════════════════════════════
     GLOBAL TEXT — comprehensive contrast fix
  ════════════════════════════════════════ */
  /* All markdown containers */
  .stMarkdown, .stMarkdown p, .stMarkdown li,
  .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
  .stMarkdown strong, .stMarkdown em { color: #1E293B !important; }

  /* Streamlit widget labels */
  .stSelectbox label, .stTextInput label,
  .stTextArea label, .stRadio label,
  .stCheckbox label, .stNumberInput label,
  [data-testid="stWidgetLabel"],
  [data-testid="stWidgetLabel"] p,
  [data-testid="stWidgetLabel"] span { color: #1E293B !important; }

  /* Selectbox selected value & dropdown */
  .stSelectbox [data-baseweb="select"] div,
  .stSelectbox [data-baseweb="select"] span,
  .stSelectbox [data-baseweb="select"] input { color: #1E293B !important; }
  [data-baseweb="popover"] li,
  [data-baseweb="menu"] li,
  [data-baseweb="option"] { color: #1E293B !important; background: white !important; }
  [data-baseweb="option"]:hover { background: #F0FDFA !important; }

  /* Text inputs */
  .stTextInput input,
  .stTextArea textarea,
  .stNumberInput input { color: #1E293B !important; }

  /* General catch-all for main content area */
  .main p, .main li, .main span,
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] span,
  [data-testid="stMarkdownContainer"] li { color: #1E293B !important; }

  /* ── Progress bar ── */
  .stProgress > div > div > div > div {
    background: linear-gradient(90deg, #028090, #0EA5E9) !important;
    border-radius: 99px;
  }

  /* ════════════════════════════════════════
     SIDEBAR — wider
  ════════════════════════════════════════ */
  section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #09162A 0%, #1B2A4A 60%, #022A33 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
    min-width: 260px !important;
    max-width: 300px !important;
    width: 270px !important;
  }
  section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] .stMarkdown,
  section[data-testid="stSidebar"] .stMarkdown p,
  section[data-testid="stSidebar"] span { color: #94A3B8 !important; }
  section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08); }
  section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    color: #94A3B8 !important;
    border-radius: 8px;
    font-size: 0.8em;
    text-align: left;
    padding: 7px 10px;
    transition: all 0.15s;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(2,128,144,0.2);
    border-color: rgba(2,128,144,0.5);
    color: #E2E8F0 !important;
  }
  section[data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); }
  section[data-testid="stSidebar"] .stTextInput > div > div > input { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: white; }

  /* ════════════════════════════════════════
     HOME PAGE — two-panel layout
  ════════════════════════════════════════ */
  .home-left {
    background: linear-gradient(155deg, #0A1628 0%, #162039 40%, #0C2A34 100%);
    border-radius: 20px;
    padding: 48px 44px 44px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 24px 64px rgba(9,22,42,0.28);
  }
  .home-left::before {
    content: '';
    position: absolute; top: -100px; right: -100px;
    width: 380px; height: 380px;
    background: radial-gradient(circle, rgba(2,128,144,0.18) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
  }
  .home-left::after {
    content: '';
    position: absolute; bottom: -60px; left: -40px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(14,165,233,0.08) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
  }
  .hl-eyebrow {
    font-size: 10px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #028090 !important;
    margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
  }
  .hl-eyebrow::before {
    content: ''; display: inline-block;
    width: 20px; height: 2px; background: #028090; border-radius: 2px;
  }
  .hl-title {
    font-size: 2.4em; font-weight: 900; line-height: 1.15;
    color: white !important; margin: 0 0 14px;
    letter-spacing: -0.5px;
  }
  .hl-title span { color: #67E8F9 !important; }
  .hl-sub {
    font-size: 0.9em; color: #7B96AA !important;
    line-height: 1.7; margin-bottom: 32px;
  }
  .hl-divider {
    border: none; border-top: 1px solid rgba(255,255,255,0.07);
    margin: 0 0 24px;
  }
  /* Level rows — no icon, left accent bar */
  .hl-level {
    display: flex; align-items: flex-start; gap: 0;
    margin-bottom: 18px;
    padding-left: 14px;
    border-left: 2px solid rgba(255,255,255,0.1);
  }
  .hl-level-body { flex: 1; }
  .hl-level-name {
    font-size: 0.88em; font-weight: 700;
    color: #E2E8F0 !important; margin-bottom: 3px;
  }
  .hl-level-desc {
    font-size: 0.78em; color: #7B96AA !important; line-height: 1.5;
    margin-bottom: 5px;
  }
  .hl-level-cnt {
    font-size: 0.72em; font-weight: 600;
    padding: 2px 8px; border-radius: 99px; display: inline-block;
  }
  .hl-footer {
    margin-top: 28px;
    font-size: 0.75em; color: #3A5468 !important;
    display: flex; align-items: center; gap: 8px;
  }
  .hl-footer::before {
    content: ''; display: inline-block;
    width: 6px; height: 6px; border-radius: 50%; background: #028090; flex-shrink: 0;
  }

  /* Right panel — white card, compact form */
  .home-right-header {
    padding: 36px 36px 0;
    background: white;
    border-radius: 20px 20px 0 0;
    border: 1px solid #E2E8F0;
    border-bottom: none;
  }
  .home-right-form {
    padding: 20px 36px 28px;
    background: white;
    border-radius: 0 0 20px 20px;
    border: 1px solid #E2E8F0;
    border-top: none;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  }
  .hr-title {
    font-size: 1.1em; font-weight: 800; color: #0F172A !important;
    margin: 0 0 5px;
  }
  .hr-sub {
    font-size: 0.81em; color: #94A3B8 !important;
    margin: 0 0 22px; line-height: 1.5;
  }
  .hr-divider {
    border: none; border-top: 1px solid #F1F5F9; margin: 18px 0 14px;
  }
  .hr-feature {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.8em; color: #64748B !important;
    margin-bottom: 8px;
  }
  .hr-feature-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #028090; flex-shrink: 0;
  }

  /* ════════════════════════════════════════
     INFO / NOTICE BOX
  ════════════════════════════════════════ */
  .info-box {
    background: white;
    border-radius: 14px;
    padding: 18px 24px;
    border: 1px solid #E2E8F0;
    font-size: 0.86em;
    color: #475569 !important;
    line-height: 1.75;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .info-box strong { color: #0F172A !important; }

  /* ════════════════════════════════════════
     QUESTION CARD
  ════════════════════════════════════════ */
  .q-card {
    background: white;
    border-radius: 16px;
    padding: 28px 32px 24px;
    margin-bottom: 18px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06);
    border-top: 3px solid #028090;
  }
  .q-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
  .q-num-bubble {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #028090, #0369A1);
    color: white !important;
    font-size: 12px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .q-category {
    background: #F0FDFA; color: #0F766E !important;
    font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 99px;
    border: 1px solid #CCFBF1;
  }
  .q-type-badge { font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 99px; margin-left: auto; }
  .badge-mc  { background: #FFF7ED; color: #C2410C !important; border: 1px solid #FED7AA; }
  .badge-sub { background: #F5F3FF; color: #6D28D9 !important; border: 1px solid #DDD6FE; }
  .q-text { font-size: 1.08em; font-weight: 600; color: #0F172A !important; line-height: 1.65; }

  /* ════════════════════════════════════════
     RADIO BUTTONS — force dark text always
  ════════════════════════════════════════ */
  div[role="radiogroup"] label,
  div[role="radiogroup"] label p,
  div[role="radiogroup"] label span,
  div[data-baseweb="radio"] label,
  div[data-baseweb="radio"] label p,
  div[data-baseweb="radio"] label span,
  .stRadio label, .stRadio label p, .stRadio span,
  [data-testid="stMarkdownContainer"] p { color: #1E293B !important; }

  .stRadio > div { gap: 8px; }
  div[data-baseweb="radio"] {
    background: #F8FAFC;
    border: 1.5px solid #E2E8F0;
    border-radius: 11px;
    padding: 13px 17px;
    transition: all 0.15s;
  }
  div[data-baseweb="radio"]:hover { border-color: #028090; background: #F0FDFA; }

  /* ════════════════════════════════════════
     TEXT AREA
  ════════════════════════════════════════ */
  .stTextArea textarea {
    border-radius: 11px;
    border: 1.5px solid #E2E8F0;
    font-size: 0.95em;
    color: #1E293B !important;
    background: #FAFAFA;
    padding: 12px 16px;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .stTextArea textarea:focus { border-color: #028090; box-shadow: 0 0 0 3px rgba(2,128,144,0.1); }

  /* ════════════════════════════════════════
     BUTTONS
  ════════════════════════════════════════ */
  .stButton > button { border-radius: 9px; font-weight: 600; font-size: 0.9em; transition: all 0.15s; }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #028090, #0369A1);
    border: none; color: white !important;
    box-shadow: 0 2px 8px rgba(2,128,144,0.25);
  }
  .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #026070, #025A8A);
    box-shadow: 0 6px 18px rgba(2,128,144,0.35);
    transform: translateY(-1px);
  }

  /* ════════════════════════════════════════
     SCORE DISPLAY
  ════════════════════════════════════════ */
  .score-hero {
    text-align: center;
    background: linear-gradient(150deg, #09162A 0%, #1B2A4A 100%);
    border-radius: 22px;
    padding: 44px 28px 36px;
    box-shadow: 0 16px 48px rgba(9,22,42,0.22);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .score-hero::before {
    content: '';
    position: absolute; top: -50px; right: -50px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(2,128,144,0.2) 0%, transparent 65%);
    border-radius: 50%;
  }
  .score-level-tag {
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #4B6380 !important;
    margin-bottom: 12px;
  }
  .score-num {
    font-size: 5.5em; font-weight: 900;
    background: linear-gradient(135deg, #FFFFFF, #94D5DB);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; letter-spacing: -3px;
  }
  .score-denom { font-size: 1.1em; color: #475569 !important; font-weight: 500; margin-top: 4px; }
  .grade-pill {
    display: inline-block; padding: 8px 22px;
    border-radius: 99px; font-size: 0.88em; font-weight: 700;
    margin-top: 16px;
  }
  .score-pct { font-size: 0.88em; color: #64748B !important; margin-top: 10px; }

  /* ── Stat chips ── */
  .stat-row { display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap; }
  .stat-chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px; padding: 12px 22px; text-align: center; min-width: 100px;
  }
  .stat-val { font-size: 1.5em; font-weight: 900; display: block; }
  .stat-lbl { font-size: 0.72em; color: #4B6380 !important; font-weight: 500; margin-top: 2px; }

  /* ════════════════════════════════════════
     RESULT DETAIL CARDS (custom HTML)
  ════════════════════════════════════════ */
  .rd-wrap {
    background: white;
    border-radius: 14px;
    margin-bottom: 12px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .rd-header {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 20px;
    cursor: pointer;
  }
  .rd-correct .rd-header  { background: #F0FDF4; border-left: 4px solid #16A34A; }
  .rd-wrong   .rd-header  { background: #FFF7ED; border-left: 4px solid #EA580C; }
  .rd-partial .rd-header  { background: #FEFCE8; border-left: 4px solid #CA8A04; }
  .rd-icon { font-size: 1.15em; flex-shrink: 0; }
  .rd-title { font-size: 0.88em; font-weight: 600; color: #1E293B !important; flex: 1; }
  .rd-score-tag {
    font-size: 0.78em; font-weight: 700; padding: 3px 10px; border-radius: 99px; flex-shrink: 0;
  }
  .rd-correct .rd-score-tag { background: #DCFCE7; color: #15803D !important; }
  .rd-wrong   .rd-score-tag { background: #FFEDD5; color: #C2410C !important; }
  .rd-partial .rd-score-tag { background: #FEF9C3; color: #A16207 !important; }
  .rd-body { padding: 0 20px 18px 20px; }
  .rd-section { margin-top: 14px; }
  .rd-section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; color: #94A3B8 !important; margin-bottom: 6px;
  }
  .rd-section-text { font-size: 0.88em; line-height: 1.65; color: #334155 !important; }
  .rd-q-text  { font-size: 0.9em; font-weight: 600; color: #1E293B !important; line-height: 1.55; }
  .rd-my-ans  { font-size: 0.87em; color: #475569 !important; line-height: 1.55; }

  /* feedback blocks */
  .fb-good {
    background: #F0FDF4; border-left: 3px solid #22C55E;
    border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px;
    font-size: 0.85em; color: #166534 !important; line-height: 1.6;
  }
  .fb-warn {
    background: #FFFBEB; border-left: 3px solid #F59E0B;
    border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px;
    font-size: 0.85em; color: #92400E !important; line-height: 1.6;
  }
  .fb-info {
    background: #EFF6FF; border-left: 3px solid #3B82F6;
    border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px;
    font-size: 0.85em; color: #1E40AF !important; line-height: 1.6;
  }
  .fb-answer {
    background: #F8FAFC; border: 1px dashed #CBD5E1;
    border-radius: 10px; padding: 12px 16px; margin-top: 10px;
    font-size: 0.83em; color: #475569 !important; line-height: 1.65;
  }
  .fb-correct-ans {
    background: #F0FDF4; border: 1px solid #BBF7D0;
    border-radius: 8px; padding: 8px 14px; margin-top: 8px;
    font-size: 0.85em; color: #166534 !important; font-weight: 600;
  }
  .fb-explan {
    background: #F8FAFC; border-left: 3px solid #94A3B8;
    border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px;
    font-size: 0.85em; color: #475569 !important; line-height: 1.6;
  }

  /* ════════════════════════════════════════
     EXPANDER OVERRIDES
  ════════════════════════════════════════ */
  .streamlit-expanderHeader { font-size: 0.9em !important; color: #1E293B !important; }
  .streamlit-expanderHeader p { color: #1E293B !important; }
  .streamlit-expanderContent { background: white !important; }
  .streamlit-expanderContent p,
  .streamlit-expanderContent span,
  .streamlit-expanderContent li { color: #334155 !important; }

  /* ── alert/info/success/warning overrides ── */
  div[data-testid="stAlert"] { border-radius: 10px; }
  div[data-testid="stAlert"] p,
  div[data-testid="stAlert"] span { color: #1E293B !important; }

  /* ════════════════════════════════════════
     MISC
  ════════════════════════════════════════ */
  .nav-hint { font-size: 12px; color: #94A3B8; text-align: center; }
  .section-divider { border: none; border-top: 1px solid #E2E8F0; margin: 24px 0; }

  /* progress bar top strip */
  .quiz-topbar {
    background: white;
    border-radius: 14px;
    padding: 14px 22px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #E8ECF0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
</style>
""", unsafe_allow_html=True)

# ── Knowledge Base ─────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
[인핸스(Enhans) & AgentOS 핵심 기술 지식]

## 회사 소개
인핸스(Enhans)는 AgentOS 기반 Vertical AI Agent 플랫폼 회사.
50+ 국가, 1,000+ 마켓플레이스, 20+ 글로벌 소비자 브랜드 서비스 중. 투자: $25M (Series B).

## AgentOS (COS) - 5가지 핵심 제품
1. Pipeline Builder: DB/API/파일 등 200개 이상 커넥터로 데이터 연결·정규화 후 온톨로지 DB 적재
2. Ontology Manager: 데이터에 의미(Semantic)와 관계(Relational)를 부여해 AI가 구조·맥락 기반으로 이해하도록 구조화
3. Workflow Builder: 멀티 에이전트 생성 + 실제 업무 흐름대로 워크플로우 구성
4. Dashboard Generation: 온톨로지 기반으로 몇 분 만에 재사용 가능한 대시보드 뷰 생성
5. CUA (Computer Use Agent / ACT-2): 화면을 보고 이해하고 판단해 실제 액션 실행

## 온톨로지 핵심 3요소
- Object: 업무에서 판단의 대상이 되는 개념(실체). RDB 테이블과 유사. 예: 설비, 고객사, 계약, 생산배치
- Property/Attribute: Object를 구성하는 특성·속성. 예: 설비.재고량, 고객사.계약만료일
- Link/Relation: Object 또는 Property 간 연결 관계. 예: 설비→공정(runs_on), 고객사→계약

## 지식 사전 (Knowledge Dictionary)
- 회사 규칙·정의·가이드라인처럼 자연어로 된 정보 저장 (Vector DB)
- RAG 기반으로 조회
- 예1: "장기 체화 재고 = 마지막 출고 이력 180일 초과 + 재고 평가액 500만원 이상"
- 예2: "30% 이상 할인 시 영업 본부장 사전 서면 승인 필요"
- 역할 분리: 규칙/정의 조회 = 지식 사전(RAG), 숫자 계산/조건 판단 = Object Graph

## 기존 접근 방식의 4가지 한계
1. RAG 한계: 문서에서 텍스트 조각 추출은 잘 하지만, 구조·관계·맥락 기반 판단 불가
2. 다양한 문서 해석 한계: 정형/비정형 동시 처리 어려움
3. Text-to-SQL 한계: 비슷한 컬럼 여러 개 있을 때 AI가 의미 "추측" → 잘못된 쿼리 생성
4. 기준 운영 한계: 규칙이 코드/프롬프트에 박혀 있어 변경 시 전체 수정 필요

## 온톨로지 구현 방식 3종류
1. Semantic Web 정통 방식 (RDF/OWL/SPARQL): 논리적으로 가장 엄밀, 자동 추론 강함. 단 실무 운영 무겁고 복잡. SPARQL = RDF 트리플 기반 질의 언어
2. GraphDB 방식 (Neo4j 등): 저장 자체가 노드/엣지(Cypher 질의). 관계 탐색 강함. 단 기존 RDB 데이터와 동기화·통합 비용 큼
3. RDB 기반 Semantic Layer 방식 (인핸스/Palantir 스타일):
   - 데이터는 기존 테이블 형태 유지 + 온톨로지가 의미/관계 상위 레이어로 추가
   - 질의 흐름: 온톨로지 참고 → SQL 생성 → LLM 자연어 요약
   - RDB + Semantic Layer + 정책/지식사전 + SQL + LLM 구조

## 인핸스가 RDB 기반 Semantic Layer를 선택한 이유 (4가지)
1. 운영이 쉽다: 기존 DWH/SQL 생태계 그대로 활용
2. 빠르게 적용: GraphDB로 전체 마이그레이션 불필요
3. 정확한 답변: SQL로 수치 추출 + LLM은 설명만 → 할루시네이션 대폭 감소
4. UI로 관리: 비엔지니어도 온톨로지/관계를 시각적으로 관리 가능

## 경쟁 기술과 인핸스 차이
- vs RAG: RAG = "이런 내용이 있어요"(검색). 인핸스 = 판단 + 실행까지. 역할 분리로 함께 쓸 수 있음
- vs Text-to-SQL: 컬럼 의미 추측 → 오류. 인핸스 = 의미 사전 정의 → 정확한 엔티티 추출
- vs OWL/RDF: 학문적 완성도(논문 수준) vs 빠른 실무 적용성(시공 매뉴얼)
- vs GraphDB: 저장 방식 자체 변경(비용↑) vs 기존 테이블 유지 + 레이어 추가
- vs Databricks/Snowflake Semantic Layer: 사람이 보는 보고서 자동화 vs AI Agent가 읽고 실행

## Cold Start (최초 구축)
- Object/Link 설계: 사람 담당 (비즈니스 도메인 지식 필요)
- 필드 매핑·비정형 문서 속성 추출: AI가 지원
- 실제 방식: AI 80% 초안 → 현업 20% 검수·수정

## 비정형 데이터 분류 기준
- Object Attribute로: 자주 꺼내 쓰는 구체적 값 (계약만료일, 고객명, 담당자)
- 지식 사전으로: 문맥·뉘앙스 중요 내용 (특약 조건, 협상 맥락, 규정 설명)
- 한 문서에서 두 방식 모두 사용 가능

## Observability (투명성)
- Agent가 어떤 Object 참조했는지, 어떤 규칙(지식사전) 적용했는지, 어떤 순서로 판단 → 어떤 액션 실행했는지 전부 이력 기록
- AI 판단 역추적 가능 = 블랙박스가 아닌 투명한 구조

## Governance
- Object 단위로 접근 권한 설정 (예: 재무 Object → 재무팀만)
- 지식 사전 규칙 변경 이력 관리 (누가, 언제 바꿨는지)
- Agent 실행 액션 전체 기록

## 온톨로지의 4가지 핵심 가치
1. AI가 데이터를 "이해" → 구조·맥락 기반 정확한 판단
2. 규칙 한 곳 관리 → 지식 사전 1곳 변경 시 연결된 모든 Agent 자동 반영
3. 지식 유지 → 베테랑 직원 퇴사해도 노하우가 시스템에 남음
4. 보고 → 실행 (기존: "이런 상황" 알림 / 인핸스: "이 상황이니 바로 실행")

## 인핸스 포지셔닝
- DS(데이터 사이언티스트) 대체 X → 분석 자동화 플랫폼, DS와 협업 구조
- 기존 인프라 교체 X → 위에 의미 레이어 추가 (기존 데이터 자산 보존)
- E2E: 데이터 연결 → 온톨로지 구성 → 멀티 Agent 구축 → 대시보드 생성 → 액션 실행
"""

# ── Quiz Data ──────────────────────────────────────────────────────────────────
QUIZ_DATA = {
    "초급": [
        # ── MC ──────────────────────────────────────────────────────────────
        {"id": "b01", "type": "mc", "category": "기본 개념",
         "question": "AgentOS에서 '업무 판단의 대상이 되는 개념'을 나타내는 기본 단위는 무엇인가요?",
         "options": ["A) Table", "B) Object", "C) Document", "D) Row"],
         "answer": "B",
         "explanation": "Object는 업무에서 판단의 대상이 되는 개념(실체)으로, RDB의 테이블과 유사합니다. 예: 설비, 고객사, 계약, 생산배치"},

        {"id": "b02", "type": "mc", "category": "기본 개념",
         "question": "Object들 사이의 연결 관계를 정의하는 요소는 무엇인가요?",
         "options": ["A) Attribute", "B) Pipeline", "C) Link", "D) Schema"],
         "answer": "C",
         "explanation": "Link(Relation)는 Object 또는 Property 간의 연결 관계를 정의합니다. 예: 고객사→계약, 설비→공정"},

        {"id": "b03", "type": "mc", "category": "AgentOS 제품",
         "question": "DB, API, 파일 등 200개 이상의 커넥터로 데이터를 연결·정규화하는 AgentOS 제품은?",
         "options": ["A) Ontology Manager", "B) Pipeline Builder", "C) Workflow Builder", "D) Dashboard Generation"],
         "answer": "B",
         "explanation": "Pipeline Builder는 DB, API, 파일 등을 연결해 데이터를 정규화하고 온톨로지 DB로 적재합니다."},

        {"id": "b04", "type": "mc", "category": "경쟁 기술 비교",
         "question": "RAG 방식의 가장 큰 한계는 무엇인가요?",
         "options": [
             "A) 처리 속도가 너무 느림",
             "B) 텍스트 검색은 잘 하지만 구조·관계·맥락 기반 판단 불가",
             "C) 비용이 너무 높음",
             "D) 영어 문서만 처리 가능"
         ],
         "answer": "B",
         "explanation": "RAG는 문서에서 유사 내용을 찾아 답변을 생성하는 데 뛰어나지만, 데이터 간 구조·관계·맥락을 이해하고 업무 수준의 판단을 내리기에는 근본적인 한계가 있습니다."},

        {"id": "b05", "type": "mc", "category": "지식 사전",
         "question": "인핸스의 '지식 사전(Knowledge Dictionary)'에 저장하기 가장 적합한 데이터는?",
         "options": [
             "A) 고객의 정확한 주문 금액",
             "B) 회사 내부 기준·규칙·가이드라인처럼 문맥이 중요한 자연어 정보",
             "C) 제품 재고 수량",
             "D) 계약 만료 날짜"
         ],
         "answer": "B",
         "explanation": "지식 사전은 '장기 체화 재고 기준', '할인율 승인 정책' 처럼 자연어로 된 규칙·정의를 저장합니다. 수치나 날짜처럼 구체적 값은 Object의 Attribute로 저장합니다."},

        {"id": "b06", "type": "mc", "category": "기본 개념",
         "question": "Object를 구성하는 특성이나 속성을 무엇이라 하나요?",
         "options": ["A) Link", "B) Pipeline", "C) Attribute(Property)", "D) Connector"],
         "answer": "C",
         "explanation": "Attribute(Property)는 Object를 구성하는 특성/속성입니다. 예: 고객사 Object의 '계약만료일', 설비 Object의 '재고량'"},

        {"id": "b07", "type": "mc", "category": "인핸스 방식",
         "question": "인핸스는 기업의 기존 데이터 인프라를 어떻게 처리하나요?",
         "options": [
             "A) 완전히 교체한다",
             "B) 기존 인프라 위에 온톨로지 의미 레이어를 추가한다",
             "C) 무시하고 새 시스템을 구축한다",
             "D) 데이터를 압축 보관한다"
         ],
         "answer": "B",
         "explanation": "인핸스는 기존 Data Lake, Warehouse 등을 교체하지 않고, 위에 온톨로지(의미 레이어)를 추가하는 방식으로 동작합니다. 기존 데이터 자산을 그대로 활용할 수 있습니다."},

        {"id": "b08", "type": "mc", "category": "경쟁 기술 비교",
         "question": "Text-to-SQL의 핵심 문제점은 무엇인가요?",
         "options": [
             "A) 처리 속도가 느리다",
             "B) 비슷한 컬럼이 여러 개 있을 때 AI가 의미를 추측해 잘못된 컬럼을 선택한다",
             "C) 한국어를 지원하지 않는다",
             "D) 클라우드에서만 동작한다"
         ],
         "answer": "B",
         "explanation": "AI가 데이터베이스 스키마만 보고 컬럼의 의미를 추측해야 하므로, 비슷한 컬럼이 여러 개일 때(예: price_a, price_b, final_price) 잘못된 컬럼을 선택해 오류가 발생합니다."},

        {"id": "b09", "type": "mc", "category": "AgentOS 제품",
         "question": "멀티 에이전트가 실제 업무를 수행하도록 워크플로우를 구성하는 AgentOS 제품은?",
         "options": ["A) Pipeline Builder", "B) Dashboard Generation", "C) Workflow Builder", "D) CUA"],
         "answer": "C",
         "explanation": "Workflow Builder는 여러 에이전트를 생성하고 실제 업무 흐름대로 워크플로우를 구성하는 제품입니다."},

        {"id": "b10", "type": "mc", "category": "Cold Start",
         "question": "온톨로지 구축 첫 시작(Cold Start) 시 Object 설계를 주로 누가 해야 하나요?",
         "options": [
             "A) AI가 전부 자동으로 설계한다",
             "B) 비즈니스 도메인 지식이 있는 사람이 설계한다",
             "C) 외부 컨설턴트만 할 수 있다",
             "D) 누가 해도 상관없다"
         ],
         "answer": "B",
         "explanation": "AI는 우리 비즈니스에서 어떤 개념이 중요한지 알 수 없습니다. '고객사 Object에 어떤 정보가 필요한가'는 비즈니스를 아는 사람이 정의해야 합니다. 단, AI가 80% 초안을 잡고 현업이 20%를 검수하는 방식을 활용합니다."},

        {"id": "b11", "type": "mc", "category": "AgentOS 제품",
         "question": "온톨로지 기반으로 몇 분 만에 재사용 가능한 대시보드 뷰를 생성하는 제품은?",
         "options": ["A) Workflow Builder", "B) Pipeline Builder", "C) Ontology Manager", "D) Dashboard Generation"],
         "answer": "D",
         "explanation": "Dashboard Generation은 온톨로지 기반으로 원하는 형태의 대시보드를 즉시 생성하는 제품입니다."},

        {"id": "b12", "type": "mc", "category": "AgentOS 제품",
         "question": "화면을 보고 이해하고 판단해 실제 액션을 실행하는 AgentOS 제품은?",
         "options": ["A) Ontology Manager", "B) Pipeline Builder", "C) CUA (ACT-2)", "D) Dashboard Generation"],
         "answer": "C",
         "explanation": "CUA(Computer Use Agent, ACT-2)는 화면을 보고 이해하고 판단해 실제 액션을 실행하는 제품입니다."},

        {"id": "b13", "type": "mc", "category": "온톨로지 가치",
         "question": "온톨로지를 도입하면 '베테랑 직원의 퇴사'에도 업무 지식이 유지되는 이유는?",
         "options": [
             "A) 영상으로 모든 업무를 녹화하기 때문",
             "B) 노하우와 판단 기준이 Object/지식사전에 명시적으로 저장되기 때문",
             "C) 자동으로 인수인계 문서가 생성되기 때문",
             "D) 재고용 계약이 있기 때문"
         ],
         "answer": "B",
         "explanation": "온톨로지 방식에서는 판단 기준, 업무 규칙, 관계 정의가 시스템에 명시적으로 저장됩니다. 따라서 담당자가 바뀌어도 모든 맥락이 시스템에 남습니다."},

        {"id": "b14", "type": "mc", "category": "Observability",
         "question": "AgentOS의 Observability(투명성) 기능으로 추적할 수 있는 것이 아닌 것은?",
         "options": [
             "A) Agent가 어떤 Object를 참조했는지",
             "B) 어떤 지식사전 규칙을 적용했는지",
             "C) Agent가 실행한 액션 이력",
             "D) 개발팀 직원의 근무 시간"
         ],
         "answer": "D",
         "explanation": "Observability는 AI가 어떤 데이터를 보고, 어떤 규칙을 적용하고, 어떤 순서로 판단해 어떤 액션을 실행했는지 역추적할 수 있게 합니다. 직원 근무시간은 관련 없습니다."},

        {"id": "b15", "type": "mc", "category": "인핸스 방식",
         "question": "기존 Data Lake / Warehouse 방식과 인핸스 온톨로지 방식의 핵심 차이는?",
         "options": [
             "A) 저장 용량의 차이",
             "B) 기존 방식은 사람이 봐야 판단, 온톨로지 방식은 AI Agent가 스스로 판단·실행",
             "C) 처리 속도 차이",
             "D) 클라우드 지원 여부"
         ],
         "answer": "B",
         "explanation": "기존 방식은 데이터를 잘 모으고 보여주지만 결국 사람이 보고 판단해야 합니다. 온톨로지 방식은 AI가 의미를 이해하고 스스로 판단·실행합니다."},

        # ── 주관식 ────────────────────────────────────────────────────────────
        {"id": "b16", "type": "subjective", "category": "기본 개념",
         "question": "Object와 RDB 테이블의 공통점과 차이점을 설명해보세요.",
         "answer_key": "공통점: 둘 다 데이터를 구조화된 형태로 담는 단위. "
                       "차이점: RDB 테이블은 데이터 저장이 목적이지만, Object는 '업무에서 판단의 대상이 되는 개념'을 정의하는 것이 목적. "
                       "Object는 다른 Object와 Link로 관계가 정의되고, 지식사전·Agent와 연결되어 판단·실행까지 이어짐."},

        {"id": "b17", "type": "subjective", "category": "경쟁 기술 비교",
         "question": "RAG를 '도서관 사서'에 비유하는 이유를 설명해보세요.",
         "answer_key": "도서관 사서는 '이런 내용이 3번 책 42페이지에 있어요'까지는 찾아주지만, "
                       "그 내용을 바탕으로 어떤 결정을 내려야 하는지는 결국 사람이 판단해야 함. "
                       "RAG도 마찬가지로 관련 문서를 찾아 답변을 만들어주지만, '이 고객이 해지 조건에 해당하는가' 같은 판단은 할 수 없음."},

        {"id": "b18", "type": "subjective", "category": "기본 개념",
         "question": "'데이터에 의미를 부여한다'는 것이 무슨 뜻인지 구체적인 예시와 함께 설명해보세요.",
         "answer_key": "단순히 price_a, price_b, final_price 컬럼이 있을 때 AI는 어느 게 '최종 청구 금액'인지 모름. "
                       "의미를 부여한다는 것은 '이 필드는 최종 청구 금액', '저 필드는 제조 원가'라고 시스템에 명확히 정의하는 것. "
                       "이렇게 되면 AI가 추측 없이 정확하게 원하는 데이터를 찾을 수 있음."},

        {"id": "b19", "type": "subjective", "category": "인핸스 방식",
         "question": "인핸스가 기존 인프라를 교체하지 않고 '위에 레이어를 얹는' 방식을 선택한 이유는 무엇인가요?",
         "answer_key": "기업은 이미 수년간 구축한 데이터 자산(DWH, Data Lake 등)이 있음. "
                       "이를 교체하면 비용·시간·리스크가 엄청남. "
                       "인핸스는 기존 SQL/DWH 생태계를 그대로 유지하면서 온톨로지 레이어만 추가해 "
                       "빠른 도입, 낮은 리스크, 기존 자산 활용 모두를 실현함."},

        {"id": "b20", "type": "subjective", "category": "인핸스 포지셔닝",
         "question": "인핸스가 '데이터 사이언티스트(DS)를 대체하는 것이 아니다'라고 설명하는 이유는 무엇인가요?",
         "answer_key": "인핸스는 '데이터 구조화 → 분석 실행 → 결과 해석 → 리포트 생성'의 전 과정을 자동화하는 플랫폼. "
                       "통계 모델의 타당성 검토, 분석 결과의 통계적 유의성 판단, 비즈니스 의사결정은 여전히 DS와 현업 팀이 담당. "
                       "인핸스는 반복적이고 자동화 가능한 과정을 처리해 DS가 더 고차원 업무에 집중하게 해주는 파트너."},
    ],

    "중급": [
        # ── MC ──────────────────────────────────────────────────────────────
        {"id": "m01", "type": "mc", "category": "데이터 분류",
         "question": "비정형 데이터를 Object Attribute로 저장할지 지식 사전에 넣을지 결정하는 기준은?",
         "options": [
             "A) 파일 크기",
             "B) 자주 꺼내 쓰는 구체적 값이면 Object Attribute, 문맥·뉘앙스가 중요하면 지식 사전",
             "C) 데이터 업데이트 빈도",
             "D) 원본 파일 형식(PDF/Excel)"
         ],
         "answer": "B",
         "explanation": "계약 만료일·고객명처럼 자주 꺼내 쓰는 구체적 값은 Object Attribute로, 특약 조건·협상 맥락처럼 전체 문장의 맥락을 이해해야 하는 내용은 지식 사전에 저장합니다."},

        {"id": "m02", "type": "mc", "category": "온톨로지 가치",
         "question": "'규칙을 한 곳에서 관리한다'는 것이 실무에서 어떤 의미를 갖나요?",
         "options": [
             "A) 서버를 하나로 통합한다",
             "B) 지식 사전 1곳에서 기준을 바꾸면 연결된 모든 Agent가 자동으로 새 기준을 따른다",
             "C) 코드 저장소를 통합한다",
             "D) 데이터를 압축 보관한다"
         ],
         "answer": "B",
         "explanation": "기존 방식은 규칙이 여러 코드/프롬프트에 분산되어 있어, 기준 하나 바꾸려면 전체를 수정해야 했습니다. 인핸스는 지식 사전 한 곳만 바꾸면 연결된 모든 Agent가 자동 반영됩니다."},

        {"id": "m03", "type": "mc", "category": "Observability",
         "question": "Observability(투명성)가 단순한 로그 기록과 다른 가장 큰 이유는?",
         "options": [
             "A) 더 많은 데이터를 저장해서",
             "B) AI가 어떤 Object·규칙을 보고 어떤 순서로 판단했는지까지 역추적 가능해서",
             "C) 실시간 알림을 보내서",
             "D) 비용을 절감해서"
         ],
         "answer": "B",
         "explanation": "Observability는 AI가 틀린 판단을 했을 때 '왜 그런 결정이 나왔는지'를 역추적할 수 있게 합니다. 어떤 Object를 봤는지, 어떤 규칙을 적용했는지, 어떤 순서로 판단했는지 전체 흐름이 기록됩니다."},

        {"id": "m04", "type": "mc", "category": "데이터 아키텍처",
         "question": "기존 Data Lake 위에 온톨로지 레이어를 얹는 방식의 핵심 장점은?",
         "options": [
             "A) 쿼리 속도가 10배 빨라진다",
             "B) 기존에 쌓아온 데이터 자산을 그대로 활용하면서 AI 활용성을 높인다",
             "C) 보안이 자동으로 강화된다",
             "D) 저장 비용이 절감된다"
         ],
         "answer": "B",
         "explanation": "인핸스는 기존 Data Lake/Warehouse를 교체하지 않고, 위에 온톨로지 레이어를 추가하는 방식입니다. 기존 데이터 자산을 그대로 활용하면서 AI가 의미를 이해하고 실행할 수 있게 됩니다."},

        {"id": "m05", "type": "mc", "category": "경쟁 기술 비교",
         "question": "RDB 기반 Semantic Layer에서 수치 관련 할루시네이션을 줄이는 방법은?",
         "options": [
             "A) 더 많은 학습 데이터를 사용한다",
             "B) SQL로 수치를 정확히 추출하고, LLM은 설명/요약만 담당한다",
             "C) 벡터 검색을 개선한다",
             "D) 더 큰 LLM 모델을 사용한다"
         ],
         "answer": "B",
         "explanation": "수치 계산에서 LLM이 스스로 계산하면 할루시네이션이 발생합니다. 인핸스는 SQL로 정확한 수치를 추출하고, LLM은 그 결과를 자연어로 설명하는 역할만 담당하게 해 정확도를 높입니다."},

        {"id": "m06", "type": "mc", "category": "기본 개념",
         "question": "SPARQL은 어떤 데이터 모델에서 사용하는 질의 언어인가요?",
         "options": [
             "A) RDB(관계형 데이터베이스)",
             "B) RDF 트리플 기반 지식 그래프",
             "C) 문서 기반 NoSQL",
             "D) 그래프 노드/엣지 (Neo4j 스타일)"
         ],
         "answer": "B",
         "explanation": "SPARQL은 RDF(Resource Description Framework) 트리플 기반 지식 그래프를 조회하는 질의 언어로, Semantic Web 정통 방식에서 사용됩니다."},

        {"id": "m07", "type": "mc", "category": "Governance",
         "question": "인핸스의 Governance에서 접근 권한을 설정하는 단위는?",
         "options": [
             "A) 데이터베이스 전체",
             "B) 테이블 단위",
             "C) Object 단위",
             "D) 사용자 그룹 단위만"
         ],
         "answer": "C",
         "explanation": "Object 단위로 접근 권한을 설정할 수 있습니다. 예: 재무 데이터 Object는 재무팀만 볼 수 있게 제한하는 식입니다."},

        {"id": "m08", "type": "mc", "category": "경쟁 기술 비교",
         "question": "Databricks/Snowflake의 Semantic Layer와 인핸스의 근본적인 목적 차이는?",
         "options": [
             "A) 가격 차이",
             "B) 사람이 보는 보고서 자동화 vs AI Agent가 스스로 이해하고 실행하는 구조",
             "C) 처리 속도 차이",
             "D) 지원하는 데이터 형식 차이"
         ],
         "answer": "B",
         "explanation": "Databricks/Snowflake Semantic Layer는 경영진을 위한 보고서 자동화 도구로, 결국 사람이 보고 판단합니다. 인핸스는 AI Agent가 스스로 이해하고 판단하고 실행하기 위한 레이어입니다."},

        {"id": "m09", "type": "mc", "category": "데이터 분류",
         "question": "계약서에서 '특약 조건 내용(예: 을이 조기 해지할 경우 위약금의 20%를 면제함)'은 어디에 저장해야 하나요?",
         "options": [
             "A) Object의 Attribute",
             "B) 지식 사전",
             "C) 별도 관계형 테이블",
             "D) 캐시 메모리"
         ],
         "answer": "B",
         "explanation": "특약 조건처럼 전체 문장의 맥락·뉘앙스를 이해해야 의미 있는 내용은 지식 사전에 저장합니다. 계약 만료일, 계약금액처럼 구체적 값은 Object Attribute에 저장합니다."},

        {"id": "m10", "type": "mc", "category": "인핸스 방식",
         "question": "온톨로지 구축 후 데이터 소스 형식이 변경되었을 때 어떻게 처리되나요?",
         "options": [
             "A) 전체 Object 설계를 처음부터 다시 해야 한다",
             "B) Object의 개념 설계는 유지하고, 새 형식에서 값이 어디 있는지 연결 부분만 수정한다",
             "C) 새 시스템으로 교체해야 한다",
             "D) 변경된 데이터는 사용할 수 없다"
         ],
         "answer": "B",
         "explanation": "엑셀 양식이 바뀌어도 '고객명', '금액'이라는 개념 자체는 안 바뀌는 것처럼, Object의 개념 설계는 그대로 유지됩니다. 새 형식에서 그 값이 어디 있는지 연결 부분만 수정하면 됩니다."},

        {"id": "m11", "type": "mc", "category": "경쟁 기술 비교",
         "question": "OWL/RDF(표준 온톨로지)와 인핸스 방식의 가장 큰 차이는?",
         "options": [
             "A) 비용 차이",
             "B) 학문적 완성도·자동 추론 강함(OWL) vs 빠른 실무 적용성과 AI Agent 연결(인핸스)",
             "C) 지원하는 언어 차이",
             "D) 서버 사양 차이"
         ],
         "answer": "B",
         "explanation": "OWL/RDF는 논리적으로 완벽하고 자동 추론이 강하지만, 배우기 어렵고 AI Agent와 연결하려면 별도 작업이 필요합니다. 인핸스는 Object/Link/Knowledge 3개 개념만으로 빠르게 구축하고 바로 Agent와 연결됩니다."},

        {"id": "m12", "type": "mc", "category": "복잡한 관계",
         "question": "관계가 복잡하게 얽힌 데이터(예: 고객사→계약→담당자→제품→재고→납기)에서 인핸스가 강점을 보이는 이유는?",
         "options": [
             "A) 단순한 데이터에만 적합하기 때문",
             "B) Object + Link 구조 자체가 복잡한 관계형 데이터를 표현하도록 설계되었기 때문",
             "C) 다른 시스템보다 서버가 빠르기 때문",
             "D) 관계를 자동으로 단순화하기 때문"
         ],
         "answer": "B",
         "explanation": "인핸스의 Object+Link 구조는 복잡한 관계형 데이터를 표현하기 위해 설계됐습니다. 복잡한 관계일수록 Orchestrator가 여러 Object를 조합해 Agent들이 협업하게 하며, 자동화 효과가 더 크게 나옵니다."},

        # ── 주관식 ────────────────────────────────────────────────────────────
        {"id": "m13", "type": "subjective", "category": "데이터 분류",
         "question": "하나의 계약서 문서에서 어떤 정보는 Object Attribute로, 어떤 정보는 지식 사전으로 분류할지 구체적인 예시를 들어 설명해보세요.",
         "answer_key": "Object Attribute: 계약만료일, 고객명, 담당자명, 계약금액 - 이런 값들은 자주 꺼내 쓰고 구체적인 값이 있음. "
                       "지식 사전: 특약 조건, 위약금 면제 조건, 협상 맥락, 계약 배경 설명 - 전체 문장의 맥락과 뉘앙스를 이해해야 의미 있는 내용. "
                       "하나의 계약서에서 두 방식 모두 사용됨."},

        {"id": "m14", "type": "subjective", "category": "온톨로지 가치",
         "question": "'보고에서 실행으로'라는 인핸스의 핵심 가치를 구체적인 업무 시나리오를 들어 설명해보세요.",
         "answer_key": "기존: 담당자가 엑셀 열어서 계약 만료일 확인 → 제안서 새로 작성(반나절) → 일정 바쁘면 놓침 → 경쟁사가 먼저 들어와 계약 뺏김. "
                       "인핸스: D-60에 Agent가 자동 감지 → 3년 거래 이력 기반 제안서 초안 자동 생성 → 담당자에게 미팅 일정 잡으라고 먼저 알림 → 경쟁사보다 2달 먼저 움직임. "
                       "핵심: '이런 상황입니다'(알림)에서 '이 상황이니 이걸 바로 실행합니다'(자동 실행)로 전환."},

        {"id": "m15", "type": "subjective", "category": "경쟁 기술 비교",
         "question": "인핸스의 지식 사전도 결국 RAG를 사용하는데, 기존 RAG의 문제가 그대로 남는 게 아닌가요? 인핸스가 이 문제를 어떻게 해결했는지 설명해보세요.",
         "answer_key": "역할 분리가 핵심. 인핸스에서 RAG(지식사전)는 딱 한 가지만 함: 회사 규칙·정의처럼 자연어로 된 정보 조회. "
                       "숫자 계산, 조건 판단, 여러 데이터를 엮어서 내리는 결정은 RAG가 아닌 온톨로지(Object Graph)가 담당. "
                       "비유: 법무팀(지식사전/RAG)은 규정을 찾아주고, 실무팀(온톨로지)이 그 규정 바탕으로 판단·실행. "
                       "법무팀 혼자 모든 걸 하려다 생기는 문제를 역할 분리로 해결."},

        {"id": "m16", "type": "subjective", "category": "경쟁 기술 비교",
         "question": "GraphDB(Neo4j 등) 방식이 기업 환경에서 갖는 실무적 한계를 설명해보세요.",
         "answer_key": "저장 방식 자체를 노드/엣지로 바꿔야 하므로 기존 RDB 데이터를 마이그레이션해야 함. "
                       "기존 기업 데이터(RDB)와의 동기화, 비용, 권한, 성능 관리 등이 복잡해짐. "
                       "인핸스는 기존 테이블 형태를 유지하면서 온톨로지 레이어만 추가하므로 이런 마이그레이션 비용이 없음."},

        {"id": "m17", "type": "subjective", "category": "복잡한 관계",
         "question": "Object와 Link의 관계가 복잡할수록 인핸스가 더 효과적인 이유를 설명해보세요.",
         "answer_key": "Object+Link 구조 자체가 복잡한 관계형 데이터를 표현하도록 설계됨. "
                       "복잡한 관계일수록 Orchestrator가 여러 Object를 필요에 따라 조합하고, Agent들이 협업해 처리함. "
                       "단순한 데이터는 자동화해도 효과가 작지만, 여러 부서에 걸친 복잡한 관계(고객→계약→담당→제품→재고→납기)일수록 자동화의 파급 효과가 큼."},

        {"id": "m18", "type": "subjective", "category": "Governance",
         "question": "온톨로지 기반 거버넌스가 기존 DB 접근 권한 관리와 다른 점은 무엇인가요?",
         "answer_key": "기존 DB 권한: 테이블/컬럼 단위. 데이터에만 접근 제어. "
                       "인핸스 거버넌스: Object 단위 접근 권한 + 지식사전 규칙 변경 이력 + Agent 실행 액션 전체 기록. "
                       "누가 어떤 데이터를 봤는지, 어떤 규칙을 썼는지, 무슨 액션을 했는지 비즈니스 맥락까지 추적 가능. "
                       "규제 준수(Compliance), 감사(Audit) 관점에서 훨씬 강력."},

        {"id": "m19", "type": "subjective", "category": "경쟁 기술 비교",
         "question": "Text-to-SQL의 문제점을 온톨로지가 어떻게 해결하는지 설명해보세요.",
         "answer_key": "Text-to-SQL 문제: AI가 스키마만 보고 컬럼 의미를 추측해야 함. price_a, price_b, final_price 같이 비슷한 컬럼이 여러 개면 잘못 선택. "
                       "온톨로지 해결: 각 필드의 의미를 미리 정의해둠('이 필드=최종 청구 금액', '저 필드=제조 원가'). "
                       "AI가 추측하지 않고 정확한 의미 기반으로 엔티티를 추출해 정확한 SQL 생성 가능."},

        {"id": "m20", "type": "subjective", "category": "Cold Start",
         "question": "온톨로지 Cold Start(처음 구축)에서 AI와 사람이 각각 어떤 역할을 담당하나요?",
         "answer_key": "사람: Object/Link 개념 설계(비즈니스 도메인 지식 필요), 최종 검수·수정. "
                       "AI: 기존 데이터 구조·문서 분석 후 Object 초안 제안, 필드 매핑, 비정형 문서에서 속성 추출. "
                       "방식: AI 80% 초안 → 현업 담당자 인터뷰 → 20% 수정·검수. "
                       "장점: 처음부터 백지에서 설계하는 것보다 훨씬 빠르고 부담이 적음."},
    ],

    "고급": [
        # ── MC ──────────────────────────────────────────────────────────────
        {"id": "a01", "type": "mc", "category": "아키텍처 비교",
         "question": "3가지 온톨로지 구현 방식(RDF/OWL, GraphDB, RDB Semantic Layer) 중 기업 기존 인프라 기준으로 마이그레이션 비용이 가장 작은 방식은?",
         "options": [
             "A) Semantic Web 정통 방식 (RDF/OWL)",
             "B) GraphDB 방식 (Neo4j 등)",
             "C) RDB 기반 Semantic Layer 방식 (인핸스 스타일)",
             "D) 세 방식 모두 동일"
         ],
         "answer": "C",
         "explanation": "RDB 기반 Semantic Layer는 기존 테이블 형태를 그대로 유지하고 위에 레이어만 추가합니다. 저장 방식을 바꾸는 GraphDB나 완전히 새로운 표준을 도입하는 RDF/OWL보다 훨씬 낮은 전환 비용으로 도입 가능합니다."},

        {"id": "a02", "type": "mc", "category": "아키텍처 비교",
         "question": "3가지 온톨로지 구현 방식 중 '논리적 추론(Reasoning)'이 가장 강한 것은?",
         "options": [
             "A) RDB 기반 Semantic Layer",
             "B) GraphDB 방식",
             "C) Semantic Web 정통 방식 (RDF/OWL)",
             "D) 모두 동일"
         ],
         "answer": "C",
         "explanation": "OWL/RDF 기반 Semantic Web은 논리적으로 가장 엄밀하고 자동 추론(Reasoning)이 가장 강합니다. 단, 이 강점이 곧 운영 복잡성이라는 단점이기도 합니다."},

        {"id": "a03", "type": "mc", "category": "AgentOS 기술",
         "question": "기준(규칙)이 변경되었을 때 인핸스 플랫폼의 처리 방식은?",
         "options": [
             "A) 모든 Agent 코드를 재배포한다",
             "B) 지식 사전 1곳만 수정하면 연결된 모든 Agent가 자동으로 새 기준을 따른다",
             "C) DB 마이그레이션을 실행한다",
             "D) LLM 모델을 재학습한다"
         ],
         "answer": "B",
         "explanation": "기준이 코드/프롬프트에 박혀 있는 기존 방식은 에이전트가 100개면 100곳을 수정해야 합니다. 인핸스는 지식 사전 1곳에서 기준을 바꾸면 연결된 모든 Agent가 자동으로 새 기준을 따릅니다."},

        {"id": "a04", "type": "mc", "category": "아키텍처 비교",
         "question": "GraphDB(Neo4j)가 기업의 기존 RDB 데이터와 통합하기 어려운 근본적 이유는?",
         "options": [
             "A) 라이센스 비용이 너무 비싸서",
             "B) 저장 방식 자체가 노드/엣지 구조라 RDB 테이블 구조와 근본적으로 다르기 때문",
             "C) 사용자 인터페이스가 복잡해서",
             "D) 클라우드를 지원하지 않아서"
         ],
         "answer": "B",
         "explanation": "GraphDB는 데이터 저장 방식 자체가 노드/엣지입니다. 기업의 기존 데이터는 대부분 관계형 테이블(RDB) 구조이므로, GraphDB로 이전하려면 전체 데이터를 마이그레이션해야 하고 동기화·비용·권한·성능 문제가 발생합니다."},

        {"id": "a05", "type": "mc", "category": "AgentOS 기술",
         "question": "AgentOS E2E(End-to-End) 플랫폼이 의미하는 것은?",
         "options": [
             "A) 전사 시스템 전체를 교체한다",
             "B) 데이터 연결부터 온톨로지 구성, Agent 구축, 대시보드 생성, 액션 실행까지 한 플랫폼에서 처리",
             "C) 모든 산업을 지원한다",
             "D) 글로벌 엔드포인트를 제공한다"
         ],
         "answer": "B",
         "explanation": "AgentOS는 Pipeline Builder(데이터 연결) → Ontology Manager(의미 구조화) → Workflow Builder(Agent 워크플로우) → Dashboard Generation → CUA(실제 실행)까지 전 과정을 하나의 플랫폼에서 처리합니다."},

        {"id": "a06", "type": "mc", "category": "온톨로지 가치",
         "question": "온톨로지 기반에서 '계약 만료 D-60에 Agent가 자동으로 제안서를 생성하는' 흐름의 핵심은?",
         "options": [
             "A) 이메일 웹훅",
             "B) Object(계약 만료일) + Link(고객 거래 이력) + 지식사전(제안서 기준) + Agent 자동 판단",
             "C) 수동 트리거",
             "D) 캘린더 API"
         ],
         "answer": "B",
         "explanation": "Object에 저장된 계약 만료일을 감지하고, Link를 통해 거래 이력을 참조하며, 지식사전의 제안서 작성 기준을 적용해 Agent가 자동으로 판단하고 실행하는 구조입니다."},

        {"id": "a07", "type": "mc", "category": "멀티 Agent",
         "question": "복잡한 업무에서 Orchestrator가 온톨로지 정보를 활용하는 방식은?",
         "options": [
             "A) 단일 Agent에 모든 작업을 위임",
             "B) 온톨로지의 Object 관계를 참고해 필요한 여러 Agent를 조합·협업하게 함",
             "C) 직접 SQL을 실행",
             "D) 배치 처리로 순차 실행"
         ],
         "answer": "B",
         "explanation": "Orchestrator는 온톨로지의 Object-Link 구조를 이해하고, 복잡한 업무를 처리하기 위해 필요한 여러 전문 Agent를 조합해 협업하게 합니다. 관계가 복잡할수록 이 조합 효과가 커집니다."},

        {"id": "a08", "type": "mc", "category": "아키텍처 비교",
         "question": "지식 사전(RAG)에서의 할루시네이션 위험이 낮은 이유는?",
         "options": [
             "A) 더 좋은 임베딩 모델을 사용해서",
             "B) 역할이 규칙/정의 조회로 제한되어 있고, 수치 판단은 온톨로지가 담당하기 때문",
             "C) 더 많은 학습 데이터 때문",
             "D) 캐싱 때문"
         ],
         "answer": "B",
         "explanation": "인핸스의 지식 사전(RAG)은 자연어 규칙·정의 조회만 담당합니다. 수치 계산과 조건 판단은 온톨로지가 처리합니다. 역할 분리로 각 영역에서 할루시네이션 위험이 최소화됩니다."},

        {"id": "a09", "type": "mc", "category": "온톨로지 가치",
         "question": "기존 방식의 '기준 운영 한계'를 인핸스가 해결하는 방식은?",
         "options": [
             "A) 더 강력한 서버 도입",
             "B) 기준을 지식 사전에 집중 관리하여 변경 시 모든 Agent가 자동 반영",
             "C) 기준을 코드에 더 체계적으로 문서화",
             "D) 변경 주기를 제한"
         ],
         "answer": "B",
         "explanation": "기존 방식은 기준이 코드/프롬프트에 분산되어 있어 변경 시 전체를 수정해야 합니다. 인핸스는 기준을 지식 사전 한 곳에 집중 관리해 1번 변경으로 모든 Agent가 자동 반영됩니다."},

        {"id": "a10", "type": "mc", "category": "데이터 처리",
         "question": "온톨로지 방식에서 과거-현재 비교 분석이 가능한 이유는?",
         "options": [
             "A) 원본 파일을 모두 보존하기 때문",
             "B) Object의 상태 변화를 시간 순서대로 기록하기 때문",
             "C) 별도 히스토리 데이터베이스를 유지하기 때문",
             "D) 주기적 스냅샷을 찍기 때문"
         ],
         "answer": "B",
         "explanation": "Object의 상태 변화(예: 고객의 구매 빈도 변화)가 시간 순서대로 기록되어, '3개월 전 대비 어떻게 달라졌는가' 같은 시간 기반 분석이 가능합니다."},

        # ── 주관식 ────────────────────────────────────────────────────────────
        {"id": "a11", "type": "subjective", "category": "아키텍처 비교",
         "question": "RDF/OWL의 자동 추론(Reasoning)과 인핸스의 LLM+온톨로지 기반 판단 방식의 차이점을 설명하고, 기업 실무 환경에서 어느 쪽이 더 적합한지 근거와 함께 서술해보세요.",
         "answer_key": "RDF/OWL: 논리 규칙 기반 자동 추론. 완전한 일관성 보장. 단, 모든 규칙을 형식 논리로 미리 정의해야 함. 실무 적용에 전문 지식 필요, 운영 무거움. "
                       "인핸스(LLM+온톨로지): Object/Link/지식사전으로 의미·관계 정의 후 LLM이 자연어 기반 판단. 비전문가도 지식사전에 자연어로 규칙 작성 가능. 빠른 도입 가능. "
                       "기업 실무 적합성: 인핸스 방식이 더 적합. 이유: 빠른 도입, 비전문가 운영 가능, 기존 RDB 활용, LLM의 유연한 자연어 판단. "
                       "단, 완전한 논리 일관성이 필요한 고규제 환경(법률, 금융)에서는 OWL의 추론 강점도 고려할 수 있음."},

        {"id": "a12", "type": "subjective", "category": "Observability",
         "question": "AI 시스템에서 Observability(투명성)가 단순한 로그 기록·모니터링과 근본적으로 다른 이유를 설명하고, 기업 운영 측면에서 이것이 왜 중요한지 서술해보세요.",
         "answer_key": "단순 로그: 시스템 이벤트(에러, 실행 시간 등) 기록. 무슨 일이 일어났는지만 파악. "
                       "Observability: AI가 어떤 데이터(Object)를 보고, 어떤 규칙(지식사전)을 적용하고, 어떤 순서로 판단해 어떤 액션을 실행했는지 전체 의사결정 과정을 역추적 가능. "
                       "기업 운영 중요성: 1) AI 틀린 판단 원인 파악 가능 → 개선 가능. 2) 블랙박스가 아닌 신뢰 가능한 AI 시스템. 3) 감사(Audit)/규제 준수 근거. 4) 책임 소재 명확화. "
                       "특히 금융·의료처럼 규제가 강한 산업에서 AI 판단 근거 제출 가능."},

        {"id": "a13", "type": "subjective", "category": "아키텍처 철학",
         "question": "인핸스가 '기존 인프라 교체 없이 위에 레이어를 얹는' 설계 철학을 선택한 것이 기업 고객 입장에서 갖는 전략적 가치를 다각도로 설명해보세요.",
         "answer_key": "1. 투자 보호: 수년간 구축한 데이터 자산(DWH, ERP, CRM 등)을 그대로 활용. 교체 비용/리스크 없음. "
                       "2. 빠른 도입: 전체 시스템 교체 없이 필요한 영역부터 점진적 도입 가능. "
                       "3. 낮은 리스크: 기존 운영 시스템에 영향 없이 AI 레이어만 추가. 실패해도 롤백 쉬움. "
                       "4. 내부 저항 최소화: IT 부서 입장에서 기존 시스템 유지 가능하므로 반발 감소. "
                       "5. SQL 생태계 활용: 기존 데이터 엔지니어, BI 팀의 역량 그대로 활용 가능."},

        {"id": "a14", "type": "subjective", "category": "기술 비교",
         "question": "기업 DX(디지털 전환) 맥락에서 온톨로지 기반 AI Agent와 RPA(Robotic Process Automation)의 차이를 설명해보세요.",
         "answer_key": "RPA: 규칙 기반 반복 작업 자동화. 화면의 특정 위치를 클릭하는 수준. 프로세스가 조금만 바뀌면 재설정 필요. 예외 상황 처리 어려움. '일을 시키는 로봇'. "
                       "온톨로지 기반 AI Agent: 데이터의 의미와 관계를 이해하고 맥락 기반 판단. 예외 상황도 지식사전의 규칙으로 처리. 규칙 변경 시 지식사전 1곳만 수정. '판단하고 행동하는 직원'. "
                       "핵심 차이: RPA는 '어떻게 하는지'가 하드코딩, AI Agent는 '무엇을 해야 하는지'를 맥락으로 이해. "
                       "즉, RPA는 자동화의 영역이고 AI Agent는 자율화의 영역."},

        {"id": "a15", "type": "subjective", "category": "멀티 Agent",
         "question": "멀티 Agent 시스템에서 Orchestrator가 온톨로지 정보를 어떻게 활용하는지, 그리고 이로 인해 단일 Agent 대비 어떤 장점이 생기는지 설명해보세요.",
         "answer_key": "Orchestrator 역할: 온톨로지의 Object-Link 구조를 이해해 복잡한 업무를 분해. 어떤 전문 Agent가 어떤 Object를 처리할지 조합·지시. "
                       "활용 방식: 예) '고객사→계약→담당자→제품→재고→납기' 관계에서 각 Object를 담당하는 전문 Agent를 순서에 맞게 조합. "
                       "단일 Agent 대비 장점: 1) 역할 분리로 각 Agent가 전문성 집중 가능. 2) 병렬 처리 가능. 3) 실패 시 해당 Agent만 재시도. 4) 새 업무 추가 시 새 Agent만 추가. "
                       "핵심: 온톨로지가 없으면 Orchestrator가 데이터 관계를 이해할 수 없어 복잡한 멀티 Agent 조합 자체가 불가능."},

        {"id": "a16", "type": "subjective", "category": "영업/설득",
         "question": "경쟁사 제품으로 RAG 기반 솔루션을 이미 도입한 고객사에게 인핸스 플랫폼의 도입 필요성을 설명해야 합니다. 어떻게 설득하시겠습니까?",
         "answer_key": "인정에서 시작: RAG는 정보 검색과 문서 기반 Q&A에서 매우 효과적. 이 가치는 인정. "
                       "한계 제시: '이 할인 주문이 승인 대상인가?'처럼 여러 조건이 얽힌 판단은 RAG가 일관되게 처리하기 어려움. 고객 등급·상품 카테고리·기간별 예외 조건 등을 동시에 고려해야 할 때 오류 발생. "
                       "인핸스 포지션: 경쟁 관계가 아닌 보완 관계. 인핸스 지식사전 내에서도 RAG를 활용하지만 역할을 분리함. "
                       "제안: 기존 RAG 솔루션은 문서 검색용으로 유지, 인핸스는 판단·실행 레이어로 추가. 두 시스템이 협력하는 구조. "
                       "증거: '보고에서 실행으로' 시나리오로 ROI 수치화해 제시."},

        {"id": "a17", "type": "subjective", "category": "아키텍처 설계",
         "question": "고객사에서 여러 부서(영업, 재무, 제조, 마케팅)의 데이터가 각각 다른 시스템에 분산되어 있습니다. 인핸스 플랫폼으로 이를 통합·활용하는 아키텍처를 설계해보세요.",
         "answer_key": "1. Pipeline Builder로 각 부서 시스템(영업CRM, 재무ERP, 제조MES, 마케팅플랫폼) 연결·정규화. "
                       "2. Ontology Manager로 부서별 핵심 Object 정의: 영업(고객사, 계약, 파이프라인), 재무(매출, 수금, 원가), 제조(제품, 재고, 납기), 마케팅(캠페인, 전환율). "
                       "3. 부서 간 Object를 Link로 연결: 고객사→계약→제품→재고, 계약→매출→수금 등. "
                       "4. 지식사전: 부서별 규칙·기준(할인 승인 정책, 재고 경보 기준, VIP 서비스 정책 등). "
                       "5. Workflow Builder로 멀티 Agent 구성: 각 부서 담당 Agent + Orchestrator. "
                       "6. Dashboard Generation으로 통합 뷰 생성. 거버넌스: 부서별 Object 접근 권한 설정."},

        {"id": "a18", "type": "subjective", "category": "장기 가치",
         "question": "온톨로지 플랫폼이 '기업 지식을 시스템화'한다는 것의 장기적 전략적 가치를 설명해보세요.",
         "answer_key": "단기: 업무 자동화, 처리 속도 향상, 오류 감소. "
                       "중기: 1) 조직 지식의 자산화 - 베테랑 퇴사해도 판단 기준·노하우 시스템에 보존. 2) 기준의 진화 - AI가 새 패턴 발견 시 지식사전 업데이트 가능. 3) 부서 간 사일로 해소 - 공통 Object 구조로 협업. "
                       "장기: 1) 경쟁 우위 - 기업만의 독자적 지식 그래프가 쌓일수록 AI 정확도 향상. 2) 데이터 전략 자산화 - 온톨로지 자체가 기업의 핵심 IP. 3) 확장성 - 새 업무 도메인 추가 시 기존 Object와 연결만 하면 됨. 4) AI 준비 상태 - LLM 능력이 향상될수록 같은 온톨로지로 더 높은 가치 창출."},

        {"id": "a19", "type": "subjective", "category": "기술 심화",
         "question": "같은 데이터를 다양한 비즈니스 질의 패턴으로 활용할 수 있다는 것이 온톨로지 Object Graph 관점에서 어떤 의미를 갖는지 설명해보세요.",
         "answer_key": "RDB 방식: 특정 질의에 맞게 JOIN을 설계하면 다른 패턴 질의에는 재설계 필요. 질의 패턴이 미리 결정되어야 함. "
                       "Object Graph: 한 번 Object와 Link를 정의하면, 다양한 탐색 경로로 다른 인사이트 추출 가능. "
                       "예: '고객사' Object에서 시작해 → Link를 따라 '계약'으로, '거래 이력'으로, '담당자'로, '제품'으로 다양하게 탐색 가능. "
                       "새로운 질문이 생겨도 기존 Object/Link 구조 재활용. 데이터 재설계 없이 새 인사이트 발굴 가능. "
                       "결과: 데이터 활용의 유연성과 확장성이 기하급수적으로 증가."},

        {"id": "a20", "type": "subjective", "category": "패러다임",
         "question": "인핸스 온톨로지 플랫폼 도입 후 기업의 데이터 활용 패러다임이 어떻게 변하는지, '데이터 → 정보 → 지식 → 행동'의 관점에서 설명해보세요.",
         "answer_key": "기존 패러다임: 데이터(저장) → 정보(BI·대시보드로 조회) → 지식(사람이 해석) → 행동(사람이 결정·실행). 각 단계에서 사람의 개입 필요. "
                       "인핸스 패러다임: 데이터(Pipeline Builder로 연결) → 정보(Object/Attribute로 의미화) → 지식(지식사전·Link로 관계·규칙 정의) → 행동(Agent가 자동 판단·실행). "
                       "핵심 변화: 1) 사람이 모든 단계에서 빠져 자동화. 2) 단순 '조회·분석'에서 '판단·실행'으로. 3) 사후 보고에서 사전 행동으로(D-60 자동 알림처럼). "
                       "4) 데이터가 '보는 것'에서 '하는 것'으로 목적 전환. 5) 조직의 모든 구성원이 AI Agent를 통해 자신의 영역을 자동화 가능."},
    ],
}


# ── LLM 평가 함수 ───────────────────────────────────────────────────────────────
def evaluate_subjective_answer(question: str, user_answer: str,
                                answer_key: str, level: str, api_key: str) -> dict:
    """Claude API로 주관식 답변을 평가하고 피드백 반환"""
    if not user_answer.strip():
        return {"score": 0, "max_score": 10, "feedback": "답변이 입력되지 않았습니다.", "grade": "미응답"}

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = f"""당신은 인핸스(Enhans) 회사의 기술 교육 담당자입니다.
신입 직원이 제출한 주관식 답변을 평가하고 건설적인 피드백을 제공하세요.

[인핸스 기술 지식베이스]
{KNOWLEDGE_BASE}

평가 기준 (총 10점):
- 핵심 개념의 정확성: 6점 (핵심 내용을 정확히 이해했는가)
- 이해 깊이: 3점 (왜 그런지까지 설명했는가, 예시를 들었는가)
- 인핸스 특화 용어 활용: 1점 (Object, Link, Agent, 지식사전 등 적절히 사용했는가)

응답 형식 (JSON):
{{
  "score": <0-10 정수>,
  "grade": "<완전 이해|양호|부분적 이해|개선 필요>",
  "correct_points": "<잘 된 부분 1-2줄>",
  "improvement": "<부족한 부분 및 보완할 내용 2-3줄>",
  "key_insight": "<이 문제의 핵심 인사이트 1-2줄>"
}}

레벨: {level}
"""

    user_msg = f"""[문제]
{question}

[답변 기준 (내부 참고용, 공개 금지)]
{answer_key}

[수험생 답변]
{user_answer}

위 답변을 평가하고 JSON 형식으로만 응답하세요."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            messages=[{"role": "user", "content": user_msg}],
            system=system_prompt,
        )
        raw = response.content[0].text.strip()
        # JSON 파싱
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw.strip())
        return {
            "score": int(result.get("score", 0)),
            "max_score": 10,
            "grade": result.get("grade", ""),
            "correct_points": result.get("correct_points", ""),
            "improvement": result.get("improvement", ""),
            "key_insight": result.get("key_insight", ""),
        }
    except Exception as e:
        return {
            "score": 0, "max_score": 10,
            "grade": "평가 오류",
            "correct_points": "",
            "improvement": f"평가 중 오류 발생: {str(e)}",
            "key_insight": "",
        }


# ── 세션 초기화 ────────────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "home",          # home | quiz | results
        "level": None,
        "api_key": "",
        "questions": [],
        "current_q": 0,
        "answers": {},           # {q_id: answer_str}
        "results": {},           # {q_id: {score, feedback...}}
        "evaluating": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding:0 4px 16px">
  <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
       color:#4B6380;margin-bottom:6px">ENHANS</div>
  <div style="font-size:1.2em;font-weight:800;color:white">기술 학습 퀴즈</div>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.page == "home":
        st.markdown("""
<div style="font-size:0.78em;font-weight:600;color:#4B6380;letter-spacing:1px;
     text-transform:uppercase;margin-bottom:12px">레벨 안내</div>
""", unsafe_allow_html=True)
        for lvl, ico, desc, cnt in [
            ("초급", "🌱", "핵심 기본 개념", "15객관 + 5주관"),
            ("중급", "⚡", "심화 이해·적용", "12객관 + 8주관"),
            ("고급", "🚀", "실전 설계·응용", "10객관 + 10주관"),
        ]:
            st.markdown(f"""
<div style="padding:10px 12px;border-radius:8px;margin-bottom:6px;
     background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08)">
  <span style="font-size:0.95em;font-weight:600;color:#CBD5E1">{ico} {lvl}</span>
  <span style="font-size:0.75em;color:#64748B;display:block;margin-top:2px">{desc} · {cnt}</span>
</div>""", unsafe_allow_html=True)

    elif st.session_state.page == "quiz":
        q_idx = st.session_state.current_q
        total = len(st.session_state.questions)
        answered = len(st.session_state.answers)

        st.markdown(f"""
<div style="margin-bottom:14px">
  <div style="font-size:0.78em;font-weight:600;color:#4B6380;letter-spacing:1px;text-transform:uppercase">
    {st.session_state.level} 레벨 진행 중
  </div>
  <div style="font-size:1em;color:#94A3B8;margin-top:4px">답변 {answered}/{total} 완료</div>
</div>
""", unsafe_allow_html=True)
        st.progress(answered / total)

        st.markdown("""
<div style="font-size:0.78em;font-weight:600;color:#4B6380;letter-spacing:1px;
     text-transform:uppercase;margin:16px 0 10px">문제 목록</div>
""", unsafe_allow_html=True)
        for i, q in enumerate(st.session_state.questions):
            answered_mark = "✓" if q["id"] in st.session_state.answers else "·"
            is_active = i == q_idx
            if st.button(
                f"{'▶ ' if is_active else ''}{answered_mark} {i+1}. {q['category']}",
                key=f"nav_{i}",
                use_container_width=True,
            ):
                st.session_state.current_q = i
                st.rerun()

    elif st.session_state.page == "results":
        total_score = sum(r.get("score", 0) for r in st.session_state.results.values())
        mc_questions = [q for q in st.session_state.questions if q["type"] == "mc"]
        sub_questions = [q for q in st.session_state.questions if q["type"] == "subjective"]
        mc_max = len(mc_questions) * 10
        sub_max = len(sub_questions) * 10
        total_max = mc_max + sub_max

        pct = int(total_score / total_max * 100) if total_max > 0 else 0
        grade = "🏆 최우수" if pct >= 90 else ("🥇 우수" if pct >= 80 else ("✅ 양호" if pct >= 60 else "📚 학습 필요"))

        st.markdown(f"""
<div style="text-align:center;padding:16px 0">
  <div style="font-size:0.78em;font-weight:600;color:#4B6380;letter-spacing:1px;text-transform:uppercase">
    {st.session_state.level} 레벨 결과
  </div>
  <div style="font-size:2.5em;font-weight:900;color:white;margin:8px 0 2px">{pct}%</div>
  <div style="font-size:0.9em;color:#94A3B8">{total_score} / {total_max}점</div>
  <div style="font-size:0.9em;color:#67E8F9;margin-top:6px">{grade}</div>
</div>
""", unsafe_allow_html=True)
        st.progress(pct / 100)


# ── Home Page ──────────────────────────────────────────────────────────────────
if st.session_state.page == "home":

    col_left, col_right = st.columns([5, 4], gap="large")

    # ── Left: brand + level info panel ────────────────────────────────────────
    with col_left:
        st.markdown("""
<div class="home-left">
  <div class="hl-eyebrow">Enhans Learning Platform</div>

  <div class="hl-title">
    AgentOS를<br><span>얼마나 이해하고</span><br>있나요?
  </div>
  <div class="hl-sub">
    온톨로지 · AI Agent · 실행 시스템의 핵심 개념을<br>
    퀴즈로 검증하고 Claude AI의 맞춤 피드백을 받으세요.
  </div>

  <hr class="hl-divider">

  <div class="hl-level" style="border-left-color:rgba(74,222,128,0.4);">
    <div class="hl-level-body">
      <div class="hl-level-name">초급 — 핵심 기본 개념</div>
      <div class="hl-level-desc">Object · Link · AgentOS 5대 제품 · RAG 비교</div>
      <span class="hl-level-cnt" style="background:rgba(34,197,94,0.15);color:#4ADE80;">15 객관식 + 5 주관식</span>
    </div>
  </div>

  <div class="hl-level" style="border-left-color:rgba(252,211,77,0.4);">
    <div class="hl-level-body">
      <div class="hl-level-name">중급 — 심화 이해 · 적용</div>
      <div class="hl-level-desc">데이터 분류 · 거버넌스 · 경쟁 기술 심층 비교</div>
      <span class="hl-level-cnt" style="background:rgba(251,191,36,0.15);color:#FCD34D;">12 객관식 + 8 주관식</span>
    </div>
  </div>

  <div class="hl-level" style="border-left-color:rgba(248,113,113,0.4);">
    <div class="hl-level-body">
      <div class="hl-level-name">고급 — 실전 설계 · 응용</div>
      <div class="hl-level-desc">아키텍처 설계 · 멀티 Agent · 영업 전략 적용</div>
      <span class="hl-level-cnt" style="background:rgba(239,68,68,0.15);color:#F87171;">10 객관식 + 10 주관식</span>
    </div>
  </div>

  <div class="hl-footer">Claude AI가 주관식 답변을 채점하고 맞춤 피드백을 제공합니다</div>
</div>
""", unsafe_allow_html=True)

    # ── Right: form panel — header HTML + Streamlit widgets as one block ───────
    with col_right:
        # White card top (title + sub)
        st.markdown("""
<div class="home-right-header">
  <div class="hr-title">퀴즈 시작하기</div>
  <div class="hr-sub">레벨을 선택하고 API 키를 입력하면 바로 시작할 수 있습니다.</div>
</div>
""", unsafe_allow_html=True)

        # White card bottom (form inputs)
        st.markdown('<div class="home-right-form">', unsafe_allow_html=True)
        level_sel = st.selectbox(
            "학습 레벨",
            ["초급", "중급", "고급"],
            key="home_level",
            help="초급: 기본 개념 | 중급: 심화 | 고급: 실전"
        )
        api_key_inp = st.text_input(
            "Claude API Key",
            type="password",
            placeholder="sk-ant-api03-...",
            help="주관식 채점에 사용됩니다. console.anthropic.com에서 발급",
            key="home_api"
        )
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("시작하기  →", type="primary", use_container_width=True):
            if not api_key_inp.strip():
                st.warning("⚠️ 주관식 채점을 위해 Claude API Key를 입력해주세요.")
            else:
                st.session_state.level = level_sel
                st.session_state.api_key = api_key_inp
                st.session_state.questions = QUIZ_DATA[level_sel].copy()
                st.session_state.current_q = 0
                st.session_state.answers = {}
                st.session_state.results = {}
                st.session_state.page = "quiz"
                st.rerun()

        st.markdown("""
<hr class="hr-divider">
<div class="hr-feature"><span class="hr-feature-dot"></span>객관식: 제출 즉시 정답 확인</div>
<div class="hr-feature"><span class="hr-feature-dot"></span>주관식: Claude AI 채점 + 상세 피드백</div>
<div class="hr-feature"><span class="hr-feature-dot"></span>결과 페이지에서 문제별 해설 제공</div>
</div>
""", unsafe_allow_html=True)


# ── Quiz Page ──────────────────────────────────────────────────────────────────
elif st.session_state.page == "quiz":
    questions = st.session_state.questions
    q_idx = st.session_state.current_q
    q = questions[q_idx]
    total = len(questions)

    # Top progress
    answered_so_far = len(st.session_state.answers)
    st.markdown(f"""
<div class="quiz-topbar">
  <span style="font-size:0.8em;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.8px">
    {st.session_state.level} 레벨
  </span>
  <span style="font-size:1em;font-weight:800;color:#028090;letter-spacing:-0.5px">
    {q_idx + 1} <span style="color:#CBD5E1;font-weight:400"> / </span> {total}
  </span>
  <span style="font-size:0.8em;color:#94A3B8;font-weight:500">
    완료 {answered_so_far}/{total}
  </span>
</div>
""", unsafe_allow_html=True)
    st.progress((q_idx) / total)

    # Question card
    type_badge = ('<span class="q-type-badge badge-mc">객관식</span>'
                  if q["type"] == "mc"
                  else '<span class="q-type-badge badge-sub">주관식</span>')

    st.markdown(f"""
<div class="q-card">
  <div class="q-meta">
    <div class="q-num-bubble">{q_idx + 1}</div>
    <span class="q-category">{q['category']}</span>
    {type_badge}
  </div>
  <div class="q-text">{q['question']}</div>
</div>
""", unsafe_allow_html=True)

    # Answer input
    current_answer = st.session_state.answers.get(q["id"], "")

    if q["type"] == "mc":
        options = q["options"]
        try:
            cur_idx = [opt[0] for opt in options].index(current_answer) if current_answer else None
        except ValueError:
            cur_idx = None

        selected = st.radio(
            "선택지:",
            options,
            index=cur_idx,
            key=f"radio_{q['id']}",
            label_visibility="collapsed",
        )
        if selected:
            st.session_state.answers[q["id"]] = selected[0]

    else:  # subjective
        st.markdown(
            '<p style="color:#64748B;font-size:0.88em;margin-bottom:6px">💬 자유롭게 서술해주세요. Claude AI가 채점 및 피드백을 제공합니다.</p>',
            unsafe_allow_html=True
        )
        text_val = st.text_area(
            "답변:",
            value=current_answer,
            height=170,
            key=f"text_{q['id']}",
            placeholder="핵심 개념, 예시, 이유 등을 포함해 설명해보세요...",
            label_visibility="collapsed",
        )
        if text_val != current_answer:
            st.session_state.answers[q["id"]] = text_val

    # Navigation
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if q_idx > 0:
            if st.button("← 이전", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()

    with col2:
        unanswered = total - len(st.session_state.answers)
        if unanswered > 0:
            st.markdown(
                f'<p class="nav-hint">미답변 {unanswered}문제 남음</p>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<p class="nav-hint" style="color:#16A34A;font-weight:600">✅ 모든 문제 답변 완료</p>',
                unsafe_allow_html=True
            )

    with col3:
        if q_idx < total - 1:
            if st.button("다음 →", type="primary", use_container_width=True):
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("📊 제출 및 채점", type="primary", use_container_width=True):
                if len(st.session_state.answers) < total:
                    st.warning(f"⚠️ 아직 {total - len(st.session_state.answers)}문제가 미답변입니다.")
                else:
                    st.session_state.page = "results"
                    st.rerun()


# ── Results Page ───────────────────────────────────────────────────────────────
elif st.session_state.page == "results":
    questions = st.session_state.questions
    answers = st.session_state.answers

    # 객관식 즉시 채점
    for q in questions:
        if q["type"] == "mc" and q["id"] not in st.session_state.results:
            user_ans = answers.get(q["id"], "")
            correct = user_ans == q["answer"]
            st.session_state.results[q["id"]] = {
                "score": 10 if correct else 0,
                "max_score": 10,
                "correct": correct,
                "explanation": q.get("explanation", ""),
            }

    # 주관식 채점 (미채점 항목만)
    sub_questions = [q for q in questions if q["type"] == "subjective"
                     and q["id"] not in st.session_state.results]

    if sub_questions:
        with st.spinner(f"🤖 Claude가 주관식 {len(sub_questions)}문제를 채점 중입니다..."):
            for q in sub_questions:
                result = evaluate_subjective_answer(
                    question=q["question"],
                    user_answer=answers.get(q["id"], ""),
                    answer_key=q["answer_key"],
                    level=st.session_state.level,
                    api_key=st.session_state.api_key,
                )
                st.session_state.results[q["id"]] = result

    # ── 결과 요약 ──────────────────────────────────────────────────────────────
    results = st.session_state.results
    total_score = sum(r.get("score", 0) for r in results.values())
    total_max = len(questions) * 10

    mc_qs = [q for q in questions if q["type"] == "mc"]
    sub_qs = [q for q in questions if q["type"] == "subjective"]
    mc_score = sum(results.get(q["id"], {}).get("score", 0) for q in mc_qs)
    sub_score = sum(results.get(q["id"], {}).get("score", 0) for q in sub_qs)

    pct = int(total_score / total_max * 100) if total_max > 0 else 0

    grade_info = {
        range(90, 101): ("🏆", "최우수", "#16A34A"),
        range(80, 90):  ("🥇", "우수",   "#2563EB"),
        range(60, 80):  ("✅", "양호",   "#CA8A04"),
        range(0, 60):   ("📚", "학습 필요", "#DC2626"),
    }
    icon, grade, gcolor = next(
        (v for k, v in grade_info.items() if pct in k),
        ("📚", "학습 필요", "#DC2626")
    )

    # Score header
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        st.markdown(f"""
<div class="score-hero">
  <div class="score-level-tag">{st.session_state.level} 레벨 결과</div>
  <div class="score-num">{total_score}</div>
  <div class="score-denom">/ {total_max} 점</div>
  <div>
    <span class="grade-pill" style="background:{gcolor}25;color:{gcolor};border:1.5px solid {gcolor}60">
      {icon} {grade}
    </span>
  </div>
  <div class="score-pct">정답률 {pct}%</div>
  <div class="stat-row">
    <div class="stat-chip">
      <span class="stat-val" style="color:#67E8F9">{mc_score}</span>
      <span class="stat-lbl">객관식 / {len(mc_qs)*10}</span>
    </div>
    <div class="stat-chip">
      <span class="stat-val" style="color:#C4B5FD">{sub_score}</span>
      <span class="stat-lbl">주관식 / {len(sub_qs)*10}</span>
    </div>
    <div class="stat-chip">
      <span class="stat-val" style="color:#86EFAC">{pct}%</span>
      <span class="stat-lbl">정답률</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── 문제별 결과 ──────────────────────────────────────────────────────────────
    st.markdown("""
<div style="margin:28px 0 16px">
  <span style="font-size:1.1em;font-weight:700;color:#1E293B">📋 문제별 상세 결과</span>
  <span style="font-size:0.82em;color:#94A3B8;margin-left:10px">클릭해서 펼쳐보기</span>
</div>
""", unsafe_allow_html=True)

    for i, q in enumerate(questions):
        r = results.get(q["id"], {})
        score = r.get("score", 0)
        max_s = r.get("max_score", 10)
        user_answer_text = answers.get(q["id"], "(미답변)")

        if q["type"] == "mc":
            correct = r.get("correct", False)
            rd_cls  = "rd-correct" if correct else "rd-wrong"
            status_icon = "✅" if correct else "❌"
            score_label = "정답" if correct else "오답"
        else:
            if score >= 8:
                rd_cls, status_icon = "rd-correct", "🏆"
                score_label = f"{score}/10"
            elif score >= 5:
                rd_cls, status_icon = "rd-partial", "📝"
                score_label = f"{score}/10"
            else:
                rd_cls, status_icon = "rd-wrong", "📚"
                score_label = f"{score}/10"

        q_preview = q["question"][:55] + ("..." if len(q["question"]) > 55 else "")

        # Build inner HTML
        inner = f"""
<div class="rd-section">
  <div class="rd-section-label">문제</div>
  <div class="rd-q-text">{q['question']}</div>
</div>
<div class="rd-section">
  <div class="rd-section-label">내 답변</div>
  <div class="rd-my-ans">{user_answer_text}</div>
</div>
"""
        if q["type"] == "mc":
            ans_letter = q["answer"]
            correct_option = next((o for o in q.get("options", []) if o.startswith(ans_letter)), ans_letter)
            inner += f"""
<div class="rd-section">
  <div class="rd-section-label">정답</div>
  <div class="fb-correct-ans">✔ {correct_option}</div>
</div>
"""
            if r.get("explanation"):
                inner += f'<div class="fb-explan">💡 <strong style="color:#475569">해설:</strong> {r["explanation"]}</div>'
        else:
            grade_txt = r.get("grade", "")
            inner += f"""
<div class="rd-section">
  <div class="rd-section-label">점수 · 평가</div>
  <div style="font-size:0.88em;font-weight:700;color:#1E293B">{score}/10점 &nbsp;·&nbsp; <span style="color:#6D28D9">{grade_txt}</span></div>
</div>
"""
            if r.get("correct_points"):
                inner += f'<div class="fb-good">✅ <strong style="color:#166534">잘 된 부분:</strong> {r["correct_points"]}</div>'
            if r.get("improvement"):
                inner += f'<div class="fb-warn">📌 <strong style="color:#92400E">보완할 부분:</strong> {r["improvement"]}</div>'
            if r.get("key_insight"):
                inner += f'<div class="fb-info">💡 <strong style="color:#1E40AF">핵심 인사이트:</strong> {r["key_insight"]}</div>'
            ak = q.get("answer_key", "")
            if ak:
                inner += f'<div class="fb-answer">📖 <strong style="color:#334155">모범 답안 기준:</strong><br>{ak}</div>'

        with st.expander(
            f"{status_icon}  문제 {i+1}  [{q['category']}]  {q_preview}  ({score_label})",
            expanded=False,
        ):
            st.markdown(
                f'<div class="rd-wrap {rd_cls}"><div class="rd-body">{inner}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:white;border-radius:12px;padding:20px 24px;border:1px solid #E2E8F0;margin-bottom:16px">
  <p style="font-size:0.9em;font-weight:600;color:#1E293B;margin:0 0 14px">다음 단계</p>
""", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        if st.button("🔄 다시 풀기", use_container_width=True):
            st.session_state.questions = QUIZ_DATA[st.session_state.level].copy()
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.results = {}
            st.session_state.page = "quiz"
            st.rerun()
    with col_r2:
        if st.button("🏠 홈으로", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.answers = {}
            st.session_state.results = {}
            st.rerun()
    with col_r3:
        levels = ["초급", "중급", "고급"]
        cur = levels.index(st.session_state.level)
        next_lvl = levels[min(cur + 1, 2)]
        if st.button(f"⬆ {next_lvl} 도전", type="primary", use_container_width=True):
            st.session_state.level = next_lvl
            st.session_state.questions = QUIZ_DATA[next_lvl].copy()
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.results = {}
            st.session_state.page = "quiz"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
