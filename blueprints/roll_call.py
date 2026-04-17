from imports import *
roll_call_bp = Blueprint("roll_call", __name__, url_prefix="/roll_call")

@roll_call_bp.route("/submit", methods=["POST"])
def submit_roll_call():
    try:
        data = request.get_json()
        
        

        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        category = data.get("category")
        point_title = data.get("point_title")
        points = data.get("points")   # 🔥 LIST
        army_number = data.get("army_number")

        # Validation
        if not category or not point_title or not points or len(points) == 0:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        status = "SUGGESSTED"

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # OR validation
        if category == "OR_REQUEST":
            if not army_number:
                return jsonify({"success": False, "message": "Army Number required"}), 400

            cursor.execute("SELECT army_number FROM personnel WHERE army_number=%s", (army_number,))
            if not cursor.fetchone():
                return jsonify({"success": False, "message": "Invalid Army Number"}), 400

            status = "PENDING"

        # 🔥 MULTIPLE INSERT
        for point in points:
            cursor.execute("""
                INSERT INTO roll_call_points 
                (category, point_title, point_description, army_number, status)
                VALUES (%s,%s,%s,%s,%s)
            """, (category, point_title, point, army_number, status))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False, "message": "Server error"}), 500



@roll_call_bp.route('/pending', methods=['GET'])
def get_pending_roll_call_points():
    user = require_login()
    company = user['company']
    role = user['role']

    category = request.args.get('category', 'OR_REQUEST')

    status_map = {
        'OR_REQUEST': 'PENDING',
        'SM_SUGGESTION': 'SUGGESSTED'
    }

    status = status_map.get(category, 'PENDING')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = '''
            SELECT 
                rcp.id,
                rcp.status,
                rcp.category,
                rcp.point_title,
                rcp.point_description,
                rcp.created_at,
                p.army_number,
                p.name,
                p.rank,
                p.company
            FROM roll_call_points rcp
            LEFT JOIN personnel p ON rcp.army_number = p.army_number
            WHERE rcp.status = %s
        '''

        params = [status]
        print('compnay',company)

        # if company != "Admin" or company == 'Center':
        #     print('filtered')
        #     query += " AND p.company = %s"
        #     params.append(company)

        query += " ORDER BY rcp.created_at DESC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        print("gggggggggggggggggggggggggggggggggggggggggggggggg")
        print(rows)

        return jsonify({"status": "success", "data": rows}), 200

    except Exception as e:
        print("Roll call fetch error:", e)
        return jsonify({"status": "error"}), 500

    finally:
        cursor.close()
        conn.close()





@roll_call_bp.route("/update_status", methods=["POST"])
def update_roll_call_status():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        roll_call_id = data.get("id")
        new_status = data.get("status")
        remark = data.get("remark")  # ✅ NEW

        # Normalize remark (optional)
        remark = remark.strip() if remark else None

        # Validate inputs
        if not roll_call_id or not new_status:
            return jsonify({
                "status": "error",
                "message": "ID and status are required"
            }), 400

        if new_status not in ["APPROVED", "REJECTED"]:
            return jsonify({
                "status": "error",
                "message": "Invalid status value"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check record
        cursor.execute("""
            SELECT id, status
            FROM roll_call_points
            WHERE id = %s
        """, (roll_call_id,))
        record = cursor.fetchone()

        if not record:
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Roll call record not found"
            }), 404

        if record["status"] != "PENDING":
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Only PENDING records can be updated"
            }), 400

        # ✅ UPDATE WITH REMARK
        cursor.execute("""
            UPDATE roll_call_points
            SET status = %s,
                remarks = %s
            WHERE id = %s
        """, (new_status, remark, roll_call_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": f"Status updated to {new_status}"
        })

    except Exception as e:
        print("Update Roll Call Status Error:", e)
        return jsonify({
            "status": "error",
            "message": "Server error"
        }), 500

@roll_call_bp.route('/approved', methods=['GET'])
def get_approved_roll_calls():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                rc.category,
                rc.point_title,
                rc.point_description,
                rc.army_number,
                rc.status,
                rc.remarks,
                rc.created_at,

                p.rank,
                p.name,
                p.company

            FROM roll_call_points rc
            LEFT JOIN personnel p 
                ON rc.army_number = p.army_number

            WHERE rc.status = 'APPROVED'
            ORDER BY rc.created_at DESC
            LIMIT 5
        """

        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False}), 500

    finally:
        cursor.close()
        conn.close()











@roll_call_bp.route('/check_army/<army_no>', methods=['GET'])
def check_army(army_no):
    try:
        conn = get_db_connection() 
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT army_number, `rank`,name, company
            FROM personnel
            WHERE army_number = %s
            LIMIT 1
        """

        cursor.execute(query, (army_no,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return jsonify({
                "success": True,
                "data": {
                    "army_number": result["army_number"],
                    "rank": result["rank"],
                    "company": result["company"],
                    "name":result['name']
                }
            })

        return jsonify({"success": False})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500