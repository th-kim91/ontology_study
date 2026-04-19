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

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #EEF0F4; }
  .main .block-container { padding-top: 2rem; max-width: 960px; }
  .stMarkdown, .stMarkdown p, .stMarkdown li,
  .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
  .stMarkdown strong, .stMarkdown em { color: #1E293B !important; }
  .stSelectbox label, .stTextInput label, .stTextArea label, .stRadio label,
  .stCheckbox label, .stNumberInput label,
  [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
  [data-testid="stWidgetLabel"] span { color: #1E293B !important; }
  .stSelectbox [data-baseweb="select"] div,
  .stSelectbox [data-baseweb="select"] span,
  .stSelectbox [data-baseweb="select"] input { color: white !important; }
  .stSelectbox [data-baseweb="select"] > div { background: #1E293B !important; border-color: #334155 !important; }
  [data-baseweb="popover"] li, [data-baseweb="menu"] li,
  [data-baseweb="option"] { color: #1E293B !important; background: white !important; }
  [data-baseweb="option"]:hover { background: #F0FDFA !important; }
  .stTextInput input, .stTextArea textarea, .stNumberInput input { color: #1E293B !important; }
  .main p, .main li, .main span,
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] span,
  [data-testid="stMarkdownContainer"] li { color: #1E293B !important; }
  .stProgress > div > div > div > div {
    background: linear-gradient(90deg, #028090, #0EA5E9) !important;
    border-radius: 99px;
  }
  section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #09162A 0%, #1B2A4A 60%, #022A33 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
    min-width: 260px !important; max-width: 300px !important; width: 270px !important;
  }
  section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
  section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
  section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
  section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09);
    color: #CBD5E1 !important; border-radius: 8px; font-size: 0.8em;
    text-align: left; padding: 7px 10px; transition: all 0.15s;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(2,128,144,0.2); border-color: rgba(2,128,144,0.5); color: #E2E8F0 !important;
  }
  .home-left {
    background: linear-gradient(155deg, #0A1628 0%, #162039 40%, #0C2A34 100%);
    border-radius: 20px; padding: 48px 44px 44px;
    position: relative; overflow: hidden;
    box-shadow: 0 24px 64px rgba(9,22,42,0.28);
  }
  .home-left::before {
    content: ''; position: absolute; top: -100px; right: -100px;
    width: 380px; height: 380px;
    background: radial-gradient(circle, rgba(2,128,144,0.18) 0%, transparent 65%);
    border-radius: 50%; pointer-events: none;
  }
  .home-left::after {
    content: ''; position: absolute; bottom: -60px; left: -40px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(14,165,233,0.08) 0%, transparent 65%);
    border-radius: 50%; pointer-events: none;
  }
  .hl-eyebrow {
    font-size: 10px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #028090 !important;
    margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
  }
  .hl-eyebrow::before { content: ''; display: inline-block; width: 20px; height: 2px; background: #028090; border-radius: 2px; }
  .hl-title { font-size: 2.4em; font-weight: 900; line-height: 1.15; color: white !important; margin: 0 0 14px; letter-spacing: -0.5px; }
  .hl-title span { color: #67E8F9 !important; }
  .hl-sub { font-size: 0.9em; color: #7B96AA !important; line-height: 1.7; margin-bottom: 32px; }
  .hl-divider { border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 0 0 24px; }
  .hl-level { display: flex; align-items: flex-start; margin-bottom: 18px; padding-left: 14px; border-left: 2px solid rgba(255,255,255,0.1); }
  .hl-level-body { flex: 1; }
  .hl-level-name { font-size: 0.88em; font-weight: 700; color: #E2E8F0 !important; margin-bottom: 3px; }
  .hl-level-desc { font-size: 0.78em; color: #7B96AA !important; line-height: 1.5; margin-bottom: 5px; }
  .hl-level-cnt { font-size: 0.73em; font-weight: 700; padding: 3px 10px; border-radius: 99px; display: inline-block; }
  .hl-footer { margin-top: 28px; font-size: 0.75em; color: #3A5468 !important; display: flex; align-items: center; gap: 8px; }
  .hl-footer::before { content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #028090; flex-shrink: 0; }
  .home-right-header { padding: 36px 36px 0; background: white; border-radius: 20px 20px 0 0; border: 1px solid #E2E8F0; border-bottom: none; margin-bottom: 0; position: relative; z-index: 2; }
  .home-right-form { padding: 20px 36px 32px; background: white; border-radius: 0 0 20px 20px; border: 1px solid #E2E8F0; border-top: none; margin-top: -2px; position: relative; z-index: 1; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
  [data-testid="stHorizontalBlock"] { align-items: stretch !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { display: flex !important; flex-direction: column !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child { justify-content: stretch !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > [data-testid="stVerticalBlockBorderWrapper"],
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > [data-testid="stVerticalBlock"] { flex: 1 !important; display: flex !important; flex-direction: column !important; }
  .hr-title { font-size: 1.1em; font-weight: 800; color: #0F172A !important; margin: 0 0 5px; }
  .hr-sub { font-size: 0.81em; color: #94A3B8 !important; margin: 0 0 22px; line-height: 1.5; }
  .hr-divider { display: none; }
  .hr-feature { display: flex; align-items: center; gap: 10px; font-size: 0.8em; color: #64748B !important; margin-bottom: 8px; }
  .hr-feature-dot { width: 5px; height: 5px; border-radius: 50%; background: #028090; flex-shrink: 0; }
  .q-card { background: white; border-radius: 16px; padding: 28px 32px 24px; margin-bottom: 18px; box-shadow: 0 2px 14px rgba(0,0,0,0.06); border-top: 3px solid #028090; }
  .q-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
  .q-num-bubble { width: 30px; height: 30px; border-radius: 50%; background: linear-gradient(135deg, #028090, #0369A1); color: white !important; font-size: 12px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .q-category { background: #F0FDFA; color: #0F766E !important; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 99px; border: 1px solid #CCFBF1; }
  .q-type-badge { font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 99px; margin-left: auto; }
  .badge-mc  { background: #FFF7ED; color: #C2410C !important; border: 1px solid #FED7AA; }
  .badge-sub { background: #F5F3FF; color: #6D28D9 !important; border: 1px solid #DDD6FE; }
  .q-text { font-size: 1.08em; font-weight: 600; color: #0F172A !important; line-height: 1.65; }
  div[role="radiogroup"] label, div[role="radiogroup"] label p, div[role="radiogroup"] label span,
  div[data-baseweb="radio"] label, div[data-baseweb="radio"] label p, div[data-baseweb="radio"] label span,
  .stRadio label, .stRadio label p, .stRadio span,
  [data-testid="stMarkdownContainer"] p { color: #1E293B !important; }
  .stRadio > div { gap: 8px; }
  div[data-baseweb="radio"] { background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 11px; padding: 13px 17px; transition: all 0.15s; }
  div[data-baseweb="radio"]:hover { border-color: #028090; background: #F0FDFA; }
  div[data-baseweb="radio"][aria-checked="true"] { background: #E0F7FA !important; border-color: #028090 !important; }
  div[data-baseweb="radio"][aria-checked="true"] label,
  div[data-baseweb="radio"][aria-checked="true"] label p,
  div[data-baseweb="radio"][aria-checked="true"] label span { color: #0C4A5A !important; }
  .stTextArea textarea { border-radius: 11px; border: 1.5px solid #E2E8F0; font-size: 0.95em; color: #1E293B !important; background: #FAFAFA; padding: 12px 16px; transition: border-color 0.15s, box-shadow 0.15s; }
  .stTextArea textarea:focus { border-color: #028090; box-shadow: 0 0 0 3px rgba(2,128,144,0.1); }
  .stButton > button { border-radius: 9px; font-weight: 600; font-size: 0.9em; transition: all 0.15s; background: #334155 !important; color: white !important; border: 1px solid #475569 !important; }
  .stButton > button p, .stButton > button span, .stButton > button div { color: white !important; }
  .stButton > button:hover { background: #1E293B !important; border-color: #64748B !important; }
  .stButton > button[kind="primary"] { background: linear-gradient(135deg, #028090, #0369A1) !important; border: none !important; color: white !important; box-shadow: 0 2px 8px rgba(2,128,144,0.25); }
  .stButton > button[kind="primary"]:hover { background: linear-gradient(135deg, #026070, #025A8A) !important; box-shadow: 0 6px 18px rgba(2,128,144,0.35); transform: translateY(-1px); }
  .score-hero { text-align: center; background: linear-gradient(150deg, #09162A 0%, #1B2A4A 100%); border-radius: 22px; padding: 44px 28px 36px; box-shadow: 0 16px 48px rgba(9,22,42,0.22); margin-bottom: 24px; position: relative; overflow: hidden; }
  .score-hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 220px; height: 220px; background: radial-gradient(circle, rgba(2,128,144,0.2) 0%, transparent 65%); border-radius: 50%; }
  .score-level-tag { font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #4B6380 !important; margin-bottom: 12px; }
  .score-num { font-size: 5.5em; font-weight: 900; background: linear-gradient(135deg, #FFFFFF, #94D5DB); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; letter-spacing: -3px; }
  .score-denom { font-size: 1.1em; color: #475569 !important; font-weight: 500; margin-top: 4px; }
  .grade-pill { display: inline-block; padding: 8px 22px; border-radius: 99px; font-size: 0.88em; font-weight: 700; margin-top: 16px; }
  .score-pct { font-size: 0.88em; color: #64748B !important; margin-top: 10px; }
  .stat-row { display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap; }
  .stat-chip { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px 22px; text-align: center; min-width: 100px; }
  .stat-val { font-size: 1.5em; font-weight: 900; display: block; }
  .stat-lbl { font-size: 0.72em; color: #4B6380 !important; font-weight: 500; margin-top: 2px; }
  .rd-wrap { background: white; border-radius: 14px; margin-bottom: 12px; overflow: hidden; border: 1px solid #E2E8F0; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .rd-header { display: flex; align-items: center; gap: 12px; padding: 14px 20px; }
  .rd-correct .rd-header { background: #F0FDF4; border-left: 4px solid #16A34A; }
  .rd-wrong   .rd-header { background: #FFF7ED; border-left: 4px solid #EA580C; }
  .rd-partial .rd-header { background: #FEFCE8; border-left: 4px solid #CA8A04; }
  .rd-icon { font-size: 1.15em; flex-shrink: 0; }
  .rd-title { font-size: 0.88em; font-weight: 600; color: #1E293B !important; flex: 1; }
  .rd-score-tag { font-size: 0.78em; font-weight: 700; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
  .rd-correct .rd-score-tag { background: #DCFCE7; color: #15803D !important; }
  .rd-wrong   .rd-score-tag { background: #FFEDD5; color: #C2410C !important; }
  .rd-partial .rd-score-tag { background: #FEF9C3; color: #A16207 !important; }
  .rd-body { padding: 0 20px 18px 20px; }
  .rd-section { margin-top: 14px; }
  .rd-section-label { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #94A3B8 !important; margin-bottom: 6px; }
  .rd-q-text { font-size: 0.9em; font-weight: 600; color: #1E293B !important; line-height: 1.55; }
  .rd-my-ans { font-size: 0.87em; color: #475569 !important; line-height: 1.55; }
  .fb-good { background: #F0FDF4; border-left: 3px solid #22C55E; border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px; font-size: 0.85em; color: #166534 !important; line-height: 1.6; }
  .fb-warn { background: #FFFBEB; border-left: 3px solid #F59E0B; border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px; font-size: 0.85em; color: #92400E !important; line-height: 1.6; }
  .fb-info { background: #EFF6FF; border-left: 3px solid #3B82F6; border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px; font-size: 0.85em; color: #1E40AF !important; line-height: 1.6; }
  .fb-answer { background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 10px; padding: 12px 16px; margin-top: 10px; font-size: 0.83em; color: #475569 !important; line-height: 1.65; }
  .fb-correct-ans { background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 8px 14px; margin-top: 8px; font-size: 0.85em; color: #166534 !important; font-weight: 600; }
  .fb-explan { background: #F8FAFC; border-left: 3px solid #94A3B8; border-radius: 0 10px 10px 0; padding: 10px 14px; margin-top: 10px; font-size: 0.85em; color: #475569 !important; line-height: 1.6; }
  .streamlit-expanderHeader { font-size: 0.9em !important; color: #1E293B !important; }
  .streamlit-expanderHeader p { color: #1E293B !important; }
  .streamlit-expanderContent { background: white !important; }
  .streamlit-expanderContent p, .streamlit-expanderContent span, .streamlit-expanderContent li { color: #334155 !important; }
  div[data-testid="stAlert"] { border-radius: 10px; }
  div[data-testid="stAlert"] p, div[data-testid="stAlert"] span { color: #1E293B !important; }
  .nav-hint { font-size: 12px; color: #94A3B8; text-align: center; }
  .section-divider { border: none; border-top: 1px solid #E2E8F0; margin: 24px 0; }
  .quiz-topbar { background: white; border-radius: 14px; padding: 14px 22px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #E8ECF0; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
</style>
""", unsafe_allow_html=True)

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
1. Semantic Web 정통 방식 (RDF/OWL/SPARQL): 논리적으로 가장 엄밀, 자동 추론 강함. 단 실무 운영 무겁고 복잡.
2. GraphDB 방식 (Neo4j 등): 저장 자체가 노드/엣지. 관계 탐색 강함. 단 기존 RDB 데이터와 동기화·통합 비용 큼
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

# ── QUIZ DATA ──────────────────────────────────────────────────────────────────
QUIZ_DATA = {
    "기본": {
        "① 회사 & 제품 개요": [
            {"id": "c01", "type": "mc", "category": "패러다임",
             "question": "AgentOS가 없을 때와 있을 때, 기업의 데이터 활용 방식에서 가장 큰 차이는?",
             "options": ["A) 데이터 저장 비용이 줄어든다", "B) 더 예쁜 대시보드를 자동으로 만들 수 있다", "C) 사람이 데이터를 보고 판단·실행하던 방식에서, AI Agent가 스스로 판단하고 실행하는 방식으로 전환된다", "D) 데이터 처리 속도가 빨라진다"],
             "answer": "C",
             "explanation": "이것이 AgentOS의 본질입니다. 없을 때: 데이터는 쌓여 있지만 사람이 직접 열어보고 판단하고 실행 지시. 있을 때: Agent가 온톨로지로 상황 파악 → 지식사전 규칙 적용 → 스스로 판단·실행. 데이터가 '보는 것'에서 '하는 것'으로 바뀝니다."},
            {"id": "c02", "type": "mc", "category": "회사 개요",
             "question": "인핸스(Enhans)를 가장 정확하게 설명한 것은?",
             "options": ["A) 클라우드 인프라 제공 회사", "B) AgentOS 기반 Vertical AI Agent 플랫폼 회사", "C) 데이터 시각화 전문 회사", "D) ERP 소프트웨어 개발사"],
             "answer": "B",
             "explanation": "인핸스는 AgentOS 기반 Vertical AI Agent 플랫폼 회사로, 50+ 국가, 1,000+ 마켓플레이스, 20+ 글로벌 소비자 브랜드를 서비스 중입니다."},
            {"id": "c03", "type": "mc", "category": "AgentOS 5대 제품",
             "question": "DB, API, 파일 등 200개 이상의 커넥터로 데이터를 연결·정규화해 온톨로지 DB에 적재하는 AgentOS 제품은?",
             "options": ["A) Ontology Manager", "B) Pipeline Builder", "C) Workflow Builder", "D) Dashboard Generation"],
             "answer": "B",
             "explanation": "Pipeline Builder는 다양한 데이터 소스를 연결·정규화하고 온톨로지 DB로 적재합니다. 인핸스가 기존 인프라를 교체하지 않아도 되는 이유가 바로 이 커넥터 기반 연결 방식입니다."},
            {"id": "c04", "type": "mc", "category": "AgentOS 5대 제품",
             "question": "데이터에 의미(Semantic)와 관계(Relational)를 부여해 AI가 구조·맥락 기반으로 이해하도록 구조화하는 AgentOS 제품은?",
             "options": ["A) Pipeline Builder", "B) CUA", "C) Ontology Manager", "D) Workflow Builder"],
             "answer": "C",
             "explanation": "Ontology Manager는 데이터에 비즈니스 의미와 관계를 정의해 AI가 단순 숫자가 아닌 개념과 맥락으로 이해하도록 구조화합니다."},
            {"id": "c05", "type": "mc", "category": "AgentOS 5대 제품",
             "question": "멀티 에이전트를 생성하고 실제 업무 흐름대로 워크플로우를 구성하는 AgentOS 제품은?",
             "options": ["A) Pipeline Builder", "B) Dashboard Generation", "C) Workflow Builder", "D) CUA"],
             "answer": "C",
             "explanation": "Workflow Builder는 여러 에이전트를 생성하고 실제 업무 흐름대로 워크플로우를 구성하는 제품입니다."},
            {"id": "c06", "type": "mc", "category": "AgentOS 5대 제품",
             "question": "온톨로지 기반으로 단시간에 재사용 가능한 대시보드 뷰를 생성하는 AgentOS 제품은?",
             "options": ["A) Workflow Builder", "B) Pipeline Builder", "C) Ontology Manager", "D) Dashboard Generation"],
             "answer": "D",
             "explanation": "Dashboard Generation은 온톨로지 기반으로 원하는 형태의 대시보드를 빠르게 생성합니다."},
            {"id": "c07", "type": "mc", "category": "AgentOS 5대 제품",
             "question": "화면을 직접 보고 이해하고 판단해 실제 액션을 실행하는 AgentOS 제품은?",
             "options": ["A) Ontology Manager", "B) Pipeline Builder", "C) CUA (ACT-2)", "D) Dashboard Generation"],
             "answer": "C",
             "explanation": "CUA(Computer Use Agent, ACT-2)는 화면을 보고 이해하고 판단해 실제 액션을 실행합니다."},
            {"id": "c08", "type": "mc", "category": "Agent 역할",
             "question": "AgentOS에서 Agent의 핵심 역할로 가장 적절한 것은?",
             "options": ["A) 데이터를 저장하고 관리한다", "B) 데이터를 차트로 시각화한다", "C) 온톨로지와 지식사전을 기반으로 상황을 판단하고 실제 액션을 실행한다", "D) SQL 쿼리를 자동으로 생성한다"],
             "answer": "C",
             "explanation": "AgentOS에서 Agent는 단순히 데이터를 저장하거나 보여주는 것이 아닙니다. Object/Link 구조(온톨로지)로 맥락을 이해하고, 지식사전의 비즈니스 규칙을 참고해 '이 상황에서 무엇을 해야 하는가'를 판단하고 실제 액션을 실행하는 것이 핵심입니다."},
            {"id": "c09", "type": "subjective", "category": "인핸스 포지셔닝",
             "question": "인핸스가 '데이터 사이언티스트(DS)를 대체하는 것이 아니다'라고 설명하는 이유는 무엇인가요?",
             "answer_key": "인핸스는 반복적이고 자동화 가능한 과정(데이터 연결, 분석 실행, 리포트 생성)을 처리하는 플랫폼. 통계 모델 타당성 검토, 분석 결과의 통계적 유의성 판단, 비즈니스 의사결정은 여전히 DS와 현업 팀이 담당. DS가 더 고차원 업무에 집중하도록 돕는 파트너 역할. 대체가 아닌 협업 구조."},
            {"id": "c10", "type": "subjective", "category": "AgentOS 5대 제품",
             "question": "AgentOS의 5대 제품을 각각 한 줄씩 설명해보세요.",
             "answer_key": "Pipeline Builder: DB/API/파일 등 200+ 커넥터로 데이터 연결·정규화·온톨로지 DB 적재. Ontology Manager: 데이터에 의미와 관계를 부여해 AI가 구조·맥락으로 이해하도록 구조화. Workflow Builder: 멀티 에이전트 생성 + 업무 흐름대로 워크플로우 구성. Dashboard Generation: 온톨로지 기반으로 재사용 가능한 대시보드 빠르게 생성. CUA(ACT-2): 화면을 보고 이해하고 판단해 실제 액션 실행."},
        ],

        "② 온톨로지 기초": [
            {"id": "d01", "type": "mc", "category": "온톨로지 3요소",
             "question": "AgentOS에서 '업무에서 판단의 대상이 되는 개념'을 나타내는 기본 단위는?",
             "options": ["A) Table", "B) Object", "C) Document", "D) Row"],
             "answer": "B",
             "explanation": "Object는 단순한 데이터 테이블이 아니라, 업무에서 판단의 대상이 되는 개념 단위입니다. 테이블이 '데이터 저장'이 목적이라면, Object는 '이 개념으로 무엇을 판단할 것인가'를 정의합니다. 예: 설비, 고객사, 계약, 생산배치"},
            {"id": "d02", "type": "mc", "category": "온톨로지 3요소",
             "question": "Object를 구성하는 특성·속성을 나타내는 요소는?",
             "options": ["A) Link", "B) Property/Attribute", "C) Pipeline", "D) Schema"],
             "answer": "B",
             "explanation": "Property/Attribute는 Object를 구성하는 특성입니다. 예: 설비.재고량, 고객사.계약만료일, 계약.금액."},
            {"id": "d03", "type": "mc", "category": "온톨로지 3요소",
             "question": "Object들 사이의 연결 관계를 정의하는 요소는?",
             "options": ["A) Attribute", "B) Pipeline", "C) Link", "D) Schema"],
             "answer": "C",
             "explanation": "Link(Relation)는 Object 또는 Property 간의 연결 관계를 정의합니다. 예: 고객사→계약, 설비→공정(runs_on)."},
            {"id": "d04", "type": "mc", "category": "온톨로지 3요소",
             "question": "온톨로지의 3가지 핵심 요소가 올바르게 나열된 것은?",
             "options": ["A) Table, Column, Row", "B) Object, Property/Attribute, Link", "C) Pipeline, Manager, Builder", "D) Data, Model, View"],
             "answer": "B",
             "explanation": "온톨로지의 3요소: Object(판단 대상 개념), Property/Attribute(Object의 특성), Link(Object 간 관계). 이 세 요소로 AI가 이해할 수 있는 구조와 맥락이 만들어집니다."},
            {"id": "d05", "type": "mc", "category": "온톨로지 구축",
             "question": "온톨로지 구축 첫 시작(Cold Start) 시 Object 설계를 주로 누가 해야 하나요?",
             "options": ["A) AI가 전부 자동으로 설계한다", "B) 비즈니스 도메인 지식이 있는 사람이 설계한다", "C) 외부 컨설턴트만 할 수 있다", "D) 누가 해도 상관없다"],
             "answer": "B",
             "explanation": "AI는 우리 비즈니스에서 어떤 개념이 중요한지 알 수 없습니다. Object 설계는 비즈니스를 아는 사람이 정의해야 합니다. AI 80% 초안 → 현업 20% 검수 방식으로 효율화합니다."},
            {"id": "d06", "type": "mc", "category": "온톨로지 가치",
             "question": "온톨로지를 도입하면 '베테랑 직원 퇴사'에도 업무 지식이 유지되는 이유는?",
             "options": ["A) 영상으로 모든 업무를 녹화하기 때문", "B) 노하우와 판단 기준이 Object·지식사전에 명시적으로 저장되기 때문", "C) 자동으로 인수인계 문서가 생성되기 때문", "D) 재고용 계약이 있기 때문"],
             "answer": "B",
             "explanation": "온톨로지 방식에서는 판단 기준, 업무 규칙, 관계 정의가 시스템에 명시적으로 저장됩니다. 담당자가 바뀌어도 모든 맥락이 시스템에 남습니다."},
            {"id": "d07", "type": "mc", "category": "온톨로지 가치",
             "question": "온톨로지(Object + Link + Attribute)가 갖춰졌을 때 AI Agent가 할 수 있게 되는 것은?",
             "options": ["A) 더 빠른 SQL 쿼리 실행", "B) 예쁜 UI 자동 생성", "C) 데이터의 구조와 맥락을 이해하고 '무엇을 판단해야 하는가'를 스스로 파악", "D) 텍스트 번역"],
             "answer": "C",
             "explanation": "온톨로지가 없으면 AI는 컬럼 이름만 보고 의미를 추측해야 합니다. 온톨로지가 갖춰지면 AI가 데이터 구조와 관계를 이해하고, 어떤 데이터를 조합해 무엇을 판단해야 하는지를 파악할 수 있게 됩니다."},
            {"id": "d08", "type": "mc", "category": "온톨로지 3요소",
             "question": "Object가 단순한 데이터베이스 테이블과 다른 핵심 차이는?",
             "options": ["A) 저장 용량이 더 크다", "B) 열(Column) 수가 더 많다", "C) 판단의 대상이 되는 '개념'을 정의하고, 다른 Object와 Link로 관계가 정의되며 Agent와 연결된다", "D) 암호화가 자동으로 된다"],
             "answer": "C",
             "explanation": "테이블은 '데이터 저장'이 목적이지만, Object는 '이 개념으로 무엇을 판단할 것인가'를 정의합니다. Object는 Link로 관계가 정의되고 Agent의 실행 대상이 됩니다."},
            {"id": "d09", "type": "subjective", "category": "온톨로지 3요소",
             "question": "Object와 RDB 테이블의 공통점과 차이점을 설명해보세요.",
             "answer_key": "공통점: 둘 다 데이터를 구조화된 형태로 담는 단위. 차이점: RDB 테이블은 데이터 저장이 목적이지만, Object는 '업무에서 판단의 대상이 되는 개념'을 정의하는 것이 목적. Object는 다른 Object와 Link로 관계가 정의되고, 지식사전·Agent와 연결되어 판단·실행까지 이어짐."},
            {"id": "d10", "type": "subjective", "category": "온톨로지 가치",
             "question": "'데이터에 의미를 부여한다'는 것이 무슨 뜻인지 구체적인 예시와 함께 설명해보세요.",
             "answer_key": "단순히 price_a, price_b, final_price 컬럼이 있을 때 AI는 어느 게 '최종 청구 금액'인지 모름. 의미를 부여한다는 것은 '이 필드는 최종 청구 금액', '저 필드는 제조 원가'라고 시스템에 명확히 정의하는 것. 이렇게 되면 AI가 추측 없이 정확하게 원하는 데이터를 찾을 수 있음."},
        ],

        "③ 데이터 연결 & 인프라": [
            {"id": "e01", "type": "mc", "category": "인프라 기초",
             "question": "고객이 'AgentOS 도입하려면 기존 ERP·CRM 시스템을 전부 교체해야 하나요?'라고 물었을 때 올바른 답변은?",
             "options": ["A) 네, 기존 시스템을 모두 AgentOS로 교체해야 합니다", "B) 아니요, 기존 시스템은 그대로 유지하고 위에 온톨로지 레이어만 추가합니다", "C) 데이터베이스만 교체하면 됩니다", "D) 클라우드 전환 후 도입 가능합니다"],
             "answer": "B",
             "explanation": "인핸스의 핵심 가치 중 하나입니다. 기존 ERP, CRM, Data Warehouse 등을 교체하지 않고, 위에 온톨로지 의미 레이어만 추가합니다. 기존 데이터 자산을 그대로 활용하면서 AI 활용성을 높입니다."},
            {"id": "e02", "type": "mc", "category": "인프라 기초",
             "question": "Pipeline Builder가 데이터를 연결·정규화한 후 최종적으로 어디에 적재하나요?",
             "options": ["A) 클라우드 스토리지", "B) 온톨로지 DB", "C) 벡터 데이터베이스", "D) 엑셀 파일"],
             "answer": "B",
             "explanation": "Pipeline Builder는 200개 이상의 커넥터로 다양한 데이터 소스를 연결·정규화한 후 온톨로지 DB에 적재합니다. 이 데이터가 Ontology Manager를 통해 의미가 부여되고 Agent가 활용하게 됩니다."},
            {"id": "e03", "type": "mc", "category": "인프라 기초",
             "question": "인핸스의 '온톨로지 레이어'가 하는 역할로 가장 정확한 것은?",
             "options": ["A) 기존 데이터를 삭제하고 새 형식으로 저장한다", "B) 기존 데이터 위에 의미(Semantic)와 관계(Relational) 구조를 추가해 AI가 이해하고 실행할 수 있게 한다", "C) 데이터를 압축해 저장 비용을 낮춘다", "D) SQL을 자동으로 최적화한다"],
             "answer": "B",
             "explanation": "온톨로지 레이어는 기존 데이터를 건드리지 않고, 그 위에 의미와 관계 구조를 추가합니다. 이를 통해 AI가 단순 숫자가 아닌 '고객사', '계약', '재고'의 개념과 관계로 데이터를 이해하고 실행할 수 있게 됩니다."},
            {"id": "e04", "type": "mc", "category": "데이터 분류",
             "question": "비정형 데이터를 Object Attribute로 저장할지 지식 사전에 넣을지 결정하는 기준은?",
             "options": ["A) 파일 크기", "B) 자주 꺼내 쓰는 구체적 값이면 Object Attribute, 문맥·뉘앙스가 중요하면 지식 사전", "C) 데이터 업데이트 빈도", "D) 원본 파일 형식(PDF/Excel)"],
             "answer": "B",
             "explanation": "계약 만료일·고객명처럼 자주 꺼내 쓰는 구체적 값은 Object Attribute로, 특약 조건·협상 맥락처럼 전체 문장의 맥락을 이해해야 하는 내용은 지식 사전에 저장합니다."},
            {"id": "e05", "type": "mc", "category": "데이터 분류",
             "question": "계약서에서 '특약 조건(예: 조기 해지 시 위약금 20% 면제)'은 어디에 저장해야 하나요?",
             "options": ["A) Object의 Attribute", "B) 지식 사전", "C) 별도 관계형 테이블", "D) 캐시 메모리"],
             "answer": "B",
             "explanation": "특약 조건처럼 전체 문장의 맥락·뉘앙스를 이해해야 의미 있는 내용은 지식 사전에 저장합니다. 계약 만료일, 계약 금액처럼 구체적 값은 Object Attribute에 저장합니다. 하나의 계약서에서 두 방식 모두 사용됩니다."},
            {"id": "e06", "type": "mc", "category": "인프라 기초",
             "question": "온톨로지 구축 후 데이터 소스 형식이 변경되었을 때 어떻게 처리되나요?",
             "options": ["A) 전체 Object 설계를 처음부터 다시 해야 한다", "B) Object의 개념 설계는 유지하고, 새 형식에서 값이 어디 있는지 연결 부분만 수정한다", "C) 새 시스템으로 교체해야 한다", "D) 변경된 데이터는 사용할 수 없다"],
             "answer": "B",
             "explanation": "엑셀 양식이 바뀌어도 '고객명', '금액'이라는 개념 자체는 변하지 않습니다. Object의 개념 설계는 그대로 유지하고, 새 형식에서 그 값이 어디 있는지 연결 부분만 수정합니다."},
            {"id": "e07", "type": "mc", "category": "온톨로지 구축",
             "question": "온톨로지 Cold Start에서 'AI 80% 초안 → 현업 20% 검수' 방식을 사용하는 이유는?",
             "options": ["A) AI가 혼자 완성할 수 없어서", "B) 빠른 시작과 비즈니스 도메인 정확성을 동시에 달성하기 위해", "C) 법규 요건 때문에", "D) 비용을 절감하기 위해서만"],
             "answer": "B",
             "explanation": "AI가 데이터 구조를 분석해 80% 초안을 빠르게 만들고, 현업 담당자가 비즈니스 맥락(어떤 개념이 중요한가, 어떤 관계가 맞는가)을 반영해 20%를 수정·검수합니다. 처음부터 백지에서 설계하는 것보다 훨씬 빠르고 정확합니다."},
            {"id": "e08", "type": "mc", "category": "Agent 실행",
             "question": "인핸스 RDB 기반 Semantic Layer에서 Agent가 질문에 답하는 흐름은?",
             "options": ["A) 문서 검색 → 요약 → 출력", "B) 온톨로지 참고 → SQL 생성 → 실행 → LLM 자연어 요약", "C) 코드 실행 → 결과 캐시 → 출력", "D) API 호출 → 데이터 변환 → 출력"],
             "answer": "B",
             "explanation": "인핸스의 질의 처리 흐름: 온톨로지(Object/Attribute 의미 정의)를 참고하여 정확한 SQL 생성 → SQL 실행으로 정확한 수치 추출 → LLM이 그 결과를 자연어로 설명. 이 역할 분리로 수치 정확도가 높아지고 할루시네이션이 줄어듭니다."},
            {"id": "e09", "type": "subjective", "category": "인프라 기초",
             "question": "인핸스가 기존 인프라를 교체하지 않고 '위에 레이어를 얹는' 방식을 선택한 이유는 무엇인가요?",
             "answer_key": "기업은 이미 수년간 구축한 데이터 자산(DWH, Data Lake, ERP 등)이 있음. 이를 교체하면 비용·시간·리스크가 엄청남. 인핸스는 기존 SQL/DWH 생태계를 그대로 유지하면서 온톨로지 레이어만 추가해 빠른 도입, 낮은 리스크, 기존 자산 활용 모두를 실현함."},
            {"id": "e10", "type": "subjective", "category": "데이터 분류",
             "question": "하나의 계약서 문서에서 어떤 정보는 Object Attribute로, 어떤 정보는 지식 사전으로 분류할지 구체적인 예시를 들어 설명해보세요.",
             "answer_key": "Object Attribute: 계약만료일, 고객명, 담당자명, 계약금액 — 자주 꺼내 쓰고 구체적인 값이 있음. 지식 사전: 특약 조건, 위약금 면제 조건, 협상 맥락, 계약 배경 설명 — 전체 문장의 맥락과 뉘앙스를 이해해야 의미 있는 내용. 하나의 계약서에서 두 방식 모두 사용됨."},
        ],

        "④ AgentOS vs 기존 기술": [
            {"id": "f01", "type": "mc", "category": "경쟁 기술 비교",
             "question": "RAG 방식의 가장 큰 한계는 무엇인가요?",
             "options": ["A) 처리 속도가 너무 느림", "B) 텍스트 검색은 잘 하지만 구조·관계·맥락 기반 판단과 실행 불가", "C) 비용이 너무 높음", "D) 영어 문서만 처리 가능"],
             "answer": "B",
             "explanation": "RAG는 문서 검색과 Q&A에서 뛰어나지만, 여러 데이터를 엮어 일관된 구조 기반 판단을 내리거나 실제 액션을 실행하는 데는 한계가 있습니다. 인핸스는 RAG를 '규칙 조회'에만 한정하고, 판단·실행은 온톨로지가 담당하는 역할 분리 방식으로 이 문제를 해결합니다."},
            {"id": "f02", "type": "mc", "category": "경쟁 기술 비교",
             "question": "Text-to-SQL의 핵심 문제점은 무엇인가요?",
             "options": ["A) 처리 속도가 느리다", "B) 비슷한 컬럼이 여러 개 있을 때 AI가 의미를 추측해 잘못된 컬럼을 선택한다", "C) 한국어를 지원하지 않는다", "D) 클라우드에서만 동작한다"],
             "answer": "B",
             "explanation": "AI가 데이터베이스 스키마만 보고 컬럼의 의미를 추측해야 하므로, 비슷한 컬럼이 여러 개일 때(예: price_a, price_b, final_price) 잘못된 컬럼을 선택해 오류가 발생합니다."},
            {"id": "f03", "type": "mc", "category": "경쟁 기술 비교",
             "question": "GraphDB(Neo4j 등)가 기업 기존 인프라에 도입하기 어려운 근본적 이유는?",
             "options": ["A) 라이선스 비용이 너무 비싸서", "B) 저장 방식 자체가 노드/엣지 구조라 기존 RDB 테이블과 달라 전체 데이터 마이그레이션이 필요하기 때문", "C) 사용자 인터페이스가 복잡해서", "D) 클라우드를 지원하지 않아서"],
             "answer": "B",
             "explanation": "GraphDB는 데이터 저장 방식 자체가 노드/엣지입니다. 기업의 기존 데이터는 대부분 관계형 테이블(RDB) 구조이므로, GraphDB로 이전하려면 전체 데이터를 마이그레이션해야 하고 동기화·비용·권한·성능 문제가 발생합니다."},
            {"id": "f04", "type": "mc", "category": "지식 사전",
             "question": "지식 사전(Knowledge Dictionary)의 역할을 가장 정확하게 표현한 것은?",
             "options": ["A) 자연어로 된 문서를 저장하는 창고", "B) 비즈니스 규칙과 판단 기준을 관리하는 규칙 엔진으로, Agent가 이를 기반으로 의사결정한다", "C) 직원 교육 자료를 보관하는 데이터베이스", "D) AI 모델을 학습시키는 데이터셋"],
             "answer": "B",
             "explanation": "지식 사전은 단순 자연어 저장소가 아닙니다. '장기 체화 재고 = 마지막 출고 180일 초과 + 평가액 500만원 이상', '30% 이상 할인 시 영업 본부장 사전 서면 승인 필요'처럼 비즈니스 규칙과 판단 기준을 관리하는 규칙 엔진입니다. Agent는 이 규칙을 기반으로 판단하고 실행합니다."},
            {"id": "f05", "type": "mc", "category": "경쟁 기술 비교",
             "question": "Databricks/Snowflake의 Semantic Layer와 인핸스의 근본적인 목적 차이는?",
             "options": ["A) 가격 차이", "B) 사람이 보는 보고서 자동화 vs AI Agent가 스스로 이해하고 판단·실행하는 구조", "C) 처리 속도 차이", "D) 지원하는 데이터 형식 차이"],
             "answer": "B",
             "explanation": "Databricks/Snowflake Semantic Layer는 경영진을 위한 보고서 자동화 도구로, 결국 사람이 보고 판단합니다. 인핸스는 AI Agent가 스스로 이해하고 판단하고 실행하기 위한 레이어입니다. 목적 자체가 다릅니다."},
            {"id": "f06", "type": "mc", "category": "경쟁 기술 비교",
             "question": "OWL/RDF(표준 온톨로지)와 인핸스 방식의 가장 큰 실무 차이는?",
             "options": ["A) 비용 차이", "B) 학문적 완성도·자동 추론 강함(OWL) vs 빠른 실무 적용성과 AI Agent 직접 연결(인핸스)", "C) 지원 언어 차이", "D) 서버 사양 차이"],
             "answer": "B",
             "explanation": "OWL/RDF는 논리적으로 완벽하고 자동 추론이 강하지만, 배우기 어렵고 AI Agent와 연결하려면 별도 작업이 필요합니다. 인핸스는 Object/Link/지식사전 3가지 개념만으로 빠르게 구축하고 바로 Agent와 연결됩니다."},
            {"id": "f07", "type": "mc", "category": "지식 사전",
             "question": "인핸스는 지식사전에도 RAG를 쓰는데, 기존 RAG의 한계가 그대로 남지 않나요? 이에 대한 올바른 설명은?",
             "options": ["A) 인핸스는 RAG를 전혀 사용하지 않습니다", "B) 인핸스의 RAG(지식사전)는 자연어 규칙 조회만 담당하고, 수치 판단과 실행은 온톨로지가 담당하는 역할 분리로 해결합니다", "C) 더 좋은 임베딩 모델을 써서 해결합니다", "D) RAG 한계는 해결되지 않습니다"],
             "answer": "B",
             "explanation": "역할 분리가 핵심입니다. 인핸스의 RAG(지식사전)는 '30% 이상 할인 시 본부장 승인 필요'같은 자연어 규칙 조회만 합니다. 실제 할인율 계산, 조건 판단, 여러 데이터를 엮어 실행하는 것은 온톨로지(Object Graph)가 담당합니다."},
            {"id": "f08", "type": "mc", "category": "Agent 역할",
             "question": "AgentOS의 Agent가 기존 BI·대시보드 시스템과 근본적으로 다른 것은?",
             "options": ["A) 더 예쁜 시각화를 제공한다", "B) 데이터를 '보는 것'(조회·보고)을 넘어 스스로 '판단하고 실행'한다", "C) 더 많은 데이터를 처리할 수 있다", "D) 실시간 알림을 보낸다"],
             "answer": "B",
             "explanation": "기존 BI는 '이런 상황입니다'라고 알려주는 것이 끝입니다. AgentOS의 Agent는 온톨로지로 상황을 파악하고, 지식사전의 규칙을 적용하고, '이 상황이니 바로 이걸 실행합니다'라고 스스로 행동합니다. 이것이 '보고에서 실행으로'의 핵심입니다."},
            {"id": "f09", "type": "subjective", "category": "경쟁 기술 비교",
             "question": "RAG를 '도서관 사서'에 비유하는 이유를 설명하고, 인핸스의 접근이 어떻게 다른지 설명해보세요.",
             "answer_key": "도서관 사서는 '이런 내용이 3번 책 42페이지에 있어요'까지는 찾아주지만, 그 내용을 바탕으로 어떤 결정을 내려야 하는지는 사람이 판단해야 함. RAG도 마찬가지로 관련 문서를 찾아 답변을 만들어주지만, '이 고객이 해지 조건에 해당하는가' 같은 판단과 실행은 할 수 없음. 인핸스: 지식사전(RAG)은 규칙 찾기만 담당, 온톨로지가 판단·실행까지 담당하는 역할 분리로 한계를 극복."},
            {"id": "f10", "type": "subjective", "category": "지식 사전",
             "question": "인핸스의 지식 사전도 결국 RAG를 사용하는데, 기존 RAG의 문제가 그대로 남는 게 아닌가요? 인핸스가 이 문제를 어떻게 해결했는지 설명해보세요.",
             "answer_key": "역할 분리가 핵심. 인핸스에서 RAG(지식사전)는 딱 한 가지만 함: 회사 규칙·정의처럼 자연어로 된 정보 조회. 숫자 계산, 조건 판단, 여러 데이터를 엮어서 내리는 결정은 RAG가 아닌 온톨로지(Object Graph)가 담당. 비유: 법무팀(지식사전/RAG)은 규정을 찾아주고, 실무팀(온톨로지)이 그 규정 바탕으로 판단·실행. 법무팀 혼자 모든 걸 하려다 생기는 문제를 역할 분리로 해결."},
        ],

        "⑤ Agent 실행 개념": [
            {"id": "g01", "type": "mc", "category": "Agent 실행",
             "question": "AgentOS에서 '판단하고 실행하는 시스템'이 작동하는 올바른 흐름은?",
             "options": ["A) 사용자 요청 → SQL 생성 → 차트 출력", "B) 데이터 수집 → 저장 → 리포트 발송", "C) 온톨로지로 상황 파악 → 지식사전에서 규칙 조회 → Agent가 판단 → 액션 실행", "D) 문서 검색 → 요약 → 이메일 발송"],
             "answer": "C",
             "explanation": "AgentOS의 실행 흐름: Object/Link 온톨로지로 현재 상황을 구조적으로 파악 → 지식사전에서 관련 비즈니스 규칙 조회 → Agent가 이를 종합해 판단 → 실제 액션(알림 발송, 문서 생성, 외부 시스템 실행 등)을 수행합니다."},
            {"id": "g02", "type": "mc", "category": "지식 사전",
             "question": "지식 사전에 저장되는 '비즈니스 규칙'의 대표적인 예시는?",
             "options": ["A) 고객사의 계약 만료일", "B) '장기 체화 재고 = 마지막 출고 이력 180일 초과 + 재고 평가액 500만원 이상'", "C) 제품의 현재 재고 수량", "D) 담당 영업사원 이름"],
             "answer": "B",
             "explanation": "지식사전은 '장기 체화 재고 = 마지막 출고 180일 초과 + 평가액 500만원 이상', '30% 이상 할인 시 영업 본부장 사전 서면 승인 필요'처럼 비즈니스 규칙과 판단 기준을 관리합니다. 계약 만료일, 재고 수량 등 구체적 값은 Object Attribute에 저장합니다."},
            {"id": "g03", "type": "mc", "category": "패러다임",
             "question": "인핸스 AgentOS의 '보고에서 실행으로(From Reporting to Execution)' 패러다임이 의미하는 것은?",
             "options": ["A) 보고서를 더 예쁘게 만든다", "B) 보고서 작성 시간을 줄인다", "C) '이런 상황입니다'(알림·보고)에서 '이 상황이니 바로 실행합니다'(자동 판단·액션)로 데이터 활용 방식이 전환된다", "D) 보고 주기를 줄인다"],
             "answer": "C",
             "explanation": "기존: 데이터→대시보드 확인→사람이 판단→실행 지시. AgentOS: 데이터→Agent가 온톨로지+지식사전으로 상황 파악→스스로 판단→바로 실행. 사람이 매번 개입하던 '보고' 단계를 건너뛰고 Agent가 직접 '실행'합니다."},
            {"id": "g04", "type": "mc", "category": "Agent 실행",
             "question": "Object, Link, 지식사전이 모두 연결되었을 때 AgentOS Agent가 할 수 있는 것은?",
             "options": ["A) 데이터를 더 빠르게 저장한다", "B) 데이터를 예쁜 차트로 자동 생성한다", "C) 구조·관계·규칙을 이해하고 실제 업무를 자동으로 판단·실행한다", "D) 데이터를 자동으로 암호화한다"],
             "answer": "C",
             "explanation": "Object(판단 대상)와 Link(관계)로 구조가 정의되고, 지식사전에 비즈니스 규칙이 있으면, Agent는 '계약 만료 D-60인 고객에게 거래 이력 기반 제안서 자동 생성'처럼 실제 업무를 스스로 판단하고 실행합니다. 이것이 인핸스의 '보고에서 실행으로'의 핵심입니다."},
            {"id": "g05", "type": "mc", "category": "Observability",
             "question": "AgentOS의 Observability(투명성) 기능으로 추적할 수 있는 것이 아닌 것은?",
             "options": ["A) Agent가 어떤 Object를 참조했는지", "B) 어떤 지식사전 규칙을 적용했는지", "C) Agent가 실행한 액션 이력", "D) 개발팀 직원의 근무 시간"],
             "answer": "D",
             "explanation": "Observability는 AI가 어떤 데이터(Object)를 보고, 어떤 규칙(지식사전)을 적용하고, 어떤 순서로 판단해 어떤 액션을 실행했는지 역추적할 수 있게 합니다. 직원 근무시간은 관련 없습니다."},
            {"id": "g06", "type": "mc", "category": "Agent 실행",
             "question": "'계약 만료 D-60 자동 대응' 시나리오에서 AgentOS Agent가 실제로 수행하는 것은?",
             "options": ["A) 계약 만료일을 달력에 표시한다", "B) 담당자에게 단순 이메일로 알린다", "C) 계약 만료 Object 감지 → Link로 거래 이력 참조 → 지식사전 제안서 기준 적용 → 제안서 자동 생성 → 담당자에게 미팅 요청", "D) 보고서를 PDF로 저장한다"],
             "answer": "C",
             "explanation": "단순 알림이 아닙니다. Object(계약 만료일) 감지 → Link(고객 거래 이력) 참조 → 지식사전(제안서 작성 기준) 적용 → Agent가 제안서 초안 자동 생성 → 담당자에게 미팅 일정 잡으라고 알림. 이것이 '보고에서 실행으로'입니다."},
            {"id": "g07", "type": "mc", "category": "지식 사전",
             "question": "'규칙을 한 곳에서 관리한다'는 것이 실무에서 어떤 의미를 갖나요?",
             "options": ["A) 서버를 하나로 통합한다", "B) 지식 사전 1곳에서 기준을 바꾸면 연결된 모든 Agent가 자동으로 새 기준을 따른다", "C) 코드 저장소를 통합한다", "D) 데이터를 압축 보관한다"],
             "answer": "B",
             "explanation": "기존 방식은 규칙이 여러 코드/프롬프트에 분산되어 있어, 기준 하나 바꾸려면 전체를 수정해야 합니다. 인핸스는 지식 사전 한 곳만 바꾸면 연결된 모든 Agent가 자동 반영됩니다."},
            {"id": "g08", "type": "mc", "category": "Agent 실행",
             "question": "인핸스에서 'Agent가 이 상황이니 바로 실행합니다'라고 할 때, 이것이 가능한 이유는?",
             "options": ["A) 빠른 서버 덕분에", "B) 온톨로지로 상황을 구조적으로 파악하고, 지식사전의 규칙을 자동 적용해 판단까지 AI가 담당하기 때문", "C) 사람이 미리 모든 시나리오를 코딩해두었기 때문", "D) 더 많은 데이터를 학습했기 때문"],
             "answer": "B",
             "explanation": "온톨로지(Object/Link)가 '현재 어떤 상황인지'를 구조적으로 파악하게 해주고, 지식사전의 비즈니스 규칙이 '이 상황에서 어떻게 해야 하는지'를 알려줍니다. 두 레이어가 결합되면 Agent가 사람 없이 스스로 판단하고 실행할 수 있습니다."},
            {"id": "g09", "type": "subjective", "category": "지식 사전",
             "question": "지식사전에서 '기준을 1곳에서 관리하는 것'이 실무에서 왜 중요한지, 구체적인 예시를 들어 설명해보세요.",
             "answer_key": "기존 방식: '장기 체화 재고' 기준(180일)이 여러 보고서·코드·프롬프트에 분산. 기준을 90일로 바꾸려면 모든 곳을 찾아 수정해야 함. Agent가 100개면 100곳 수정. 인핸스 방식: 지식사전에 '장기 체화 재고 = 마지막 출고 90일 초과 + 평가액 500만원 이상'으로 1번 수정하면, 이 규칙을 참고하는 모든 Agent가 자동으로 새 기준을 적용. 실무 중요성: 규정 변경, 시즌 기준 조정, 정책 업데이트 시 단 1번 수정으로 전체 시스템에 즉시 반영 가능."},
            {"id": "g10", "type": "subjective", "category": "패러다임",
             "question": "'보고에서 실행으로'라는 인핸스의 핵심 가치를 구체적인 업무 시나리오를 들어 설명해보세요.",
             "answer_key": "기존: 담당자가 엑셀 열어서 계약 만료일 확인 → 제안서 새로 작성(반나절) → 일정 바쁘면 놓침 → 경쟁사가 먼저 들어와 계약 뺏김. 인핸스: D-60에 Agent가 자동 감지 → 3년 거래 이력 기반 제안서 초안 자동 생성 → 담당자에게 미팅 일정 잡으라고 먼저 알림 → 경쟁사보다 2달 먼저 움직임. 핵심: '이런 상황입니다'(알림)에서 '이 상황이니 이걸 바로 실행합니다'(자동 실행)로 전환."},
        ],

        "📋 기본 종합": [
            # from ① 회사 & 제품 개요
            {"id": "c01", "type": "mc", "category": "패러다임",
             "question": "AgentOS가 없을 때와 있을 때, 기업의 데이터 활용 방식에서 가장 큰 차이는?",
             "options": ["A) 데이터 저장 비용이 줄어든다", "B) 더 예쁜 대시보드를 자동으로 만들 수 있다", "C) 사람이 데이터를 보고 판단·실행하던 방식에서, AI Agent가 스스로 판단하고 실행하는 방식으로 전환된다", "D) 데이터 처리 속도가 빨라진다"],
             "answer": "C",
             "explanation": "이것이 AgentOS의 본질입니다. 없을 때: 데이터는 쌓여 있지만 사람이 직접 열어보고 판단하고 실행 지시. 있을 때: Agent가 온톨로지로 상황 파악 → 지식사전 규칙 적용 → 스스로 판단·실행. 데이터가 '보는 것'에서 '하는 것'으로 바뀝니다."},
            {"id": "c03", "type": "mc", "category": "AgentOS 5대 제품",
             "question": "DB, API, 파일 등 200개 이상의 커넥터로 데이터를 연결·정규화해 온톨로지 DB에 적재하는 AgentOS 제품은?",
             "options": ["A) Ontology Manager", "B) Pipeline Builder", "C) Workflow Builder", "D) Dashboard Generation"],
             "answer": "B",
             "explanation": "Pipeline Builder는 다양한 데이터 소스를 연결·정규화하고 온톨로지 DB로 적재합니다. 인핸스가 기존 인프라를 교체하지 않아도 되는 이유가 바로 이 커넥터 기반 연결 방식입니다."},
            {"id": "c08", "type": "mc", "category": "Agent 역할",
             "question": "AgentOS에서 Agent의 핵심 역할로 가장 적절한 것은?",
             "options": ["A) 데이터를 저장하고 관리한다", "B) 데이터를 차트로 시각화한다", "C) 온톨로지와 지식사전을 기반으로 상황을 판단하고 실제 액션을 실행한다", "D) SQL 쿼리를 자동으로 생성한다"],
             "answer": "C",
             "explanation": "AgentOS에서 Agent는 Object/Link 구조(온톨로지)로 맥락을 이해하고, 지식사전의 비즈니스 규칙을 참고해 판단하고 실제 액션을 실행합니다."},
            {"id": "c09", "type": "subjective", "category": "인핸스 포지셔닝",
             "question": "인핸스가 '데이터 사이언티스트(DS)를 대체하는 것이 아니다'라고 설명하는 이유는 무엇인가요?",
             "answer_key": "인핸스는 반복적이고 자동화 가능한 과정(데이터 연결, 분석 실행, 리포트 생성)을 처리하는 플랫폼. 통계 모델 타당성 검토, 분석 결과의 통계적 유의성 판단, 비즈니스 의사결정은 여전히 DS와 현업 팀이 담당. DS가 더 고차원 업무에 집중하도록 돕는 파트너 역할. 대체가 아닌 협업 구조."},
            # from ② 온톨로지 기초
            {"id": "d01", "type": "mc", "category": "온톨로지 3요소",
             "question": "AgentOS에서 '업무에서 판단의 대상이 되는 개념'을 나타내는 기본 단위는?",
             "options": ["A) Table", "B) Object", "C) Document", "D) Row"],
             "answer": "B",
             "explanation": "Object는 업무에서 판단의 대상이 되는 개념 단위입니다. 테이블이 '데이터 저장'이 목적이라면, Object는 '이 개념으로 무엇을 판단할 것인가'를 정의합니다. 예: 설비, 고객사, 계약, 생산배치"},
            {"id": "d03", "type": "mc", "category": "온톨로지 3요소",
             "question": "Object들 사이의 연결 관계를 정의하는 요소는?",
             "options": ["A) Attribute", "B) Pipeline", "C) Link", "D) Schema"],
             "answer": "C",
             "explanation": "Link(Relation)는 Object 또는 Property 간의 연결 관계를 정의합니다. 예: 고객사→계약, 설비→공정(runs_on)."},
            {"id": "d06", "type": "mc", "category": "온톨로지 가치",
             "question": "온톨로지를 도입하면 '베테랑 직원 퇴사'에도 업무 지식이 유지되는 이유는?",
             "options": ["A) 영상으로 모든 업무를 녹화하기 때문", "B) 노하우와 판단 기준이 Object·지식사전에 명시적으로 저장되기 때문", "C) 자동으로 인수인계 문서가 생성되기 때문", "D) 재고용 계약이 있기 때문"],
             "answer": "B",
             "explanation": "온톨로지 방식에서는 판단 기준, 업무 규칙, 관계 정의가 시스템에 명시적으로 저장됩니다. 담당자가 바뀌어도 모든 맥락이 시스템에 남습니다."},
            {"id": "d10", "type": "subjective", "category": "온톨로지 가치",
             "question": "'데이터에 의미를 부여한다'는 것이 무슨 뜻인지 구체적인 예시와 함께 설명해보세요.",
             "answer_key": "단순히 price_a, price_b, final_price 컬럼이 있을 때 AI는 어느 게 '최종 청구 금액'인지 모름. 의미를 부여한다는 것은 '이 필드는 최종 청구 금액', '저 필드는 제조 원가'라고 시스템에 명확히 정의하는 것. 이렇게 되면 AI가 추측 없이 정확하게 원하는 데이터를 찾을 수 있음."},
            # from ③ 데이터 연결 & 인프라
            {"id": "e01", "type": "mc", "category": "인프라 기초",
             "question": "고객이 'AgentOS 도입하려면 기존 ERP·CRM 시스템을 전부 교체해야 하나요?'라고 물었을 때 올바른 답변은?",
             "options": ["A) 네, 기존 시스템을 모두 AgentOS로 교체해야 합니다", "B) 아니요, 기존 시스템은 그대로 유지하고 위에 온톨로지 레이어만 추가합니다", "C) 데이터베이스만 교체하면 됩니다", "D) 클라우드 전환 후 도입 가능합니다"],
             "answer": "B",
             "explanation": "기존 ERP, CRM, Data Warehouse 등을 교체하지 않고, 위에 온톨로지 의미 레이어만 추가합니다. 기존 데이터 자산을 그대로 활용하면서 AI 활용성을 높입니다."},
            {"id": "e03", "type": "mc", "category": "인프라 기초",
             "question": "인핸스의 '온톨로지 레이어'가 하는 역할로 가장 정확한 것은?",
             "options": ["A) 기존 데이터를 삭제하고 새 형식으로 저장한다", "B) 기존 데이터 위에 의미(Semantic)와 관계(Relational) 구조를 추가해 AI가 이해하고 실행할 수 있게 한다", "C) 데이터를 압축해 저장 비용을 낮춘다", "D) SQL을 자동으로 최적화한다"],
             "answer": "B",
             "explanation": "온톨로지 레이어는 기존 데이터를 건드리지 않고, 그 위에 의미와 관계 구조를 추가합니다. AI가 개념과 관계로 데이터를 이해하고 실행할 수 있게 됩니다."},
            {"id": "e04", "type": "mc", "category": "데이터 분류",
             "question": "비정형 데이터를 Object Attribute로 저장할지 지식 사전에 넣을지 결정하는 기준은?",
             "options": ["A) 파일 크기", "B) 자주 꺼내 쓰는 구체적 값이면 Object Attribute, 문맥·뉘앙스가 중요하면 지식 사전", "C) 데이터 업데이트 빈도", "D) 원본 파일 형식(PDF/Excel)"],
             "answer": "B",
             "explanation": "계약 만료일·고객명처럼 자주 꺼내 쓰는 구체적 값은 Object Attribute로, 특약 조건·협상 맥락처럼 전체 문장의 맥락을 이해해야 하는 내용은 지식 사전에 저장합니다."},
            {"id": "e09", "type": "subjective", "category": "인프라 기초",
             "question": "인핸스가 기존 인프라를 교체하지 않고 '위에 레이어를 얹는' 방식을 선택한 이유는 무엇인가요?",
             "answer_key": "기업은 이미 수년간 구축한 데이터 자산(DWH, Data Lake, ERP 등)이 있음. 이를 교체하면 비용·시간·리스크가 엄청남. 인핸스는 기존 SQL/DWH 생태계를 그대로 유지하면서 온톨로지 레이어만 추가해 빠른 도입, 낮은 리스크, 기존 자산 활용 모두를 실현함."},
            # from ④ AgentOS vs 기존 기술
            {"id": "f01", "type": "mc", "category": "경쟁 기술 비교",
             "question": "RAG 방식의 가장 큰 한계는 무엇인가요?",
             "options": ["A) 처리 속도가 너무 느림", "B) 텍스트 검색은 잘 하지만 구조·관계·맥락 기반 판단과 실행 불가", "C) 비용이 너무 높음", "D) 영어 문서만 처리 가능"],
             "answer": "B",
             "explanation": "RAG는 문서 검색과 Q&A에서 뛰어나지만, 여러 데이터를 엮어 일관된 구조 기반 판단을 내리거나 실제 액션을 실행하는 데는 한계가 있습니다."},
            {"id": "f04", "type": "mc", "category": "지식 사전",
             "question": "지식 사전(Knowledge Dictionary)의 역할을 가장 정확하게 표현한 것은?",
             "options": ["A) 자연어로 된 문서를 저장하는 창고", "B) 비즈니스 규칙과 판단 기준을 관리하는 규칙 엔진으로, Agent가 이를 기반으로 의사결정한다", "C) 직원 교육 자료를 보관하는 데이터베이스", "D) AI 모델을 학습시키는 데이터셋"],
             "answer": "B",
             "explanation": "지식 사전은 단순 자연어 저장소가 아닙니다. 비즈니스 규칙과 판단 기준을 관리하는 규칙 엔진입니다. Agent는 이 규칙을 기반으로 판단하고 실행합니다."},
            {"id": "f07", "type": "mc", "category": "지식 사전",
             "question": "인핸스는 지식사전에도 RAG를 쓰는데, 기존 RAG의 한계가 그대로 남지 않나요? 이에 대한 올바른 설명은?",
             "options": ["A) 인핸스는 RAG를 전혀 사용하지 않습니다", "B) 인핸스의 RAG(지식사전)는 자연어 규칙 조회만 담당하고, 수치 판단과 실행은 온톨로지가 담당하는 역할 분리로 해결합니다", "C) 더 좋은 임베딩 모델을 써서 해결합니다", "D) RAG 한계는 해결되지 않습니다"],
             "answer": "B",
             "explanation": "역할 분리가 핵심입니다. 인핸스의 RAG(지식사전)는 자연어 규칙 조회만 합니다. 실제 판단과 실행은 온톨로지(Object Graph)가 담당합니다."},
            {"id": "f09", "type": "subjective", "category": "경쟁 기술 비교",
             "question": "RAG를 '도서관 사서'에 비유하는 이유를 설명하고, 인핸스의 접근이 어떻게 다른지 설명해보세요.",
             "answer_key": "도서관 사서는 '이런 내용이 3번 책 42페이지에 있어요'까지는 찾아주지만, 그 내용을 바탕으로 어떤 결정을 내려야 하는지는 사람이 판단해야 함. RAG도 마찬가지로 관련 문서를 찾아 답변을 만들어주지만, '이 고객이 해지 조건에 해당하는가' 같은 판단과 실행은 할 수 없음. 인핸스: 지식사전(RAG)은 규칙 찾기만 담당, 온톨로지가 판단·실행까지 담당하는 역할 분리로 한계를 극복."},
            # from ⑤ Agent 실행 개념
            {"id": "g01", "type": "mc", "category": "Agent 실행",
             "question": "AgentOS에서 '판단하고 실행하는 시스템'이 작동하는 올바른 흐름은?",
             "options": ["A) 사용자 요청 → SQL 생성 → 차트 출력", "B) 데이터 수집 → 저장 → 리포트 발송", "C) 온톨로지로 상황 파악 → 지식사전에서 규칙 조회 → Agent가 판단 → 액션 실행", "D) 문서 검색 → 요약 → 이메일 발송"],
             "answer": "C",
             "explanation": "AgentOS의 실행 흐름: 온톨로지로 현재 상황 파악 → 지식사전에서 비즈니스 규칙 조회 → Agent가 판단 → 실제 액션 수행."},
            {"id": "g03", "type": "mc", "category": "패러다임",
             "question": "인핸스 AgentOS의 '보고에서 실행으로(From Reporting to Execution)' 패러다임이 의미하는 것은?",
             "options": ["A) 보고서를 더 예쁘게 만든다", "B) 보고서 작성 시간을 줄인다", "C) '이런 상황입니다'(알림·보고)에서 '이 상황이니 바로 실행합니다'(자동 판단·액션)로 데이터 활용 방식이 전환된다", "D) 보고 주기를 줄인다"],
             "answer": "C",
             "explanation": "사람이 매번 개입하던 '보고' 단계를 건너뛰고 Agent가 직접 '실행'합니다. 데이터가 '보는 것'에서 '하는 것'으로 바뀝니다."},
            {"id": "g04", "type": "mc", "category": "Agent 실행",
             "question": "Object, Link, 지식사전이 모두 연결되었을 때 AgentOS Agent가 할 수 있는 것은?",
             "options": ["A) 데이터를 더 빠르게 저장한다", "B) 데이터를 예쁜 차트로 자동 생성한다", "C) 구조·관계·규칙을 이해하고 실제 업무를 자동으로 판단·실행한다", "D) 데이터를 자동으로 암호화한다"],
             "answer": "C",
             "explanation": "Object(판단 대상)와 Link(관계)로 구조가 정의되고, 지식사전에 비즈니스 규칙이 있으면, Agent는 실제 업무를 스스로 판단하고 실행합니다."},
            {"id": "g10", "type": "subjective", "category": "패러다임",
             "question": "'보고에서 실행으로'라는 인핸스의 핵심 가치를 구체적인 업무 시나리오를 들어 설명해보세요.",
             "answer_key": "기존: 담당자가 엑셀 열어서 계약 만료일 확인 → 제안서 새로 작성(반나절) → 일정 바쁘면 놓침 → 경쟁사가 먼저 들어와 계약 뺏김. 인핸스: D-60에 Agent가 자동 감지 → 3년 거래 이력 기반 제안서 초안 자동 생성 → 담당자에게 미팅 일정 잡으라고 먼저 알림 → 경쟁사보다 2달 먼저 움직임. 핵심: '이런 상황입니다'(알림)에서 '이 상황이니 이걸 바로 실행합니다'(자동 실행)로 전환."},
        ],
    },

    "심화": {
        "⑥ 데이터 아키텍처 심화": [
            {"id": "h01", "type": "mc", "category": "아키텍처 비교",
             "question": "3가지 온톨로지 구현 방식 중 기업 기존 인프라 기준으로 마이그레이션 비용이 가장 작은 방식은?",
             "options": ["A) Semantic Web 정통 방식 (RDF/OWL)", "B) GraphDB 방식 (Neo4j 등)", "C) RDB 기반 Semantic Layer 방식 (인핸스 스타일)", "D) 세 방식 모두 동일"],
             "answer": "C",
             "explanation": "RDB 기반 Semantic Layer는 기존 테이블 형태를 그대로 유지하고 위에 레이어만 추가합니다. 저장 방식을 바꾸는 GraphDB나 완전히 새로운 표준을 도입하는 RDF/OWL보다 훨씬 낮은 전환 비용으로 도입 가능합니다."},
            {"id": "h02", "type": "mc", "category": "아키텍처 비교",
             "question": "3가지 온톨로지 구현 방식 중 '논리적 추론(Reasoning)'이 가장 강한 것은?",
             "options": ["A) RDB 기반 Semantic Layer", "B) GraphDB 방식", "C) Semantic Web 정통 방식 (RDF/OWL)", "D) 모두 동일"],
             "answer": "C",
             "explanation": "OWL/RDF 기반 Semantic Web은 논리적으로 가장 엄밀하고 자동 추론(Reasoning)이 가장 강합니다. 단, 이 강점이 곧 운영 복잡성이라는 단점이기도 합니다."},
            {"id": "h03", "type": "mc", "category": "아키텍처 비교",
             "question": "GraphDB(Neo4j)가 기업의 기존 RDB 데이터와 통합하기 어려운 근본적 이유는?",
             "options": ["A) 라이선스 비용이 너무 비싸서", "B) 저장 방식 자체가 노드/엣지 구조라 RDB 테이블 구조와 근본적으로 달라 전체 마이그레이션이 필요하기 때문", "C) 사용자 인터페이스가 복잡해서", "D) 클라우드를 지원하지 않아서"],
             "answer": "B",
             "explanation": "GraphDB는 데이터 저장 방식 자체가 노드/엣지입니다. 기존 기업 데이터(RDB)와의 동기화, 비용, 권한, 성능 관리 등이 복잡해집니다. 인핸스는 기존 테이블 형태를 유지하면서 온톨로지 레이어만 추가합니다."},
            {"id": "h04", "type": "mc", "category": "아키텍처 비교",
             "question": "인핸스가 RDB 기반 Semantic Layer를 선택한 4가지 이유 중 옳지 않은 것은?",
             "options": ["A) 운영이 쉬움 — 기존 DWH/SQL 생태계 그대로 활용", "B) 빠른 적용 — GraphDB로 전체 마이그레이션 불필요", "C) 정확한 답변 — SQL로 수치 추출 + LLM은 설명만", "D) 완전한 논리 추론 — OWL보다 강력한 추론 엔진 보유"],
             "answer": "D",
             "explanation": "인핸스가 RDB Semantic Layer를 선택한 이유: 운영 쉬움, 빠른 적용, 정확한 답변(SQL+LLM 역할 분리), UI로 관리(비엔지니어도 온톨로지 관리 가능). '완전한 논리 추론'은 오히려 OWL/RDF의 강점이며, 인핸스는 실무 적용성과 AI Agent 연결을 우선합니다."},
            {"id": "h05", "type": "mc", "category": "아키텍처 비교",
             "question": "RDB 기반 Semantic Layer에서 수치 관련 할루시네이션을 줄이는 방법은?",
             "options": ["A) 더 많은 학습 데이터를 사용한다", "B) SQL로 수치를 정확히 추출하고, LLM은 설명·요약만 담당한다", "C) 벡터 검색을 개선한다", "D) 더 큰 LLM 모델을 사용한다"],
             "answer": "B",
             "explanation": "수치 계산에서 LLM이 스스로 계산하면 할루시네이션이 발생합니다. 인핸스는 SQL로 정확한 수치를 추출하고, LLM은 그 결과를 자연어로 설명하는 역할만 담당하게 해 정확도를 높입니다."},
            {"id": "h06", "type": "mc", "category": "아키텍처 비교",
             "question": "온톨로지 방식에서 과거-현재 비교 분석(예: 고객 구매 패턴 3개월 전 대비 변화)이 가능한 이유는?",
             "options": ["A) 원본 파일을 모두 보존하기 때문", "B) Object의 상태 변화를 시간 순서대로 기록하기 때문", "C) 별도 히스토리 데이터베이스를 유지하기 때문", "D) 주기적 스냅샷을 찍기 때문"],
             "answer": "B",
             "explanation": "AgentOS는 시간 기반 상태 변화 추적이 가능한 구조를 제공합니다. Object의 상태 변화가 기록되어 '3개월 전 대비 어떻게 달라졌는가' 형태의 시간 기반 비교 분석이 가능합니다."},
            {"id": "h07", "type": "subjective", "category": "아키텍처 비교",
             "question": "RDF/OWL의 자동 추론(Reasoning)과 인핸스의 LLM+온톨로지 기반 판단 방식의 차이점을 설명하고, 기업 실무 환경에서 어느 쪽이 더 적합한지 근거와 함께 서술해보세요.",
             "answer_key": "RDF/OWL: 논리 규칙 기반 자동 추론. 완전한 일관성 보장. 단, 모든 규칙을 형식 논리로 미리 정의해야 함. 실무 적용에 전문 지식 필요, 운영 무거움. 인핸스(LLM+온톨로지): Object/Link/지식사전으로 의미·관계 정의 후 LLM이 자연어 기반 판단. 비전문가도 지식사전에 자연어로 규칙 작성 가능. 빠른 도입 가능. 기업 실무 적합성: 인핸스 방식이 더 적합. 이유: 빠른 도입, 비전문가 운영 가능, 기존 RDB 활용, LLM의 유연한 자연어 판단. 단, 완전한 논리 일관성이 필요한 고규제 환경(법률, 금융)에서는 OWL의 추론 강점도 고려할 수 있음."},
            {"id": "h08", "type": "subjective", "category": "아키텍처 비교",
             "question": "GraphDB(Neo4j 등) 방식이 기업 환경에서 갖는 실무적 한계를 설명해보세요.",
             "answer_key": "저장 방식 자체를 노드/엣지로 바꿔야 하므로 기존 RDB 데이터를 마이그레이션해야 함. 기존 기업 데이터(RDB)와의 동기화, 비용, 권한, 성능 관리 등이 복잡해짐. 인핸스는 기존 테이블 형태를 유지하면서 온톨로지 레이어만 추가하므로 이런 마이그레이션 비용이 없음."},
            {"id": "h09", "type": "subjective", "category": "아키텍처 비교",
             "question": "Text-to-SQL의 문제점을 온톨로지가 어떻게 해결하는지 설명해보세요.",
             "answer_key": "Text-to-SQL 문제: AI가 스키마만 보고 컬럼 의미를 추측해야 함. price_a, price_b, final_price 같이 비슷한 컬럼이 여러 개면 잘못 선택. 온톨로지 해결: 각 필드의 의미를 미리 정의해둠('이 필드=최종 청구 금액', '저 필드=제조 원가'). AI가 추측하지 않고 정확한 의미 기반으로 엔티티를 추출해 정확한 SQL 생성 가능."},
            {"id": "h10", "type": "subjective", "category": "아키텍처 비교",
             "question": "같은 데이터를 다양한 비즈니스 질의 패턴으로 활용할 수 있다는 것이 온톨로지 Object Graph 관점에서 어떤 의미를 갖는지 설명해보세요.",
             "answer_key": "RDB 방식: 특정 질의에 맞게 JOIN을 설계하면 다른 패턴 질의에는 재설계 필요. 질의 패턴이 미리 결정되어야 함. Object Graph: 한 번 Object와 Link를 정의하면, 다양한 탐색 경로로 다른 인사이트 추출 가능. 예: '고객사' Object에서 시작해 Link를 따라 '계약'으로, '거래 이력'으로, '담당자'로, '제품'으로 다양하게 탐색 가능. 새로운 질문이 생겨도 기존 Object/Link 구조 재활용. 데이터 재설계 없이 새 인사이트 발굴 가능."},
        ],

        "⑦ 멀티 Agent & 워크플로우": [
            {"id": "i01", "type": "mc", "category": "멀티 Agent",
             "question": "복잡한 업무에서 Orchestrator가 온톨로지 정보를 활용하는 방식은?",
             "options": ["A) 단일 Agent에 모든 작업을 위임", "B) 온톨로지의 Object 관계를 참고해 필요한 여러 Agent를 조합·협업하게 함", "C) 직접 SQL을 실행", "D) 배치 처리로 순차 실행"],
             "answer": "B",
             "explanation": "Orchestrator는 온톨로지의 Object-Link 구조를 이해하고, 복잡한 업무를 처리하기 위해 필요한 여러 전문 Agent를 조합해 협업하게 합니다. 관계가 복잡할수록 이 조합 효과가 커집니다."},
            {"id": "i02", "type": "mc", "category": "멀티 Agent",
             "question": "Workflow Builder로 멀티 Agent를 구성할 때 각 Agent의 역할 분리 기준으로 가장 적절한 것은?",
             "options": ["A) 실행 시간 균등 분배", "B) Object 단위로 전문화 — 각 Agent가 특정 Object 영역을 담당", "C) 팀 구조와 동일하게 구성", "D) 알파벳 순서로 배분"],
             "answer": "B",
             "explanation": "온톨로지의 Object 구조를 따라 각 Agent가 담당 Object 영역을 전문화합니다. 예: 고객 Agent(고객사 Object 전문), 계약 Agent(계약 Object 전문), 재고 Agent(재고 Object 전문). Orchestrator가 이들을 조합해 복잡한 업무를 처리합니다."},
            {"id": "i03", "type": "mc", "category": "멀티 Agent",
             "question": "관계가 복잡하게 얽힌 데이터(예: 고객사→계약→담당자→제품→재고→납기)에서 인핸스가 강점을 보이는 이유는?",
             "options": ["A) 단순한 데이터에만 적합하기 때문", "B) Object + Link 구조 자체가 복잡한 관계형 데이터를 표현하도록 설계되었기 때문", "C) 다른 시스템보다 서버가 빠르기 때문", "D) 관계를 자동으로 단순화하기 때문"],
             "answer": "B",
             "explanation": "인핸스의 Object+Link 구조는 복잡한 관계형 데이터를 표현하기 위해 설계됐습니다. 복잡한 관계일수록 Orchestrator가 여러 Object를 조합해 Agent들이 협업하게 하며, 자동화 효과가 더 크게 나옵니다."},
            {"id": "i04", "type": "mc", "category": "멀티 Agent",
             "question": "멀티 Agent 시스템의 장점 중 '안정성' 측면에서 단일 Agent 대비 우수한 이유는?",
             "options": ["A) 하드웨어가 더 좋아서", "B) 특정 Agent 실패 시 해당 Agent만 재시도하고, 나머지 Agent는 계속 실행 가능", "C) 코드가 더 짧아서", "D) 자동으로 백업이 생성되어서"],
             "answer": "B",
             "explanation": "단일 Agent 방식에서는 하나가 실패하면 전체가 중단됩니다. 멀티 Agent에서는 실패한 Agent만 재시도하고 나머지는 계속 실행됩니다. 또한 병렬 처리로 전체 처리 시간도 단축됩니다."},
            {"id": "i05", "type": "mc", "category": "Agent 실행",
             "question": "온톨로지 기반에서 '계약 만료 D-60에 Agent가 자동으로 제안서를 생성하는' 흐름의 핵심 구성 요소는?",
             "options": ["A) 이메일 웹훅", "B) Object(계약 만료일) + Link(고객 거래 이력) + 지식사전(제안서 기준) + Agent 자동 판단·실행", "C) 수동 트리거", "D) 캘린더 API"],
             "answer": "B",
             "explanation": "Object에 저장된 계약 만료일을 감지하고, Link를 통해 거래 이력을 참조하며, 지식사전의 제안서 작성 기준을 적용해 Agent가 자동으로 판단하고 실행하는 구조입니다."},
            {"id": "i06", "type": "mc", "category": "멀티 Agent",
             "question": "Orchestrator 없이 단일 Agent가 모든 업무를 처리할 때의 근본적인 한계는?",
             "options": ["A) 비용이 더 많이 든다", "B) 업무가 복잡해질수록 컨텍스트가 과부하되고, 새 업무 추가 시 전체를 수정해야 한다", "C) UI가 복잡해진다", "D) 사용자가 직접 학습해야 한다"],
             "answer": "B",
             "explanation": "단일 Agent는 모든 Object 정보와 모든 규칙을 한 번에 처리해야 해서 컨텍스트 한계가 생깁니다. 멀티 Agent+Orchestrator 구조에서는 각 Agent가 전문 영역만 담당하고, 새 업무 추가 시 새 Agent만 추가하면 됩니다."},
            {"id": "i07", "type": "subjective", "category": "멀티 Agent",
             "question": "멀티 Agent 시스템에서 Orchestrator가 온톨로지 정보를 어떻게 활용하는지, 그리고 이로 인해 단일 Agent 대비 어떤 장점이 생기는지 설명해보세요.",
             "answer_key": "Orchestrator 역할: 온톨로지의 Object-Link 구조를 이해해 복잡한 업무를 분해. 어떤 전문 Agent가 어떤 Object를 처리할지 조합·지시. 활용 방식: 예) '고객사→계약→담당자→제품→재고→납기' 관계에서 각 Object를 담당하는 전문 Agent를 순서에 맞게 조합. 단일 Agent 대비 장점: 1) 역할 분리로 각 Agent가 전문성 집중 가능. 2) 병렬 처리 가능. 3) 실패 시 해당 Agent만 재시도. 4) 새 업무 추가 시 새 Agent만 추가. 핵심: 온톨로지가 없으면 Orchestrator가 데이터 관계를 이해할 수 없어 복잡한 멀티 Agent 조합 자체가 불가능."},
            {"id": "i08", "type": "subjective", "category": "멀티 Agent",
             "question": "Object와 Link의 관계가 복잡할수록 인핸스가 더 효과적인 이유를 설명해보세요.",
             "answer_key": "Object+Link 구조 자체가 복잡한 관계형 데이터를 표현하도록 설계됨. 복잡한 관계일수록 Orchestrator가 여러 Object를 필요에 따라 조합하고, Agent들이 협업해 처리함. 단순한 데이터는 자동화해도 효과가 작지만, 여러 부서에 걸친 복잡한 관계(고객→계약→담당→제품→재고→납기)일수록 자동화의 파급 효과가 큼."},
            {"id": "i09", "type": "subjective", "category": "Agent 실행",
             "question": "부서 간 데이터가 복잡하게 연결된 환경에서 Agent 자동화의 효과가 더 커지는 이유를 설명하고, 구체적인 시나리오를 하나 들어보세요.",
             "answer_key": "이유: 복잡한 데이터 관계일수록 사람이 수동으로 처리할 때 시간·오류 비용이 크고, Orchestrator가 여러 Agent를 조합해 자동화할 때 절감 효과가 큼. Object+Link 구조가 이 복잡성을 체계적으로 다룰 수 있게 함. 시나리오 예: '고객 A의 계약 만료 D-60' 감지 → 고객 Agent: 3년 거래 이력 조회 → 계약 Agent: 갱신 조건 분석 → 재고 Agent: 현재 납기 가능 재고 확인 → 영업 Agent: 맞춤 제안서 초안 생성 → 담당자에게 미팅 요청. 이 모든 과정이 사람 개입 없이 자동 실행."},
            {"id": "i10", "type": "subjective", "category": "멀티 Agent",
             "question": "제조업체에서 영업팀, 생산팀, 물류팀 데이터가 각각 다른 시스템에 분산되어 있습니다. 인핸스로 이를 통합해 '납기 지연 자동 대응' Agent를 설계해보세요.",
             "answer_key": "1. Pipeline Builder: 영업CRM(주문), 생산MES(생산계획), 물류시스템(배송) 데이터 연결. 2. Ontology Manager: 핵심 Object 정의 — 고객주문(납기일, 수량), 생산배치(생산진척률, 완료예정일), 배송(출하예정일). 3. Object Link 연결: 고객주문→생산배치→배송. 4. 지식사전: '납기 3일 전 생산 미완료 시 → 영업팀 즉시 통보 + 대체 공급처 탐색' 규칙 정의. 5. Orchestrator + Agent 구성: 모니터링 Agent(납기 위험 감지) → 분석 Agent(지연 원인 파악) → 대응 Agent(고객 통보 + 대안 제시). 이 전체 흐름이 사람 개입 없이 자동 실행."},
        ],

        "⑧ 거버넌스 & Observability": [
            {"id": "j01", "type": "mc", "category": "Governance",
             "question": "인핸스의 Governance에서 접근 권한을 설정하는 기본 단위는?",
             "options": ["A) 데이터베이스 전체", "B) 테이블 단위", "C) Object 단위", "D) 사용자 그룹 단위만"],
             "answer": "C",
             "explanation": "Object 중심으로 접근 권한을 설정합니다. 예: 재무 Object는 재무팀만 접근 가능. 필요에 따라 Attribute(속성 단위)나 Role(역할 단위)로 세부 권한도 확장 적용할 수 있습니다."},
            {"id": "j02", "type": "mc", "category": "Observability",
             "question": "Observability(투명성)가 단순한 로그 기록과 다른 가장 큰 이유는?",
             "options": ["A) 더 많은 데이터를 저장해서", "B) AI가 어떤 Object·규칙을 보고 어떤 순서로 판단했는지까지 역추적 가능해서", "C) 실시간 알림을 보내서", "D) 비용을 절감해서"],
             "answer": "B",
             "explanation": "Observability는 AI가 틀린 판단을 했을 때 '왜 그런 결정이 나왔는지'를 역추적할 수 있게 합니다. 어떤 Object를 봤는지, 어떤 규칙을 적용했는지, 어떤 순서로 판단했는지 전체 흐름이 기록됩니다."},
            {"id": "j03", "type": "mc", "category": "Governance",
             "question": "인핸스 거버넌스에서 지식사전 규칙 변경 이력을 관리하는 이유는?",
             "options": ["A) 저장 공간을 효율적으로 쓰기 위해", "B) 누가, 언제 규칙을 변경했는지 추적하고, AI 판단 결과와 연결해 책임 소재를 명확히 하기 위해", "C) 규칙 자동 백업을 위해", "D) 비용 청구를 위해"],
             "answer": "B",
             "explanation": "지식사전의 규칙이 바뀌면 Agent의 행동이 바뀝니다. '누가 언제 어떤 규칙을 바꿔 Agent가 어떤 액션을 실행했는가'를 추적할 수 있어야 감사(Audit), 오류 원인 분석, 책임 소재 파악이 가능합니다."},
            {"id": "j04", "type": "mc", "category": "Governance",
             "question": "기존 방식의 '기준 운영 한계'를 인핸스가 해결하는 방식은?",
             "options": ["A) 더 강력한 서버 도입", "B) 기준을 지식 사전에 집중 관리하여 변경 시 모든 Agent가 자동 반영", "C) 기준을 코드에 더 체계적으로 문서화", "D) 변경 주기를 제한"],
             "answer": "B",
             "explanation": "기존 방식은 기준이 코드/프롬프트에 분산되어 있어 변경 시 전체를 수정해야 합니다. 인핸스는 기준을 지식 사전 한 곳에 집중 관리해 1번 변경으로 모든 Agent가 자동 반영됩니다."},
            {"id": "j05", "type": "mc", "category": "Observability",
             "question": "지식사전(RAG)에서의 할루시네이션 위험이 낮은 이유는?",
             "options": ["A) 더 좋은 임베딩 모델을 사용해서", "B) 역할이 규칙·정의 조회로 제한되어 있고, 수치 판단은 온톨로지가 담당하기 때문", "C) 더 많은 학습 데이터 때문", "D) 캐싱 때문"],
             "answer": "B",
             "explanation": "인핸스의 지식사전(RAG)은 자연어 규칙·정의 조회만 담당합니다. 수치 계산과 조건 판단은 온톨로지가 처리합니다. 역할 분리로 각 영역에서 할루시네이션 위험이 최소화됩니다."},
            {"id": "j06", "type": "mc", "category": "Observability",
             "question": "AgentOS에서 Agent의 모든 실행 액션을 기록하는 주된 목적은?",
             "options": ["A) 서버 성능 최적화", "B) AI 판단과 실행 과정을 역추적 가능하게 해 신뢰성 확보, 오류 분석, 감사(Audit) 지원", "C) 저장 비용 최적화", "D) 사용자 행동 분석"],
             "answer": "B",
             "explanation": "Agent가 어떤 데이터를 보고, 어떤 규칙을 적용하고, 어떤 액션을 실행했는지 전체 이력이 기록됩니다. 이를 통해 AI 판단의 신뢰성 확보, 오류 원인 분석, 규제 감사 대응이 가능합니다."},
            {"id": "j07", "type": "subjective", "category": "Observability",
             "question": "AI 시스템에서 Observability(투명성)가 단순한 로그 기록·모니터링과 근본적으로 다른 이유를 설명하고, 기업 운영 측면에서 이것이 왜 중요한지 서술해보세요.",
             "answer_key": "단순 로그: 시스템 이벤트(에러, 실행 시간 등) 기록. 무슨 일이 일어났는지만 파악. Observability: AI가 어떤 데이터(Object)를 보고, 어떤 규칙(지식사전)을 적용하고, 어떤 순서로 판단해 어떤 액션을 실행했는지 전체 의사결정 과정을 역추적 가능. 기업 운영 중요성: 1) AI 틀린 판단 원인 파악 가능 → 개선 가능. 2) 블랙박스가 아닌 신뢰 가능한 AI 시스템. 3) 감사(Audit)/규제 준수 근거. 4) 책임 소재 명확화. 특히 금융·의료처럼 규제가 강한 산업에서 AI 판단 근거 제출 가능."},
            {"id": "j08", "type": "subjective", "category": "Governance",
             "question": "온톨로지 기반 거버넌스가 기존 DB 접근 권한 관리와 다른 점은 무엇인가요?",
             "answer_key": "기존 DB 권한: 테이블/컬럼 단위. 데이터에만 접근 제어. 인핸스 거버넌스: Object 단위 접근 권한 + 지식사전 규칙 변경 이력 + Agent 실행 액션 전체 기록. 누가 어떤 데이터를 봤는지, 어떤 규칙을 썼는지, 무슨 액션을 했는지 비즈니스 맥락까지 추적 가능. 규제 준수(Compliance), 감사(Audit) 관점에서 훨씬 강력."},
            {"id": "j09", "type": "subjective", "category": "Observability",
             "question": "'AI가 틀린 판단을 내렸다'는 상황에서 AgentOS Observability가 어떻게 도움이 되는지, 구체적인 시나리오를 들어 설명해보세요.",
             "answer_key": "시나리오: Agent가 특정 고객에게 잘못된 할인율로 제안서를 자동 생성. 기존 방식: AI가 왜 그런 결정을 내렸는지 알 수 없음(블랙박스). Observability 활용: 1) 어떤 Object(고객 등급, 주문 이력)를 참조했는지 확인. 2) 어떤 지식사전 규칙('VIP 고객 15% 할인')을 적용했는지 확인. 3) 잘못된 고객 등급 분류 또는 잘못된 규칙 적용이 원인임을 발견. 4) 지식사전 규칙을 수정해 재발 방지. 결과: AI 판단 오류를 원인까지 추적하고 수정 가능 → 지속적 개선과 신뢰 구축."},
            {"id": "j10", "type": "subjective", "category": "Governance",
             "question": "금융 규제 환경에서 AI Agent를 도입하려는 고객이 '감독당국에 AI 판단을 설명할 수 있나요?'라고 물었을 때 인핸스의 Observability와 Governance를 활용해 어떻게 답변하시겠습니까?",
             "answer_key": "핵심 답변: 네, 가능합니다. AgentOS는 AI의 모든 판단 과정을 역추적할 수 있습니다. 구체적 설명: 1) Observability: 어떤 데이터(Object)를 보고, 어떤 규칙(지식사전)을 적용하고, 어떤 순서로 판단해 어떤 액션을 실행했는지 전체 기록 보존. 2) Governance: 지식사전 규칙 변경 이력(누가, 언제, 무엇을 변경) 관리. Object 단위 접근 권한 기록. 3) 실제 활용: 감독당국에 'X 날짜에 Y Agent가 Z 규칙을 적용해 W 결정을 내렸다'는 전체 근거 제출 가능. 4) 강점: AI가 블랙박스가 아닌 투명한 시스템으로 운영 → 규제 환경에서 신뢰 확보."},
        ],

        "⑨ 영업 & 고객 설득": [
            {"id": "k01", "type": "mc", "category": "영업 대응",
             "question": "고객이 'AgentOS 도입하면 기존 ERP를 교체해야 하나요?'라고 물을 때 올바른 영업 대응은?",
             "options": ["A) '네, 전부 교체해야 합니다'", "B) '기존 ERP는 그대로 유지하면서, 위에 AgentOS 온톨로지 레이어만 추가합니다. 기존 투자가 그대로 보존됩니다.'", "C) 'ERP와 별개로 새 데이터베이스를 구축해야 합니다'", "D) '클라우드 전환 후에만 도입 가능합니다'"],
             "answer": "B",
             "explanation": "인핸스의 핵심 가치 제안: 기존 인프라 교체 불필요. 기존 ERP, CRM, Data Warehouse 위에 온톨로지 레이어만 추가합니다. 고객의 기존 데이터 자산이 모두 보존되고, 도입 리스크와 비용이 최소화됩니다."},
            {"id": "k02", "type": "mc", "category": "영업 대응",
             "question": "'우리 회사는 이미 RAG 기반 AI를 도입했습니다'라는 고객에게 인핸스를 추가 도입해야 하는 이유를 설명할 때 가장 핵심적인 포인트는?",
             "options": ["A) RAG는 구식 기술이니 교체해야 한다", "B) RAG는 정보 검색에 뛰어나지만, 여러 데이터를 엮어 판단하고 실제 액션을 실행하는 것은 인핸스가 추가로 담당한다", "C) 비용이 더 저렴하다", "D) 더 많은 문서를 처리할 수 있다"],
             "answer": "B",
             "explanation": "경쟁이 아닌 보완 관계입니다. RAG 솔루션을 문서 검색용으로 유지하면서, 인핸스가 판단·실행 레이어로 추가됩니다. 두 시스템이 협력해 '검색+판단+실행'의 완전한 AI 자동화를 실현합니다."},
            {"id": "k03", "type": "mc", "category": "AgentOS 가치",
             "question": "AgentOS E2E(End-to-End) 플랫폼이 의미하는 것은?",
             "options": ["A) 전사 시스템 전체를 교체한다", "B) 데이터 연결부터 온톨로지 구성, Agent 구축, 대시보드 생성, 액션 실행까지 한 플랫폼에서 처리", "C) 모든 산업을 지원한다", "D) 글로벌 엔드포인트를 제공한다"],
             "answer": "B",
             "explanation": "AgentOS는 Pipeline Builder(데이터 연결) → Ontology Manager(의미 구조화) → Workflow Builder(Agent 워크플로우) → Dashboard Generation → CUA(실제 실행)까지 전 과정을 하나의 플랫폼에서 처리합니다."},
            {"id": "k04", "type": "mc", "category": "AgentOS 가치",
             "question": "온톨로지 플랫폼 도입의 장기적 경쟁 우위 관점에서 가장 중요한 것은?",
             "options": ["A) 초기 도입 비용 절감", "B) 기업만의 독자적 지식 그래프(온톨로지)가 누적될수록 AI 정확도와 경쟁 우위가 기하급수적으로 향상된다", "C) 처리 속도 향상", "D) 클라우드 비용 절감"],
             "answer": "B",
             "explanation": "온톨로지는 기업만의 독자적 IP(지식 자산)가 됩니다. 비즈니스 규칙, 도메인 지식, 관계 구조가 시스템에 누적될수록 AI 정확도가 높아지고, 경쟁사가 복제하기 어려운 차별화 요소가 됩니다."},
            {"id": "k05", "type": "subjective", "category": "패러다임",
             "question": "AgentOS가 없을 때와 있을 때를 하나의 구체적인 업무 시나리오로 대비해서 고객에게 설명하세요.",
             "answer_key": "없을 때: 데이터는 쌓여 있지만 사람이 직접 열어보고 판단하고 실행 지시. 예) 계약 만료 관리: 담당자가 매일 엑셀 열어 확인 → 바쁘면 놓침 → 경쟁사가 먼저 들어옴. 있을 때: Agent가 온톨로지로 상황 파악 → 지식사전 규칙 적용 → 스스로 판단·실행. 예) D-60 자동 감지 → 거래 이력 기반 제안서 초안 생성 → 담당자에게 미팅 요청. 핵심: 데이터가 '보는 것'에서 '하는 것'으로 바뀐다. 사람이 개입해야 하는 단계가 사라지고, Agent가 직접 실행한다."},
            {"id": "k06", "type": "subjective", "category": "패러다임",
             "question": "'보고에서 실행으로'라는 인핸스의 핵심 가치를 구체적인 영업 시나리오로 고객에게 설명해보세요.",
             "answer_key": "기존: 담당자가 엑셀 열어서 계약 만료일 확인 → 제안서 새로 작성(반나절) → 일정 바쁘면 놓침 → 경쟁사가 먼저 들어와 계약 뺏김. 인핸스: D-60에 Agent가 자동 감지 → 3년 거래 이력 기반 제안서 초안 자동 생성 → 담당자에게 미팅 일정 잡으라고 먼저 알림 → 경쟁사보다 2달 먼저 움직임. 핵심: '이런 상황입니다'(알림)에서 '이 상황이니 이걸 바로 실행합니다'(자동 실행)로 전환."},
            {"id": "k07", "type": "subjective", "category": "영업 대응",
             "question": "기업 DX(디지털 전환) 맥락에서 온톨로지 기반 AI Agent와 RPA(Robotic Process Automation)의 차이를 설명해보세요.",
             "answer_key": "RPA: 규칙 기반 반복 작업 자동화. 화면의 특정 위치를 클릭하는 수준. 프로세스가 조금만 바뀌면 재설정 필요. 예외 상황 처리 어려움. '일을 시키는 로봇'. 온톨로지 기반 AI Agent: 데이터의 의미와 관계를 이해하고 맥락 기반 판단. 예외 상황도 지식사전의 규칙으로 처리. 규칙 변경 시 지식사전 1곳만 수정. '판단하고 행동하는 직원'. 핵심 차이: RPA는 '어떻게 하는지'가 하드코딩, AI Agent는 '무엇을 해야 하는지'를 맥락으로 이해. RPA는 자동화의 영역, AI Agent는 자율화의 영역."},
            {"id": "k08", "type": "subjective", "category": "영업 대응",
             "question": "경쟁사 제품으로 RAG 기반 솔루션을 이미 도입한 고객사에게 인핸스 플랫폼의 도입 필요성을 설명해야 합니다. 어떻게 설득하시겠습니까?",
             "answer_key": "인정에서 시작: RAG는 정보 검색과 문서 기반 Q&A에서 매우 효과적. 이 가치는 인정. 한계 제시: '이 할인 주문이 승인 대상인가?'처럼 여러 조건이 얽힌 판단은 RAG가 일관되게 처리하기 어려움. 고객 등급·상품 카테고리·기간별 예외 조건 등을 동시에 고려해야 할 때 오류 발생. 인핸스 포지션: 경쟁이 아닌 보완 관계. RAG 솔루션은 문서 검색용으로 유지, 인핸스는 판단·실행 레이어로 추가. 두 시스템이 협력하는 구조. 증거: '보고에서 실행으로' 시나리오로 ROI 수치화해 제시."},
            {"id": "k09", "type": "subjective", "category": "영업 대응",
             "question": "고객사에서 여러 부서(영업, 재무, 제조, 마케팅)의 데이터가 각각 다른 시스템에 분산되어 있습니다. 인핸스 플랫폼으로 이를 통합·활용하는 아키텍처를 설계해보세요.",
             "answer_key": "1. Pipeline Builder로 각 부서 시스템(영업CRM, 재무ERP, 제조MES, 마케팅플랫폼) 연결·정규화. 2. Ontology Manager로 부서별 핵심 Object 정의: 영업(고객사, 계약, 파이프라인), 재무(매출, 수금, 원가), 제조(제품, 재고, 납기), 마케팅(캠페인, 전환율). 3. 부서 간 Object를 Link로 연결: 고객사→계약→제품→재고, 계약→매출→수금 등. 4. 지식사전: 부서별 규칙·기준(할인 승인 정책, 재고 경보 기준, VIP 서비스 정책 등). 5. Workflow Builder로 멀티 Agent 구성: 각 부서 담당 Agent + Orchestrator. 6. Dashboard Generation으로 통합 뷰 생성. 거버넌스: 부서별 Object 접근 권한 설정."},
            {"id": "k10", "type": "subjective", "category": "AgentOS 가치",
             "question": "온톨로지 플랫폼이 '기업 지식을 시스템화'한다는 것의 장기적 전략적 가치를 설명해보세요.",
             "answer_key": "단기: 업무 자동화, 처리 속도 향상, 오류 감소. 중기: 1) 조직 지식의 자산화 — 베테랑 퇴사해도 판단 기준·노하우 시스템에 보존. 2) 기준의 진화 — AI가 새 패턴 발견 시 지식사전 업데이트 가능. 3) 부서 간 사일로 해소 — 공통 Object 구조로 협업. 장기: 1) 경쟁 우위 — 기업만의 독자적 지식 그래프가 쌓일수록 AI 정확도 향상. 2) 데이터 전략 자산화 — 온톨로지 자체가 기업의 핵심 IP. 3) 확장성 — 새 업무 도메인 추가 시 기존 Object와 연결만 하면 됨."},
        ],

        "📋 심화 종합": [
            # from ⑥ 데이터 아키텍처 심화
            {"id": "h01", "type": "mc", "category": "아키텍처 비교",
             "question": "3가지 온톨로지 구현 방식 중 기업 기존 인프라 기준으로 마이그레이션 비용이 가장 작은 방식은?",
             "options": ["A) Semantic Web 정통 방식 (RDF/OWL)", "B) GraphDB 방식 (Neo4j 등)", "C) RDB 기반 Semantic Layer 방식 (인핸스 스타일)", "D) 세 방식 모두 동일"],
             "answer": "C",
             "explanation": "RDB 기반 Semantic Layer는 기존 테이블 형태를 그대로 유지하고 위에 레이어만 추가합니다. 훨씬 낮은 전환 비용으로 도입 가능합니다."},
            {"id": "h04", "type": "mc", "category": "아키텍처 비교",
             "question": "인핸스가 RDB 기반 Semantic Layer를 선택한 4가지 이유 중 옳지 않은 것은?",
             "options": ["A) 운영이 쉬움 — 기존 DWH/SQL 생태계 그대로 활용", "B) 빠른 적용 — GraphDB로 전체 마이그레이션 불필요", "C) 정확한 답변 — SQL로 수치 추출 + LLM은 설명만", "D) 완전한 논리 추론 — OWL보다 강력한 추론 엔진 보유"],
             "answer": "D",
             "explanation": "'완전한 논리 추론'은 오히려 OWL/RDF의 강점이며, 인핸스는 실무 적용성과 AI Agent 연결을 우선합니다."},
            {"id": "h05", "type": "mc", "category": "아키텍처 비교",
             "question": "RDB 기반 Semantic Layer에서 수치 관련 할루시네이션을 줄이는 방법은?",
             "options": ["A) 더 많은 학습 데이터를 사용한다", "B) SQL로 수치를 정확히 추출하고, LLM은 설명·요약만 담당한다", "C) 벡터 검색을 개선한다", "D) 더 큰 LLM 모델을 사용한다"],
             "answer": "B",
             "explanation": "SQL로 정확한 수치를 추출하고, LLM은 그 결과를 자연어로 설명하는 역할만 담당하게 해 정확도를 높입니다."},
            {"id": "h07", "type": "subjective", "category": "아키텍처 비교",
             "question": "RDF/OWL의 자동 추론(Reasoning)과 인핸스의 LLM+온톨로지 기반 판단 방식의 차이점을 설명하고, 기업 실무 환경에서 어느 쪽이 더 적합한지 근거와 함께 서술해보세요.",
             "answer_key": "RDF/OWL: 논리 규칙 기반 자동 추론. 완전한 일관성 보장. 단, 모든 규칙을 형식 논리로 미리 정의해야 함. 실무 적용에 전문 지식 필요, 운영 무거움. 인핸스(LLM+온톨로지): Object/Link/지식사전으로 의미·관계 정의 후 LLM이 자연어 기반 판단. 비전문가도 지식사전에 자연어로 규칙 작성 가능. 빠른 도입 가능. 기업 실무 적합성: 인핸스 방식이 더 적합. 이유: 빠른 도입, 비전문가 운영 가능, 기존 RDB 활용, LLM의 유연한 자연어 판단."},
            {"id": "h09", "type": "subjective", "category": "아키텍처 비교",
             "question": "Text-to-SQL의 문제점을 온톨로지가 어떻게 해결하는지 설명해보세요.",
             "answer_key": "Text-to-SQL 문제: AI가 스키마만 보고 컬럼 의미를 추측해야 함. price_a, price_b, final_price 같이 비슷한 컬럼이 여러 개면 잘못 선택. 온톨로지 해결: 각 필드의 의미를 미리 정의해둠('이 필드=최종 청구 금액', '저 필드=제조 원가'). AI가 추측하지 않고 정확한 의미 기반으로 엔티티를 추출해 정확한 SQL 생성 가능."},
            # from ⑦ 멀티 Agent & 워크플로우
            {"id": "i01", "type": "mc", "category": "멀티 Agent",
             "question": "복잡한 업무에서 Orchestrator가 온톨로지 정보를 활용하는 방식은?",
             "options": ["A) 단일 Agent에 모든 작업을 위임", "B) 온톨로지의 Object 관계를 참고해 필요한 여러 Agent를 조합·협업하게 함", "C) 직접 SQL을 실행", "D) 배치 처리로 순차 실행"],
             "answer": "B",
             "explanation": "Orchestrator는 온톨로지의 Object-Link 구조를 이해하고, 복잡한 업무를 처리하기 위해 필요한 여러 전문 Agent를 조합해 협업하게 합니다."},
            {"id": "i03", "type": "mc", "category": "멀티 Agent",
             "question": "관계가 복잡하게 얽힌 데이터(예: 고객사→계약→담당자→제품→재고→납기)에서 인핸스가 강점을 보이는 이유는?",
             "options": ["A) 단순한 데이터에만 적합하기 때문", "B) Object + Link 구조 자체가 복잡한 관계형 데이터를 표현하도록 설계되었기 때문", "C) 다른 시스템보다 서버가 빠르기 때문", "D) 관계를 자동으로 단순화하기 때문"],
             "answer": "B",
             "explanation": "복잡한 관계일수록 Orchestrator가 여러 Object를 조합해 Agent들이 협업하게 하며, 자동화 효과가 더 크게 나옵니다."},
            {"id": "i05", "type": "mc", "category": "Agent 실행",
             "question": "온톨로지 기반에서 '계약 만료 D-60에 Agent가 자동으로 제안서를 생성하는' 흐름의 핵심 구성 요소는?",
             "options": ["A) 이메일 웹훅", "B) Object(계약 만료일) + Link(고객 거래 이력) + 지식사전(제안서 기준) + Agent 자동 판단·실행", "C) 수동 트리거", "D) 캘린더 API"],
             "answer": "B",
             "explanation": "Object에 저장된 계약 만료일을 감지하고, Link를 통해 거래 이력을 참조하며, 지식사전의 제안서 작성 기준을 적용해 Agent가 자동으로 판단하고 실행하는 구조입니다."},
            {"id": "i07", "type": "subjective", "category": "멀티 Agent",
             "question": "멀티 Agent 시스템에서 Orchestrator가 온톨로지 정보를 어떻게 활용하는지, 그리고 이로 인해 단일 Agent 대비 어떤 장점이 생기는지 설명해보세요.",
             "answer_key": "Orchestrator 역할: 온톨로지의 Object-Link 구조를 이해해 복잡한 업무를 분해. 어떤 전문 Agent가 어떤 Object를 처리할지 조합·지시. 단일 Agent 대비 장점: 1) 역할 분리로 각 Agent가 전문성 집중 가능. 2) 병렬 처리 가능. 3) 실패 시 해당 Agent만 재시도. 4) 새 업무 추가 시 새 Agent만 추가."},
            {"id": "i09", "type": "subjective", "category": "Agent 실행",
             "question": "부서 간 데이터가 복잡하게 연결된 환경에서 Agent 자동화의 효과가 더 커지는 이유를 설명하고, 구체적인 시나리오를 하나 들어보세요.",
             "answer_key": "이유: 복잡한 데이터 관계일수록 사람이 수동으로 처리할 때 시간·오류 비용이 크고, Orchestrator가 여러 Agent를 조합해 자동화할 때 절감 효과가 큼. 시나리오 예: '고객 A의 계약 만료 D-60' 감지 → 고객 Agent: 3년 거래 이력 조회 → 계약 Agent: 갱신 조건 분석 → 재고 Agent: 현재 납기 가능 재고 확인 → 영업 Agent: 맞춤 제안서 초안 생성 → 담당자에게 미팅 요청. 이 모든 과정이 사람 개입 없이 자동 실행."},
            # from ⑧ 거버넌스 & Observability
            {"id": "j01", "type": "mc", "category": "Governance",
             "question": "인핸스의 Governance에서 접근 권한을 설정하는 기본 단위는?",
             "options": ["A) 데이터베이스 전체", "B) 테이블 단위", "C) Object 단위", "D) 사용자 그룹 단위만"],
             "answer": "C",
             "explanation": "Object 중심으로 접근 권한을 설정합니다. 예: 재무 Object는 재무팀만 접근 가능."},
            {"id": "j02", "type": "mc", "category": "Observability",
             "question": "Observability(투명성)가 단순한 로그 기록과 다른 가장 큰 이유는?",
             "options": ["A) 더 많은 데이터를 저장해서", "B) AI가 어떤 Object·규칙을 보고 어떤 순서로 판단했는지까지 역추적 가능해서", "C) 실시간 알림을 보내서", "D) 비용을 절감해서"],
             "answer": "B",
             "explanation": "Observability는 AI 의사결정 과정 전체를 역추적할 수 있게 합니다."},
            {"id": "j04", "type": "mc", "category": "Governance",
             "question": "기존 방식의 '기준 운영 한계'를 인핸스가 해결하는 방식은?",
             "options": ["A) 더 강력한 서버 도입", "B) 기준을 지식 사전에 집중 관리하여 변경 시 모든 Agent가 자동 반영", "C) 기준을 코드에 더 체계적으로 문서화", "D) 변경 주기를 제한"],
             "answer": "B",
             "explanation": "기준을 지식 사전 한 곳에 집중 관리해 1번 변경으로 모든 Agent가 자동 반영됩니다."},
            {"id": "j07", "type": "subjective", "category": "Observability",
             "question": "AI 시스템에서 Observability(투명성)가 단순한 로그 기록·모니터링과 근본적으로 다른 이유를 설명하고, 기업 운영 측면에서 이것이 왜 중요한지 서술해보세요.",
             "answer_key": "단순 로그: 시스템 이벤트(에러, 실행 시간 등) 기록. 무슨 일이 일어났는지만 파악. Observability: AI가 어떤 데이터(Object)를 보고, 어떤 규칙(지식사전)을 적용하고, 어떤 순서로 판단해 어떤 액션을 실행했는지 전체 의사결정 과정을 역추적 가능. 기업 운영 중요성: 1) AI 틀린 판단 원인 파악 가능 → 개선 가능. 2) 블랙박스가 아닌 신뢰 가능한 AI 시스템. 3) 감사(Audit)/규제 준수 근거. 4) 책임 소재 명확화."},
            {"id": "j08", "type": "subjective", "category": "Governance",
             "question": "온톨로지 기반 거버넌스가 기존 DB 접근 권한 관리와 다른 점은 무엇인가요?",
             "answer_key": "기존 DB 권한: 테이블/컬럼 단위. 데이터에만 접근 제어. 인핸스 거버넌스: Object 단위 접근 권한 + 지식사전 규칙 변경 이력 + Agent 실행 액션 전체 기록. 누가 어떤 데이터를 봤는지, 어떤 규칙을 썼는지, 무슨 액션을 했는지 비즈니스 맥락까지 추적 가능. 규제 준수(Compliance), 감사(Audit) 관점에서 훨씬 강력."},
            # from ⑨ 영업 & 고객 설득
            {"id": "k01", "type": "mc", "category": "영업 대응",
             "question": "고객이 'AgentOS 도입하면 기존 ERP를 교체해야 하나요?'라고 물을 때 올바른 영업 대응은?",
             "options": ["A) '네, 전부 교체해야 합니다'", "B) '기존 ERP는 그대로 유지하면서, 위에 AgentOS 온톨로지 레이어만 추가합니다. 기존 투자가 그대로 보존됩니다.'", "C) 'ERP와 별개로 새 데이터베이스를 구축해야 합니다'", "D) '클라우드 전환 후에만 도입 가능합니다'"],
             "answer": "B",
             "explanation": "기존 ERP, CRM, Data Warehouse 위에 온톨로지 레이어만 추가합니다. 기존 데이터 자산이 보존되고, 도입 리스크와 비용이 최소화됩니다."},
            {"id": "k02", "type": "mc", "category": "영업 대응",
             "question": "'우리 회사는 이미 RAG 기반 AI를 도입했습니다'라는 고객에게 인핸스를 추가 도입해야 하는 이유를 설명할 때 가장 핵심적인 포인트는?",
             "options": ["A) RAG는 구식 기술이니 교체해야 한다", "B) RAG는 정보 검색에 뛰어나지만, 여러 데이터를 엮어 판단하고 실제 액션을 실행하는 것은 인핸스가 추가로 담당한다", "C) 비용이 더 저렴하다", "D) 더 많은 문서를 처리할 수 있다"],
             "answer": "B",
             "explanation": "경쟁이 아닌 보완 관계입니다. RAG 솔루션을 문서 검색용으로 유지하면서, 인핸스가 판단·실행 레이어로 추가됩니다."},
            {"id": "k03", "type": "mc", "category": "AgentOS 가치",
             "question": "AgentOS E2E(End-to-End) 플랫폼이 의미하는 것은?",
             "options": ["A) 전사 시스템 전체를 교체한다", "B) 데이터 연결부터 온톨로지 구성, Agent 구축, 대시보드 생성, 액션 실행까지 한 플랫폼에서 처리", "C) 모든 산업을 지원한다", "D) 글로벌 엔드포인트를 제공한다"],
             "answer": "B",
             "explanation": "Pipeline Builder → Ontology Manager → Workflow Builder → Dashboard Generation → CUA까지 전 과정을 하나의 플랫폼에서 처리합니다."},
            {"id": "k05", "type": "subjective", "category": "패러다임",
             "question": "AgentOS가 없을 때와 있을 때를 하나의 구체적인 업무 시나리오로 대비해서 고객에게 설명하세요.",
             "answer_key": "없을 때: 데이터는 쌓여 있지만 사람이 직접 열어보고 판단하고 실행 지시. 예) 계약 만료 관리: 담당자가 매일 엑셀 열어 확인 → 바쁘면 놓침 → 경쟁사가 먼저 들어옴. 있을 때: Agent가 온톨로지로 상황 파악 → 지식사전 규칙 적용 → 스스로 판단·실행. 예) D-60 자동 감지 → 거래 이력 기반 제안서 초안 생성 → 담당자에게 미팅 요청. 핵심: 데이터가 '보는 것'에서 '하는 것'으로 바뀐다."},
            {"id": "k06", "type": "subjective", "category": "패러다임",
             "question": "'보고에서 실행으로'라는 인핸스의 핵심 가치를 구체적인 영업 시나리오로 고객에게 설명해보세요.",
             "answer_key": "기존: 담당자가 엑셀 열어서 계약 만료일 확인 → 제안서 새로 작성(반나절) → 일정 바쁘면 놓침 → 경쟁사가 먼저 들어와 계약 뺏김. 인핸스: D-60에 Agent가 자동 감지 → 3년 거래 이력 기반 제안서 초안 자동 생성 → 담당자에게 미팅 일정 잡으라고 먼저 알림 → 경쟁사보다 2달 먼저 움직임. 핵심: '이런 상황입니다'(알림)에서 '이 상황이니 이걸 바로 실행합니다'(자동 실행)로 전환."},
        ],
    },
}


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


# ─────────────────────────────────────────────
# 세션 초기화
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "home",
        "level": None,
        "sub_test": None,
        "questions": [],
        "current_q": 0,
        "answers": {},
        "results": [],
        "api_key": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─────────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 AgentOS 퀴즈")
    st.markdown("---")

    if st.session_state.page == "home":
        st.markdown("**레벨을 선택하고 시작하세요.**")
        st.markdown("""
- **기본**: 회사/제품 개요, 온톨로지 기초, 데이터 연결 & 인프라, AgentOS vs 기존 기술, Agent 실행 개념
- **심화**: 데이터 아키텍처 심화, 멀티 Agent & 워크플로우, 거버넌스 & Observability, 영업 & 고객 설득
""")
    elif st.session_state.page == "quiz":
        level = st.session_state.level or ""
        sub_test = st.session_state.sub_test or ""
        total = len(st.session_state.questions)
        current = st.session_state.current_q + 1
        st.markdown(f"**레벨:** {level}")
        st.markdown(f"**파트:** {sub_test}")
        st.markdown(f"**진행:** {current} / {total}")
        progress = (st.session_state.current_q) / total if total > 0 else 0
        st.progress(progress)
    elif st.session_state.page == "results":
        st.markdown(f"**레벨:** {st.session_state.level or ''}")
        st.markdown(f"**파트:** {st.session_state.sub_test or ''}")
        st.markdown("**결과를 확인하세요.**")

    st.markdown("---")
    st.markdown("<small>Enhans AgentOS Quiz v2.0</small>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 홈 페이지
# ─────────────────────────────────────────────
def show_home():
    if "home_level_radio" not in st.session_state:
        st.session_state.home_level_radio = "기본"

    # Dynamic left panel content
    level_info = {
        "기본": {
            "title": "기본 레벨",
            "subtitle": "AgentOS 핵심 개념 이해",
            "desc": "인핸스 제품과 AgentOS의 기본 개념을 학습합니다.",
            "topics": [
                "① 회사 & 제품 개요",
                "② 온톨로지 기초",
                "③ 데이터 연결 & 인프라",
                "④ AgentOS vs 기존 기술",
                "⑤ Agent 실행 개념",
                "📋 기본 종합",
            ],
            "total_q": "파트당 10문제 (종합 20문제)",
            "badge": "BASIC",
        },
        "심화": {
            "title": "심화 레벨",
            "subtitle": "고급 아키텍처 & 영업 설득",
            "desc": "데이터 아키텍처, 멀티 Agent, 거버넌스, 영업 전략을 심층 학습합니다.",
            "topics": [
                "⑥ 데이터 아키텍처 심화",
                "⑦ 멀티 Agent & 워크플로우",
                "⑧ 거버넌스 & Observability",
                "⑨ 영업 & 고객 설득",
                "📋 심화 종합",
            ],
            "total_q": "파트당 10문제 (종합 20문제)",
            "badge": "ADVANCED",
        },
    }

    # 위젯 키에서 직접 읽어야 라디오 선택 즉시 왼쪽 패널이 반영됨
    sel_level = st.session_state.get("home_level_radio_widget", st.session_state.home_level_radio)
    info = level_info[sel_level]

    # Build topics HTML — use div/span (not li/p) to avoid CSS !important override on dark bg
    topics_html = "".join([
        f'<div style="color: rgba(255,255,255,0.8); font-size: 0.88rem; line-height: 1.8; margin-bottom: 2px;">• {t}</div>'
        for t in info["topics"]
    ])

    left_html = f"""
<div class="home-left">
  <div style="margin-bottom: 20px;">
    <span style="background: rgba(255,255,255,0.2); color: #fff; font-size: 11px; font-weight: 700;
                 letter-spacing: 2px; padding: 4px 12px; border-radius: 20px;">{info['badge']}</span>
  </div>
  <div style="color: #fff; font-size: 2rem; font-weight: 800; margin-bottom: 8px; line-height: 1.2;">{info['title']}</div>
  <div style="color: rgba(255,255,255,0.85); font-size: 1rem; margin-bottom: 24px;">{info['subtitle']}</div>
  <div style="color: rgba(255,255,255,0.75); font-size: 0.9rem; margin-bottom: 28px; line-height: 1.6;">{info['desc']}</div>
  <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
    <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 700; margin-bottom: 12px; letter-spacing: 1px;">📚 포함 파트</div>
    <div style="padding-left: 4px;">
      {topics_html}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px;">
    <div style="color: rgba(255,255,255,0.7); font-size: 0.82rem;">📝 {info['total_q']}</div>
  </div>
</div>
"""

    col_left, col_right = st.columns([5, 4], gap="large")

    with col_left:
        st.markdown(left_html, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="home-right-header"><div style="font-size:1.1em; font-weight:800; color:#0F172A; margin:0 0 5px;">퀴즈 시작</div><div style="font-size:0.81em; color:#94A3B8; margin:0 0 22px; line-height:1.5;">레벨과 파트를 선택하고 시작하세요</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="home-right-form">', unsafe_allow_html=True)

        level_sel = st.radio(
            "**레벨 선택**",
            options=["기본", "심화"],
            index=0 if st.session_state.home_level_radio == "기본" else 1,
            horizontal=True,
            key="home_level_radio_widget",
        )
        # sync
        st.session_state.home_level_radio = level_sel

        # Sub-test selectbox based on selected level
        sub_tests = list(QUIZ_DATA[level_sel].keys())
        sub_test_sel = st.selectbox(
            "**파트 선택**",
            options=sub_tests,
            index=0,
            key="home_sub_test_widget",
        )

        api_key = st.text_input(
            "**Anthropic API Key**",
            type="password",
            placeholder="sk-ant-...",
            value=st.session_state.api_key,
            key="home_api_key_widget",
        )

        st.markdown("---")

        if st.button("🚀 퀴즈 시작", use_container_width=True, key="start_btn"):
            if not api_key.strip():
                st.error("API Key를 입력해주세요.")
            else:
                questions = QUIZ_DATA[level_sel][sub_test_sel].copy()
                st.session_state.level = level_sel
                st.session_state.sub_test = sub_test_sel
                st.session_state.questions = questions
                st.session_state.api_key = api_key.strip()
                st.session_state.current_q = 0
                st.session_state.answers = {}
                st.session_state.results = []
                st.session_state.page = "quiz"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 퀴즈 페이지
# ─────────────────────────────────────────────
def show_quiz():
    questions = st.session_state.questions
    idx = st.session_state.current_q

    if idx >= len(questions):
        st.session_state.page = "results"
        st.rerun()
        return

    q = questions[idx]
    total = len(questions)
    level = st.session_state.level
    sub_test = st.session_state.sub_test

    # Header
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
            padding: 20px 28px; border-radius: 14px; margin-bottom: 24px;
            display: flex; justify-content: space-between; align-items: center;">
  <div>
    <span style="color: rgba(255,255,255,0.6); font-size: 0.8rem; font-weight: 600; letter-spacing: 1px;">{level} · {sub_test}</span>
    <div style="color: #fff; margin: 4px 0 0 0; font-size: 1.1rem; font-weight: 700;">문제 {idx + 1} / {total}</div>
  </div>
  <div style="background: rgba(255,255,255,0.15); border-radius: 50px; padding: 6px 16px;">
    <span style="color: #fff; font-size: 0.85rem; font-weight: 600;">
      {"객관식" if q["type"] == "mc" else "주관식"}
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

    # Progress bar
    progress_pct = int((idx / total) * 100)
    st.markdown(f"""
<div style="background: #E2E8F0; border-radius: 6px; height: 6px; margin-bottom: 28px;">
  <div style="background: linear-gradient(90deg, #3B82F6, #6366F1); height: 100%;
              width: {progress_pct}%; border-radius: 6px; transition: width 0.3s;"></div>
</div>
""", unsafe_allow_html=True)

    # Category badge
    category = q.get("category", "")
    if category:
        st.markdown(f'<span style="background:#EFF6FF; color:#3B82F6; font-size:0.78rem; font-weight:600; padding:3px 10px; border-radius:20px; border:1px solid #BFDBFE;">{category}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Question
    st.markdown(f'<div class="question-text">{q["question"]}</div>', unsafe_allow_html=True)

    # Answer input
    if q["type"] == "mc":
        options = q["options"]
        option_labels = [opt for opt in options]
        existing = st.session_state.answers.get(q["id"], None)
        existing_idx = None
        if existing is not None:
            for i, opt in enumerate(options):
                if opt.startswith(existing):
                    existing_idx = i
                    break

        selected = st.radio(
            "선택지",
            options=option_labels,
            index=existing_idx,
            label_visibility="collapsed",
            key=f"mc_{q['id']}",
        )

        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("다음 →", use_container_width=True, key=f"next_{q['id']}"):
                if selected:
                    # Extract letter (A/B/C/D)
                    answer_letter = selected[0] if selected else ""
                    st.session_state.answers[q["id"]] = answer_letter
                    correct = q["answer"]
                    is_correct = answer_letter == correct

                    result = {
                        "id": q["id"],
                        "type": "mc",
                        "question": q["question"],
                        "user_answer": selected,
                        "correct_answer": next((o for o in options if o.startswith(correct)), correct),
                        "is_correct": is_correct,
                        "explanation": q.get("explanation", ""),
                        "score": 10 if is_correct else 0,
                        "max_score": 10,
                    }
                    st.session_state.results.append(result)
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.warning("선택지를 선택해주세요.")

    else:  # subjective
        existing_text = st.session_state.answers.get(q["id"], "")
        user_answer = st.text_area(
            "답변을 입력하세요",
            value=existing_text,
            height=160,
            placeholder="여기에 답변을 입력하세요...",
            key=f"subj_{q['id']}",
        )

        answer_key = q.get("answer_key", q.get("answer", ""))

        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("제출 & 다음 →", use_container_width=True, key=f"submit_{q['id']}"):
                st.session_state.answers[q["id"]] = user_answer
                with st.spinner("AI가 답변을 평가 중입니다..."):
                    eval_result = evaluate_subjective_answer(
                        question=q["question"],
                        user_answer=user_answer,
                        answer_key=answer_key,
                        level=level,
                        api_key=st.session_state.api_key,
                    )
                result = {
                    "id": q["id"],
                    "type": "subjective",
                    "question": q["question"],
                    "user_answer": user_answer,
                    "answer_key": answer_key,
                    "score": eval_result.get("score", 0),
                    "max_score": 10,
                    "grade": eval_result.get("grade", ""),
                    "correct_points": eval_result.get("correct_points", ""),
                    "improvement": eval_result.get("improvement", ""),
                    "key_insight": eval_result.get("key_insight", ""),
                }
                st.session_state.results.append(result)
                st.session_state.current_q += 1
                st.rerun()


# ─────────────────────────────────────────────
# 결과 페이지
# ─────────────────────────────────────────────
def show_results():
    results = st.session_state.results
    level = st.session_state.level
    sub_test = st.session_state.sub_test

    total_score = sum(r["score"] for r in results)
    total_max = sum(r["max_score"] for r in results)
    mc_results = [r for r in results if r["type"] == "mc"]
    subj_results = [r for r in results if r["type"] == "subjective"]
    mc_correct = sum(1 for r in mc_results if r.get("is_correct", False))

    pct = int((total_score / total_max * 100)) if total_max > 0 else 0

    if pct >= 80:
        grade_text, grade_color = "우수", "#10B981"
    elif pct >= 60:
        grade_text, grade_color = "양호", "#3B82F6"
    elif pct >= 40:
        grade_text, grade_color = "보통", "#F59E0B"
    else:
        grade_text, grade_color = "학습 필요", "#EF4444"

    # Summary card
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
            border-radius: 20px; padding: 36px; text-align: center; margin-bottom: 32px;">
  <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; letter-spacing: 1px; margin-bottom: 8px;">
    {level} · {sub_test}
  </div>
  <div style="color: #fff; font-size: 3.5rem; font-weight: 900; margin: 0 0 8px 0; line-height: 1;">
    {total_score}<span style="font-size: 1.5rem; opacity: 0.7;">/{total_max}</span>
  </div>
  <div style="background: {grade_color}; color: #fff; display: inline-block;
              padding: 6px 24px; border-radius: 50px; font-weight: 700; font-size: 1rem; margin-bottom: 20px;">
    {grade_text} · {pct}%
  </div>
  <div style="display: flex; justify-content: center; gap: 32px; margin-top: 8px;">
    <div style="color: rgba(255,255,255,0.8);">
      <div style="font-size: 1.5rem; font-weight: 800;">{mc_correct}/{len(mc_results)}</div>
      <div style="font-size: 0.78rem; opacity: 0.6; margin-top: 2px;">객관식 정답</div>
    </div>
    <div style="color: rgba(255,255,255,0.8);">
      <div style="font-size: 1.5rem; font-weight: 800;">{sum(r['score'] for r in subj_results)}/{sum(r['max_score'] for r in subj_results) if subj_results else 0}</div>
      <div style="font-size: 0.78rem; opacity: 0.6; margin-top: 2px;">주관식 점수</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 풀기", use_container_width=True, key="retry_btn"):
            questions = QUIZ_DATA[level][sub_test].copy()
            st.session_state.questions = questions
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.results = []
            st.session_state.page = "quiz"
            st.rerun()
    with col2:
        if st.button("🏠 홈으로", use_container_width=True, key="home_btn"):
            st.session_state.page = "home"
            st.session_state.level = None
            st.session_state.sub_test = None
            st.session_state.questions = []
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.results = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 문제별 상세 결과")

    for i, r in enumerate(results):
        q_num = i + 1
        if r["type"] == "mc":
            is_correct = r.get("is_correct", False)
            status_icon = "✅" if is_correct else "❌"
            status_bg = "#F0FDF4" if is_correct else "#FFF1F2"
            status_border = "#86EFAC" if is_correct else "#FECDD3"
            status_text = "정답" if is_correct else "오답"

            st.markdown(f"""
<div style="background: {status_bg}; border: 1px solid {status_border};
            border-radius: 14px; padding: 20px; margin-bottom: 16px;">
  <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
    <div style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">Q{q_num}. {r['question']}</div>
    <span style="background: {'#22C55E' if is_correct else '#EF4444'}; color: #fff; font-size: 0.75rem;
                 padding: 3px 10px; border-radius: 20px; font-weight: 700; white-space: nowrap; margin-left: 12px;">
      {status_icon} {status_text}
    </span>
  </div>
  <div style="font-size: 0.85rem; color: #475569; margin-bottom: 6px;">
    <strong>내 답변:</strong> {r['user_answer']}
  </div>
  {'<div style="font-size: 0.85rem; color: #059669; margin-bottom: 6px;"><strong>정답:</strong> ' + r['correct_answer'] + '</div>' if not is_correct else ''}
  <div style="font-size: 0.83rem; color: #64748B; background: rgba(0,0,0,0.04);
              border-radius: 8px; padding: 10px 14px; margin-top: 8px; line-height: 1.6;">
    💡 {r.get('explanation', '')}
  </div>
</div>
""", unsafe_allow_html=True)

        else:  # subjective
            score = r.get("score", 0)
            max_s = r.get("max_score", 10)
            grade = r.get("grade", "")
            grade_colors = {"완전 이해": "#10B981", "양호": "#3B82F6", "부분적 이해": "#F59E0B", "개선 필요": "#EF4444", "미응답": "#94A3B8", "평가 오류": "#94A3B8"}
            g_color = grade_colors.get(grade, "#94A3B8")

            st.markdown(f"""
<div style="background: #F8FAFC; border: 1px solid #E2E8F0;
            border-radius: 14px; padding: 20px; margin-bottom: 16px;">
  <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
    <div style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">Q{q_num}. {r['question']}</div>
    <div style="text-align: right; white-space: nowrap; margin-left: 12px;">
      <span style="background: {g_color}; color: #fff; font-size: 0.75rem;
                   padding: 3px 10px; border-radius: 20px; font-weight: 700;">{grade}</span>
      <div style="color: #1E293B; font-weight: 800; font-size: 1.1rem; margin-top: 4px;">{score}/{max_s}</div>
    </div>
  </div>
  <div style="font-size: 0.84rem; color: #475569; background: #fff; border-radius: 8px;
              padding: 10px 14px; border: 1px solid #E2E8F0; margin-bottom: 12px; line-height: 1.6;">
    <strong>내 답변:</strong><br>{r.get('user_answer', '(미입력)') or '(미입력)'}
  </div>
""", unsafe_allow_html=True)

            if r.get("correct_points"):
                st.markdown(f"""
  <div style="font-size: 0.83rem; color: #059669; background: #F0FDF4; border-radius: 8px;
              padding: 10px 14px; border: 1px solid #86EFAC; margin-bottom: 8px; line-height: 1.6;">
    ✅ <strong>잘한 점:</strong> {r['correct_points']}
  </div>
""", unsafe_allow_html=True)

            if r.get("improvement"):
                st.markdown(f"""
  <div style="font-size: 0.83rem; color: #92400E; background: #FFFBEB; border-radius: 8px;
              padding: 10px 14px; border: 1px solid #FDE68A; margin-bottom: 8px; line-height: 1.6;">
    📝 <strong>보완할 점:</strong> {r['improvement']}
  </div>
""", unsafe_allow_html=True)

            if r.get("key_insight"):
                st.markdown(f"""
  <div style="font-size: 0.83rem; color: #1E40AF; background: #EFF6FF; border-radius: 8px;
              padding: 10px 14px; border: 1px solid #BFDBFE; margin-bottom: 0; line-height: 1.6;">
    💡 <strong>핵심 인사이트:</strong> {r['key_insight']}
  </div>
""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 라우터
# ─────────────────────────────────────────────
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "quiz":
    show_quiz()
elif st.session_state.page == "results":
    show_results()
