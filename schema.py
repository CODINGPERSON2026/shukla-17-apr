"""
HRMS Database Schema Definition
Users Table + Personnel Table
"""
import re

# ==========================================================
# USERS TABLE SCHEMA
# ==========================================================

USERS_SCHEMA = """
Table: users
Purpose: Stores system login and role information for HRMS users.

Columns:
- id (int, primary key, auto increment)
- username (varchar(100), unique username for login)
- email (varchar(150), user email address)
- password (varchar(255), encrypted - NEVER SELECT THIS)
- role (varchar(50), military or system role)
- created_at (timestamp, account creation date)
- company (varchar(100), assigned company)
- army_number (varchar(100), NULL for officers)

VALID ROLE VALUES:
Commissioned Officers  : CO, OC, 2IC, ADJUTANT
JCO Roles             : JCO, S/JCO, JCO PWR, JCO CHQ, JCO IT, JCO MW, JCO LINE, JCO OP, JCO MCCS, JCO RHQ, JCO TM, JCO MT, JCO LRW, JA JCO, ACCOUNT JCO, PROJECT JCO
NCO Roles             : NCO, ONCO, NCO PWR, NCO CHQ, NCO IT, NCO MW, NCO LINE, NCO OP, NCO MCCS, NCO RHQ, NCO LRW, NCO QM, NCO MT, NCO TM, NCO RP
Other Roles           : admin, clerk, TRG, QM, HEAD CLK, PA, ACCOUNT OFFICER, PROJECT OFFICER, CENTRE

COMPANY VALUES:
- '1 Company'
- '2 Company'
- '3 Company'
- 'HQ Company'

IMPORTANT:
- NEVER select password column
- Only return username, role and company unless specifically asked for more
- Role matching is case sensitive in DB

EXAMPLE QUERIES:

Q: who is co
SQL: SELECT username, role, company FROM users WHERE role = 'CO'

Q: who is oc of 1 coy
SQL: SELECT username, role, company FROM users WHERE role = 'OC' AND company = '1 Company'

Q: how many nco are there
SQL: SELECT COUNT(*) FROM users WHERE role LIKE 'NCO%'

Q: who is nco
SQL: SELECT username, role, company FROM users WHERE role LIKE 'NCO%'

Q: who is jco
SQL: SELECT username, role, company FROM users WHERE role LIKE 'JCO%'

Q: how many jco in 2 coy
SQL: SELECT COUNT(*) FROM users WHERE role LIKE 'JCO%' AND company = '2 Company'

Q: how many users are there
SQL: SELECT COUNT(*) FROM users

Q: list all jco in 2 coy
SQL: SELECT username, role, company FROM users WHERE role LIKE 'JCO%' AND company = '2 Company'

Q: how many officers are there
SQL: SELECT COUNT(*) FROM users WHERE role IN ('CO', 'OC', '2IC', 'ADJUTANT')

Q: who is nco mccs
SQL: SELECT username, role, company FROM users WHERE role = 'NCO MCCS'

Q: who is nco it of 1 coy
SQL: SELECT username, role, company FROM users WHERE role = 'NCO IT' AND company = '1 Company'
"""

# ==========================================================
# PERSONNEL TABLE SCHEMA (SOLDIERS ONLY)
# ==========================================================

PERSONNEL_SCHEMA = """
Table: personnel
Purpose: Stores ONLY soldier data.

IMPORTANT:
- `rank` is a reserved MySQL word — ALWAYS wrap in backticks: `rank`
- Commissioned Officers DO NOT exist in this table
- NEVER use rank without backticks

Columns:
- id (int, primary key, auto increment)
- army_number (varchar(100), unique army identifier)
- name (varchar(100), soldier full name)
- `rank` (varchar(100), military rank)
- company (varchar(100), assigned company)
- onleave_status (tinyint, 1 = on leave, 0 = not on leave)
- detachment_status (tinyint, 1 = on detachment, 0 = not on detachment)

VALID RANK VALUES (exact DB values):
- 'Agniveer'
- 'HAV'
- 'L HAV'
- 'L NK'
- 'LOC NK'
- 'Naib Subedar'
- 'NK'
- 'Signal Man'
- 'Subedar Major'

RANK SHORT FORMS (user may type these):
- hav, havaldar, havl       → HAV
- l hav, lance hav          → L HAV
- l nk, lance nk, lance naik → L NK
- loc nk                    → LOC NK
- nb sub, nb subedar        → Naib Subedar
- nk, naik                  → NK
- sig man                   → Signal Man
- sub maj                   → Subedar Major
- agniveer                  → Agniveer

COMPANY VALUES:
- '1 Company'
- '2 Company'
- '3 Company'
- 'HQ Company'

EXAMPLE QUERIES:

Q: how many soldiers are there
SQL: SELECT COUNT(*) FROM personnel

Q: what is unit strength
SQL: SELECT COUNT(*) FROM personnel

Q: strength of 1 coy
SQL: SELECT COUNT(*) FROM personnel WHERE company = '1 Company'

Q: list all agniveer
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE `rank` = 'Agniveer'

Q: how many agniveer
SQL: SELECT COUNT(*) FROM personnel WHERE `rank` = 'Agniveer'

Q: how many nk in 2 coy
SQL: SELECT COUNT(*) FROM personnel WHERE `rank` = 'NK' AND company = '2 Company'

Q: who is on leave
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE onleave_status = 1

Q: who is on detachment
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE detachment_status = 1

Q: agniveer on leave
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE `rank` = 'Agniveer' AND onleave_status = 1

Q: agniveer on detachment
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE `rank` = 'Agniveer' AND detachment_status = 1

Q: agniveer on det in 1 coy
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE `rank` = 'Agniveer' AND detachment_status = 1 AND company = '1 Company'

Q: how many hav in hq coy
SQL: SELECT COUNT(*) FROM personnel WHERE `rank` = 'HAV' AND company = 'HQ Company'

Q: list all sub maj
SQL: SELECT army_number, name, `rank`, company FROM personnel WHERE `rank` = 'Subedar Major'

Q: how many nb sub in 1 coy
SQL: SELECT COUNT(*) FROM personnel WHERE `rank` = 'Naib Subedar' AND company = '1 Company'
"""

# ==========================================================
# KEYWORD → SCHEMA ROUTING
# ==========================================================

USERS_TABLE_KEYWORDS = [
    "co", "oc", "adjutant", "jco", "2ic", "centre", "nco", "onco", "trg",
    "account officer", "project officer", "project jco",
    "account jco", "s/jco", "nco pwr", "nco chq", "nco it", "nco mw",
    "nco line", "nco op", "nco mccs", "nco rhq", "nco lrw", "nco qm",
    "nco mt", "nco tm", "nco rp", "jco pwr", "jco chq", "jco it",
    "jco mw", "jco line", "jco op", "jco mccs", "jco rhq", "jco tm",
    "jco mt", "jco lrw", "ja jco", "qm", "head clk", "pa",
    "user", "users", "admin", "clerk"
]

PERSONNEL_TABLE_KEYWORDS = [
    "agniveer",
    "hav", "havaldar", "havl",
    "l hav", "lance hav",
    "l nk", "lance nk", "lance naik",
    "loc nk",
    "naib subedar", "nb sub", "nb subedar",
    "nk", "naik",
    "signal man", "sig man",
    "subedar major", "sub maj",
    "soldier", "soldiers",
    "strength",
    "on leave", "onleave",
    "on detachment", "detachment", "det",
    "personnel"
]


def get_schema_for_question(question: str):
    """
    Match question keywords to correct schema.
    Uses whole word matching to prevent partial matches.
    USERS keywords checked first, then PERSONNEL.
    Returns (schema, matched_keyword, table) or (None, None, None).
    """
    q = question.lower()

    # USERS TABLE FIRST
    for keyword in USERS_TABLE_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', q):
            print(f"🟠 Keyword matched: '{keyword}' → using USERS_SCHEMA")
            return USERS_SCHEMA, keyword, "users"

    # PERSONNEL TABLE SECOND
    for keyword in PERSONNEL_TABLE_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', q):
            print(f"🟣 Keyword matched: '{keyword}' → using PERSONNEL_SCHEMA")
            return PERSONNEL_SCHEMA, keyword, "personnel"

    print("🟠 No keyword matched.")
    return None, None, None


def get_schema_summary():
    return """
HRMS Database Summary:
- Users table: Officers (CO, OC, 2IC, ADJUTANT), JCOs, NCOs, system users
- Personnel table: Soldiers (Agniveer, HAV, L HAV, L NK, LOC NK, Naib Subedar, NK, Signal Man, Subedar Major)
"""