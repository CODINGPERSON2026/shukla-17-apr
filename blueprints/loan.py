from imports import *
loan_bp = Blueprint('loan_bp', __name__, url_prefix='/loan_details')

@loan_bp.route("/summary")
def loan_summary():
    print("in this route")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            SUM(CASE WHEN total_amount BETWEEN 0 AND 500000 THEN 1 ELSE 0 END) AS l0_5,
            SUM(CASE WHEN total_amount BETWEEN 500001 AND 1000000 THEN 1 ELSE 0 END) AS l6_10,
            SUM(CASE WHEN total_amount BETWEEN 1000001 AND 1500000 THEN 1 ELSE 0 END) AS l11_15,
            SUM(CASE WHEN total_amount BETWEEN 1500001 AND 2000000 THEN 1 ELSE 0 END) AS l16_20,
            SUM(CASE WHEN total_amount > 2000000 THEN 1 ELSE 0 END) AS l20_plus
        FROM loans
    """)

    data = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify(data)

@loan_bp.route("/by-range/<range_key>")
def loans_by_range(range_key):
    ranges = {
        "0_5": (0, 500000),
        "6_10": (500001, 1000000),
        "11_15": (1000001, 1500000),
        "16_20": (1500001, 2000000),
        "20_plus": (2000000, None)
    }

    low, high = ranges.get(range_key, (None, None))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Updated query to include rank
    base_query = """
        SELECT
            l.army_number,
            p.rank,  # ADD THIS LINE
            p.name AS name,
            p.company AS company_name,
            l.loan_type,
            l.total_amount,
            l.pending,
            l.emi_per_month
        FROM loans l
        JOIN personnel p ON p.id = l.personnel_id
        
    """

    if high:
        query = base_query + """
            WHERE l.total_amount BETWEEN %s AND %s
            ORDER BY l.total_amount DESC
        """
        cursor.execute(query, (low, high))
    else:
        query = base_query + """
            WHERE l.total_amount > %s
            ORDER BY l.total_amount DESC
        """
        cursor.execute(query, (low,))

    rows = cursor.fetchall()
    print(rows)  # Debug: check if rank is included
    cursor.close()
    conn.close()

    return jsonify(rows)