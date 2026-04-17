from imports import *
from datetime import datetime

sensitive_bp = Blueprint('sensitive_bp',__name__,url_prefix='/sensitive')
@sensitive_bp.route("/remove_sensitive", methods=["POST"])
def remove_sensitive():
    army_number = request.form.get("army_number")
    
    if not army_number:
        return jsonify({"success": False, "error": "Missing army number"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM sensitive_marking WHERE army_number = %s", (army_number,))
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Personnel not found in sensitive list"}), 404
        
        conn.commit()
        return jsonify({"success": True, "message": "Personnel removed from sensitive list."})

    except Exception as e:
        conn.rollback()
        print("ERROR in remove_sensitive:", e)
        return jsonify({"success": False, "error": "Remove failed"}), 500
    finally:
        cursor.close()
        conn.close()


@sensitive_bp.route("/mark_sensitive", methods=["POST"])
def mark_sensitive():
    user = require_login()
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")

    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing army number or reason"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert into sensitive_marking if not already there
        cursor.execute("SELECT 1 FROM sensitive_marking WHERE army_number = %s", (army_number,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO sensitive_marking (army_number, marked_on)
                VALUES (%s, %s)
            """, (army_number, datetime.now()))

        # Always log the reason with user info
        cursor.execute("""
            INSERT INTO sensitive_reason_log (army_number, reason, added_by, added_by_role, added_on)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            army_number,
            reason.strip(),
            user.get('username', 'Unknown'),
            user.get('role', 'Unknown'),
            datetime.now()
        ))

        conn.commit()
        return jsonify({"success": True, "message": "Personnel marked as sensitive successfully."})
    except Exception as e:
        conn.rollback()
        print("ERROR in mark_sensitive:", e)
        return jsonify({"success": False, "error": "Database error"}), 500
    finally:
        cursor.close()
        conn.close()


@sensitive_bp.route("/update_sensitive_reason", methods=["POST"])
def update_sensitive_reason():
    user = require_login()
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")

    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check exists in sensitive_marking
        cursor.execute("SELECT 1 FROM sensitive_marking WHERE army_number = %s", (army_number,))
        if not cursor.fetchone():
            return jsonify({"success": False, "error": "Personnel not found in sensitive list"}), 404

        # Add new reason log entry (don't overwrite — append as new block)
        cursor.execute("""
            INSERT INTO sensitive_reason_log (army_number, reason, added_by, added_by_role, added_on)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            army_number,
            reason.strip(),
            user.get('username', 'Unknown'),
            user.get('role', 'Unknown'),
            datetime.now()
        ))

        conn.commit()
        return jsonify({"success": True, "message": "Reason added successfully."})
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return jsonify({"success": False, "error": "Update failed"}), 500
    finally:
        cursor.close()
        conn.close()


@sensitive_bp.route("/get_sensitive_list")
def get_sensitive_list():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get logged-in user (adjust based on your auth system)
    user = require_login() # or however you're storing it
    user_company = user.get("company")
    user_role = user.get("role")

    try:
        # ✅ Admin → see all
        if user_company == "Admin" or user_role == "admin":
            cursor.execute("""
                SELECT s.army_number, s.marked_on,
                       p.name, p.rank, p.company
                FROM sensitive_marking s
                JOIN personnel p ON s.army_number = p.army_number
                ORDER BY s.marked_on DESC
            """)
        else:
            # ✅ Non-admin → filter by company
            cursor.execute("""
                SELECT s.army_number, s.marked_on,
                       p.name, p.rank, p.company
                FROM sensitive_marking s
                JOIN personnel p ON s.army_number = p.army_number
                WHERE p.company = %s
                ORDER BY s.marked_on DESC
            """, (user_company,))

        rows = cursor.fetchall()

        result = []
        for r in rows:
            army_number = r[0]

            # Fetch all reason logs for this person
            cursor.execute("""
                SELECT reason, added_by, added_by_role, added_on
                FROM sensitive_reason_log
                WHERE army_number = %s
                ORDER BY added_on ASC
            """, (army_number,))
            logs = cursor.fetchall()

            reason_logs = [{
                "reason": l[0],
                "added_by": l[1],
                "added_by_role": l[2],
                "added_on": l[3].strftime("%d %b %Y, %H:%M") if l[3] else ""
            } for l in logs]

            result.append({
                "army_number": army_number,
                "marked_on": r[1].strftime("%Y-%m-%d %H:%M:%S") if r[1] else "",
                "name": r[2],
                "rank": r[3],
                "company": r[4] or "N/A",
                "reason_logs": reason_logs
            })

        return jsonify({"success": True, "data": result})

    finally:
        cursor.close()
        conn.close()

@sensitive_bp.route("/mark_personnel", methods=["GET"])
def mark_personnel():
    user = require_login()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.army_number, s.marked_on,
               p.name, p.rank, p.company
        FROM sensitive_marking s
        JOIN personnel p ON s.army_number = p.army_number
        ORDER BY s.marked_on DESC
    """)
    rows = cursor.fetchall()

    sensitive_list = []
    for r in rows:
        sensitive_list.append({
            "army_number": r[0],
            "marked_on": r[1].strftime("%Y-%m-%d %H:%M:%S") if r[1] else "",
            "name": r[2],
            "rank": r[3],
            "company": r[4] or "N/A"
        })

    cursor.close()
    conn.close()

    response = make_response(render_template(
        "sensitive_indl/mark_personnel.html",
        sensitive_list=sensitive_list,
        current_user=user
    ))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response
