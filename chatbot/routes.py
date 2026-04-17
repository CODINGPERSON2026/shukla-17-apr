"""
Chatbot routes - Flask blueprint and chat API.
Uses db_config.get_db_connection() for all database access.
Read-only queries only; parameterized to prevent SQL injection.
Supports any question: pattern-matched SQL first, then:
- LLM with schema + optional text-to-SQL (if configured), OR
- Generic auto-answer that inspects the live schema and returns best-effort data.
"""
import os
import re
from flask import Blueprint, request, jsonify
from middleware import require_login
from db_config import get_db_connection

from chatbot.nlp_processor import classify_question
from chatbot.sql_generator import get_sql, ALLOWED_TABLES
from chatbot.response_builder import format_result, format_schema, format_clarification, format_error

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# Use LLM for open-ended questions and optional text-to-SQL
_USE_LLM_FALLBACK = os.environ.get("CHATBOT_LLM_FALLBACK", "1") == "1"
# Regex to extract SQL from LLM reply: "SQL:" then SELECT until double newline or end
_LLM_SQL_PATTERN = re.compile(r"\bSQL:\s*(SELECT\s+.+?)(?=\n\s*\n|\Z)", re.I | re.DOTALL)


def _fetch_schema(conn):
    """Get table and column list from INFORMATION_SCHEMA."""
    if not conn:
        return ""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            ORDER BY TABLE_NAME, ORDINAL_POSITION
        """)
        rows = cur.fetchall()
        cur.close()
        current = None
        lines = []
        for r in rows:
            t, c, typ = r.get("TABLE_NAME"), r.get("COLUMN_NAME"), r.get("DATA_TYPE")
            if t != current:
                current = t
                lines.append("\n**" + t + "**: " + (c + " (" + typ + ")" if c else ""))
            else:
                lines.append("  - " + c + " (" + typ + ")")
        return "\n".join(lines) if lines else "No schema."
    except Exception as e:
        return "Schema error: " + str(e)


def _run_query(conn, sql, params):
    """Execute read-only SELECT; return list of dicts or (None, error_message)."""
    if not conn or not sql or sql.strip().startswith(("INSERT", "UPDATE", "DELETE", "DROP", "ALTER")):
        return None, "Invalid or unsafe query."
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        rows = cur.fetchall()
        cur.close()
        return rows, None
    except Exception as e:
        return None, str(e)


def _validate_llm_sql(sql):
    """Ensure SQL is a single read-only SELECT and only uses ALLOWED_TABLES. Returns (True, None) or (False, error_msg)."""
    if not sql or not sql.strip().upper().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."
    s = sql.strip()
    if ";" in s:
        return False, "Multiple statements not allowed."
    for forbidden in ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE", "EXEC", "CALL"):
        if forbidden in s.upper():
            return False, "Only read-only SELECT is allowed."
    # Extract table names: FROM `t` or FROM t, JOIN `t` or JOIN t (with optional alias)
    table_refs = re.findall(r"(?:FROM|JOIN)\s+[`]?(\w+)[`]?\s*(?:AS|\s|$|,|ON)", s, re.I)
    for t in table_refs:
        if t.lower() not in {x.lower() for x in ALLOWED_TABLES}:
            return False, "Table not allowed: " + t
    return True, None


def _llm_fallback(user_question, schema_text, db_stats, history=None):
    """
    Use OpenAI to answer any question. Pass conversation history for context.
    LLM may output a line "SQL: SELECT ..." which we can run (validated). Returns (reply_text, extracted_sql or None).
    """
    try:
        import openai
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")
        if not api_key:
            return None, None
        client = openai.OpenAI(api_key=api_key)
        system = """You are an HRMS assistant for a military unit. You answer ANY question about the project using the LIVE database.

Database schema (use only these tables and columns):
""" + (schema_text or "Not available") + """

Table row counts:
""" + (db_stats or "N/A") + """

Rules:
1. Answer from this schema and stats. For counts, aggregations, or lookups, you MAY output a line starting with exactly "SQL:" followed by one MySQL SELECT statement (one line). Use backticks for reserved words like `rank`. We will run it and show results.
2. After SQL: (if you use it), add a brief explanation in markdown.
3. If the question needs live data and you can write a SELECT, do so. Otherwise answer from schema/stats or suggest how to rephrase.
4. Be concise. Use markdown for lists and **bold**. Never make up column or table names."""
        messages = [{"role": "system", "content": system}]
        for h in (history or [])[-10:]:  # last 10 turns
            role = (h.get("role") or "user").lower()
            if role == "assistant":
                role = "assistant"
            else:
                role = "user"
            content = (h.get("content") or "").strip()
            if content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_question})
        r = client.chat.completions.create(
            model=os.environ.get("CHATBOT_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=0.2,
            max_tokens=1200,
        )
        raw = (r.choices[0].message.content or "").strip()
        # Extract optional SQL from reply
        sql_match = _LLM_SQL_PATTERN.search(raw)
        if sql_match:
            extracted_sql = sql_match.group(1).strip().replace("\n", " ").strip()
            # Remove SQL line from reply so we don't show raw SQL to user
            reply_without_sql = _LLM_SQL_PATTERN.sub("", raw).strip()
            return reply_without_sql or raw, extracted_sql
        return raw, None
    except Exception:
        return None, None


def _auto_answer_from_db(conn, user_question):
    """
    Generic fallback when we don't have a specific SQL pattern or LLM.
    - Looks at INFORMATION_SCHEMA to see what tables/columns exist.
    - Scores tables based on overlap with question words.
    - Returns a simple COUNT(*) or sample rows from the best-matching table.
    """
    if not conn or not user_question:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT TABLE_NAME, COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            """
        )
        rows = cur.fetchall()
        cur.close()
    except Exception:
        return None

    # Build table -> set(columns)
    table_cols = {}
    for r in rows or []:
        t = (r.get("TABLE_NAME") or "").strip()
        c = (r.get("COLUMN_NAME") or "").strip()
        if not t or t not in ALLOWED_TABLES:
            continue
        table_cols.setdefault(t, set()).add(c)

    if not table_cols:
        return None

    q_lower = (user_question or "").lower()
    tokens = re.findall(r"[a-zA-Z_]+", q_lower)
    tokens = [t for t in tokens if len(t) > 2]

    # Manual boosts for known domains
    domain_boosts = {
        "personnel": ["person", "soldier", "troop", "army", "rank", "company", "strength"],
        "leave_status_info": ["leave", "al", "cl", "aal", "onleave", "holiday", "vacation"],
        "loans": ["loan", "emi", "bank", "installment", "pending"],
        "tasks": ["task", "todo", "pending", "assigned"],
        "weight_info": ["weight", "fitness", "fit", "unfit", "bmi"],
        "family_members": ["family", "dependent", "spouse", "children", "kin"],
        "courses": ["course", "training", "qualified", "school"],
        "parade_state_daily": ["parade", "attendance", "present", "absent"],
    }

    best_table = None
    best_score = 0
    for tbl, cols in table_cols.items():
        score = 0
        tl = tbl.lower()
        for tok in tokens:
            if tok in tl:
                score += 3
        for col in cols:
            cl = col.lower()
            for tok in tokens:
                if tok in cl:
                    score += 2
        # domain boosts
        boosts = domain_boosts.get(tbl, [])
        for b in boosts:
            if b in q_lower:
                score += 4
        if score > best_score:
            best_score = score
            best_table = tbl

    if not best_table or best_score <= 0:
        return None

    # Decide whether user is asking for a count or details
    is_count = any(
        phrase in q_lower
        for phrase in ("how many", "count", "total ", "number of", "strength", "total strength")
    )

    if is_count:
        sql = f"SELECT COUNT(*) AS count FROM `{best_table}`"
        rows, err = _run_query(conn, sql, [])
        if err or not rows:
            return None
        cnt = rows[0].get("count", 0)
        # Short natural language + table
        reply = f"**Approximate answer from live database**\n\nThere are **{cnt}** rows in table `{best_table}` that best matches your question.\n\n"
        reply += format_result(rows, "general", {"title": f"Row count for `{best_table}`"})
        return reply

    # Sample details
    sql = f"SELECT * FROM `{best_table}` LIMIT 20"
    rows, err = _run_query(conn, sql, [])
    if err or not rows:
        return None
    reply = (
        "**Best-effort answer from live database**\n\n"
        f"I couldn't map your question to a specific report, "
        f"but based on the wording it most closely matches table `{best_table}`. "
        "Here are sample rows:\n\n"
    )
    reply += format_result(rows, "general", {"title": f"Sample from `{best_table}`"})
    return reply


def _get_db_stats(conn):
    """Short stats and sample values for LLM context."""
    if not conn:
        return ""
    try:
        cur = conn.cursor(dictionary=True)
        out = []
        for t in ["personnel", "leave_status_info", "tasks", "loans", "weight_info", "family_members", "courses"]:
            try:
                cur.execute("SELECT COUNT(*) AS c FROM `" + t.replace("`", "``") + "`")
                r = cur.fetchone()
                if r:
                    out.append(t + ": " + str(r.get("c", 0)) + " rows")
            except Exception:
                pass
        try:
            cur.execute("SELECT DISTINCT company FROM personnel WHERE company IS NOT NULL ORDER BY company LIMIT 20")
            companies = [row["company"] for row in cur.fetchall() if row.get("company")]
            if companies:
                out.append("Companies in personnel: " + ", ".join(companies))
        except Exception:
            pass
        cur.close()
        return "; ".join(out)
    except Exception:
        return ""


@chatbot_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    POST body: { "message": "...", "history": [] }
    Returns: { "reply": "...", "error": null }
    Answers from live database via db_config; supports any question type we can map to SQL or LLM.
    """
    user = require_login()
    if not user:
        return jsonify({"reply": None, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []  # [{ role: "user"|"assistant", content: "..." }, ...]
    if not user_message:
        return jsonify({
            "reply": "Ask me **any** question about this HRMS project or the database—personnel, leave, company strength, loans, tasks, weight/fitness, family, courses, parade state, or anything else. I'll answer from the live database.",
            "error": None,
        })

    conn = get_db_connection()
    if not conn:
        return jsonify({
            "reply": format_error("Database connection failed. Check db_config and MySQL."),
            "error": None,
        })

    try:
        # 1) Classify and extract entities
        entities = classify_question(user_message)
        # Attach logged-in user context so SQL generator can align with CO dashboard logic
        try:
            entities["user_company"] = getattr(user, "get", None) and user.get("company") or user["company"]
            entities["user_role"] = getattr(user, "get", None) and user.get("role") or user["role"]
            entities["user_army_number"] = getattr(user, "get", None) and user.get("army_number") or user["army_number"]
        except Exception:
            # If user is not a dict-like object, ignore; chatbot will still work with generic queries
            entities.setdefault("user_company", None)
            entities.setdefault("user_role", None)
            entities.setdefault("user_army_number", None)
        q_type = entities.get("type", "general")

        # 2) Schema request
        if q_type == "schema":
            schema_text = _fetch_schema(conn)
            reply = format_schema(schema_text)
            return jsonify({"reply": reply, "error": None})

        # 3) Generate SQL
        sql, params = get_sql(q_type, entities)

        if sql == "__SCHEMA__":
            schema_text = _fetch_schema(conn)
            reply = format_schema(schema_text)
            return jsonify({"reply": reply, "error": None})

        if sql:
            rows, err = _run_query(conn, sql, params)
            if err:
                reply = format_error(err, "Try rephrasing or ask for a specific table.")
            else:
                title = "Result"
                if q_type == "personnel_lookup":
                    title = "Personnel details"
                elif q_type == "company_count":
                    title = "Company distribution"
                elif q_type == "leave_status":
                    title = "Leave status"
                elif q_type == "loan_query":
                    title = "Loan information"
                elif q_type == "task_query":
                    title = "Tasks"
                elif q_type == "personnel_list_company":
                    title = "Personnel in company"
                elif q_type == "family_lookup":
                    title = "Family & dependents"
                elif q_type == "dashboard_summary":
                    title = "CO dashboard summary"
                reply = format_result(rows, q_type, {"title": title})
                # For family lookup also append children if present
                if q_type == "family_lookup" and entities.get("army_number"):
                    child_sql = "SELECT name, date_of_birth, class, part_ii_order FROM children WHERE army_number = %s ORDER BY sr_no"
                    child_rows, _ = _run_query(conn, child_sql, [entities["army_number"]])
                    if child_rows:
                        reply += "\n\n**Children:**\n\n" + format_result(child_rows, "general", {"title": "Children"})
            return jsonify({"reply": reply, "error": None})

        # 4) No SQL matched: clarify or LLM fallback (answers any question with schema + optional text-to-SQL)
        if q_type == "personnel_lookup" and not entities.get("army_number"):
            reply = format_clarification("Please provide an army number (e.g. 778G or 156WE) to look up personnel details.")
            return jsonify({"reply": reply, "error": None})

        if _USE_LLM_FALLBACK:
            schema_text = _fetch_schema(conn)
            db_stats = _get_db_stats(conn)
            llm_reply, llm_sql = _llm_fallback(user_message, schema_text, db_stats, history)
            if llm_reply is not None:
                reply = llm_reply
                if llm_sql:
                    ok, err = _validate_llm_sql(llm_sql)
                    if ok:
                        rows, run_err = _run_query(conn, llm_sql, [])
                        if run_err:
                            reply += "\n\n*Query execution failed: " + run_err + "*"
                        elif rows is not None:
                            reply += "\n\n" + format_result(rows, "general", {"title": "Result"})
                    else:
                        reply += "\n\n*Could not run query: " + (err or "invalid") + "*"
                return jsonify({"reply": reply, "error": None})

        # 5) As a final safety net, auto-analyse schema and return best-effort data
        auto_reply = _auto_answer_from_db(conn, user_message)
        if auto_reply:
            return jsonify({"reply": auto_reply, "error": None})

        reply = (
            "I couldn't map that to a specific report. "
            "Try asking in different words, or request: "
            "\"Database schema\", \"How many in each company?\", "
            "\"Who is on leave today?\", \"Details for army number X\", \"Pending tasks\"."
        )
        return jsonify({"reply": reply, "error": None})

    finally:
        try:
            conn.close()
        except Exception:
            pass


@chatbot_bp.route("/api/health", methods=["GET"])
def health():
    conn = get_db_connection()
    if conn:
        try:
            conn.close()
        except Exception:
            pass
        return jsonify({"status": "ok", "service": "hrms-chatbot", "database": "connected"})
    return jsonify({"status": "ok", "service": "hrms-chatbot", "database": "disconnected"}), 503
