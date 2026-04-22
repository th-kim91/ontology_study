import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import hashlib


def _hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def sheets_configured():
    try:
        _ = st.secrets["gcp_service_account"]
        _ = st.secrets["sheets"]["spreadsheet_id"]
        return True
    except Exception:
        return False


def _get_client():
    try:
        creds_info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception:
        return None


def _get_or_create_worksheet(spreadsheet, title, headers):
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows=2000, cols=len(headers))
        ws.append_row(headers)
    return ws


def save_quiz_result(name, level, sub_test, results):
    """퀴즈 결과를 Google Sheets에 저장. 성공 시 True, 실패 시 False."""
    client = _get_client()
    if client is None:
        return False
    try:
        sheet_id = st.secrets["sheets"]["spreadsheet_id"]
        spreadsheet = client.open_by_key(sheet_id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        total_score = sum(r["score"] for r in results)
        total_max = sum(r["max_score"] for r in results)
        pct = round(total_score / total_max * 100, 1) if total_max > 0 else 0

        results_ws = _get_or_create_worksheet(
            spreadsheet, "results",
            ["이름", "날짜", "레벨", "파트", "총점", "최대점수", "백분율"],
        )
        results_ws.append_row([name, now, level, sub_test, total_score, total_max, pct])

        details_ws = _get_or_create_worksheet(
            spreadsheet, "details",
            ["이름", "날짜", "문제ID", "카테고리", "유형", "정답여부", "획득점수", "최대점수", "문제내용", "내답변"],
        )
        for r in results:
            if r["type"] == "mc":
                correct_str = "O" if r.get("is_correct", False) else "X"
            else:
                score = r.get("score", 0)
                correct_str = "O" if score >= 8 else ("△" if score >= 5 else "X")
            details_ws.append_row([
                name, now, r["id"],
                r.get("category", ""),
                "객관식" if r["type"] == "mc" else "주관식",
                correct_str,
                r["score"],
                r["max_score"],
                r.get("question", ""),
                r.get("user_answer", ""),
            ])
        return True
    except Exception:
        return False


def get_all_results():
    """모든 결과 반환. (results 리스트, details 리스트) 또는 실패 시 (None, None)."""
    client = _get_client()
    if client is None:
        return None, None
    try:
        sheet_id = st.secrets["sheets"]["spreadsheet_id"]
        spreadsheet = client.open_by_key(sheet_id)

        try:
            results_data = spreadsheet.worksheet("results").get_all_records()
        except gspread.WorksheetNotFound:
            results_data = []

        try:
            details_data = spreadsheet.worksheet("details").get_all_records()
        except gspread.WorksheetNotFound:
            details_data = []

        return results_data, details_data
    except Exception:
        return None, None


def verify_user(name, password):
    """이름 + 비밀번호 검증. True/False 반환."""
    client = _get_client()
    if client is None:
        return False
    try:
        sheet_id = st.secrets["sheets"]["spreadsheet_id"]
        ws = client.open_by_key(sheet_id).worksheet("users")
        hashed = _hash_pw(password)
        for r in ws.get_all_records():
            if r["이름"] == name and str(r["비밀번호"]) == hashed:
                return True
        return False
    except Exception:
        return False


def update_password(name, new_password):
    """비밀번호 변경. True/False 반환."""
    client = _get_client()
    if client is None:
        return False
    try:
        sheet_id = st.secrets["sheets"]["spreadsheet_id"]
        ws = client.open_by_key(sheet_id).worksheet("users")
        records = ws.get_all_records()
        hashed = _hash_pw(new_password)
        for i, r in enumerate(records):
            if r["이름"] == name:
                ws.update_cell(i + 2, 2, hashed)
                return True
        return False
    except Exception:
        return False
