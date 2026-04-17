"""
Natural Language Processing for HRMS Chatbot.
Classifies question types and extracts entities (army numbers, companies, dates, ranks, etc.).
Understands military terminology: JCO, OR, AL, CL, TOS, TORS, company names, synonyms.
"""
import re
from datetime import datetime, timedelta

# Question type constants
TYPE_PERSONNEL_LOOKUP = "personnel_lookup"       # Show details for army number / name
TYPE_COMPANY_COUNT = "company_count"             # How many in company / each company
TYPE_LEAVE_STATUS = "leave_status"               # Leave status, who on leave
TYPE_LEAVE_BALANCE = "leave_balance"             # Leave balance for person
TYPE_WEIGHT_FITNESS = "weight_fitness"           # Fit/unfit count, weight analysis
TYPE_LOAN_QUERY = "loan_query"                   # Loans by type, person, company
TYPE_TASK_QUERY = "task_query"                   # Pending tasks, by assignee
TYPE_FAMILY = "family_lookup"                    # Family of person
TYPE_COURSES = "courses_lookup"                  # Courses by person
TYPE_PARADE_STATE = "parade_state"               # Parade state, attendance
TYPE_ANALYTICAL = "analytical"                   # Comparisons, averages, trends
TYPE_SCHEMA = "schema"                           # What tables/columns exist
TYPE_PERSONNEL_LIST_COMPANY = "personnel_list_company"  # Who is in company / list personnel
TYPE_DASHBOARD_SUMMARY = "dashboard_summary"     # High-level CO dashboard-style summary
TYPE_GENERAL = "general"                         # Fallback

# Synonyms and normalizations
COMPANY_PATTERNS = [
    (r"\b1\s*company\b", "1 Company"),
    (r"\b2\s*company\b", "2 Company"),
    (r"\b3\s*company\b", "3 Company"),
    (r"\bhq\s*company\b", "HQ company"),
    (r"\bheadquarters\b", "HQ company"),
    (r"\bcompany\s*1\b", "1 Company"),
    (r"\bcompany\s*2\b", "2 Company"),
    (r"\bcompany\s*3\b", "3 Company"),
]
RANK_PATTERNS = [
    r"\bJCO\b", r"\bOR\b", r"\bHAV\b", r"\bNK\b", r"\bL\s*NK\b", r"\bNaib\s*Subedar\b",
    r"\bSubedar\b", r"\bAgniveer\b", r"\bSignal\s*Man\b", r"\bNCO\b", r"\bOC\b", r"\bCO\b",
]
LEAVE_TYPES = ["AL", "CL", "AAL", "leave", "casual", "annual"]
DATE_PATTERN = re.compile(
    r"\b(\d{4})-(\d{2})-(\d{2})\b|"  # 2026-01-15
    r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b|"  # 15/01/2026
    r"\b(today|yesterday|tomorrow)\b",
    re.I
)
# Army number: JC457693, 15740527W, 778G, 156WE, A4203413X - letters and digits, typically 6-12 chars
ARMY_NUMBER_PATTERN = re.compile(
    r"\b([A-Z]{0,2}\d{4,10}[A-Z]?|[A-Z]\d{5,9}[A-Z]?|\d{3,8}[A-Z]{1,2})\b",
    re.I
)
# Also capture "army number XXXXX" so we get the token after "army number"
ARMY_NUMBER_AFTER_PHRASE = re.compile(
    r"\barmy\s*number\s+([A-Za-z0-9]+)\b",
    re.I
)


def _normalize_company(text):
    for pat, repl in COMPANY_PATTERNS:
        if re.search(pat, text, re.I):
            return repl
    return None


def _extract_army_number(text):
    # First try "army number XXXXX" - captures any alphanumeric after the phrase
    m = ARMY_NUMBER_AFTER_PHRASE.search(text)
    if m:
        return m.group(1).strip()
    m = ARMY_NUMBER_PATTERN.search(text)
    if m:
        return m.group(1).strip()
    return None


def _extract_date(text):
    m = DATE_PATTERN.search(text)
    if not m:
        return None
    g = m.groups()
    if g[6]:  # today/yesterday/tomorrow
        today = datetime.now().date()
        if g[6].lower() == "today":
            return today
        if g[6].lower() == "yesterday":
            return today - timedelta(days=1)
        if g[6].lower() == "tomorrow":
            return today + timedelta(days=1)
    if g[0]:  # 2026-01-15
        return datetime(int(g[0]), int(g[1]), int(g[2])).date()
    if g[3]:  # d/m/y
        day, month, year = int(g[3]), int(g[4]), int(g[5])
        if year < 100:
            year += 2000
        return datetime(year, month, day).date()
    return None


def _extract_rank(text):
    for r in RANK_PATTERNS:
        if re.search(r, text, re.I):
            return re.search(r, text, re.I).group(0).strip()
    return None


def classify_question(question):
    """
    Classify question and extract entities.
    Returns: dict with keys: type, army_number, company, date, rank, leave_type, name_hint, raw_question
    """
    q = (question or "").strip()
    q_lower = q.lower()
    entities = {
        "type": TYPE_GENERAL,
        "army_number": None,
        "company": None,
        "date": None,
        "rank": None,
        "leave_type": None,
        "name_hint": None,
        "raw_question": q,
    }

    # Army number / personnel lookup
    army = _extract_army_number(q)
    if army:
        entities["army_number"] = army

    # Company
    company = _normalize_company(q)
    if company:
        entities["company"] = company

    # Date
    dt = _extract_date(q)
    if dt:
        entities["date"] = dt

    # Rank
    rank = _extract_rank(q)
    if rank:
        entities["rank"] = rank

    # Leave type
    for lt in LEAVE_TYPES:
        if lt.lower() in q_lower:
            entities["leave_type"] = "AL" if lt in ("AL", "annual", "leave") else ("CL" if lt in ("CL", "casual") else lt)
            break

    # Question type classification (order matters)
    if re.search(r"\b(details?|info|information|show|get|find|look\s*up|who\s+is)\b.*(army\s*number|778G|156WE|\d{5,})", q_lower) or (army and re.search(r"\b(show|details?|info|about)\b", q_lower)):
        entities["type"] = TYPE_PERSONNEL_LOOKUP
        return entities
    if re.search(r"\b(who\s+is\s+in|list\s+(all\s+)?(personnel|soldiers?|troops?|persons?|people|members?)|names?\s+in)\s+.*company\b", q_lower) or re.search(r"\b(personnel|persons?|people|members?)\s+in\s+(\d|one|two|three|1|2|3|hq)\s*company\b", q_lower):
        entities["type"] = TYPE_PERSONNEL_LIST_COMPANY
        if not company:
            company = _normalize_company(q)
            entities["company"] = company
        return entities
    if re.search(r"\bhow\s+many\s+(personnel|soldiers?|troops?|people|persons?|members?)\b", q_lower) or re.search(r"\b(count|number\s+of)\s+(personnel|persons?|people|in\s+company)\b", q_lower) or re.search(r"\b(personnel|persons?|people)\s+in\s+(each\s+)?company\b", q_lower) or re.search(r"\bhow\s+many\s+(persons?|people)\s+(are\s+there\s+)?in\s+.*company\b", q_lower):
        entities["type"] = TYPE_COMPANY_COUNT
        if not company:
            company = _normalize_company(q)
            entities["company"] = company
        return entities
    if re.search(r"\bleave\s*(status|balance|details?)\b|\bon\s+leave\b|who\s+is\s+on\s+leave|leave\s+for\s+army", q_lower) or (entities["leave_type"] and "balance" in q_lower):
        entities["type"] = TYPE_LEAVE_STATUS if "balance" not in q_lower else TYPE_LEAVE_BALANCE
        return entities
    if re.search(r"\bfamily|dependent|children|kin\b", q_lower) and (army or "army" in q_lower):
        entities["type"] = TYPE_FAMILY
        return entities
    if re.search(r"\bcourse[s]?|training\s*(completed|history)\b", q_lower) and (army or "army" in q_lower):
        entities["type"] = TYPE_COURSES
        return entities
    if re.search(r"\b(weight|fit|unfit|fitness|shape|category)\b", q_lower):
        entities["type"] = TYPE_WEIGHT_FITNESS
        return entities
    if re.search(r"\bloan[s]?|home\s*loan|personal\s*loan\b", q_lower):
        entities["type"] = TYPE_LOAN_QUERY
        return entities
    if re.search(r"\btask[s]?|pending\s*task|assigned\s*to\b", q_lower):
        entities["type"] = TYPE_TASK_QUERY
        return entities
    if re.search(r"\bparade\s*state|attendance|present\s*today\b", q_lower):
        entities["type"] = TYPE_PARADE_STATE
        return entities
    if re.search(r"\b(average|compare|trend|highest|lowest|total\s*amount)\b", q_lower):
        entities["type"] = TYPE_ANALYTICAL
        return entities
    if re.search(r"\btable[s]?|schema|column[s]?|database\s*structure\b", q_lower):
        entities["type"] = TYPE_SCHEMA
        return entities
    # Explicit request for CO dashboard-style overview
    if "dashboard" in q_lower or "co dashboard" in q_lower or "overall status" in q_lower:
        entities["type"] = TYPE_DASHBOARD_SUMMARY
        return entities

    # Default: if we have army number, treat as personnel lookup
    if army:
        entities["type"] = TYPE_PERSONNEL_LOOKUP
    return entities
