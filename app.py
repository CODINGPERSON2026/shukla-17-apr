from imports import *
from waitress import serve

import os
import csv
from io import StringIO, BytesIO
from flask import send_file
from functools import wraps

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.secret_key = os.urandom(24)

app.register_blueprint(personnel_info)
app.register_blueprint(weight_ms)
app.register_blueprint(leave_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(task_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(loan_bp)
app.register_blueprint(roll_call_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(inteview_bp)
app.register_blueprint(add_user_bp)
app.register_blueprint(oncourses_bp)
app.register_blueprint(agniveer_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(ollama_bot_bp)
app.register_blueprint(onco_leave_bp)
app.register_blueprint(dues_bp)
app.register_blueprint(sensitive_bp)



@app.route('/chat_bot')
def chat_bot():
    return render_template('/chat_ai.html')

@app.route("/admin_login", methods=["POST",'GET'])
def admin_login():
    print('in this route of admin login')
    if request.method == 'GET':
        return render_template('/loginpage/loginpage.html')
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    if conn is None:
         return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401
    username  =  user['username']
    role = user['role']
    print(role,"this is role")
    
    cursor.close()
    conn.close()


    # create JWT
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        'username':user['username'],
        "role": user["role"],
        'company':user['company'],
        'army_number':user['army_number']
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # set JWT in cookie
    resp = jsonify({"success": True,"username":username,'role' : role})
    resp.set_cookie("token", token, httponly=True, samesite="Lax")

    return resp

@app.route("/logout")
def logout():
    # Simple logout that clears cookie and redirects to root
    resp = redirect("/")  # This will trigger the dashboard() function which checks authentication
    resp.set_cookie("token", "", expires=0)
    return resp


@app.context_processor
def inject_user():
    user = require_login()
    
    if user:
        return {
            "current_user": user,
            "current_user_name": user['username'],
            "role": user['role'],
            'company':user['company']
        }
    # Return empty or default values if no user
    return {
        "current_user": None,
        "current_user_name": None,
        "role": None,
        'company':None
    }

 # password change
@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"success": False, "error": "Invalid request body."}), 400

    army_number  = data.get("army_number", "").strip()
    new_password = data.get("new_password", "").strip()

    if not army_number:
        return jsonify({"success": False, "error": "Army number is required."}), 400

    if not new_password:
        return jsonify({"success": False, "error": "New password is required."}), 400

    if len(new_password) < 3:
        return jsonify({"success": False, "error": "Password must be at least 3 characters."}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"success": False, "error": "Database connection failed."}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM users WHERE army_number = %s", (army_number,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"success": False, "error": "No user found with that Army Number."}), 404

        cursor.execute(
            "UPDATE users SET password = %s WHERE army_number = %s",
            (new_password, army_number)
        )

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Database error: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()
@app.route('/')
def dashboard():
    user = require_login()

    if not user:
        return redirect(url_for('admin_login'))
    subscript = user['username'].capitalize()
    user_company = user['company']
    role = user['role']
    welcome_msg = f'Welcome {role} , {subscript}'
    if user_company == 'Admin':
        print('entering co dashboard')
        return render_template('CO/co_dashboard.html', role = role,user_company=user_company)
    else:
        return render_template('dashboard.html', role = role,user_company=user_company)


@app.route('/api/dashboard_heading')
def dashboard_heading():
    # Determine heading dynamically
    # You can base this on user role, current tab, or any condition
    user = require_login()
    if user['role'] == 'CO':
        company = 'CO 15CESR'
    elif user['role'] == '2IC':
        company = '2IC 15CESR'
    else:
        company = user['company']  # Example
    print(company)
    
    
    return jsonify({"heading": company})










@app.route('/mt', methods=['GET', 'POST'])
def mt():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        vehicle_no = request.form['vehicle_no']
        vtype = request.form['type']
        vclass = request.form['class']
        detailment = request.form['detailment']
        dist_travelled = request.form['dist_travelled']
        quantity = request.form['quantity']
        bullet_proof = request.form.get('bullet_proof', 'N')

        insert_query = """
            INSERT INTO Vehicle_detail 
            (vehicle_no, type, class, detailment, dist_travelled, quantity, bullet_proof)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (vehicle_no, vtype, vclass, detailment, dist_travelled, quantity, bullet_proof))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('mt'))

    cursor.execute("SELECT * FROM Vehicle_detail")
    vehicles = cursor.fetchall()
    cursor.close()
    conn.close()

    drivers = [
        {"name": "Rajesh Kumar", "license": "MH14A12345", "hill_test": True, "vehicle": "Jeep"},
        {"name": "Amit Verma", "license": "MH12B67890", "hill_test": False, "vehicle": "Truck"},
        {"name": "Suresh Patel", "license": "MH13C99887", "hill_test": True, "vehicle": "Scorpio"},
    ]

    maintenance = [
        {"vehicle": "Truck MH14CD5678", "issue": "Brake fluid leakage", "date_reported": "2025-10-25", "status": "In Progress"},
        {"vehicle": "Motorcycle MH13GH2345", "issue": "Engine oil change", "date_reported": "2025-10-27", "status": "Pending"},
    ]

    return render_template('mt/mtView.html', vehicles=vehicles, drivers=drivers, maintenance=maintenance)
    
@app.route('/personal_info')
def personal_info():
    return render_template('personalInfoView.html')

@app.route('/personal/create', methods=['GET', 'POST'])
def create_personal():
    if request.method == 'POST':
        data = request.form.to_dict()
    return render_template('personalInfoView.html', form_view='create')

@app.route('/personal/update')
def update_personal():
    return render_template('personalInfoView.html', form_view='update')

@app.route('/personal/view')
def view_personal():
    return render_template('personalInfoView.html', form_view='view')


@app.route('/search_personnel', methods=['GET', 'POST'])
def search_person():
    print("in this route")

    # Get logged-in user
    user = require_login()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_company = user.get('company')
    if not user_company:
        return jsonify({'error': 'User company not found'}), 400

    if request.method == 'POST':
        query = request.form.get('army_number')  # ✅ CORRECT
        
        if not query:
            return jsonify([])

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        get_query = """
                SELECT 
                    name, 
                    army_number, 
                    `rank`, 
                    trade, 
                    company,
                    detachment_status AS det_status,
                    posting_status,
                    onleave_status AS leave_status
                FROM personnel
                WHERE army_number = %s
            """
        current_role = user['role']
        if current_role == 'Subedar Major':
            print("this should be here")
            cursor.execute(get_query,(query,))  # Added company filter
        else:
            get_query += 'AND company = %s'
            cursor.execute(get_query,(query,user_company))

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(results)
    
    else: # GET for Domain Specialization
        trade = request.args.get('trade')
        if not trade:
            return jsonify([])

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            query = """
                SELECT DISTINCT 
                    p.name, 
                    p.army_number, 
                    p.rank, 
                    p.trade, 
                    p.company,
                    u.duty_performed as current_duty
                FROM personnel p
                JOIN units_served u ON p.id = u.personnel_id
            """
            params = []
            where_clauses = []

            if trade != 'All':
                where_clauses.append("u.duty_performed = %s")
                params.append(trade)

            if user_company != "Admin":
                where_clauses.append("p.company = %s")
                params.append(user_company)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            cursor.execute(query, params)
            results = cursor.fetchall()
            return jsonify(results)
        except Exception as e:
            print("Error in specialization search:", str(e))
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/get_locations')
def get_locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT det_id, det_name FROM dets")
    locations = cursor.fetchall()
    conn.close()
    return jsonify(locations)

@app.route('/get_dets')
def get_dets():
    user = require_login()
    company = user['company']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT COUNT(*) AS count
                FROM personnel
                WHERE detachment_status = 1
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) AS count
                FROM personnel
                WHERE detachment_status = 1
                AND company = %s
            """, (company,))

        result = cursor.fetchone()

        return jsonify({'count': result['count']})

    finally:
        cursor.close()
        conn.close()

# @app.route('/get_interview_pending_count')
# def interview():
#     conn = get_db_connection()
#     cursor  =  conn.cursor(dictionary=True)
#     query = """
#     SELECT 
#         SUM(interview_status = 0) AS pending_count,
#         COUNT(*) AS total_count
#     FROM personnel
# """

#     cursor.execute(query)
#     result = cursor.fetchone()
#     pending_count = result["pending_count"]
#     total_count = result["total_count"]
#     percentage = 0
#     if total_count > 0:
#         percentage = pending_count/total_count * 100
#     cursor.close()
#     conn.close()
#     return jsonify({'result':result,'percentage':round(percentage, 2)})


@app.route('/get_pending_interview_list')
def get_pending_interview_list():
    print("in this route")

    search = request.args.get("search", "").strip()
    company_filter = request.args.get("company", "all").strip()

    current_user = require_login()
    current_user_company = current_user['company']
    print('Current user company:', current_user_company)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        excluded_ranks = ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
        rank_placeholders = ",".join(["%s"] * len(excluded_ranks))

        # =========================
        # 🔹 BASE CONDITION BUILD
        # =========================
        base_condition = f"""
            FROM personnel
            WHERE interview_status = 0
            AND `rank` NOT IN ({rank_placeholders})
        """

        params = list(excluded_ranks)

        # 👉 Company filter (if not Admin)
        if current_user_company != 'Admin':
            base_condition += " AND company = %s"
            params.append(current_user_company)

        # Admin can filter companies
        elif company_filter != "all":
            base_condition += " AND company = %s"
            params.append(company_filter)

        # 👉 Search filter
        if search:
            base_condition += " AND (army_number LIKE %s OR name LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])

        # =========================
        # 🔹 COUNT QUERY
        # =========================
        count_query = "SELECT COUNT(*) as total " + base_condition
        cursor.execute(count_query, tuple(params))
        count_result = cursor.fetchone()
        total_count = count_result['total']

        print("🔵 Total Pending Interviews Count:", total_count)

        # =========================
        # 🔹 DATA QUERY
        # =========================
        data_query = f"""
            SELECT name, army_number, home_state, company, `rank`
        """ + base_condition + " ORDER BY home_state"

        cursor.execute(data_query, tuple(params))
        pending_data = cursor.fetchall()

        print("🟢 Records Fetched:", len(pending_data))

        # =========================
        # 2️⃣ Collect home_states
        # =========================
        home_states = list({row['home_state'].strip().lower() for row in pending_data if row['home_state']})

        # =========================
        # 3️⃣ Fetch senior ranks — keyed by (home_state, company)
        # =========================
        senior_ranks = []
        senior_map = {}  # key = (home_state, company)

        if home_states:
            format_strings = ",".join(["%s"] * len(home_states))
            query = f"""
                SELECT name, army_number, home_state, company, `rank`
                FROM personnel
                WHERE home_state IN ({format_strings})
                AND `rank` IN ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
                ORDER BY home_state
            """
            cursor.execute(query, home_states)
            senior_ranks = cursor.fetchall()

            for jco in senior_ranks:
                state = jco['home_state'].strip().lower()
                jco_company = jco['company'].strip().lower()
                key = (state, jco_company)       # ← keyed by both
                if key not in senior_map:
                    senior_map[key] = jco['name']

        # =========================
        # 4️⃣ Assigned JCO fallback
        # =========================
        assigned_jco_map = {}

        if home_states:
            placeholders = ",".join(["%s"] * len(home_states))
            cursor.execute(f"""
                SELECT ja.additional_assigned_home_state AS home_state, 
                       p.name AS jco_name
                FROM jco_kunda_assignment ja
                JOIN personnel p ON p.army_number = ja.army_number
                WHERE ja.additional_assigned_home_state IN ({placeholders})
                AND ja.interview_status = 'Pending'
            """, home_states)

            assigned_rows = cursor.fetchall()

            for row in assigned_rows:
                state = row['home_state']
                if state not in assigned_jco_map:
                    assigned_jco_map[state] = f"Temporary Assigned JCO {row['jco_name']}"

        # =========================
        # 5️⃣ Attach JCO info — company-aware lookup
        # =========================
        for row in pending_data:
            state = row['home_state']
            soldier_company = row['company'].strip().lower()
            key = (state, soldier_company)       # ← match soldier's company

            if key in senior_map:
                row['jco_name'] = senior_map[key]
                row['jco_source'] = 'live'
            elif state in assigned_jco_map:
                row['jco_name'] = assigned_jco_map[state]
                row['jco_source'] = 'assigned'
            else:
                row['jco_name'] = None
                row['jco_source'] = None

        return jsonify({
            "status": "success",
            "total_count": total_count,
            "pending_interviews": pending_data,
            "senior_same_state": senior_ranks
        })

    except Exception as e:
        print("❌ Error fetching pending interview list:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/assign_personnel', methods=['POST'])
def assign_personnel():
    data = request.get_json()

    # Get logged-in user
    user = require_login()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401

    user_company = user.get('company')
    if not user_company:
        return jsonify({'error': 'User company not found'}), 400

    personnel_ids = data.get('army_number', [])
    action_type = data.get('status', '').lower()
    remarks = data.get('remarks', '')

    if not personnel_ids or not action_type:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    conn.start_transaction()  # ✅ Explicit Transaction Start
    cursor = conn.cursor(dictionary=True)
    user_role = user['role']
    try:
        # 🔐 Lock rows to prevent race condition
        placeholders = ', '.join(['%s'] * len(personnel_ids))

        if user_role == "Subedar Major":
            # 🚀 Admin-level access (no company restriction)
            verify_query = f"""
                SELECT army_number, detachment_status, posting_status, td_status
                FROM personnel
                WHERE army_number IN ({placeholders})
                FOR UPDATE
            """
            cursor.execute(verify_query, tuple(personnel_ids))
        else:
            # 🔒 Normal users (company restricted)
            verify_query = f"""
                SELECT army_number, detachment_status, posting_status, td_status
                FROM personnel
                WHERE army_number IN ({placeholders})
                AND company = %s
                FOR UPDATE
            """
            cursor.execute(verify_query, tuple(personnel_ids) + (user_company,))

        rows = cursor.fetchall()

        if len(rows) != len(personnel_ids):
            conn.rollback()
            return jsonify({"error": "Some personnel not found in your company"}), 403

        # 🔎 Validate status before assignment
        for status in rows:
            pid = status['army_number']

            if action_type == "det" and status['detachment_status'] == 1:
                conn.rollback()
                return jsonify({"error": f"{pid} is already in Detachment"}), 400

            if action_type == "posting" and status['posting_status'] == 1:
                conn.rollback()
                return jsonify({"error": f"{pid} is already Posted"}), 400

            if action_type == "td" and status['td_status'] == 1:
                conn.rollback()
                return jsonify({"error": f"{pid} is already on TD"}), 400

        # ✅ Perform Assignment
        for pid in personnel_ids:

            if action_type == "det":
                cursor.execute("""
                    INSERT INTO assigned_det (army_number, det_id)
                    VALUES (%s, %s)
                """, (pid, remarks))

                cursor.execute("""
                    UPDATE personnel 
                    SET detachment_status = 1
                    WHERE army_number = %s
                """, (pid,))

            elif action_type == "posting":
                cursor.execute("""
                    INSERT INTO posting_details_table
                    (army_number, location_posted_to, posting_date)
                    VALUES (%s, %s, NOW())
                """, (pid, remarks))

                cursor.execute("""
                    DELETE FROM personnel
                    WHERE army_number = %s
                """, (pid,))

            elif action_type == "td":

                td_location = ""
                td_authority = ""

                if "Location:" in remarks and "Authority:" in remarks:
                    parts = remarks.split(",")
                    td_location = parts[0].replace("Location:", "").strip()
                    td_authority = parts[1].replace("Authority:", "").strip()

                cursor.execute("""
                    INSERT INTO td_table
                    (
                        army_number,
                        remarks,
                        td_date,
                        location,
                        authority,
                        company
                    )
                    VALUES (%s, %s, NOW(), %s, %s, %s)
                """, (
                    pid,
                    remarks,
                    td_location,
                    td_authority,
                    user_company
                ))

                cursor.execute("""
                    UPDATE personnel 
                    SET td_status = 1
                    WHERE army_number = %s
                """, (pid,))

        # ✅ Commit Only If Everything Successful
        conn.commit()
        return jsonify({"message": f"{action_type.upper()} Assigned Successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route("/get_personnel_details/<army_number>")
def get_personnel_details(army_number):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT company 
            FROM personnel 
            WHERE army_number = %s
        """, (army_number,))
        
        result = cursor.fetchone()
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"company": "N/A"}), 404
            
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/get_sales_data")
def get_sales_data():
    try:
        data_type = request.args.get("type")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT date, liquor_sale, grocery_sale FROM sales")
        rows = cursor.fetchall()
        db.close()

        df = pd.DataFrame(rows)
        df['date'] = pd.to_datetime(df['date'])

        if data_type == "daily":
            df_group = df.groupby(df['date'].dt.date)[['liquor_sale', 'grocery_sale']].sum()

        elif data_type == "monthly":
            df_group = df.groupby(df['date'].dt.to_period('M'))[['liquor_sale', 'grocery_sale']].sum()
            df_group.index = df_group.index.astype(str)

        elif data_type == "yearly":
            df_group = df.groupby(df['date'].dt.year)[['liquor_sale', 'grocery_sale']].sum()

        labels = list(df_group.index.astype(str))
        liquor = df_group['liquor_sale'].tolist()
        grocery = df_group['grocery_sale'].tolist()

        return jsonify({
            "labels": labels,
            "liquor": liquor,
            "grocery": grocery
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/apply_leave')
def apply_leave():
    return render_template('apply_leave.html')

@app.route('/daily_running')
def daily_running():
    return render_template('mt/daily_running.html')


@app.route('/get_vehicle_details', methods=['POST'])
def get_vehicle_details():
    vehicle_no = request.form.get('vehicle_no')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT type, class FROM vehicle_detail WHERE vehicle_no=%s", (vehicle_no,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Vehicle not found"}), 500


@app.route('/submit_running', methods=['POST'])
def submit_running():
    vehicle_no = request.form['vehicle_no']
    v_type = request.form['type']
    v_class = request.form['class']
    from_place = request.form['from_place']
    to_place = request.form['to_place']
    remarks = request.form['remarks']
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO daily_running (vehicle_no, type, class, from_place, to_place, remarks, date)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(query, (vehicle_no, v_type, v_class, from_place, to_place, remarks))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Saved successfully"})


@app.route('/board_details')
def board_details():
    return render_template('boo/board_details.html')


@app.route("/get_boards")
def get_boards():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM boards ORDER BY id DESC")
    boards = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(boards)


@app.route("/add_board", methods=["POST"])
def add_board():
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO boards 
        (order_no, entry_date, authority, subject, presiding_officer, completion_date, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        data.get("order_no"),
        data.get("entry_date"),
        data.get("authority"),
        data.get("subject"),
        data.get("presiding_officer"),
        data.get("completion_date"),
        data.get("remarks"),
    ))

    conn.commit()
    cur.close()

    return jsonify({"status": "success"})


@app.route("/delete_board/<int:board_id>", methods=["DELETE"])
def delete_board(board_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM boards WHERE id=%s", (board_id,))
    conn.commit()
    cur.close()
    return jsonify({"status": "success"})


@app.route("/edit_board/<int:board_id>", methods=["POST"])
def edit_board(board_id):
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        UPDATE boards
        SET order_no=%s, entry_date=%s, authority=%s, subject=%s,
            presiding_officer=%s, completion_date=%s, remarks=%s
        WHERE id=%s
    """

    cur.execute(query, (
        data.get("order_no"),
        data.get("entry_date"),
        data.get("authority"),
        data.get("subject"),
        data.get("presiding_officer"),
        data.get("completion_date"),
        data.get("remarks"),
        board_id
    ))

    conn.commit()
    cur.close()

    return jsonify({"status": "success"})


@app.route("/get_board_members/<order_no>")
def get_board_members(order_no):
    print(order_no,'these are boards members')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM board_members WHERE order_no=%s", (order_no,))
    members = cur.fetchall()
    cur.close()
    return jsonify(members)


@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO board_members (order_no, member_name, army_number)
        VALUES (%s, %s, %s)
    """, (data.get("order_no"), data.get("member_name"), data.get("army_number")))
    conn.commit()
    cur.close()

    return jsonify({"status": "success"})
















@app.route("/delete_member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM board_members WHERE id=%s", (member_id,))
    conn.commit()
    cur.close()
    return jsonify({"status": "success"})

@app.route("/edit_member/<int:member_id>", methods=["POST"])
def edit_member(member_id):
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE board_members
        SET member_name=%s, army_number=%s
        WHERE id=%s
    """, (data.get("member_name"), data.get("army_number"), member_id))

    conn.commit()
    cur.close()

    return jsonify({"status": "success"})


# ===============================================
# SENSITIVE PERSONNEL MANAGEMENT - FIXED
# ===============================================
@app.route("/search_personnel_to_mark", methods=["POST"])
def search_personnel():
    query = request.form.get("query", "").strip()
    
    print("THIS IS INCOMING:", query)  # Should now print
    import sys
    sys.stdout.flush()

    if len(query) < 2:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        like_pattern = f"%{query}%"

        
        cursor.execute("""
            SELECT army_number, name,`rank`, company
            FROM personnel
            WHERE LOWER(name) LIKE LOWER(%s)
               OR army_number LIKE %s
            ORDER BY name
            LIMIT 50
        """, (like_pattern, like_pattern))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                "army_number": row[0],
                "name": row[1],
                "rank": row[2],
                "company": row[3] or "N/A"
            })

        print(f"Found {len(results)} results for '{query}'")
        return jsonify(results)

    except Exception as e:
        print("Search error:", e)
        import traceback
        traceback.print_exc()  # This will show full error in console
        return jsonify({"error": "Database error"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route("/mark_personnel", methods=["GET"])
def mark_personnel():
    conn = get_db_connection()
    cursor = conn.cursor()   
    cursor.execute("""
        SELECT s.id, s.army_number, s.reason, s.marked_on, 
               p.name, p.rank, p.company
        FROM sensitive_marking s
        JOIN personnel p ON s.army_number = p.army_number
        ORDER BY s.marked_on DESC
    """)
    rows = cursor.fetchall()

    sensitive_list = []
    for r in rows:
        sensitive_list.append({
            "id": r[0],
            "army_number": r[1],
            "reason": r[2],
            "marked_on": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else "",
            "name": r[4],
            "rank": r[5],
            "company": r[6] or "N/A"
        })
    
    cursor.close()
    conn.close()
    
    response = make_response(render_template("sensitive_indl/mark_personnel.html", sensitive_list=sensitive_list))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# AJAX: Mark as Sensitive
@app.route("/mark_sensitive", methods=["POST"])
def mark_sensitive():
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")
    
    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing army number or reason"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if already marked
        cursor.execute("SELECT 1 FROM sensitive_marking WHERE army_number = %s", (army_number,))
        if cursor.fetchone():
            return jsonify({"success": False, "error": "This personnel is already marked as sensitive."}), 400

        cursor.execute("""
            INSERT INTO sensitive_marking (army_number, reason, marked_on)
            VALUES (%s, %s, %s)
        """, (army_number, reason.strip(), datetime.now()))
        conn.commit()

        return jsonify({"success": True, "message": "Personnel marked as sensitive successfully."})

    except Exception as e:
        conn.rollback()
        print("ERROR in mark_sensitive:", e)
        return jsonify({"success": False, "error": "Database error"}), 500
    finally:
        cursor.close()
        conn.close()


# AJAX: Update Reason
@app.route("/update_sensitive_reason", methods=["POST"])
def update_sensitive_reason():
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")
    
    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing data"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE sensitive_marking SET reason = %s WHERE army_number = %s", (reason.strip(), army_number))
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Personnel not found in sensitive list"}), 404
        
        conn.commit()
        return jsonify({"success": True, "message": "Reason updated successfully."})
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return jsonify({"success": False, "error": "Update failed"}), 500
    finally:
        cursor.close()
        conn.close()


# AJAX: Remove from Sensitive List
@app.route("/remove_sensitive", methods=["POST"])
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


# New: AJAX endpoint to refresh sensitive list
@app.route("/get_sensitive_list", methods=["GET"])
def get_sensitive_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.id, s.army_number, s.reason, s.marked_on, 
                   p.name, p.rank, p.company
            FROM sensitive_marking s
            JOIN personnel p ON s.army_number = p.army_number
            ORDER BY s.marked_on DESC
        """)
        rows = cursor.fetchall()
        print(rows)

        sensitive_list = []
        for r in rows:
            sensitive_list.append({
                "army_number": r[1],
                "reason": r[2],
                "marked_on": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else "",
                "name": r[4],
                "rank": r[5],
                "company": r[6] or "N/A"
            })
        print(sensitive_list,"this is sensitive list")
        return jsonify({"success": True, "data": sensitive_list})
    
    except Exception as e:
        print("Error fetching sensitive list:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ===============================================
# PARADE STATE
# ===============================================

@app.route("/leave_status")
def leave_status():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
    company,
    SUM(CASE WHEN onleave_status = '1' THEN 1 ELSE 0 END) AS leave_count,
    COUNT(*) AS total_count,
    ROUND((SUM(CASE WHEN onleave_status = '1' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS leave_percentage
    FROM personnel
    GROUP BY company
    ORDER BY company
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


@app.route("/company_status")
def company_status():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    data = []

    rank_sql = """
    SELECT
        SUM(CASE WHEN `rank` IN ('agniveer', 'Signal Man','nk','lnk','hav') THEN 1 ELSE 0 END) AS other_rank_count,
        SUM(CASE WHEN `rank` IN ('nbsub','subedar','JCO','sub maj') THEN 1 ELSE 0 END) AS jco_count,
        SUM(CASE WHEN `rank` IN ('lt','capt','maj','ltcol','col','OC') THEN 1 ELSE 0 END) AS officer_count
    FROM personnel
    """

    try:
        cur.execute(rank_sql)
        overall = cur.fetchone() or {"other_rank_count": 0, "jco_count": 0, "officer_count": 0}
        overall["company"] = "15 XYZ"
        data.append(overall)

        companies = ["1 company", "2 company", "3 company", "HQ company"]
        sql_with_where = rank_sql + " WHERE company = %s"

        for company in companies:
            cur.execute(sql_with_where, (company,))
            row = cur.fetchone() or {"other_rank_count": 0, "jco_count": 0, "officer_count": 0}
            row["company"] = company
            data.append(row)

        return jsonify(data)

    finally:
        cur.close()
        conn.close()


@app.route("/paradeState")
def paradeState():
    return render_template("daily_state/daily_parade_state.html")

@app.route("/add_event", methods=["POST"])
def add_event():
    user = require_login()  # Get logged-in user
    user_company = user['company']
    
    event_date = request.form["event_date"]
    event_name = request.form["event_name"]
    venue = request.form["venue"]

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if company column exists
    cursor.execute("DESCRIBE daily_events")
    columns = [col[0] for col in cursor.fetchall()]
    has_company = 'company' in columns
    
    if has_company:
        cursor.execute(
            "INSERT INTO daily_events (event_date, event_name, venue, company) VALUES (%s, %s, %s, %s)",
            (event_date, event_name, venue, user_company)
        )
    else:
        cursor.execute(
            "INSERT INTO daily_events (event_date, event_name, venue) VALUES (%s, %s, %s)",
            (event_date, event_name, venue)
        )
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/daily_event")
def daily_event():
    today = date.today()

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM daily_events WHERE event_date = %s", (today,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


# ===============================================
# ALARM FUNCTIONALITY
# ===============================================


@app.route('/api/assigned_alarm')
def assigned_alarm():
    conn = None
    cursor = None
    try:
        user = require_login()  # Get logged-in user
        user_company = user['company']
        print("Logged-in user's company:", user_company)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = '''
        SELECT 
            ad.army_number, 
            p.name,
            p.rank,
            p.company,
            ad.det_id, 
            d.det_name, 
            ad.assigned_on,
            ad.det_status,
            DATEDIFF(NOW(), ad.assigned_on) AS days_on_det
        FROM assigned_det ad
        LEFT JOIN dets d ON ad.det_id = d.det_id
        LEFT JOIN personnel p ON ad.army_number = p.army_number
        WHERE DATEDIFF(NOW(), ad.assigned_on) > 90
          AND ad.det_status = 1
        '''

        params = []

        # Apply company filter if user is not Admin
        if user_company != "Admin":
            query += " AND p.company = %s"
            params.append(user_company)

        query += " ORDER BY ad.assigned_on ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "rows": rows})

    except Exception as e:
        print("Error fetching assigned alarms:", e)
        return jsonify({"status": "error", "message": str(e)})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




@app.route("/api/assistant_test_alarm")
def assistant_test_alarm():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        army_no,
        name,
        batch,
        next_test_date
    FROM assistant_tests
    WHERE next_test_date > CURDATE()
    ORDER BY next_test_date ASC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"rows": rows})




@app.route("/api/leave_pending_alarm", methods=["GET"])
def leave_pending_alarm():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    role = user['role']
    

    try:
        query = """
            SELECT
                COUNT(*) AS pending_count
            FROM leave_status_info
            WHERE request_status LIKE 'Pending%'
            AND updated_at < NOW() - INTERVAL 7 DAY
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if role != 'CO':
            result['pending_count'] = 0


        return jsonify({
            "pending": result["pending_count"]
        })

    except Exception as e:
        print(str(e))
        return jsonify({
            "pending": 0,
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


@app.route("/api/leave_pending_details", methods=["GET"])
def leave_pending_details():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    role = user['role']

    if role != 'CO':
        return jsonify({"error": "Unauthorized"}), 403

    try:
        query = """
            SELECT
                id            AS leave_id,
                army_number,
                name          AS full_name,
                `rank`,
                company,
                leave_type,
                leave_days,
                from_date,
                to_date,
                request_status,
                request_sent_to,
                leave_reason,
                updated_at,
                DATEDIFF(NOW(), updated_at) AS days_pending
            FROM leave_status_info
            WHERE request_status LIKE 'Pending%'
            AND updated_at < NOW() - INTERVAL 7 DAY
            ORDER BY days_pending DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            for key, val in row.items():
                if hasattr(val, 'isoformat'):
                    row[key] = val.isoformat()

        return jsonify({
            "pending":  len(rows),
            "requests": rows
        })

    except Exception as e:
        return jsonify({"pending": 0, "requests": [], "error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()






@app.route('/api/today_event_alarm')
def today_event_alarm():
    user = require_login()  # Get logged-in user
    user_company = user['company']
    print("Logged-in user's company:", user_company)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 🔹 Dynamically check if 'company' column exists to avoid SQL errors
        cursor.execute("DESCRIBE daily_events")
        columns = [col['Field'] for col in cursor.fetchall()]
        has_company = 'company' in columns

        query = "SELECT id, event_name, venue FROM daily_events WHERE event_date = CURDATE()"
        params = []

        # Apply company filter only if column exists and user is not Admin
        if has_company and user_company != "Admin":
            query += " AND company = %s"
            params.append(user_company)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        print(rows,"these are todays events")
        return jsonify({"status": "success", "rows": rows})

    except Exception as e:
        print("Error fetching today's events:", e)
        return jsonify({"status": "error", "message": str(e)})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()









@app.route("/api/assistant_test_alarm")
def assistant_test_alarm_api():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT army_no, name, batch,
               asst_test1, asst_test2, asst_test3, asst_test4
        FROM agniveers
        WHERE asst_test_status = 'Pending'
    """)

    rows = cursor.fetchall()
    print(rows,"asistent test pending alarm")
    cursor.close()
    conn.close()

    today = date.today()
    alarms = []

    for r in rows:
        dates = [r["asst_test1"], r["asst_test2"],
                 r["asst_test3"], r["asst_test4"]]
        dates = [d for d in dates if d and d >= today]

        if dates:
            next_test = min(dates)
            alarms.append({
                "army_no": r["army_no"],
                "name": r["name"],
                "batch": r["batch"],
                "next_test_date": next_test.strftime("%Y-%m-%d")
            })

    return jsonify({
        "count": len(alarms),
        "rows": alarms
    })




# ===============================================
# PROJECTS
# ===============================================
@app.route('/projects-dashboard')
def projects_dashboard():
    return render_template('/projects/projects.html')

@app.route('/stats/cost_by_head', methods=['GET'])
def get_cost_by_head():
    connection = get_db_connection()
    if not connection:
        return jsonify({
            "status": "error",
            "message": "Database connection failed"
        }), 500

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT 
            COALESCE(head, 'Unassigned') AS head,
            ROUND(SUM(project_cost), 2) AS total_cost,
            COUNT(*) AS count
        FROM projects
        GROUP BY head
        ORDER BY total_cost DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()

        # Convert decimal to float for JSON serialization
        for row in results:
            row['total_cost'] = float(row['total_cost'])

        return jsonify({
            "status": "success",
            "data": results
        })

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()






@app.route('/get_project_heads')
def get_project_heads():
    print("in this route of project heads")
    try:
     
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT id, head_name FROM project_heads ORDER BY head_name")
        heads = cursor.fetchall()

        cursor.close()
        conn.close()
        print(heads)
        return jsonify(heads)  # Returns: [{"id": 1, "head_name": "Civil Works"}, ...]

    except Exception as e:
        print(f"Error fetching heads: {e}")
        return jsonify([]), 500


@app.route("/get_projects_count", methods=["GET"])
def get_project_count():
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select count(*) as count from projects')
    project_count = cursor.fetchone()
    count = project_count['count']
    conn.close()
    return jsonify({"status": "success",'count':count})


@app.route('/update_project_stage', methods=['POST'])
def update_project_stage():
    data = request.get_json()
    project_id = data.get('project_id')
    new_stage = data.get('new_stage')

    if not project_id or not new_stage:
        return jsonify({"status": "error", "message": "Missing project ID or stage"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projects
            SET current_stage = %s
            WHERE project_id = %s
        """, (new_stage, project_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        print("Error updating stage:", e)
        return jsonify({"status": "error", "message": "Database error"}), 500


# Add new head
@app.route('/add_head', methods=['POST'])
def add_head():
    data = request.get_json()
    head_name = data.get("head_name").strip()
    if not head_name:
        return jsonify(status='error', message='Head name cannot be empty')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO project_heads (head_name) VALUES (%s)", (head_name,))
        conn.commit()
        return jsonify(status='success')
    except mysql.connector.IntegrityError:
        return jsonify(status='error', message='Head already exists')
    except Exception as e:
        return jsonify(status='error', message=str(e))

ranks = ('Naib Subedar', 'Subedar', 'Subedar Major')
@app.route("/search_officer")
def search_officer():
    name_query = request.args.get("name", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT name, `rank`, company,army_number
    FROM personnel
    WHERE name LIKE %s AND `rank` IN (%s, %s, %s)
    LIMIT 10
""", (f"%{name_query}%", *ranks))

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print('results these are ',results)
    return jsonify(results)


@app.route('/get_man_power')
def manPower():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query= 'select count(*) as total_count from personnel'
        cursor.execute(query,)
        total_count = cursor.fetchone()
        count = total_count['total_count']
        return jsonify({'count':count}),200
    except Exception as e:
        print('There was an exception',str(e))
        return jsonify({'error':'Internal Server Error'}),500

#-------------parade state count fuction--------------------------------------------
@app.route('/api/get-parade-count')
def get_parade_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT `rank`, `company`, COUNT(*) AS count 
        FROM personnel
        GROUP BY `rank`, `company`
        ORDER BY `rank`;
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    formatted = {}

    for row in results:
        rank = row['rank']
        company_name = row['company']
        count = row['count']

        company_number = ''.join(filter(str.isdigit, company_name))
        company_key = f"c{company_number}"

        if rank not in formatted:
            formatted[rank] = {"c1": 0, "c2": 0, "c3": 0, "c4": 0}

        formatted[rank][company_key] = count

    return jsonify(formatted)


@app.route('/api/unfit-graph')
def line_unfit_graph():
    company = request.args.get('company', 'All')
    print('the value is',company)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT month, unfit_count
        FROM monthly_medical_status
        WHERE year = YEAR(CURDATE())
          AND unit = %s
        ORDER BY month
    """, (company,))
    result = cursor.fetchall()
    return jsonify(result)



@app.route('/projects')
def get_projects():
    print('in this project route')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    company = user['company']
    role = user.get('role') or ''

    try:
        # 1️⃣ Fetch projects
        project_query = """
            SELECT project_id, head, project_name, current_stage, project_cost, project_items, quantity, project_description
            FROM projects
        """
        params = []

        # Apply company filter if not Admin; PROJECT JCO and PROJECT OFFICER see all projects
        if company != "Admin" and role not in ('PROJECT JCO', 'PROJECT OFFICER'):
            project_query += " WHERE company = %s"
            params.append(company)

        cursor.execute(project_query, params)
        projects = cursor.fetchall()

        # 2️⃣ Fetch all heads from project_heads table
       

        # 3️⃣ Render template with both projects and heads
        return render_template("projects/projects.html", projects=projects)

    except Exception as e:
        print("Error fetching projects or heads:", str(e))
        return "Server Error", 500

    finally:
        cursor.close()
        conn.close()


# single route for all dashboard
# #################################################################### MAIN API FOR DASHB AORD ##############################


JCO_RANKS = ('Subedar', 'Naib Subedar', 'Subedar Major')

OFFICER_RANKS = (
    'Lieutenant', 'Captain', 'Major',
    'Lieutenant Colonel', 'Colonel',
    'Brigadier', 'Major General',
    'Lieutenant General', 'General'
)

@app.route('/api/dashboard_summary', methods=['GET'])
def dashboard_summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    current_user = user['army_number']
    company = user['company']
    role = user['role']
    print("Logged-in user's company:", company)
    
    try:
        # 1️⃣ Detachments Count
        cursor.execute(
            "SELECT COUNT(*) AS count FROM personnel WHERE detachment_status = 1" + 
            (f" AND company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        detachment_result = cursor.fetchone()
        detachments = detachment_result['count'] if detachment_result else 0

        

        # 2️⃣ Manpower Count (Rank-wise - Aggregated for latest available date)
        # Get the latest reporting date across all companies (if Admin) or for specific company
        date_query = "SELECT MAX(report_date) as max_date FROM parade_state_daily"
        date_params = []
        if company != "Admin":
            date_query += " WHERE company = %s"
            date_params.append(company)
        
        cursor.execute(date_query, date_params)
        
        max_date_result = cursor.fetchone()
        print("max_date_result")
        print(max_date_result)
        latest_date = max_date_result['max_date'] if max_date_result else None

        if latest_date:
            query = """
                SELECT 
                    SUM(IFNULL(offr_present_unit, 0)) AS officerCount,
                    SUM(IFNULL(jco_present_unit, 0) + IFNULL(jcoEre_present_unit, 0)) AS jcoCount,
                    SUM(IFNULL(or_present_unit, 0) + IFNULL(orEre_present_unit, 0)) AS orCount,
                    SUM(
                        IFNULL(offr_present_unit, 0) + 
                        IFNULL(jco_present_unit, 0) + 
                        IFNULL(jcoEre_present_unit, 0) + 
                        IFNULL(or_present_unit, 0) + 
                        IFNULL(orEre_present_unit, 0)
                    ) AS total
                FROM parade_state_daily
                WHERE report_date = %s
            """
            params = [latest_date]
            if company != "Admin":
                query += " AND company = %s"
                params.append(company)
            
            cursor.execute(query, params)
            manpower_result = cursor.fetchone()
        else:
            manpower_result = None

        if manpower_result and manpower_result['total'] is not None:
            manpower = {
                "total": int(manpower_result["total"]),
                "jcoCount": int(manpower_result["jcoCount"]),
                "officerCount": int(manpower_result["officerCount"]),
                "orCount": int(manpower_result["orCount"])
            }
        else:
            manpower = {"total": 0, "jcoCount": 0, "officerCount": 0, "orCount": 0}

        print(manpower_result,"this is the main power result")
        # Check if we have valid data from parade_state_daily
        has_parade_data = manpower_result and (
            (manpower_result["officerCount"] or 0) > 0 or 
            (manpower_result["jcoCount"] or 0) > 0 or 
            (manpower_result["orCount"] or 0) > 0
        )

        if has_parade_data:
            manpower = {
                "total": int(manpower_result["total"] or 0),
                "jcoCount": int(manpower_result["jcoCount"] or 0),
                "officerCount": int(manpower_result["officerCount"] or 0),
                "orCount": int(manpower_result["orCount"] or 0)
            }
        
        # 3️⃣ Interview Pending
        if role in ['JCO', 'S/JCO']:
             cursor.execute('SELECT home_state FROM personnel WHERE army_number = %s', (current_user,))
             home_result = cursor.fetchone()
             home_state = home_result['home_state'] if home_result else None

             query = """
           SELECT 
    COALESCE(SUM(interview_status = 0), 0) AS pending_count,
    COUNT(*) AS total_count
FROM personnel
WHERE company = %s
  AND home_state = %s
  AND `rank` NOT IN (
      'Subedar', 'Naib Subedar', 'Subedar Major',
      'Lieutenant', 'Captain', 'Major',
      'Lieutenant Colonel', 'Colonel',
      'Brigadier', 'Major General',
      'Lieutenant General', 'General'
  );
        """
             cursor.execute(query, (company, home_state))
        else:
            query = """
            SELECT 
                COALESCE(SUM(interview_status = 0), 0) AS pending_count,
                COUNT(*) AS total_count
            FROM personnel
            WHERE `rank` IN ('AGNIVEER', 'Signal Man', 'L NK', 'NK','CFN', 'HAV','LOC NK','L HAV','CHM','RHM')
        """
            params = []
            if company != "Admin":
                query += " AND company = %s"
                params.append(company)
            cursor.execute(query, params)

        interview_result = cursor.fetchone()
        pending_count = interview_result['pending_count'] if interview_result else 0
        total_interview_count = interview_result['total_count'] if interview_result else 0
        interview_percentage = round((pending_count / total_interview_count) * 100, 2) if total_interview_count > 0 else 0

        # 4️⃣ Projects Count
        project_query = "SELECT COUNT(*) AS count FROM projects WHERE 1=1"
        project_params = []
        if company != "Admin":
            project_query += " AND company = %s"
            project_params.append(company)
        cursor.execute(project_query, project_params)
        projects_result = cursor.fetchone()
        projects = projects_result['count'] if projects_result else 0

        # 5️⃣ Assigned Alarm (Assignments older than 5 days)
        cursor.execute(
            '''
            SELECT 
                ad.army_number, 
                p.name,
                p.rank,
                p.company,
                ad.det_id, 
                d.det_name, 
                ad.assigned_on,
                ad.det_status,
                DATEDIFF(NOW(), ad.assigned_on) AS days_on_det
            FROM assigned_det ad
            LEFT JOIN dets d ON ad.det_id = d.det_id
            LEFT JOIN personnel p ON ad.army_number = p.army_number
            WHERE DATEDIFF(NOW(), ad.assigned_on) > 5
              AND ad.det_status = 1
              ''' + (f" AND p.company = %s" if company != "Admin" else "") +
            '''
            ORDER BY ad.assigned_on ASC;
            ''',
            (company,) if company != "Admin" else ()
        )
        assigned_alarm_rows = cursor.fetchall()

        # 6️⃣ Sensitive Personnel Count
        cursor.execute(
            '''
            SELECT COUNT(*) AS count
            FROM sensitive_marking sm
            LEFT JOIN personnel p ON sm.army_number = p.army_number
            ''' + (f" WHERE p.company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        sensitive_result = cursor.fetchone()
        sensitive_count = sensitive_result['count'] if sensitive_result else 0
        
        # 7️⃣ Boards Count
        cursor.execute("SELECT COUNT(*) AS count FROM boards")
        boards_result = cursor.fetchone()
        boards_count = boards_result['count'] if boards_result else 0

        # 🔹 TD Attachments Count (td_status = 1)
        cursor.execute(
            "SELECT COUNT(*) AS count FROM personnel WHERE td_status = 1" +
            (f" AND company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        td_result = cursor.fetchone()
        td_attachments = td_result['count'] if td_result else 0
        
        # 🔹 Courses Count
        course_query = """
            SELECT COUNT(*) AS count 
            FROM candidate_on_courses c
            LEFT JOIN personnel p ON c.army_number = p.army_number
            WHERE 1=1
        """
        course_params = []
        if company != "Admin":
            course_query += " AND p.company = %s"
            course_params.append(company)
        cursor.execute(course_query, course_params)
        courses_result = cursor.fetchone()
        courses_count = courses_result['count'] if courses_result else 0

        # 🔹 Loans Count
        cursor.execute(
            '''
            SELECT COUNT(*) AS count
            FROM loans l
            LEFT JOIN personnel p ON l.army_number = p.army_number
            ''' + (f" WHERE p.company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        loan_result = cursor.fetchone()
        loan_count = loan_result['count'] if loan_result else 0
        
        # 8️⃣ Roll Call Pending Points
        cursor.execute("SELECT count(id) as count FROM roll_call_points WHERE status = 'PENDING'")
        roll_call_result = cursor.fetchone()
        roll_call_pending_count = roll_call_result['count'] if roll_call_result else 0

        # 🔹 Tasks Count (Assigned to current user)
        cursor.execute(
            """
            SELECT 
                COUNT(*) AS total_tasks,
                COALESCE(SUM(task_status != 'COMPLETED'), 0) AS pending_tasks
            FROM tasks
            WHERE assigned_to = %s
            """,
            (current_user,)
        )
        task_result = cursor.fetchone()
        total_tasks = task_result['total_tasks'] if task_result else 0
        pending_tasks = task_result['pending_tasks'] if task_result else 0
        pending_percentage = round((pending_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0

        # 🔹 Duty Count (Domain Specialization)
        duty_query = """
    SELECT COUNT(DISTINCT p.army_number) AS count
    FROM personnel p
    LEFT JOIN (
        SELECT army_number, duty_performed
        FROM units_served
        WHERE (army_number, sr_no) IN (
            SELECT army_number, MAX(sr_no)
            FROM units_served
            GROUP BY army_number
        )
    ) u ON p.army_number = u.army_number
    WHERE u.duty_performed IS NOT NULL AND u.duty_performed != ''
"""
        duty_params = []
        if company != "Admin":
            duty_query += " AND p.company = %s"
            duty_params.append(company)
        
        cursor.execute(duty_query, duty_params)
        duty_result = cursor.fetchone()
        duty_count = duty_result['count'] if duty_result else 0
        
        cursor.execute("SELECT COUNT(*) AS dues_in FROM dues_in")
        dues_in = cursor.fetchone()['dues_in'] or 0

        cursor.execute("SELECT COUNT(*) AS dues_out FROM dues_out")
        dues_out = cursor.fetchone()['dues_out'] or 0

        # AGNIVEER
        agniveer_query = "SELECT COUNT(id) as agniveer_count from personnel where `rank` = 'Agniveer'"
        agniveer_params = []
        # Roles that should see total unit count
        privileged_roles = ['Admin', 'CO', '2IC', 'ADJUTANT', 'TRGJCO', 'OC']
        if company != "Admin" and role not in privileged_roles:
            agniveer_query += " AND company = %s"
            agniveer_params.append(company)
        cursor.execute(agniveer_query, agniveer_params)
        agniveer_result = cursor.fetchone()
        count_of_agniveer = agniveer_result['agniveer_count'] if agniveer_result else 0
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(manpower,'this is result of man power')

        # Return combined JSON
        return jsonify({
            "status": "success",
            "detachments": detachments,
            "tasks": {
                "total": total_tasks,
                "pending": pending_tasks,
                "pending_percentage": pending_percentage
            },
            "manpower": manpower,
            "interview": {
                "pending_count": pending_count,
                "total_count": total_interview_count,
                "percentage": interview_percentage
            },
            "projects": projects,
            "boards_count": boards_count, 
            "assigned_alarm": assigned_alarm_rows,
            "sensitive_count": sensitive_count,
            "attachment_count": td_attachments,
            "courses_count": courses_count,
            "loan_count": loan_count,
            "roll_call_pending_points": roll_call_pending_count,
            "agniveer_count": count_of_agniveer,
            "duty_count": duty_count,
            "dues_in":dues_in,
            "dues_out":dues_out
        }), 200

    except Exception as e:
        print("Error fetching dashboard summary:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

    finally:
        cursor.close()
        conn.close()




        
#================start course details in table format ============

@app.route('/personnel_info/course')
def course_view():
    require_login()
    return render_template('course.html')




#======================================== end course details in table format show=============================================
        
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    """Get current user information"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'username': user.get('username'),
        'company': user.get('company'),
        'role': user.get('role')
    })

def get_current_user():
    """Get current user from JWT token"""
    token = request.cookies.get('token')
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except:
        return None

def get_column_name(index):
    """Helper to map index to column names"""
    columns = [
        'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
        'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
        'present_det', 'present_unit', 'dues_in', 'dues_out'
    ]
    return columns[index] if index < len(columns) else f'col_{index}'

@app.route('/api/parade-state/get/<date_str>', methods=['GET'])
def get_parade_state(date_str):
    """Get parade state with calculated columns"""
    print(f"\n=== GET PARADE STATE for date: {date_str} ===")
    
    # Get current user
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    company = user.get('company')
    if not company:
        return jsonify({'success': False, 'error': 'No company assigned'}), 400
    
    print(f"User: {user.get('username')}, Company: {company}")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # FIX: Use datetime.strptime and date.today() correctly
        requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today_date = date.today()
        
        # If user is trying to access future date, return error
        if requested_date > today_date:
            return jsonify({
                'success': False,
                'error': 'Cannot access data for future dates',
                'is_future': True
            }), 400
        
        # Get data for specific date and company
        cursor.execute("""
            SELECT * FROM parade_state_daily 
            WHERE report_date = %s AND company = %s
        """, (date_str, company))
        
        row = cursor.fetchone()
        
        # If no data found for today, try to get previous day's data
        if not row and requested_date == today_date:
            print(f"No data found for today ({date_str}), trying previous day...")
            
            # Get previous day's date
            previous_date = today_date - timedelta(days=1)
            cursor.execute("""
                SELECT * FROM parade_state_daily 
                WHERE report_date = %s AND company = %s
            """, (previous_date.strftime('%Y-%m-%d'), company))
            
            row = cursor.fetchone()
            
            if row:
                print(f"Using previous day's data ({previous_date}) as template")
                row['is_previous_day_template'] = True
                row['original_date'] = row['report_date']
                row['report_date'] = date_str
            else:
                print(f"No data found for date: {date_str} or previous day, company: {company}")
                return jsonify({
                    'success': False,
                    'message': 'No data found for this date or previous day'
                }), 404
        
        # Convert database row back to frontend format
        result = {
            'date': row['report_date'],
            'company': row['company'],
            'data': {}
        }
        
        # Add flags if using previous day's data
        if 'is_previous_day_template' in row:
            result['is_previous_day_template'] = True
            result['original_date'] = row['original_date']
        
        # All categories in the exact order they appear in frontend
        all_categories = [
            'offr', 'jco', 'jcoEre', 'or', 'orEre',
            'firstTotal',
            'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
            'secondTotal',
            'grandTotal'
        ]
        
        for category in all_categories:
            category_data = []
            for i in range(17):
                column_name = f"{category}_{get_column_name(i)}"
                category_data.append(row.get(column_name, 0))
            result['data'][category] = category_data
        
        result['calculations'] = {
            't_out_formula': 'LVE + COURSE + DET + MH + SICK/LVE + EX + TD + ATT + AWL/OSL/JC',
            'present_det': 'Same as DET column value',
            'present_unit': 'POSTED/STR - T/OUT'
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/test-auth')
def test_auth():
    user = get_current_user()
    if user:
        return jsonify({
            'authenticated': True,
            'username': user.get('username'),
            'role': user.get('role'),
            'company': user.get('company')
        })
    else:
        return jsonify({'authenticated': False}), 401
    

# co dashboard view
# Add these routes to your Flask app (app.py)

@app.route('/api/co-dashboard/all-data/<date_str>', methods=['GET'])
def get_co_all_dashboard_data(date_str):
    """Get all CO dashboard data in a single request for a specific date"""
    user = require_login()
    
    role = user.get('role', '')
    if role not in ['CO', '2IC', 'ADJUTANT', 'OC']:
        return jsonify({'success': False, 'error': 'Unauthorized - access denied'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    company_filter = ""
    params = [date_str]
    if role == 'OC':
        company_filter = " AND company = %s"
        params.append(user.get('company'))
    
    try:
        cursor.execute(f"""
            SELECT 
                SUM(grandTotal_posted_str) as total_posted_str,
                SUM(grandTotal_present_unit) as present_unit,
                SUM(grandTotal_trout_det) as total_out,
                SUM(grandTotal_lve) as total_lve,  -- Add this line
                COUNT(DISTINCT company) as company_count
            FROM parade_state_daily
            WHERE report_date = %s {company_filter}
        """, tuple(params))
        parade_summary = cursor.fetchone()
        
        cursor.execute(f"""
            SELECT 
                company,
                grandTotal_lve as on_leave,  -- Changed from grandTotal_trout_det to grandTotal_lve
                grandTotal_posted_str as total_strength,
                ROUND((grandTotal_lve / NULLIF(grandTotal_posted_str, 0) * 100), 2) as leave_percentage  -- Changed here too
            FROM parade_state_daily
            WHERE report_date = %s {company_filter}
            ORDER BY company
        """, tuple(params))
        leave_data = cursor.fetchall()
        
        cursor.execute(f"""
            SELECT 
                company,
                (IFNULL(offr_present_unit, 0) + IFNULL(attOffr_present_unit, 0)) as officers,
                (IFNULL(jco_present_unit, 0) + IFNULL(jcoEre_present_unit, 0) + IFNULL(attJco_present_unit, 0)) as jcos,
                (IFNULL(or_present_unit, 0) + IFNULL(orEre_present_unit, 0) + IFNULL(oaOr_present_unit, 0) + IFNULL(attOr_present_unit, 0)) as other_ranks
            FROM parade_state_daily
            WHERE report_date = %s {company_filter}
            ORDER BY company
        """, tuple(params))
        manpower_data = cursor.fetchall()
        
        if not parade_summary or parade_summary['company_count'] == 0:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        # Update totals to use leave (lve) instead of total out (trout_det)
        total_on_leave = sum(row['on_leave'] or 0 for row in leave_data)
        total_strength = sum(row['total_strength'] or 0 for row in leave_data)
        total_leave_percentage = round((total_on_leave / total_strength * 100), 2) if total_strength > 0 else 0
        
        for row in manpower_data:
            row['total'] = (row['officers'] or 0) + (row['jcos'] or 0) + (row['other_ranks'] or 0)
        
        total_officers = sum(row['officers'] or 0 for row in manpower_data)
        total_jcos = sum(row['jcos'] or 0 for row in manpower_data)
        total_other_ranks = sum(row['other_ranks'] or 0 for row in manpower_data)
        total_manpower = total_officers + total_jcos + total_other_ranks
        
        return jsonify({
            'success': True,
            'data': {
                'parade_summary': {
                    'total_posted_str': parade_summary['total_posted_str'] or 0,
                    'present_unit': parade_summary['present_unit'] or 0,
                    'total_out': parade_summary['total_out'] or 0,
                    'total_lve': parade_summary['total_lve'] or 0,  # Add this
                    'company_count': parade_summary['company_count'] or 0,
                    'report_date': date_str
                },
                'leave_status': {
                    'by_company': leave_data,
                    'total': {
                        'on_leave': total_on_leave,
                        'total_strength': total_strength,
                        'leave_percentage': total_leave_percentage
                    }
                },
                'manpower': {
                    'by_company': manpower_data,
                    'total': {
                        'officers': total_officers,
                        'jcos': total_jcos,
                        'other_ranks': total_other_ranks,
                        'total': total_manpower
                    }
                }
            }
        })
        
    except Exception as e:
        print(f"Error fetching CO dashboard data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()        
# Add this new route to your Flask app (app.py)
# Place it near your other CO dashboard endpoints

@app.route('/api/co-dashboard/parade-table/<date_str>', methods=['GET'])
def get_co_aggregated_parade_table(date_str):
    """Get aggregated parade state data from all companies for CO view"""
    user = require_login()
    print("in this route")
    role = user.get('role', '')
    if role not in ['CO', '2IC', 'OC']:
        return jsonify({'success': False, 'error': 'Unauthorized - access denied'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    company_filter = ""
    params = [date_str]
    if role == 'OC':
        company_filter = " AND company = %s"
        params.append(user.get('company'))
        
    try:
        # Get all companies' data for the specified date
        cursor.execute(f"""
            SELECT * FROM parade_state_daily
            WHERE report_date = %s {company_filter}
        """, tuple(params))
        
        companies_data = cursor.fetchall()
        
        if not companies_data:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        aggregated = {
            'date': date_str,
            'company': 'ALL COMPANIES (CO VIEW)',
            'data': {}
        }
        all_categories = [
            'offr', 'jco', 'jcoEre', 'or', 'orEre',
            'firstTotal',
            'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
            'secondTotal',
            'grandTotal'
        ]
        column_names = [
            'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
            'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
            'present_det', 'present_unit', 'dues_in', 'dues_out'
        ]
        for category in all_categories:
            aggregated['data'][category] = [0] * 17
        
        for company_row in companies_data:
            for category in all_categories:
                for i, col_name in enumerate(column_names):
                    db_column = f"{category}_{col_name}"
                    if db_column in company_row:
                        aggregated['data'][category][i] += (company_row[db_column] or 0)
        
        return jsonify({
            'success': True,
            'data': aggregated,
            'companies_count': len(companies_data)
        })
        
    except Exception as e:
        print(f"Error fetching CO aggregated parade table: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# ===============================================
# PARADE DATA ROUTES FOR O CENTRE NCO
# ===============================================

@app.route('/api/parade-data/get/<date_str>/<company>', methods=['GET'])
def get_parade_data_by_company(date_str, company):
    """Get parade data for specific date and company - O CENTRE NCO & ONCO only"""
    print(f"\n=== GET PARADE DATA BY COMPANY ===")
    print(f"Date: {date_str}, Company: {company}")
    
    # Get current user
    user = get_current_user()
    
    # Check authentication
    if not user:
        print("DEBUG: No user found - not authenticated")
        return jsonify({
            'success': False, 
            'error': 'Not authenticated. Please login again.'
        }), 401
    
    user_role = user.get('role', '').strip()
    user_company = user.get('company', '').strip()
    
    print(f"DEBUG: User: {user.get('username')}, Role: '{user_role}', Company: '{user_company}'")
    
    # Check authorization based on role
    if user_role == 'O CENTRE NCO':
        # O CENTRE NCO can access all companies
        print("DEBUG: O CENTRE NCO access granted")
        pass
    elif user_role == 'ONCO':
        # ONCO can only access their own company
        if company != user_company:
            print(f"DEBUG: ONCO access denied - trying to access {company} but belongs to {user_company}")
            return jsonify({
                'success': False, 
                'error': f'Access denied - ONCO can only access data for {user_company}'
            }), 403
        print("DEBUG: ONCO access granted for own company")
    else:
        # Other roles cannot access
        print(f"DEBUG: Access denied for role: {user_role}")
        return jsonify({
            'success': False, 
            'error': f'Access denied - Only O CENTRE NCO and ONCO can access parade data'
        }), 403
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        print(f"DEBUG: Querying database for date={date_str}, company={company}")
        
        # Check if table exists first
        cursor.execute("SHOW TABLES LIKE 'parade_state_daily'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("DEBUG: parade_state_daily table doesn't exist")
            return jsonify({
                'success': True,
                'data': {
                    'date': date_str,
                    'company': company,
                    'data': {}
                },
                'is_empty': True
            }), 200
        
        cursor.execute("""
            SELECT * FROM parade_state_daily 
            WHERE report_date = %s AND company = %s
        """, (date_str, company))
        
        row = cursor.fetchone()
        print(f"DEBUG: Database query result: {row}")
        
        if not row:
            print("DEBUG: No data found in database")
            return jsonify({
                'success': True,
                'data': {
                    'date': date_str,
                    'company': company,
                    'data': {}
                },
                'is_empty': True
            }), 200
        
        # Convert database row to frontend format
        result = {
            'date': row['report_date'],
            'company': row['company'],
            'data': {}
        }
        
        categories = [
            'offr', 'jco', 'jcoEre', 'or', 'orEre',
            'firstTotal',
            'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
            'secondTotal',
            'grandTotal'
        ]
        
        column_names = [
            'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
            'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
            'present_det', 'present_unit', 'dues_in', 'dues_out'
        ]
        
        for category in categories:
            category_data = []
            for col in column_names:
                column_name = f"{category}_{col}"
                category_data.append(row.get(column_name, 0))
            result['data'][category] = category_data
        
        print(f"DEBUG: Returning data for {company} on {date_str}")
        return jsonify({
            'success': True,
            'data': result,
            'user_role': user_role,
            'user_company': user_company
        }), 200
        
    except Exception as e:
        print(f"ERROR in get_parade_data_by_company: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': f'Database error: {str(e)}'
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            
def require_role(*allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
            user_role = user.get('role', '').strip()
            if user_role not in allowed_roles:
                return jsonify({
                    'success': False, 
                    'error': f'Access denied. Required roles: {", ".join(allowed_roles)}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ===============================================
# ALSO ADD THESE RELATED ROUTES
# ===============================================

@app.route('/api/parade-data/view-all/<date_str>', methods=['GET'])
@require_role('O CENTRE NCO')  # Only O CENTRE NCO can view all companies
def get_all_companies_parade_data(date_str):
    """Get aggregated parade data for all companies - O CENTRE NCO ONLY"""
    print(f"\n=== GET ALL COMPANIES PARADE DATA ===")
    print(f"Date: {date_str}")
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'parade_state_daily'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            return jsonify({
                'success': True,
                'data': {
                    'date': date_str,
                    'company': 'ALL COMPANIES',
                    'data': {}
                },
                'is_empty': True,
                'companies_count': 0
            }), 200
        
        cursor.execute("""
            SELECT * FROM parade_state_daily
            WHERE report_date = %s
        """, (date_str,))
        
        companies_data = cursor.fetchall()
        
        if not companies_data:
            return jsonify({
                'success': True,
                'data': {
                    'date': date_str,
                    'company': 'ALL COMPANIES',
                    'data': {}
                },
                'is_empty': True,
                'companies_count': 0
            }), 200
        
        # Aggregate data
        aggregated = {
            'date': date_str,
            'company': 'ALL COMPANIES',
            'data': {}
        }
        
        categories = [
            'offr', 'jco', 'jcoEre', 'or', 'orEre',
            'firstTotal',
            'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
            'secondTotal',
            'grandTotal'
        ]
        
        column_names = [
            'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
            'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
            'present_det', 'present_unit', 'dues_in', 'dues_out'
        ]
        
        for category in categories:
            aggregated['data'][category] = [0] * 17
        
        for company_row in companies_data:
            for category in categories:
                for i, col in enumerate(column_names):
                    db_column = f"{category}_{col}"
                    if db_column in company_row:
                        aggregated['data'][category][i] += (company_row[db_column] or 0)
        
        return jsonify({
            'success': True,
            'data': aggregated,
            'companies_count': len(companies_data)
        }), 200
        
    except Exception as e:
        print(f"ERROR in get_all_companies_parade_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': f'Database error: {str(e)}'
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
@app.route('/api/parade-data/user-info', methods=['GET'])
def get_parade_user_info():
    """Get parade-specific user information"""
    user = get_current_user()
    
    if not user:
        return jsonify({
            'success': False, 
            'error': 'Not authenticated'
        }), 401
    
    user_role = user.get('role', '').strip()
    user_company = user.get('company', '').strip()
    
    # Only allow O CENTRE NCO and ONCO
    if user_role not in ['O CENTRE NCO', 'ONCO']:
        return jsonify({
            'success': False,
            'error': 'Access denied'
        }), 403
    
    return jsonify({
        'success': True,
        'role': user_role,
        'company': user_company,
        'username': user.get('username')
    })

# ===============================================
# DEBUG ENDPOINT - ADD THIS
# ===============================================

@app.route('/debug/user-info')
def debug_user_info():
    """Debug endpoint to check user authentication"""
    user = get_current_user()
    if user:
        return jsonify({
            'is_authenticated': True,
            'username': user.get('username'),
            'role': user.get('role'),
            'company': user.get('company')
        })
    else:
        return jsonify({
            'is_authenticated': False,
            'error': 'No user found'
        }), 401

@app.route('/api/parade-data/save', methods=['POST'])
def save_parade_data():
    """Save parade data - O CENTRE NCO can save for any company, ONCO only for own"""
    
    user = get_current_user()
    
    if not user:
        return jsonify({
            'success': False, 
            'error': 'Not authenticated. Please login again.'
        }), 401
    
    user_role = user.get('role', '').strip()
    user_company = user.get('company', '').strip()
    
    print(f"\n=== SAVE PARADE DATA ===")
    print(f"User: {user.get('username')}, Role: '{user_role}', Company: '{user_company}'")
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False, 
                'error': 'No data received'
            }), 400
        
        report_date_str = data.get('date')
        selected_company = data.get('company')  # From dropdown (for O CENTRE NCO) or user's company (for ONCO)
        parade_data = data.get('data')
        
        if not report_date_str or not selected_company or not parade_data:
            return jsonify({
                'success': False, 
                'error': 'Missing required fields: date, company, or data'
            }), 400
        
        # Validate user role
        if user_role not in ['O CENTRE NCO', 'ONCO']:
            return jsonify({
                'success': False, 
                'error': 'Access denied - Only O CENTRE NCO and ONCO can save parade data'
            }), 403
        
        # Determine which company to save to
        if user_role == 'O CENTRE NCO':
            # O CENTRE NCO saves to the company they selected from dropdown
            final_company = selected_company
            print(f"DEBUG: O CENTRE NCO saving to selected company: {final_company}")
            
            # Validate that O CENTRE NCO doesn't try to save for "All"
            if final_company == 'All':
                return jsonify({
                    'success': False,
                    'error': 'Cannot save data for "All Companies". Please select a specific company.'
                }), 400
                
        elif user_role == 'ONCO':
            # ONCO ALWAYS saves to their own company, regardless of what frontend sends
            final_company = user_company  # Use logged-in user's company
            print(f"DEBUG: ONCO detected. Overriding frontend company '{selected_company}' with user's company: '{final_company}'")
            
            # Optional: Warn if frontend is sending wrong company (for debugging)
            if selected_company != user_company:
                print(f"WARNING: ONCO frontend sent company '{selected_company}' but saving to '{final_company}'")
        
        # Validate date restriction for ONCO
        if user_role == 'ONCO':
            requested_date = datetime.strptime(report_date_str, '%Y-%m-%d').date()
            today_date = date.today()
            
            if requested_date != today_date:
                return jsonify({
                    'success': False,
                    'error': 'ONCO can only save data for today'
                }), 400
        
        # Validate date is not in future for any user
        requested_date = datetime.strptime(report_date_str, '%Y-%m-%d').date()
        today_date = date.today()
        if requested_date > today_date:
            return jsonify({
                'success': False,
                'error': 'Cannot save data for future dates'
            }), 400
        
        print(f"DEBUG: Saving data for date: {report_date_str}, company: {final_company}, user role: {user_role}")
        
        # Continue with save logic...
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # All input categories from your frontend (editable categories)
            input_categories = [
                'offr', 'jco', 'jcoEre', 'or', 'orEre',  # First section
                'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr'  # Second section
            ]
            
            # Build SQL columns and values - Use final_company (determined above)
            columns = ['report_date', 'company']
            values = [report_date_str, final_company]
            
            # Helper function to get column name from index
            def get_column_name_for_db(index):
                columns_list = [
                    'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
                    'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
                    'present_det', 'present_unit', 'dues_in', 'dues_out'
                ]
                return columns_list[index] if index < len(columns_list) else f'col_{index}'
            
            # Process each input category with calculations
            for category in input_categories:
                category_data = parade_data.get(category, [0]*17)
                
                # Ensure we have at least 13 values (minimum needed for calculations)
                if len(category_data) < 13:
                    # Pad with zeros if needed
                    category_data = category_data + [0] * (13 - len(category_data))
                
                # Extract values for calculations
                posted_str = category_data[2] if len(category_data) > 2 else 0
                lve = category_data[3] if len(category_data) > 3 else 0
                course = category_data[4] if len(category_data) > 4 else 0
                det_value = category_data[5] if len(category_data) > 5 else 0
                mh = category_data[6] if len(category_data) > 6 else 0
                sick_lve = category_data[7] if len(category_data) > 7 else 0
                ex = category_data[8] if len(category_data) > 8 else 0
                td = category_data[9] if len(category_data) > 9 else 0
                att = category_data[10] if len(category_data) > 10 else 0
                awl_osl_jc = category_data[11] if len(category_data) > 11 else 0
                
                # Calculate T/OUT = LVE + COURSE + DET + MH + SICK/LVE + EX + TD + ATT + AWL/OSL/JC
                trout = lve + course + det_value + mh + sick_lve + ex + td + att + awl_osl_jc
                trout = max(0, trout)  # Ensure non-negative
                
                # PRESENT/STR DET = DET column value
                present_det = det_value
                
                # PRESENT/STR UNIT = POSTED/STR - T/OUT
                present_unit = posted_str - trout
                present_unit = max(0, present_unit)  # Ensure non-negative
                
                # Create final array with calculated values
                final_data = [
                    category_data[0] if len(category_data) > 0 else 0,  # AUTH
                    category_data[1] if len(category_data) > 1 else 0,  # H/S
                    posted_str,  # POSTED/STR
                    lve,         # LVE
                    course,      # COURSE
                    det_value,   # DET
                    mh,          # MH
                    sick_lve,    # SICK/LVE
                    ex,          # EX
                    td,          # TD
                    att,         # ATT
                    awl_osl_jc,  # AWL/OSL/JC
                    trout,       # T/OUT (calculated)
                    present_det, # PRESENT/STR DET (from DET column)
                    present_unit, # PRESENT/STR UNIT (calculated)
                    category_data[15] if len(category_data) > 15 else 0,  # DUES IN
                    category_data[16] if len(category_data) > 16 else 0   # DUES OUT
                ]
                
                # Add each of the 17 columns for this category
                for i in range(17):
                    column_name = f"{category}_{get_column_name_for_db(i)}"
                    columns.append(column_name)
                    values.append(final_data[i])
            
            # Calculate FIRST TOTAL (sum of offr, jco, jcoEre, or, orEre)
            first_total_values = [0] * 17
            for cat in ['offr', 'jco', 'jcoEre', 'or', 'orEre']:
                cat_data = parade_data.get(cat, [0]*17)
                if len(cat_data) >= 13:
                    posted_str = cat_data[2] if len(cat_data) > 2 else 0
                    lve = cat_data[3] if len(cat_data) > 3 else 0
                    course = cat_data[4] if len(cat_data) > 4 else 0
                    det_value = cat_data[5] if len(cat_data) > 5 else 0
                    mh = cat_data[6] if len(cat_data) > 6 else 0
                    sick_lve = cat_data[7] if len(cat_data) > 7 else 0
                    ex = cat_data[8] if len(cat_data) > 8 else 0
                    td = cat_data[9] if len(cat_data) > 9 else 0
                    att = cat_data[10] if len(cat_data) > 10 else 0
                    awl_osl_jc = cat_data[11] if len(cat_data) > 11 else 0
                    
                    trout = lve + course + det_value + mh + sick_lve + ex + td + att + awl_osl_jc
                    trout = max(0, trout)                                               
                    
                    present_unit = posted_str - trout
                    present_unit = max(0, present_unit)
                    
                    # Sum all columns
                    for i in range(17):
                        if i == 12:  # T/OUT
                            first_total_values[i] += trout
                        elif i == 14:  # PRESENT/STR UNIT
                            first_total_values[i] += present_unit
                        elif i < len(cat_data):
                            first_total_values[i] += cat_data[i]
                        else:
                            first_total_values[i] += 0
            
            # Store first total in database
            for i in range(17):
                column_name = f"firstTotal_{get_column_name_for_db(i)}"
                columns.append(column_name)
                values.append(first_total_values[i])
            
            # Calculate SECOND TOTAL (sum of oaOr, attSummary, attOffr, attJco, attOr)
            second_total_values = [0] * 17
            for cat in ['oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr']:
                cat_data = parade_data.get(cat, [0]*17)
                if len(cat_data) >= 13:
                    posted_str = cat_data[2] if len(cat_data) > 2 else 0
                    lve = cat_data[3] if len(cat_data) > 3 else 0
                    course = cat_data[4] if len(cat_data) > 4 else 0
                    det_value = cat_data[5] if len(cat_data) > 5 else 0
                    mh = cat_data[6] if len(cat_data) > 6 else 0
                    sick_lve = cat_data[7] if len(cat_data) > 7 else 0
                    ex = cat_data[8] if len(cat_data) > 8 else 0
                    td = cat_data[9] if len(cat_data) > 9 else 0
                    att = cat_data[10] if len(cat_data) > 10 else 0
                    awl_osl_jc = cat_data[11] if len(cat_data) > 11 else 0
                    
                    trout = lve + course + det_value + mh + sick_lve + ex + td + att + awl_osl_jc
                    trout = max(0, trout)
                    
                    present_unit = posted_str - trout
                    present_unit = max(0, present_unit)
                    
                    # Sum all columns
                    for i in range(17):
                        if i == 12:  # T/OUT
                            second_total_values[i] += trout
                        elif i == 14:  # PRESENT/STR UNIT
                            second_total_values[i] += present_unit
                        elif i < len(cat_data):
                            second_total_values[i] += cat_data[i]
                        else:
                            second_total_values[i] += 0
            
            # Store second total in database
            for i in range(17):
                column_name = f"secondTotal_{get_column_name_for_db(i)}"
                columns.append(column_name)
                values.append(second_total_values[i])
            
            # Calculate GRAND TOTAL (firstTotal + secondTotal)
            grand_total_values = [0] * 17
            for i in range(17):
                grand_total_values[i] = first_total_values[i] + second_total_values[i]
            
            # Store grand total in database
            for i in range(17):
                column_name = f"grandTotal_{get_column_name_for_db(i)}"
                columns.append(column_name)
                values.append(grand_total_values[i])
            
            # Build SQL query
            placeholders = ['%s'] * len(values)
            
            sql = f"""
                INSERT INTO parade_state_daily ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                ON DUPLICATE KEY UPDATE
                {', '.join([f"{col} = VALUES({col})" for col in columns if col not in ['report_date', 'company']])},
                updated_at = NOW()
            """
            
            print(f"Executing SQL for company: {final_company}")
            cursor.execute(sql, values)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': f'Parade data saved successfully for {final_company} on {report_date_str}',
                'details': {
                    'company': final_company,
                    'date': report_date_str,
                    'entered_by': user.get('username'),
                    'user_role': user_role,
                    'grand_total': {
                        'auth': grand_total_values[0],
                        'posted_str': grand_total_values[2],
                        't_out': grand_total_values[12],
                        'present_unit': grand_total_values[14]
                    }
                }
            }), 200
            
        except Exception as e:
            conn.rollback()
            print(f"Database error in save: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False, 
                'error': f'Database error: {str(e)}'
            }), 500
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"Error in save_parade_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/parade-data/export-csv/<date_str>/<company>', methods=['GET'])
def export_parade_csv(date_str, company):
    """Export parade data to CSV"""
    
    # Get current user
    user = get_current_user()
    
    # Check authentication
    if not user:
        return jsonify({
            'success': False, 
            'error': 'Not authenticated. Please login again.'
        }), 401
    
    user_role = user.get('role', '').strip()
    user_company = user.get('company', '').strip()
    
    # Check authorization based on role
    if user_role == 'O CENTRE NCO':
        # O CENTRE NCO can export any company
        pass
    elif user_role == 'ONCO':
        # ONCO can only export their own company
        if company != user_company:
            return jsonify({
                'success': False, 
                'error': f'Access denied - ONCO can only export data for {user_company}'
            }), 403
    else:
        # Other roles cannot export
        return jsonify({
            'success': False, 
            'error': 'Access denied - Only O CENTRE NCO and ONCO can export parade data'
        }), 403
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if company == 'All':
            # Only O CENTRE NCO can export all companies
            if user_role != 'O CENTRE NCO':
                return jsonify({
                    'success': False, 
                    'error': 'Only O CENTRE NCO can export data for all companies'
                }), 403
                
            # Get all companies data
            cursor.execute("""
                SELECT * FROM parade_state_daily
                WHERE report_date = %s
            """, (date_str,))
            companies_data = cursor.fetchall()
            
            if not companies_data:
                return jsonify({
                    'success': False, 
                    'error': 'No data found'
                }), 404
            
            # Create aggregated CSV
            output = StringIO()
            writer = csv.writer(output)
            
            # Headers
            headers = ['Category', 'AUTH', 'H/S', 'POSTED/STR', 'LVE', 'COURSE', 'DET', 
                      'MH', 'SICK/LVE', 'EX', 'TD', 'ATT', 'AWL/OSL/JC', 'T/OUT', 
                      'PRES/DET', 'PRES/UNIT', 'DUES IN', 'DUES OUT']
            writer.writerow(['AGGREGATED PARADE STATE - ALL COMPANIES'])
            writer.writerow([f'Date: {date_str}'])
            writer.writerow([f'Exported by: {user.get("username")} ({user_role})'])
            writer.writerow([])
            writer.writerow(headers)
            
            # Aggregate data
            categories = [
                ('offr', 'OFFR'),
                ('jco', 'JCO'),
                ('jcoEre', 'JCO (ERE)'),
                ('or', 'OR'),
                ('orEre', 'OR (ERE)'),
                ('firstTotal', 'TOTAL (I)'),
                ('oaOr', 'OA/OR'),
                ('attSummary', 'SUPERNUMARARY'),
                ('attOffr', 'ATT (OFFR)'),
                ('attJco', 'ATT (JCO)'),
                ('attOr', 'ATT (OR)'),
                ('secondTotal', 'TOTAL (II)'),
                ('grandTotal', 'GRAND TOTAL')
            ]
            
            column_names = [
                'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
                'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
                'present_det', 'present_unit', 'dues_in', 'dues_out'
            ]
            
            for cat_key, cat_label in categories:
                row_data = [cat_label]
                for col in column_names:
                    total = sum(company.get(f"{cat_key}_{col}", 0) or 0 for company in companies_data)
                    row_data.append(total)
                writer.writerow(row_data)
            
            filename = f"parade_state_all_companies_{date_str}.csv"
            
        else:
            # Get specific company data
            cursor.execute("""
                SELECT * FROM parade_state_daily
                WHERE report_date = %s AND company = %s
            """, (date_str, company))
            
            row = cursor.fetchone()
            
            if not row:
                return jsonify({
                    'success': False, 
                    'error': 'No data found'
                }), 404
            
            # Create CSV
            output = StringIO()
            writer = csv.writer(output)
            
            # Headers
            headers = ['Category', 'AUTH', 'H/S', 'POSTED/STR', 'LVE', 'COURSE', 'DET', 
                      'MH', 'SICK/LVE', 'EX', 'TD', 'ATT', 'AWL/OSL/JC', 'T/OUT', 
                      'PRES/DET', 'PRES/UNIT', 'DUES IN', 'DUES OUT']
            writer.writerow([f'PARADE STATE - {company}'])
            writer.writerow([f'Date: {date_str}'])
            writer.writerow([f'Exported by: {user.get("username")} ({user_role})'])
            writer.writerow([])
            writer.writerow(headers)
            
            categories = [
                ('offr', 'OFFR'),
                ('jco', 'JCO'),
                ('jcoEre', 'JCO (ERE)'),
                ('or', 'OR'),
                ('orEre', 'OR (ERE)'),
                ('firstTotal', 'TOTAL (I)'),
                ('oaOr', 'OA/OR'),
                ('attSummary', 'SUPERNUMARARY'),
                ('attOffr', 'ATT (OFFR)'),
                ('attJco', 'ATT (JCO)'),
                ('attOr', 'ATT (OR)'),
                ('secondTotal', 'TOTAL (II)'),
                ('grandTotal', 'GRAND TOTAL')
            ]
            
            column_names = [
                'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
                'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
                'present_det', 'present_unit', 'dues_in', 'dues_out'
            ]
            
            for cat_key, cat_label in categories:
                row_data = [cat_label]
                for col in column_names:
                    row_data.append(row.get(f"{cat_key}_{col}", 0))
                writer.writerow(row_data)
            
            filename = f"parade_state_{company.replace(' ', '_')}_{date_str}.csv"
        
        # Prepare response
        output.seek(0)
        return send_file(
            BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename,
            max_age=0
        )
        
    except Exception as e:
        print(f"Export error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': f'Export error: {str(e)}'
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/get_projects')
def api_get_projects():
    print("this is in new route of getting projects")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    role = user['role']
    company = user['company']

    try:
        query = """
            SELECT project_id, head, project_name, current_stage, 
                   project_cost, project_items, quantity, project_description
            FROM projects
        """
        params = []

        if company != "Admin" and role != 'PROJECT JCO' and  role != 'PROJECT OFFICER':
            query += " WHERE company = %s"
            params.append(company)

        cursor.execute(query, params)
        projects = cursor.fetchall()

        return jsonify(projects)  

    except Exception as e:
        print("Error:", str(e))
        return jsonify([]), 500
    finally:
        cursor.close()
        conn.close()


    
@app.route('/api/get-all-courses', methods=['GET'])
def get_courses():
    print("in this route")
    user = require_login()
    if not user:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            coc.army_number,
            p.name,
            p.rank,
            p.company,
            coc.course_name,
            DATE_FORMAT(coc.course_starting_date, '%d-%m-%Y') AS from_date,
            DATE_FORMAT(coc.course_end_date, '%d-%m-%Y') AS to_date,
            coc.institute_name
        FROM candidate_on_courses coc
        LEFT JOIN personnel p 
            ON coc.army_number = p.army_number
    """)

    data = cursor.fetchall()
    print("get all courses")
    print("data",data)
    cursor.close()
    conn.close()

    return jsonify(data)


@app.route('/account/departments/all_transactions')
def all_transactions():
    limit = int(request.args.get('limit', 10))
    query = """
        SELECT date, account_holder, old_balance, credit_amount, debit_amount, new_balance
        FROM transactions
        ORDER BY date DESC
        LIMIT %s
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (limit,))
    transactions = cursor.fetchall()
    return jsonify({'transactions': transactions})


def reset_interview_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personnel
SET interview_status = 0
WHERE interview_status = 1
  AND TIMESTAMPDIFF(MINUTE, updated_at, NOW()) > 1;


                   
    """)
    conn.commit()
    cursor.close()
    conn.close()


# kunba interview timing     

scheduler = BackgroundScheduler()
scheduler.add_job(func=reset_interview_status, trigger="interval", seconds=1296000)  # check every 30s
scheduler.start()

# AGNIVEER DATA FATCH WITH TABLE STARTING CODE++++++++++++++++++++++++++++++++++++++++++++++++++++




@app.route('/get_all_agniveers', methods=['GET'])
def get_all_agniveers():
    

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM assistant_test")
    rows = cursor.fetchall()

    

    cursor.close()
    conn.close()

    return jsonify(rows)


#=================================AGNIVEER TABLE ENDING CODE---------------------------------------------



#=======================================================AV details============




@app.route('/api/assistant-test', methods=['POST'])
def save_assistant_test():
    """Simple API to store assistant test data"""
    try:
        # Get data from frontend
        data = request.json
        
        # Validate batch (required field)
        if not data.get('batch'):
            return jsonify({'success': False, 'error': 'Batch is required'}), 400
        
        # Connect to MySQL
        
        
        conn = get_db_connection()
        cursor  =  conn.cursor()
        
        # Insert query matching your table structure
        sql = """
        INSERT INTO assistant_test 
        (batch, asst_test1, asst_test2, asst_test3, asst_test4, 
         test1_status, test2_status, test3_status, test4_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Prepare values
        values = (
            data.get('batch'),
            data.get('asst_test1'),  # Can be null or datetime string
            data.get('asst_test2'),
            data.get('asst_test3'),
            data.get('asst_test4'),
            data.get('test1_status', 0),  # Default to 0 if not provided
            data.get('test2_status', 0),
            data.get('test3_status', 0),
            data.get('test4_status', 0)
        )
        
        # Execute insert
        cursor.execute(sql, values)
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Data saved successfully'
        }), 200
        
    except mysql.connector.Error as db_err:
        return jsonify({'success': False, 'error': f'Database error: {db_err}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {e}'}), 500






@app.route("/api/upcomming_test_alarms")
def upcomming_test_alarms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            id,
            batch,
            'TEST-1' AS test_name,
            asst_test1 AS test_date
        FROM assistant_test
        WHERE test1_status = 0
          AND asst_test1 BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)

        UNION ALL

        SELECT 
            id,
            batch,
            'TEST-2' AS test_name,
            asst_test2 AS test_date
        FROM assistant_test
        WHERE test2_status = 0
          AND asst_test2 BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)

        UNION ALL

        SELECT 
            id,
            batch,
            'TEST-3' AS test_name,
            asst_test3 AS test_date
        FROM assistant_test
        WHERE test3_status = 0
          AND asst_test3 BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)

        UNION ALL

        SELECT 
            id,
            batch,
            'TEST-4' AS test_name,
            asst_test4 AS test_date
        FROM assistant_test
        WHERE test4_status = 0
          AND asst_test4 BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows,"these are rows")
    cursor.close()
    conn.close()

    return jsonify({"rows": rows})









##############################################################################################################################################################################################################################################################################################


# ========== 1. DETACHMENTS COUNT ==========
@app.route('/api/dashboard/detachments', methods=['GET'])
def get_detachments_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        query = "SELECT COUNT(*) AS count FROM personnel WHERE detachment_status = 1"
        params = []
        if company != "Admin":
            query += " AND company = %s"
            params.append(company)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching detachments count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 1.1 DOMAIN SPECIALIZATION COUNT ==========
@app.route('/api/dashboard/duty_count', methods=['GET'])
def get_duty_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        # Match search_personnel logic: count unique personnel who have either a section or a recorded duty
        query = """
            SELECT COUNT(DISTINCT p.army_number) AS count
            FROM personnel p
            LEFT JOIN (
                SELECT army_number, duty_performed
                FROM units_served
                WHERE (army_number, sr_no) IN (
                    SELECT army_number, MAX(sr_no)
                    FROM units_served
                    GROUP BY army_number
                )
            ) u ON p.army_number = u.army_number
            WHERE ((u.duty_performed IS NOT NULL AND u.duty_performed != '')
               OR (p.section IS NOT NULL AND p.section != ''))
        """
        params = []
        if company != "Admin":
            query += " AND p.company = %s"
            params.append(company)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching duty count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()



# ========== 2. MANPOWER DATA ==========
@app.route('/api/dashboard/manpower', methods=['GET'])
def get_manpower_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        # Get the latest reporting date
        date_query = "SELECT MAX(report_date) as max_date FROM parade_state_daily"
        date_params = []
        if company != "Admin":
            date_query += " WHERE company = %s"
            date_params.append(company)
        
        cursor.execute(date_query, date_params)
        max_date_result = cursor.fetchone()
        latest_date = max_date_result['max_date'] if max_date_result else None

        if latest_date:
            query = """
                SELECT 
                    SUM(IFNULL(offr_present_unit, 0)) AS officerCount,
                    SUM(IFNULL(jco_present_unit, 0) + IFNULL(jcoEre_present_unit, 0)) AS jcoCount,
                    SUM(IFNULL(or_present_unit, 0) + IFNULL(orEre_present_unit, 0)) AS orCount,
                    SUM(
                        IFNULL(offr_present_unit, 0) + 
                        IFNULL(jco_present_unit, 0) + 
                        IFNULL(jcoEre_present_unit, 0) + 
                        IFNULL(or_present_unit, 0) + 
                        IFNULL(orEre_present_unit, 0)
                    ) AS total
                FROM parade_state_daily
                WHERE report_date = %s
            """
            params = [latest_date]
            if company != "Admin":
                query += " AND company = %s"
                params.append(company)
            
            cursor.execute(query, params)
            manpower_result = cursor.fetchone()
        else:
            manpower_result = None

        # Check if we have valid parade data
        has_parade_data = manpower_result and (
            (manpower_result["officerCount"] or 0) > 0 or 
            (manpower_result["jcoCount"] or 0) > 0 or 
            (manpower_result["orCount"] or 0) > 0
        )

        if has_parade_data:
            officerCount = int(manpower_result["officerCount"] or 0)
            jcoCount = int(manpower_result["jcoCount"] or 0)
            orCount = int(manpower_result["orCount"] or 0)
            total = int(manpower_result["total"] or 0)
        else:
            # Fallback to personnel table
            fallback_query = """
                SELECT 
                    SUM(CASE WHEN `rank` IN ('Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 'Colonel', 'Brigadier', 'Major General', 'Lieutenant General', 'General', 'OC') THEN 1 ELSE 0 END) as officerCount,
                    SUM(CASE WHEN `rank` IN ('Subedar', 'Naib Subedar', 'Subedar Major', 'JCO') THEN 1 ELSE 0 END) as jcoCount,
                    SUM(CASE WHEN `rank` NOT IN ('Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 'Colonel', 'Brigadier', 'Major General', 'Lieutenant General', 'General', 'OC', 'Subedar', 'Naib Subedar', 'Subedar Major', 'JCO') THEN 1 ELSE 0 END) as orCount
                FROM personnel
                WHERE 1=1
            """
            fallback_params = []
            if company != "Admin":
                fallback_query += " AND company = %s"
                fallback_params.append(company)
            
            cursor.execute(fallback_query, fallback_params)
            fb_res = cursor.fetchone()
            
            if fb_res:
                officerCount = int(fb_res["officerCount"] or 0)
                jcoCount = int(fb_res["jcoCount"] or 0)
                orCount = int(fb_res["orCount"] or 0)
                total = officerCount + jcoCount + orCount
            else:
                officerCount = jcoCount = orCount = total = 0

        return jsonify({
            "status": "success",
            "officerCount": officerCount,
            "jcoCount": jcoCount,
            "orCount": orCount,
            "total": total
        }), 200
        
    except Exception as e:
        print("Error fetching manpower data:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()
excluded_ranks = ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
# ========== 3. INTERVIEW DATA ==========
@app.route('/api/dashboard/interviews', methods=['GET'])
def get_interview_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    role = user['role']
    current_user = user['army_number']
    
    try:
        if role in ['JCO', 'S/JCO']:
            cursor.execute('SELECT home_state FROM personnel WHERE army_number = %s', (current_user,))
            home_result = cursor.fetchone()
            home_state = home_result['home_state'] if home_result else None

            query = """
                SELECT 
                    COALESCE(SUM(interview_status = 0), 0) AS pending_count,
                    COUNT(*) AS total_count
                FROM personnel
                WHERE company = %s
                  AND home_state = %s
                  AND `rank` NOT IN (
                      'Subedar', 'Naib Subedar', 'Subedar Major',
                      'Lieutenant', 'Captain', 'Major',
                      'Lieutenant Colonel', 'Colonel',
                      'Brigadier', 'Major General',
                      'Lieutenant General', 'General'
                  )
            """
            cursor.execute(query, (company, home_state))
        else:
            query = """
                SELECT 
                    COALESCE(SUM(interview_status = 0), 0) AS pending_count,
                    COUNT(*) AS total_count
                FROM personnel
                WHERE `rank` NOT IN ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
            """
            params = []
            if company != "Admin":
                query += " AND company = %s"
                params.append(company)
            cursor.execute(query, params)

        result = cursor.fetchone()
        pending_count = result['pending_count'] if result else 0
        total_count = result['total_count'] if result else 0
        percentage = round((pending_count / total_count) * 100, 2) if total_count > 0 else 0

        return jsonify({
            "status": "success",
            "pending_count": pending_count,
            "total_count": total_count,
            "percentage": percentage
        }), 200
        
    except Exception as e:
        print("Error fetching interview data:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 4. ATTACHMENTS/TD COUNT ==========
@app.route('/api/dashboard/attachments', methods=['GET'])
def get_attachments_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        query = "SELECT COUNT(*) AS count FROM personnel WHERE td_status = 1"
        params = []
        if company != "Admin":
            query += " AND company = %s"
            params.append(company)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching attachments count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 5. AGNIVEER COUNT ==========
@app.route('/api/dashboard/agniveers', methods=['GET'])
def get_agniveer_count():

    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    company = user['company']
    role = user['role']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT COUNT(id) as count
            FROM personnel
            WHERE `rank` = 'Agniveer'
        """
        params = []

        privileged_roles = ['Admin', 'CO', '2IC', 'ADJUTANT', 'TRGJCO','Subedar Major']

        # Company restriction
        if company != "Admin" and role not in privileged_roles:
            query += " AND company = %s"
            params.append(company)

        cursor.execute(query, params)
        result = cursor.fetchone()

        count = result['count'] if result else 0

        return jsonify({
            "status": "success",
            "count": count
        }), 200

    except Exception as e:
        print("Error fetching agniveer count:", str(e))
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500

    finally:
        cursor.close()
        conn.close()

# ========== 6. PROJECTS COUNT ==========
@app.route('/api/dashboard/projects', methods=['GET'])
def get_projects_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        query = "SELECT COUNT(*) AS count FROM projects WHERE 1=1"
        params = []
        if company != "Admin":
            query += " AND company = %s"
            params.append(company)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching projects count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 7. SENSITIVE PERSONNEL COUNT ==========
@app.route('/api/dashboard/sensitive', methods=['GET'])
def get_sensitive_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        query = """
            SELECT COUNT(*) AS count
            FROM sensitive_marking sm
            LEFT JOIN personnel p ON sm.army_number = p.army_number
            WHERE 1=1
        """
        params = []
        if company != "Admin":
            query += " AND p.company = %s"
            params.append(company)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching sensitive count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 8. LOANS COUNT ==========
    @app.route('/api/dashboard/loans', methods=['GET'])
    def get_loans_count():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        user = require_login()
        if not user:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
        company = user['company']
        
        try:
            query = """
                SELECT COUNT(*) AS count
                FROM loans l
                LEFT JOIN personnel p ON l.army_number = p.army_number
                WHERE 1=1
            """
            params = []
            if company != "Admin":
                query += " AND p.company = %s"
                params.append(company)
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            count = result['count'] if result else 0
            
            return jsonify({
                "status": "success",
                "count": count
            }), 200
            
        except Exception as e:
            print("Error fetching loans count:", str(e))
            return jsonify({"status": "error", "message": "Internal Server Error"}), 500
        finally:
            cursor.close()
            conn.close()
# ========== 9. COURSES COUNT ==========
@app.route('/api/dashboard/courses', methods=['GET'])
def get_courses_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        query = """
            SELECT COUNT(*) AS count 
            FROM candidate_on_courses c
            LEFT JOIN personnel p ON c.army_number = p.army_number
            WHERE 1=1
        """
        params = []
        if company != "Admin":
            query += " AND p.company = %s"
            params.append(company)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching courses count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 10. ROLL CALL POINTS ==========
@app.route('/api/dashboard/rollcall', methods=['GET'])
def get_rollcall_points():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        cursor.execute("SELECT count(id) as count FROM roll_call_points WHERE status = 'PENDING'")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "points": count
        }), 200
        
    except Exception as e:
        print("Error fetching rollcall points:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 11. BOARDS COUNT ==========
@app.route('/api/dashboard/boards', methods=['GET'])
def get_boards_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM boards")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        return jsonify({
            "status": "success",
            "count": count
        }), 200
        
    except Exception as e:
        print("Error fetching boards count:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 12. TASKS DATA ==========
@app.route('/api/dashboard/tasks', methods=['GET'])
def get_tasks_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    current_user = user['army_number']
    
    try:
        cursor.execute(
            """
            SELECT 
                COUNT(*) AS total,
                COALESCE(SUM(task_status != 'COMPLETED'), 0) AS pending
            FROM tasks
            WHERE assigned_to = %s
            """,
            (current_user,)
        )
        result = cursor.fetchone()
        total = result['total'] if result else 0
        pending = result['pending'] if result else 0
        
        return jsonify({
            "status": "success",
            "total": total,
            "pending": pending
        }), 200
        
    except Exception as e:
        print("Error fetching tasks data:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# ========== 13. ASSIGNED ALARM (for modal) ==========
@app.route('/api/dashboard/assigned_alarm', methods=['GET'])
def get_assigned_alarm():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    company = user['company']
    
    try:
        query = '''
            SELECT 
                ad.army_number, 
                p.name,
                p.rank,
                p.company,
                ad.det_id, 
                d.det_name, 
                ad.assigned_on,
                ad.det_status,
                DATEDIFF(NOW(), ad.assigned_on) AS days_on_det
            FROM assigned_det ad
            LEFT JOIN dets d ON ad.det_id = d.det_id
            LEFT JOIN personnel p ON ad.army_number = p.army_number
            WHERE DATEDIFF(NOW(), ad.assigned_on) > 90
              
        '''
        params = []
        if company != "Admin":
            query += " AND p.company = %s"
            params.append(company)
        
        query += " ORDER BY ad.assigned_on ASC;"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "data": rows
        }), 200
        
    except Exception as e:
        print("Error fetching assigned alarm data:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()






#api for trade functionality


def format_data_for_frontend(db_row, requested_date, is_template=False):
    """
    Convert database row to frontend format
    """
    if not db_row:
        return []
    
    trades = [
        {'code': 'op_ciph', 'name': 'OP CIPH'},
        {'code': 'oss', 'name': 'OSS'},
        {'code': 'occ', 'name': 'OCC'},
        {'code': 'ttc', 'name': 'TTC'},
        {'code': 'lmn', 'name': 'LMN'},
        {'code': 'efs', 'name': 'EFS'},
        {'code': 'dvr_mt', 'name': 'DVR MT'},
        {'code': 'dr', 'name': 'DR'},
        {'code': 'dtmn', 'name': 'DTMN'},
        {'code': 'skt', 'name': 'SKT'},
        {'code': 'artsn', 'name': 'ARTSN'},
        {'code': 'w_man', 'name': 'W/MAN'},
        {'code': 'steward', 'name': 'STEWARD'},
        {'code': 'dresser', 'name': 'DRESSER'},
        {'code': 'hkeeper', 'name': 'HKEEPER'},
        {'code': 'mkeeper', 'name': 'MKEEPER'},
        {'code': 'chef_mess', 'name': 'CHEF MESS'},
        {'code': 'chef_com', 'name': 'CHEF COM'},
        {'code': 'er', 'name': 'ER'},
        {'code': 'tlr', 'name': 'TLR'},
        {'code': 'clk_sd', 'name': 'CLK SD'},
        {'code': 'ere', 'name': 'ERE'}
    ]
    
    result = []
    for trade in trades:
        trade_data = {
            'trade': trade['name'],
            'auth': db_row.get(f"{trade['code']}_auth", 0),
            'hs': db_row.get(f"{trade['code']}_hs", 0),
            'held': db_row.get(f"{trade['code']}_held", 0),
            'av': db_row.get(f"{trade['code']}_av", 0),
            'dist_hq': db_row.get(f"{trade['code']}_dist_hq", 0),
            'dist_1': db_row.get(f"{trade['code']}_dist_1", 0),
            'dist_2': db_row.get(f"{trade['code']}_dist_2", 0),
            'dist_3': db_row.get(f"{trade['code']}_dist_3", 0),
            'state_hq': db_row.get(f"{trade['code']}_state_hq", 0),
            'state_1': db_row.get(f"{trade['code']}_state_1", 0),
            'state_2': db_row.get(f"{trade['code']}_state_2", 0),
            'state_3': db_row.get(f"{trade['code']}_state_3", 0),
            'present_hq': db_row.get(f"{trade['code']}_present_hq", 0),
            'present_1': db_row.get(f"{trade['code']}_present_1", 0),
            'present_2': db_row.get(f"{trade['code']}_present_2", 0),
            'present_3': db_row.get(f"{trade['code']}_present_3", 0),
            'is_template': is_template  # Flag for frontend to show template indicator
        }
        result.append(trade_data)
    
    return result


@app.route('/api/trade-manpower/get/<date>', methods=['GET'])
def get_trade_manpower(date):
    """
    Get trade manpower data for a specific date.
    If data doesn't exist for requested date, return data from last available date.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # First, check if data exists for requested date
        cursor.execute("""
            SELECT * FROM trade_manpower_daily 
            WHERE report_date = %s
        """, (date,))
        
        current_data = cursor.fetchone()
        
        if current_data:
            # Data exists for requested date
            return_data = format_data_for_frontend(current_data, date, False)
            return jsonify({
                'success': True,
                'has_data': True,
                'data': return_data,
                'message': f'Data loaded for {date}',
                'is_template': False,
                'template_date': None,
                'is_present_day': True  # Add this flag
            })
        else:
            # No data for requested date, find last available date
            cursor.execute("""
                SELECT report_date FROM trade_manpower_daily 
                WHERE report_date < %s
                ORDER BY report_date DESC 
                LIMIT 1
            """, (date,))
            
            last_date_row = cursor.fetchone()
            
            if last_date_row:
                # Found data from previous date
                last_date = last_date_row['report_date'].strftime('%Y-%m-%d')
                
                cursor.execute("""
                    SELECT * FROM trade_manpower_daily 
                    WHERE report_date = %s
                """, (last_date,))
                
                template_data = cursor.fetchone()
                return_data = format_data_for_frontend(template_data, date, True)
                
                return jsonify({
                    'success': True,
                    'has_data': False,  # No data for current date
                    'data': return_data,
                    'message': f'No data found for {date}. Showing template from {last_date}.',
                    'is_template': True,
                    'template_date': last_date,
                    'is_present_day': True  # Add this flag
                })
            else:
                # No data at all in database
                return jsonify({
                    'success': True,
                    'has_data': False,
                    'data': [],  # Empty array to trigger new data entry
                    'message': 'No historical data found. Please enter new data.',
                    'is_template': False,
                    'template_date': None,
                    'is_present_day': True  # Add this flag
                })
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
def calculate_totals(data):
    """
    Calculate total columns from all trades
    """
    trades = ['op_ciph', 'oss', 'occ', 'ttc', 'lmn', 'efs', 'dvr_mt', 'dr', 'dtmn', 
              'skt', 'artsn', 'w_man', 'steward', 'dresser', 'hkeeper', 'mkeeper', 
              'chef_mess', 'chef_com', 'er', 'tlr', 'clk_sd', 'ere']
    
    fields = ['auth', 'hs', 'held', 'av', 'dist_hq', 'dist_1', 'dist_2', 'dist_3',
              'state_hq', 'state_1', 'state_2', 'state_3', 'present_hq', 'present_1',
              'present_2', 'present_3']
    
    totals = {}
    
    for field in fields:
        total = 0
        for trade in trades:
            key = f"{trade}_{field}"
            total += data.get(key, 0)
        totals[f"total_{field}"] = total
    
    return totals
@app.route('/api/trade-manpower/save', methods=['POST'])
def save_trade_manpower():
    """
    Save trade manpower data for a specific date
    """
    try:
        data = request.json
        date = data.get('date')
        trades = data.get('trades', [])
        
        if not date or not trades:
            return jsonify({
                'success': False,
                'error': 'Missing date or trades data'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if data already exists for this date
        cursor.execute("SELECT id FROM trade_manpower_daily WHERE report_date = %s", (date,))
        existing = cursor.fetchone()
        
        print(f"DEBUG: Saving for date {date}, existing: {existing}")
        
        # Create data dictionary for insertion
        insert_data = {'report_date': date}
        
        # Map trade names to column names
        trade_mapping = {
            'OP CIPH': 'op_ciph',
            'OSS': 'oss',
            'OCC': 'occ',
            'TTC': 'ttc',
            'LMN': 'lmn',
            'EFS': 'efs',
            'DVR MT': 'dvr_mt',
            'DR': 'dr',
            'DTMN': 'dtmn',
            'SKT': 'skt',
            'ARTSN': 'artsn',
            'W/MAN': 'w_man',
            'STEWARD': 'steward',
            'DRESSER': 'dresser',
            'HKEEPER': 'hkeeper',
            'MKEEPER': 'mkeeper',
            'CHEF MESS': 'chef_mess',
            'CHEF COM': 'chef_com',
            'ER': 'er',
            'TLR': 'tlr',
            'CLK SD': 'clk_sd',
            'ERE': 'ere'
        }
        
        # Process each trade
        for trade in trades:
            trade_name = trade['trade']
            trade_code = trade_mapping.get(trade_name)
            
            if not trade_code:
                print(f"WARNING: No mapping for trade: {trade_name}")
                continue
                
            # Map each field to column name
            fields_to_map = [
                ('auth', 'auth'),
                ('hs', 'hs'),
                ('held', 'held'),
                ('av', 'av'),
                ('dist_hq', 'dist_hq'),
                ('dist_1', 'dist_1'),
                ('dist_2', 'dist_2'),
                ('dist_3', 'dist_3'),
                ('state_hq', 'state_hq'),
                ('state_1', 'state_1'),
                ('state_2', 'state_2'),
                ('state_3', 'state_3'),
                ('present_hq', 'present_hq'),
                ('present_1', 'present_1'),
                ('present_2', 'present_2'),
                ('present_3', 'present_3')
            ]
            
            for frontend_field, db_field in fields_to_map:
                column_name = f"{trade_code}_{db_field}"
                value = trade.get(frontend_field, 0)
                insert_data[column_name] = value
        
        # Calculate totals
        totals = calculate_totals(insert_data)
        insert_data.update(totals)
        
        print(f"DEBUG: insert_data keys: {list(insert_data.keys())[:5]}...")
        print(f"DEBUG: insert_data sample values: {list(insert_data.values())[:5]}...")
        
        if existing:
            # Update existing record - FIXED VERSION
            print(f"DEBUG: Updating existing record for {date}")
            
            # Create SET clause
            set_items = []
            set_values = []
            
            for key, value in insert_data.items():
                if key != 'report_date':  # Don't update the report_date in SET clause
                    set_items.append(f"{key} = %s")
                    set_values.append(value)
            
            # Add the WHERE clause value
            set_values.append(date)
            
            query = f"""
                UPDATE trade_manpower_daily 
                SET {', '.join(set_items)}
                WHERE report_date = %s
            """
            
            print(f"DEBUG: UPDATE query: {query}")
            print(f"DEBUG: UPDATE values: {set_values[:5]}...")
            
            cursor.execute(query, set_values)
            action = 'updated'
        else:
            # Insert new record
            print(f"DEBUG: Inserting new record for {date}")
            
            columns = ', '.join(insert_data.keys())
            placeholders = ', '.join(['%s'] * len(insert_data))
            
            query = f"""
                INSERT INTO trade_manpower_daily ({columns})
                VALUES ({placeholders})
            """
            
            cursor.execute(query, list(insert_data.values()))
            action = 'inserted'
        
        conn.commit()
        
        print(f"DEBUG: Data {action} successfully for {date}")
        
        return jsonify({
            'success': True,
            'message': f'Data {action} successfully for {date}',
            'date': date,
            'action': action
        })
        
    except Exception as e:
        print(f"ERROR in save_trade_manpower: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
                        
@app.route('/api/trade-manpower/export-csv/<date>', methods=['GET'])
def export_trade_csv(date):
    """
    Export trade manpower data to CSV
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM trade_manpower_daily 
            WHERE report_date = %s
        """, (date,))
        
        data = cursor.fetchone()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data found for the specified date'
            }), 404
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        header = [
            'SR NO', 'TRADE/CAT', 'AUTH', 'H/S', 'HELD', 'AV',
            'HQ COY DIST', '1 COY DIST', '2 COY DIST', '3 COY DIST',
            'HQ COY STATE', '1 COY STATE', '2 COY STATE', '3 COY STATE',
            'HQ COY PRESENT', '1 COY PRESENT', '2 COY PRESENT', '3 COY PRESENT'
        ]
        writer.writerow(header)
        
        # Trade order
        trades = [
            ('OP CIPH', 'op_ciph'),
            ('OSS', 'oss'),
            ('OCC', 'occ'),
            ('TTC', 'ttc'),
            ('LMN', 'lmn'),
            ('EFS', 'efs'),
            ('DVR MT', 'dvr_mt'),
            ('DR', 'dr'),
            ('DTMN', 'dtmn'),
            ('SKT', 'skt'),
            ('ARTSN', 'artsn'),
            ('W/MAN', 'w_man'),
            ('STEWARD', 'steward'),
            ('DRESSER', 'dresser'),
            ('HKEEPER', 'hkeeper'),
            ('MKEEPER', 'mkeeper'),
            ('CHEF MESS', 'chef_mess'),
            ('CHEF COM', 'chef_com'),
            ('ER', 'er'),
            ('TLR', 'tlr'),
            ('CLK SD', 'clk_sd'),
            ('ERE', 'ere')
        ]
        
        # Write trade rows
        for sr_no, (trade_name, trade_code) in enumerate(trades, 1):
            row = [
                sr_no,
                trade_name,
                data.get(f"{trade_code}_auth", 0),
                data.get(f"{trade_code}_hs", 0),
                data.get(f"{trade_code}_held", 0),
                data.get(f"{trade_code}_av", 0),
                data.get(f"{trade_code}_dist_hq", 0),
                data.get(f"{trade_code}_dist_1", 0),
                data.get(f"{trade_code}_dist_2", 0),
                data.get(f"{trade_code}_dist_3", 0),
                data.get(f"{trade_code}_state_hq", 0),
                data.get(f"{trade_code}_state_1", 0),
                data.get(f"{trade_code}_state_2", 0),
                data.get(f"{trade_code}_state_3", 0),
                data.get(f"{trade_code}_present_hq", 0),
                data.get(f"{trade_code}_present_1", 0),
                data.get(f"{trade_code}_present_2", 0),
                data.get(f"{trade_code}_present_3", 0)
            ]
            writer.writerow(row)
        
        # Write totals row
        totals_row = [
            '', 'TOTAL',
            data.get('total_auth', 0),
            data.get('total_hs', 0),
            data.get('total_held', 0),
            data.get('total_av', 0),
            data.get('total_dist_hq', 0),
            data.get('total_dist_1', 0),
            data.get('total_dist_2', 0),
            data.get('total_dist_3', 0),
            data.get('total_state_hq', 0),
            data.get('total_state_1', 0),
            data.get('total_state_2', 0),
            data.get('total_state_3', 0),
            data.get('total_present_hq', 0),
            data.get('total_present_1', 0),
            data.get('total_present_2', 0),
            data.get('total_present_3', 0)
        ]
        writer.writerow(totals_row)
        
        # Prepare response
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = f'attachment; filename=trade_manpower_{date}.csv'
        response.headers['Content-type'] = 'text/csv'
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/company/interview-pending')
def company_interview_pending():
    user = require_login()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    company = user['company']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        excluded_ranks = ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
        rank_placeholders = ",".join(["%s"] * len(excluded_ranks))

        # 1️⃣ Pending interviews
        cursor.execute(f"""
            SELECT name, army_number, home_state, company, `rank`
            FROM personnel
            WHERE interview_status = 0
              AND company = %s
              AND `rank` NOT IN ({rank_placeholders})
            ORDER BY home_state, name
        """, (company, *excluded_ranks))

        pending_data = cursor.fetchall()

        # 2️⃣ Collect unique home_states
        home_states = list({
            row['home_state']
            for row in pending_data
            if row['home_state']
        })

        # Maps
        jco_map = {}              # live eligible JCOs
        assigned_jco_map = {}     # assigned (Pending) JCOs

        if home_states:
            placeholders = ",".join(["%s"] * len(home_states))

            # 3️⃣ Live eligible JCOs
            cursor.execute(f"""
                SELECT name, home_state, `rank`
                FROM personnel
                WHERE home_state IN ({placeholders})
                  AND `rank` IN ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
                  AND onleave_status = 0
                  AND detachment_status = 0
                  AND posting_status = 0
                ORDER BY
                  FIELD(`rank`,
                        'Sub Maj',
                        'Subedar Major',
                        'Subedar',
                        'Naib Subedar'),
                  name
            """, home_states)

            senior_ranks = cursor.fetchall()

            for jco in senior_ranks:
                state = jco['home_state']
                if state not in jco_map:
                    jco_map[state] = jco['name']

            # 4️⃣ Assigned JCOs (Pending)
            cursor.execute(f"""
                SELECT 
                    ja.additional_assigned_home_state AS home_state,
                    p.name AS jco_name
                FROM jco_kunda_assignment ja
                JOIN personnel p
                    ON p.army_number = ja.army_number
                WHERE ja.additional_assigned_home_state IN ({placeholders})
                  AND ja.interview_status = 'Pending'
            """, home_states)

            assigned_rows = cursor.fetchall()

            for row in assigned_rows:
                state = row['home_state']
                if state not in assigned_jco_map:
                    assigned_jco_map[state] = row['jco_name']

        # 5️⃣ Attach JCO with fallback logic
        for row in pending_data:
            state = row['home_state']

            if state in jco_map:
                row['jco_name'] = jco_map[state]
                row['jco_source'] = 'live'

            elif state in assigned_jco_map:
                row['jco_name'] = f"Temporaray assigned JCO {assigned_jco_map[state]}"
                row['jco_source'] = 'assigned'

            else:
                row['jco_name'] = None
                row['jco_source'] = None


        return jsonify({
            "status": "success",
            "pending_interviews": pending_data
        })

    finally:
        cursor.close()
        conn.close()



@app.route('/api/company/available-jcos')
def get_available_jcos():
    user = require_login()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    company = user['company']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                army_number,
                name,
                `rank`,
                home_state
            FROM personnel
            
              where `rank` IN ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
              AND onleave_status = 0
              AND detachment_status = 0
              AND posting_status = 0
            ORDER BY
              FIELD(`rank`,
                    'Sub Maj',
                    'Subedar Major',
                    'Subedar',
                    'Naib Subedar'),
              name
        """,)

        jco_result = cursor.fetchall()
        print(jco_result)

        return jsonify({
            "status": "success",
            "jcos": jco_result
        })

    finally:
        cursor.close()
        conn.close()

@app.route('/assign_jco', methods=['POST'])
def assign_jco():
    data = request.get_json()

    army_number = data.get('army_number')
    state = data.get('additional_assigned_home_state')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO jco_kunda_assignment 
            (army_number, additional_assigned_home_state, interview_status)
            VALUES (%s, %s, 'Pending')
            ON DUPLICATE KEY UPDATE
                additional_assigned_home_state = VALUES(additional_assigned_home_state),
                interview_status = 'Pending'
        """, (army_number, state))

        conn.commit()
        return jsonify(success=True)

    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=str(e))

    finally:
        cursor.close()
        conn.close()
@app.route('/api/alarms_pending_kunda_assignments')
def pending_kunda_assignments():
    user = require_login()
    army_number = user['army_number']
    print(army_number)
    print("this api is getting triggered")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    print('route hit')
    print('------------------------')

    try:
        cursor.execute("""
            SELECT army_number, additional_assigned_home_state
            FROM jco_kunda_assignment
            WHERE interview_status = 'Pending' AND army_number = %s
        """, (army_number,))  # ✅ Correctly pass parameters as a tuple

        rows = cursor.fetchall()
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(rows)

    finally:
        cursor.close()
        conn.close()

    return jsonify({"rows": rows})

@app.route('/api/kunda_pending_personnel')
def kunda_pending_personnel():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ensure the user is logged in
    user = require_login()
    army_number = user['army_number']

    # 1️⃣ Get pending home_states assigned to this army_number
    cursor.execute("""
        SELECT additional_assigned_home_state
        FROM jco_kunda_assignment
        WHERE interview_status='Pending' AND army_number=%s
    """, (army_number,))
    
    home_states = [row['additional_assigned_home_state'] for row in cursor.fetchall()]

    if not home_states:
        cursor.close()
        conn.close()
        return jsonify({"rows": []})

    # 2️⃣ Fetch personnel with all statuses = 0 and home_state in pending list
    placeholders = ",".join(["%s"] * len(home_states))
    query = f"""
        SELECT id, army_number, `rank`, name, home_state
        FROM personnel
        WHERE onleave_status=0
          AND detachment_status=0
          AND posting_status=0
          AND interview_status=0
          AND home_state IN ({placeholders})
    """
    cursor.execute(query, home_states)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify({"rows": rows})
@app.route('/api/mark_interview_done', methods=['POST'])
def mark_interview_done():
    data = request.get_json()
    home_state = data.get('home_state')
    army_number_front_end = data.get('army_number_front_end')
    print(data, 'incoming data')

    if not home_state or not army_number_front_end:
        return jsonify({"success": False, "message": "home_state and army_number are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # 1️⃣ Update the specific personnel row
        cursor.execute("""
            UPDATE personnel
            SET interview_status = 1
            WHERE home_state = %s
              AND army_number = %s
              AND interview_status = 0
        """, (home_state, army_number_front_end))

        # 2️⃣ Check if any other personnel with the same home_state is still pending
        cursor.execute("""
            SELECT COUNT(*) AS pending_count
            FROM personnel
            WHERE home_state = %s
              AND interview_status = 0
        """, (home_state,))
        result = cursor.fetchone()
        pending_count = result['pending_count'] if result else 0

        # 3️⃣ If no pending personnel, mark assignment done
        if pending_count == 0:
            cursor.execute("""
                UPDATE jco_kunda_assignment
                SET interview_status = 'Done'
                WHERE additional_assigned_home_state = %s
                  AND interview_status = 'Pending'
            """, (home_state,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": str(e)}), 500

    cursor.close()
    conn.close()
    return jsonify({"success": True})




@app.route('/gallery/manage')
def manager_file():
    user = require_login()
    if not user or user.get('role') not in ['O CENTRE NCO', 'Admin', 'CO']:
        return "Unauthorized", 403
    return render_template('gallery/manage.html')


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "jpg", "jpeg", "png", "webp"
    }

from werkzeug.utils import secure_filename
import time
import os
@app.route("/gallery/save", methods=["POST"])
def save_gallery():
    try:
        user = require_login()
        if not user or user.get('role') not in ['O CENTRE NCO', 'Admin', 'CO']:
            return jsonify(success=False, message="Unauthorized"), 403

        print("🟢 STEP 1: Request received")

        title = request.form.get("title", "").strip()
        subtitle = request.form.get("subtitle", "").strip()
        image = request.files.get("image")

        print("🟢 STEP 2: Form data")
        print("Title:", title)
        print("Subtitle:", subtitle)
        print("Image:", image)

        if not image or image.filename == "":
            print("🔴 ERROR: No image selected")
            return jsonify(success=False, message="No image selected")

        if not allowed_file(image.filename):
            print("🔴 ERROR: Invalid file type")
            return jsonify(success=False, message="Invalid image type")

        print("🟢 STEP 3: File validation passed")

        filename = f"{int(time.time())}_{secure_filename(image.filename)}"
        upload_folder = os.path.join("static", "uploads", "gallery")
        os.makedirs(upload_folder, exist_ok=True)

        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        print("🟢 STEP 4: Image saved at", image_path)

        conn = get_db_connection()
        cursor = conn.cursor()

        print("🟢 STEP 5: DB connected")

        cursor.execute(
            "INSERT INTO gallery_settings (title, subtitle, image) VALUES (%s, %s, %s)",
            (title, subtitle, filename)
        )

        conn.commit()
        print("🟢 STEP 6: DB commit success")

        cursor.close()
        conn.close()

        print("✅ DONE: Gallery saved successfully")

        return jsonify(success=True, filename=filename)

    except Exception as e:
        print("❌ Gallery upload error (FULL):", repr(e))
        return jsonify(success=False, message=str(e)), 500
    
@app.route('/api/dashboard/birthdays', methods=['GET'])
def get_today_birthdays():
    """Return personnel whose birthday is today (month-day match, ignoring year)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    company = user['company']

    try:
        query = """
            SELECT name, army_number, `rank`, company,
                   home_state, home_village, home_district,
                   CONCAT_WS(', ', NULLIF(TRIM(home_village), ''), NULLIF(TRIM(home_district), ''), NULLIF(TRIM(home_state), '')) AS address
            FROM personnel
            WHERE date_of_birth IS NOT NULL
              AND MONTH(date_of_birth) = MONTH(CURDATE())
              AND DAY(date_of_birth) = DAY(CURDATE())
        """
        params = []
        if company != "Admin":
            query += " AND company = %s"
            params.append(company)

        query += " ORDER BY name;"
        cursor.execute(query, params)
        rows = cursor.fetchall()

        result = []
        for r in rows:
            addr = r.get('address') or r.get('home_state') or '—'
            result.append({
                "name": r.get("name") or "—",
                "rank": r.get("rank") or "—",
                "army_number": r.get("army_number") or "—",
                "company": r.get("company") or "—",
                "address": addr.strip() if addr and addr != ',' else (r.get('home_state') or '—')
            })

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        print("Error fetching today's birthdays:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/settings')
def settings_page():
    """Settings page - theme and other preferences."""
    user = require_login()
    if not user:
        return redirect(url_for('admin_login'))
    return render_template('settings/settings.html', role=user['role'])

@app.route("/api/gallery", methods=["GET"])
def get_gallery():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id,title, subtitle, image
            FROM gallery_settings
            ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        print("❌ Gallery fetch error:", e)
        return jsonify([]), 500


@app.route('/company_based_domain_sp', methods=['GET'])
def get_company_duty_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user = require_login()
    if not user:
        return jsonify(0), 401  # Return 0 if unauthorized

    company = user['company']

    try:
        duty_query = """
            SELECT COUNT(DISTINCT p.army_number) AS count
            FROM personnel p
            LEFT JOIN (
                SELECT army_number, duty_performed
                FROM units_served
                WHERE (army_number, sr_no) IN (
                    SELECT army_number, MAX(sr_no)
                    FROM units_served
                    GROUP BY army_number
                )
            ) u ON p.army_number = u.army_number
            WHERE u.duty_performed IS NOT NULL AND u.duty_performed != ''
            AND p.company = %s
        """

        cursor.execute(duty_query, (company,))
        duty_result = cursor.fetchone()
        duty_count = duty_result['count'] if duty_result else 0
        print(duty_count)

        # Return only the count
        return jsonify(duty_count)

    except Exception as e:
        print(str(e))
        return jsonify(0), 500

    finally:
        cursor.close()
        conn.close()
@app.route('/api/gallery/<int:id>', methods=['DELETE'])
def delete_gallery(id):
    print("🔥 DELETE API HIT:", id)  # DEBUG

    user = require_login()
    if not user:
        return jsonify({"success": False}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get image name
        cursor.execute("SELECT image FROM gallery_settings WHERE id = %s", (id,))
        row = cursor.fetchone()

        if not row:
            print("❌ Image not found in DB")
            return jsonify({"success": False, "message": "Not found"}), 404

        # Delete file
        import os
        image_path = os.path.join('static/uploads/gallery', row['image'])

        if os.path.exists(image_path):
            os.remove(image_path)
            print("🗑 File deleted:", image_path)

        # Delete DB record
        cursor.execute("DELETE FROM gallery_settings WHERE id = %s", (id,))
        conn.commit()

        print("✅ Deleted from DB")

        return jsonify({"success": True})

    except Exception as e:
        print("❌ DELETE ERROR:", str(e))
        return jsonify({"success": False})

    finally:
        cursor.close()
        conn.close()
if __name__ == '__main__':
    app.run(port=4000,debug=True)
