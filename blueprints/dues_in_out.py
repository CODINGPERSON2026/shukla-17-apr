from imports import *

dues_bp = Blueprint('dues_bp', __name__, url_prefix='/dues')
@dues_bp.route('/add', methods=['POST'])
def add_dues_in():
    try:
        data = request.get_json()

        conn = get_db_connection()   # your pool function
        cursor = conn.cursor()

        query = """
        INSERT INTO dues_in 
        (army_number, `rank`, trade, name, unit, posting_order_no, date_of_move, dor, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            data.get('army_number'),
            data.get('rank'),
            data.get('trade'),
            data.get('name'),
            data.get('unit'),
            data.get('posting_order_no'),
            data.get('date_of_move'),
            data.get('dor'),
            data.get('remarks')
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": str(e)})
    

@dues_bp.route('/out', methods=['POST'])
def add_dues_out():
    try:
        

        data = request.get_json()

        # Basic validation
        if not data.get("army_number") or not data.get("name"):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        conn = get_db_connection()   # your pooled connection
        cursor = conn.cursor()
        
        query = """
        INSERT INTO dues_out
        (army_number, `rank`, trade, name, posted_to, posting_order_no, date_of_move, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            data.get('army_number'),
            data.get('rank'),
            data.get('trade'),
            data.get('name'),
            data.get('posted_to'),
            data.get('posting_order_no'),
            data.get('date_of_move'),
            data.get('remarks')
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Dues Out Added Successfully"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    



@dues_bp.route('/dues_in_count', methods=['GET'])
def get_dues_in_count():
    try:
        

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT COUNT(id) FROM dues_in"
        cursor.execute(query)

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "dues_in": count   # 👈 matches your frontend key
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    



@dues_bp.route('/dues_out_count', methods=['GET'])
def get_dues_out_count():
    print("in dues out")
    try:
        

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM dues_out")
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "dues_out": count
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@dues_bp.route('/dues-out/list', methods=['GET'])
def get_dues_out():
    try:
        # 🔒 Role check
  

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            army_number,
            `rank`,
            name,
            trade,
            posted_to,
            posting_order_no,
            date_of_move,
            remarks
        FROM dues_out
        ORDER BY id DESC
        """

        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    

@dues_bp.route('/dues-in/list', methods=['GET'])
def get_dues_in():
    try:
        

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                army_number,
                `rank`,
                name,
                trade,
                unit,
                posting_order_no,
                date_of_move,
                dor,
                remarks
            FROM dues_in
            ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500