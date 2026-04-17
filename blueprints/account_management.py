from imports import *
from datetime import datetime

accounts_bp = Blueprint('account', __name__, url_prefix='/account')


# ==========================================
# HELPER: FINANCIAL YEAR
# ==========================================
def get_financial_year():
    today = datetime.today()
    year = today.year

    if today.month >= 4:  # April onwards
        return f"{year}-{year+1}"
    else:
        return f"{year-1}-{year}"


# ==========================================
# DASHBOARD PAGE
# ==========================================
@accounts_bp.route('/')
def accounts():

    fy = request.args.get("fy") or get_financial_year()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT 
            g.id,
            g.name,
            g.code_head,
            IFNULL(a.total_allotment, 0) AS total_allotment,
            IFNULL(s.no_of_sos, 0) AS no_of_sos,
            IFNULL(e.total_expenditure, 0) AS total_expenditure
        FROM grants g

        LEFT JOIN (
            SELECT grant_id, SUM(amount) AS total_allotment
            FROM grant_allocations
            WHERE financial_year = %s
            GROUP BY grant_id
        ) a ON g.id = a.grant_id

        LEFT JOIN (
            SELECT grant_id, COUNT(*) AS no_of_sos
            FROM sanction_orders
            WHERE financial_year = %s
            GROUP BY grant_id
        ) s ON g.id = s.grant_id

        LEFT JOIN (
            SELECT grant_id, SUM(amount) AS total_expenditure
            FROM expenditures
            WHERE financial_year = %s
            GROUP BY grant_id
        ) e ON g.id = e.grant_id

        WHERE g.financial_year = %s
    """

    cursor.execute(query, (fy, fy, fy, fy))
    grants = cursor.fetchall()

    for row in grants:

        total_allotment = float(row['total_allotment'] or 0)
        total_expenditure = float(row['total_expenditure'] or 0)

        row['balance'] = total_allotment - total_expenditure
        row['exp_percent'] = (
            round((total_expenditure / total_allotment) * 100, 2)
            if total_allotment > 0 else 0
        )

        print("DASHBOARD DEBUG:", row['name'], total_allotment, fy)

    cursor.close()
    db.close()

    return render_template(
        "account_management/account.html",
        grants=grants,
        current_fy=fy
    )


# ==========================================
# SUMMARY API
# ==========================================
@accounts_bp.route('/grants/summary')
def grant_summary():

    fy = request.args.get("fy") or get_financial_year()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            g.id,
            g.name,
            g.code_head,
            IFNULL(a.total_allotment, 0) AS total_allotment,
            IFNULL(s.no_of_sos, 0) AS no_of_sos,
            IFNULL(e.total_expenditure, 0) AS total_expenditure
        FROM grants g

        LEFT JOIN (
            SELECT grant_id, SUM(amount) AS total_allotment
            FROM grant_allocations
            WHERE financial_year = %s
            GROUP BY grant_id
        ) a ON g.id = a.grant_id

        LEFT JOIN (
            SELECT grant_id, COUNT(*) AS no_of_sos
            FROM sanction_orders
            WHERE financial_year = %s
            GROUP BY grant_id
        ) s ON g.id = s.grant_id

        LEFT JOIN (
            SELECT grant_id, SUM(amount) AS total_expenditure
            FROM expenditures
            WHERE financial_year = %s
            GROUP BY grant_id
        ) e ON g.id = e.grant_id

        WHERE g.financial_year = %s
    """

    cursor.execute(query, (fy, fy, fy, fy))
    results = cursor.fetchall()

    for row in results:

        total_allotment = float(row['total_allotment'] or 0)
        total_expenditure = float(row['total_expenditure'] or 0)

        row['balance'] = total_allotment - total_expenditure
        row['exp_percent'] = (
            round((total_expenditure / total_allotment) * 100, 2)
            if total_allotment > 0 else 0
        )

        print("SUMMARY DEBUG:", row['name'], total_allotment, fy)

    cursor.close()
    conn.close()

    return jsonify(results)


# ==========================================
# CREATE GRANT + ORIGINAL ALLOCATION
# ==========================================
@accounts_bp.route('/grants/add', methods=['POST'])
def add_grant():

    data = request.get_json()
    fy = get_financial_year()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO grants (name, code_head, allotment, financial_year, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (data['name'], data['code_head'], data['allotment'], fy))

    grant_id = cursor.lastrowid
    original_amount = float(data['allotment'] or 0)

    print("Creating Grant:", data['name'], fy)

    cursor.execute("""
        INSERT INTO grant_allocations
        (grant_id, amount, allocation_type, remarks, financial_year)
        VALUES (%s, %s, 'Original', 'Initial Allotment', %s)
    """, (grant_id, original_amount, fy))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})


# ==========================================
# GRANT DETAIL PAGE
# ==========================================
@accounts_bp.route('/grants/<int:grant_id>')
def grant_detail(grant_id):

    fy = request.args.get("fy") or get_financial_year()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, code_head
        FROM grants
        WHERE id = %s AND financial_year = %s
    """, (grant_id, fy))
    grant = cursor.fetchone()

    if not grant:
        return "Grant not found", 404

    # TOTAL ALLOTMENT
    cursor.execute("""
        SELECT IFNULL(SUM(amount),0) AS total_allotment
        FROM grant_allocations
        WHERE grant_id = %s AND financial_year = %s
    """, (grant_id, fy))
    total_allotment = float(cursor.fetchone()['total_allotment'] or 0)

    grant["allotment"] = total_allotment

    # TOTAL EXPENDITURE
    cursor.execute("""
        SELECT IFNULL(SUM(amount),0) AS total_exp
        FROM expenditures
        WHERE grant_id = %s AND financial_year = %s
    """, (grant_id, fy))
    total_exp = float(cursor.fetchone()['total_exp'] or 0)

    # SANCTION ORDERS
    cursor.execute("""
        SELECT id, so_number, so_amount, created_at
        FROM sanction_orders
        WHERE grant_id = %s AND financial_year = %s
        ORDER BY created_at DESC
    """, (grant_id, fy))
    sos = cursor.fetchall()

    # EXPENDITURES
    cursor.execute("""
        SELECT id, amount, remarks, created_at
        FROM expenditures
        WHERE grant_id = %s AND financial_year = %s
        ORDER BY created_at DESC
    """, (grant_id, fy))
    expenditures = cursor.fetchall()

    balance = total_allotment - total_exp
    exp_percent = (
        round((total_exp / total_allotment) * 100, 2)
        if total_allotment > 0 else 0
    )

    print("DETAIL DEBUG:", grant["name"], total_allotment, fy)

    cursor.close()
    conn.close()

    return render_template(
        "account_management/grant_detail.html",
        grant=grant,
        total_exp=total_exp,
        sos=sos,
        expenditures=expenditures,
        balance=balance,
        exp_percent=exp_percent,
        current_fy=fy
    )


# ==========================================
# ADD ADDITIONAL ALLOCATION
# ==========================================
@accounts_bp.route('/grants/<int:grant_id>/add-allocation', methods=['POST'])
def add_allocation(grant_id):

    data = request.get_json()
    amount = float(data.get("amount") or 0)
    fy = get_financial_year()

    if amount <= 0:
        return jsonify({"success": False, "message": "Invalid amount"})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO grant_allocations
        (grant_id, amount, allocation_type, remarks, financial_year)
        VALUES (%s, %s, 'Additional', %s, %s)
    """, (grant_id, amount, data.get("remarks", ""), fy))

    conn.commit()
    cursor.close()
    conn.close()

    print("Added Additional Allocation:", amount, fy)

    return jsonify({"success": True})


# ==========================================
# ADD EXPENDITURE
# ==========================================
@accounts_bp.route("/grants/<int:grant_id>/add-exp", methods=["POST"])
def add_expenditure(grant_id):

    data = request.get_json()
    amount = float(data.get("amount") or 0)
    fy = get_financial_year()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0) AS total_allotment
        FROM grant_allocations
        WHERE grant_id = %s AND financial_year = %s
    """, (grant_id, fy))
    total_allotment = float(cursor.fetchone()["total_allotment"] or 0)

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0) AS total_exp
        FROM expenditures
        WHERE grant_id = %s AND financial_year = %s
    """, (grant_id, fy))
    total_exp = float(cursor.fetchone()["total_exp"] or 0)

    current_balance = total_allotment - total_exp

    print("EXP DEBUG - Balance:", current_balance, fy)

    if amount > current_balance:
        cursor.close()
        conn.close()
        return jsonify({
            "success": False,
            "message": "Expenditure exceeds available balance"
        })

    cursor.execute("""
        INSERT INTO expenditures (grant_id, amount, financial_year)
        VALUES (%s, %s, %s)
    """, (grant_id, amount, fy))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})