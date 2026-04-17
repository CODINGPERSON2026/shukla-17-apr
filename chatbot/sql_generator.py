"""
SQL Query Generator for HRMS Chatbot.
Builds parameterized, read-only SELECT queries from question type and entities.
Uses only safe table/column names; all values are parameterized.
"""
from datetime import date

# Table names we are allowed to query (read-only)
ALLOWED_TABLES = {
    "personnel", "users", "family_members", "children", "courses", "detailed_courses",
    "candidate_on_courses", "leave_details", "leave_status_info", "leave_history",
    "weight_info", "ideal_weights", "loans", "tasks", "department_accounts", "department_transactions",
    "parade_state_daily", "daily_events", "assigned_det", "assigned_personnel", "dets",
    "posting_details_table", "board_members", "boards", "punishments", "mobile_phones",
    "vehicle_detail", "marital_discord_cases", "personnel_sports", "sensitive_marking",
    "monthly_medical_status", "td_table", "stores", "store_items", "sales", "units_served",
    "project_heads", "projects", "roll_call_points", "trade_manpower_daily", "assistant_test",
}


def _safe_table(t):
    return t if t in ALLOWED_TABLES else None


def get_sql(question_type, entities):
    """
    Return (sql_string, params_list) for read-only query, or (None, []) if no query.
    """
    army = entities.get("army_number")
    company = entities.get("company")
    dt = entities.get("date")
    rank = entities.get("rank")
    leave_type = entities.get("leave_type")
    user_company = entities.get("user_company")
    user_role = entities.get("user_role")
    user_army = entities.get("user_army_number")

    params = []
    sql = None

    # Personnel lookup by army number (backticks for reserved words e.g. rank, trade in MySQL 8)
    if question_type == "personnel_lookup" and army:
        sql = """
            SELECT name, army_number, `rank`, trade, company, date_of_birth, date_of_enrollment,
                   date_of_tos, date_of_tors, blood_group, religion, food_preference,
                   height, weight, chest, kin_name, kin_relation, personnel_status
            FROM personnel WHERE army_number = %s LIMIT 1
        """
        params = [army]

    # List personnel in a company
    elif question_type == "personnel_list_company" and company:
        sql = """
            SELECT name, army_number, `rank`, trade, company
            FROM personnel WHERE company = %s ORDER BY `rank`, name LIMIT 50
        """
        params = [company]

    # Company-wise count
    elif question_type == "company_count":
        if company:
            sql = "SELECT company, COUNT(*) AS count FROM personnel WHERE company = %s GROUP BY company"
            params = [company]
        else:
            sql = "SELECT company, COUNT(*) AS count FROM personnel WHERE company IS NOT NULL GROUP BY company ORDER BY company"
            params = []

    # Leave status
    elif question_type == "leave_status":
        if army:
            sql = """
                SELECT army_number, name, leave_type, leave_days, from_date, to_date, request_status, leave_reason, company
                FROM leave_status_info WHERE army_number = %s ORDER BY from_date DESC LIMIT 20
            """
            params = [army]
        elif dt:
            sql = """
                SELECT army_number, name, leave_type, from_date, to_date, request_status, company
                FROM leave_status_info WHERE %s BETWEEN from_date AND to_date AND request_status = 'Approved'
                ORDER BY from_date LIMIT 50
            """
            params = [dt]
        else:
            sql = """
                SELECT request_status, COUNT(*) AS count FROM leave_status_info GROUP BY request_status ORDER BY count DESC
            """
            params = []

    # Leave balance
    elif question_type == "leave_balance" and army:
        sql = """
            SELECT year, al_days, cl_days, aal_days, total_days, remarks
            FROM leave_details WHERE army_number = %s ORDER BY year DESC LIMIT 5
        """
        params = [army]

    # Weight / fitness
    elif question_type == "weight_fitness":
        if company:
            sql = """
                SELECT status_type, COUNT(*) AS count FROM weight_info WHERE company = %s GROUP BY status_type
            """
            params = [company]
        else:
            sql = """
                SELECT status_type, COUNT(*) AS count FROM weight_info GROUP BY status_type
            """
            params = []

    # Loans
    elif question_type == "loan_query":
        if army:
            sql = """
                SELECT army_number, loan_type, total_amount, bank_details, emi_per_month, pending, remarks
                FROM loans WHERE army_number = %s ORDER BY sr_no LIMIT 20
            """
            params = [army]
        elif rank and company:
            sql = """
                SELECT p.name, p.army_number, p.`rank`, l.loan_type, l.total_amount, l.pending
                FROM loans l JOIN personnel p ON p.army_number = l.army_number
                WHERE p.`rank` LIKE %s AND p.company = %s AND l.loan_type LIKE %s
                LIMIT 30
            """
            params = ["%" + rank + "%", company, "%HOME%"]
        elif company:
            sql = """
                SELECT l.loan_type, COUNT(*) AS count, SUM(l.total_amount) AS total
                FROM loans l JOIN personnel p ON p.army_number = l.army_number
                WHERE p.company = %s GROUP BY l.loan_type
            """
            params = [company]
        else:
            sql = "SELECT loan_type, COUNT(*) AS count, SUM(total_amount) AS total FROM loans GROUP BY loan_type"
            params = []

    # Tasks
    elif question_type == "task_query":
        sql = """
            SELECT task_name, description, priority, assigned_to, assigned_by, due_date, task_status, remarks
            FROM tasks WHERE task_status IN ('Pending', 'In Progress') ORDER BY due_date LIMIT 30
        """
        params = []

    # Family
    elif question_type == "family_lookup" and army:
        sql = """
            SELECT relation, name, date_of_birth, uid_no, part_ii_order
            FROM family_members WHERE army_number = %s ORDER BY relation
        """
        params = [army]

    # Courses
    elif question_type == "courses_lookup" and army:
        sql = """
            SELECT course, from_date, to_date, institute, grading, remarks
            FROM courses WHERE army_number = %s ORDER BY from_date DESC LIMIT 20
        """
        params = [army]

    # Parade state
    elif question_type == "parade_state":
        if dt:
            sql = """
                SELECT report_date, company, grandTotal_auth, grandTotal_present_unit, grandTotal_lve, grandTotal_att
                FROM parade_state_daily WHERE report_date = %s ORDER BY company LIMIT 20
            """
            params = [dt]
        else:
            sql = """
                SELECT report_date, company, grandTotal_auth, grandTotal_present_unit
                FROM parade_state_daily ORDER BY report_date DESC LIMIT 10
            """
            params = []

    # Analytical: average age by company
    elif question_type == "analytical":
        q_lower = (entities.get("raw_question") or "").lower()
        if "average" in q_lower and "age" in q_lower:
            if company:
                sql = """
                    SELECT company, COUNT(*) AS count, ROUND(AVG(TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())), 1) AS avg_age
                    FROM personnel WHERE company = %s AND date_of_birth IS NOT NULL GROUP BY company
                """
                params = [company]
            else:
                sql = """
                    SELECT company, COUNT(*) AS count, ROUND(AVG(TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())), 1) AS avg_age
                    FROM personnel WHERE date_of_birth IS NOT NULL AND company IS NOT NULL GROUP BY company ORDER BY company
                """
                params = []
        elif "loan" in q_lower and ("highest" in q_lower or "total" in q_lower):
            sql = """
                SELECT p.company, COUNT(l.id) AS loan_count, SUM(l.total_amount) AS total_amount
                FROM loans l JOIN personnel p ON p.army_number = l.army_number
                GROUP BY p.company ORDER BY total_amount DESC LIMIT 10
            """
            params = []
        else:
            sql = None

    # Schema: return special marker; handled in routes via INFORMATION_SCHEMA
    elif question_type == "schema":
        return ("__SCHEMA__", [])

    # CO dashboard-style summary: detachments, manpower, interviews, projects, sensitive, loans, etc.
    elif question_type == "dashboard_summary":
        # Prefer explicit company from user context; fall back to parsed company
        comp = user_company or company
        role = (user_role or "").upper()

        # Whether to restrict by company for most counts
        restrict_by_company = comp is not None and comp != "Admin"

        sql_parts = []
        params = []

        # 1) Detachments (personnel on detachment)
        det_where = "WHERE detachment_status = 1"
        if restrict_by_company:
            det_where += " AND company = %s"
            params.append(comp)
        sql_parts.append(
            f"(SELECT COUNT(*) FROM personnel {det_where}) AS detachments"
        )

        # 2) Manpower breakdown from personnel (officers / JCOs / ORs)
        mp_where = "WHERE 1=1"
        if restrict_by_company:
            mp_where += " AND company = %s"
            params.append(comp)
        sql_parts.append(
            """
            (SELECT
                SUM(CASE WHEN `rank` IN (
                    'Lieutenant', 'Captain', 'Major',
                    'Lieutenant Colonel', 'Colonel',
                    'Brigadier', 'Major General',
                    'Lieutenant General', 'General', 'OC'
                ) THEN 1 ELSE 0 END)
             FROM personnel """ + mp_where + """
            ) AS officerCount
            """
        )
        sql_parts.append(
            """
            (SELECT
                SUM(CASE WHEN `rank` IN (
                    'Subedar', 'Naib Subedar', 'Subedar Major', 'JCO'
                ) THEN 1 ELSE 0 END)
             FROM personnel """ + mp_where + """
            ) AS jcoCount
            """
        )
        sql_parts.append(
            """
            (SELECT
                SUM(CASE WHEN `rank` NOT IN (
                    'Lieutenant', 'Captain', 'Major',
                    'Lieutenant Colonel', 'Colonel',
                    'Brigadier', 'Major General',
                    'Lieutenant General', 'General', 'OC',
                    'Subedar', 'Naib Subedar', 'Subedar Major', 'JCO'
                ) THEN 1 ELSE 0 END)
             FROM personnel """ + mp_where + """
            ) AS orCount
            """
        )

        # 3) Interview pending / total (agniveer / OR ranks)
        iv_where = """
            WHERE `rank` IN ('AGNIVEER', 'Signal Man', 'L NK', 'NK', 'HAV','LOC NK','L HAV','CHM','RHM')
        """
        if restrict_by_company:
            iv_where += " AND company = %s"
            params.append(comp)
        sql_parts.append(
            f"""
            (SELECT
                COALESCE(SUM(interview_status = 0), 0)
             FROM personnel
             {iv_where}
            ) AS interview_pending_count
            """
        )
        sql_parts.append(
            f"""
            (SELECT
                COUNT(*)
             FROM personnel
             {iv_where}
            ) AS interview_total_count
            """
        )

        # 4) Projects count
        proj_where = "WHERE 1=1"
        if restrict_by_company:
            proj_where += " AND company = %s"
            params.append(comp)
        sql_parts.append(
            f"(SELECT COUNT(*) FROM projects {proj_where}) AS projects"
        )

        # 5) Sensitive individuals (sensitive_marking joined to personnel)
        sens_where = ""
        if restrict_by_company:
            sens_where = "WHERE p.company = %s"
            params.append(comp)
        sql_parts.append(
            f"""
            (
                SELECT COUNT(*)
                FROM sensitive_marking sm
                LEFT JOIN personnel p ON sm.army_number = p.army_number
                {sens_where}
            ) AS sensitive_count
            """
        )

        # 6) Boards count
        sql_parts.append("(SELECT COUNT(*) FROM boards) AS boards_count")

        # 7) TD / attachment count (td_status = 1)
        td_where = "WHERE td_status = 1"
        if restrict_by_company:
            td_where += " AND company = %s"
            params.append(comp)
        sql_parts.append(
            f"(SELECT COUNT(*) FROM personnel {td_where}) AS attachment_count"
        )

        # 8) Courses count (candidate_on_courses joined to personnel for company filter)
        course_where = """
            WHERE 1=1
        """
        if restrict_by_company:
            course_where += " AND p.company = %s"
            params.append(comp)
        sql_parts.append(
            f"""
            (
                SELECT COUNT(*)
                FROM candidate_on_courses c
                LEFT JOIN personnel p ON c.army_number = p.army_number
                {course_where}
            ) AS courses_count
            """
        )

        # 9) Loan count (loans joined to personnel for company filter)
        loan_where = ""
        if restrict_by_company:
            loan_where = "WHERE p.company = %s"
            params.append(comp)
        sql_parts.append(
            f"""
            (
                SELECT COUNT(*)
                FROM loans l
                LEFT JOIN personnel p ON l.army_number = p.army_number
                {loan_where}
            ) AS loan_count
            """
        )

        # 10) Roll call pending points
        sql_parts.append(
            "(SELECT COUNT(*) FROM roll_call_points WHERE status = 'PENDING') AS roll_call_pending_points"
        )

        # 11) Tasks for current user (if available)
        if user_army:
            sql_parts.append(
                """
                (SELECT
                    COUNT(*)
                 FROM tasks
                 WHERE assigned_to = %s
                ) AS total_tasks
                """
            )
            params.append(user_army)
            sql_parts.append(
                """
                (SELECT
                    COALESCE(SUM(task_status != 'COMPLETED'), 0)
                 FROM tasks
                 WHERE assigned_to = %s
                ) AS pending_tasks
                """
            )
            params.append(user_army)
        else:
            # Whole-unit summary if army not known
            sql_parts.append(
                """
                (SELECT
                    COUNT(*)
                 FROM tasks
                ) AS total_tasks
                """
            )
            sql_parts.append(
                """
                (SELECT
                    COALESCE(SUM(task_status != 'COMPLETED'), 0)
                 FROM tasks
                ) AS pending_tasks
                """
            )

        # 12) Agniveer count (respect role-based visibility like dashboard)
        priv_roles = {"ADMIN", "CO", "2IC", "ADJUTANT", "TRGJCO", "OC"}
        ag_where = "WHERE `rank` = 'Agniveer'"
        if restrict_by_company and role not in priv_roles:
            ag_where += " AND company = %s"
            params.append(comp)
        sql_parts.append(
            f"(SELECT COUNT(*) FROM personnel {ag_where}) AS agniveer_count"
        )

        # Assemble into single-row SELECT
        sql = "SELECT " + ", ".join(sql_parts)

    return (sql, params)
