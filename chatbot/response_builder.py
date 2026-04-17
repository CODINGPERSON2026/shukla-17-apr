"""
Response Builder for HRMS Chatbot.
Formats query results as clear text/markdown: tables, bullet points, headers.
Masks sensitive data (UID, full bank/account numbers).
"""
from datetime import date, datetime

# Columns to mask (show partial only)
MASK_COLUMNS = {"uid_no", "aadhar_card_no", "pan_card_no", "joint_account_no", "kin_account_no"}


def _mask_value(col_name, value):
    if value is None or value == "":
        return "—"
    if col_name in MASK_COLUMNS or "account" in col_name.lower() or "uid" in col_name.lower():
        s = str(value).strip()
        if len(s) > 4:
            return "XXXX" + s[-4:]
        return "XXXX"
    return value


def _format_cell(val):
    if val is None:
        return "—"
    if isinstance(val, (date, datetime)):
        return str(val)
    if isinstance(val, float):
        return str(round(val, 2)) if val == val else "—"  # avoid NaN
    return str(val)


def format_result(rows, question_type, query_meta=None):
    """
    Format list of dicts (rows) into a readable response string.
    query_meta: optional dict with keys like title, total, etc.
    """
    if not rows:
        return "No records found."
    meta = query_meta or {}
    title = meta.get("title", "Result")
    lines = ["**" + title + "**", ""]

    # Single row (e.g. personnel lookup)
    if len(rows) == 1 and question_type == "personnel_lookup":
        r = rows[0]
        lines.append("| Field | Value |")
        lines.append("|------|-------|")
        for k, v in r.items():
            if v is None or str(v).strip() == "":
                continue
            val = _mask_value(k, _format_cell(v))
            lines.append("| " + str(k).replace("_", " ").title() + " | " + str(val) + " |")
        return "\n".join(lines)

    # Count/aggregation (e.g. company count, leave status count)
    if question_type in ("company_count", "leave_status", "weight_fitness") and len(rows) <= 20:
        if "count" in (rows[0] or {}):
            total = sum((r.get("count") or 0) for r in rows)
            for r in rows:
                label = r.get("company") or r.get("request_status") or r.get("status_type") or r.get("loan_type") or "—"
                cnt = r.get("count", 0)
                lines.append("• **" + str(label) + "**: " + str(cnt))
            if total and question_type == "company_count":
                lines.append("")
                lines.append("**Total: " + str(total) + " personnel**")
            return "\n".join(lines)

    # Loan type summary (aggregate)
    if question_type == "loan_query" and rows and ("total" in (rows[0] or {}) or "total_amount" in (rows[0] or {})):
        for r in rows:
            lt = r.get("loan_type", "—")
            cnt = r.get("count", r.get("loan_count", 0))
            tot = r.get("total") or r.get("total_amount")
            tot_str = "₹" + str(round(float(tot), 0)) if tot is not None else "—"
            lines.append("• **" + str(lt) + "**: " + str(cnt) + " loan(s), Total " + tot_str)
        return "\n".join(lines)

    # CO dashboard-style summary: turn single-row metrics into bullet list
    if question_type == "dashboard_summary" and len(rows) == 1:
        r = rows[0] or {}
        lines = ["**CO dashboard summary (live)**", ""]
        mapping = [
            ("detachments", "Personnel on detachment"),
            ("officerCount", "Officers present"),
            ("jcoCount", "JCOs present"),
            ("orCount", "ORs present"),
            ("interview_pending_count", "Pending kunba interviews"),
            ("interview_total_count", "Total personnel for interviews"),
            ("projects", "Projects"),
            ("sensitive_count", "Sensitive individuals"),
            ("boards_count", "Boards (BOOs)"),
            ("attachment_count", "TD / attachments"),
            ("courses_count", "Personnel on courses"),
            ("loan_count", "Active loans"),
            ("roll_call_pending_points", "Pending roll call points"),
            ("total_tasks", "Total tasks assigned to you"),
            ("pending_tasks", "Pending tasks for you"),
            ("agniveer_count", "Agniveers in unit"),
        ]
        for key, label in mapping:
            if key in r:
                lines.append("• **" + label + "**: " + _format_cell(r.get(key)))
        return "\n".join(lines)

    # Table format for multiple rows
    keys = list(rows[0].keys()) if rows else []
    header = "| " + " | ".join(k.replace("_", " ").title() for k in keys) + " |"
    sep = "|" + "|".join("---" for _ in keys) + "|"
    lines.append(header)
    lines.append(sep)
    for r in rows[:50]:  # cap at 50 rows
        cells = [_format_cell(_mask_value(k, r.get(k))) for k in keys]
        lines.append("| " + " | ".join(cells) + " |")
    if len(rows) > 50:
        lines.append("")
        lines.append("*... and " + str(len(rows) - 50) + " more rows.*")
    return "\n".join(lines)


def format_schema(schema_text):
    """Format raw schema info for display."""
    return "**Database schema (live):**\n\n" + schema_text


def format_clarification(message):
    """Ask user to clarify."""
    return "**Clarification:** " + message


def format_error(message, suggestion=None):
    """Format error with optional suggestion."""
    out = "Sorry, I couldn't complete that: " + str(message)
    if suggestion:
        out += "\n\n*Suggestion: " + suggestion + "*"
    return out
