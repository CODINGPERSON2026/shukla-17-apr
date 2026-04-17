from imports import *
from db_config import get_db_connection


leave_bp = Blueprint('apply_leave', __name__, url_prefix='/apply_leave')
@leave_bp.route("/", methods=["GET"])
def apply_leave():
       return render_template("apply_leave/apply_leave.html")

@leave_bp.route("/get_leave_details", methods=["POST"])
def get_leave_details():
    data = request.get_json()
    army_no = data.get("person_id")

    if not army_no:
        return jsonify({"success": False, "message": "Army number missing"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT name, army_number, trade, `rank`, company
            FROM personnel
            WHERE army_number = %s
        """, (army_no,))
        personnel = cursor.fetchone()

        if not personnel:
            return jsonify({"success": False, "message": "No such soldier found"}), 404

        cursor.execute("""
            SELECT sr_no, year, al_days, cl_days, aal_days, total_days, remarks
            FROM leave_details
            WHERE army_number = %s
            ORDER BY year DESC
            LIMIT 1
        """, (army_no,))
        leaveinfo = cursor.fetchone()
        print(leaveinfo)

        if not leaveinfo:
            # If no record in leave_details, we can still show standard entitlements
            # or return empty. Given the user's comment, I'll provide the standard ones.
            leaveinfo = {
                "al_days": 60,
                "cl_days": 30,
                "aal_days": 30
            }

        # Query actual leave taken from approved requests
        cursor.execute("""
            SELECT leave_type, SUM(leave_days) as taken
            FROM leave_status_info
            WHERE army_number = %s AND request_status = 'Approved'
            GROUP BY leave_type
        """, (army_no,))
        taken_info = cursor.fetchall()
        taken_dict = {row['leave_type']: row['taken'] for row in taken_info}

        # Get personnel rank to determine entitlements
        rank = personnel.get('rank', '').strip().upper()
        
        # Check if Agniveer rank
        is_agniveer = rank in ['AGNIVEER', 'AV']
        
        # Set entitlements based on rank
        if is_agniveer:
            # Agniveer: Only AL=30 days
            al_total = 30
            cl_total = 0
            aal_total = 0
        else:
            # Other ranks: AL=60, CL=30, AAL=30
            al_total = 60
            cl_total = 30
            aal_total = 30

        al_taken = taken_dict.get('AL', 0) or 0
        cl_taken = taken_dict.get('CL', 0) or 0
        aal_taken = taken_dict.get('AAL', 0) or 0

        # Build leave balance array based on rank
        leave_balance = [
            {
                "leave_type": "AL",
                "total_leave": al_total,
                "leave_taken": int(al_taken),
                "balance_leave": al_total - int(al_taken)
            }
        ]
        
        # Only add CL and AAL for non-Agniveer ranks
        if not is_agniveer:
            leave_balance.extend([
                {
                    "leave_type": "CL",
                    "total_leave": cl_total,
                    "leave_taken": int(cl_taken),
                    "balance_leave": cl_total - int(cl_taken)
                },
                {
                    "leave_type": "AAL",
                    "total_leave": aal_total,
                    "leave_taken": int(aal_taken),
                    "balance_leave": aal_total - int(aal_taken)
                }
            ])

        # Add Summary Total Row
        total_auth = sum(l['total_leave'] for l in leave_balance)
        total_taken = sum(l['leave_taken'] for l in leave_balance)
        total_balance = sum(l['balance_leave'] for l in leave_balance)

        leave_balance.append({
            "leave_type": "Total",
            "total_leave": total_auth,
            "leave_taken": total_taken,
            "balance_leave": total_balance
        })

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "personnel": personnel,
            "leave_balance": leave_balance
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@leave_bp.route("/search_personnel")
def search_personnel():
    query = request.args.get("query", "").strip()

    if query == "":
        return jsonify([])

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 🔍 Check if any leave exists for this army number
        cursor.execute("""
            SELECT army_number, request_status, leave_type, from_date, to_date
            FROM leave_status_info
            WHERE army_number = %s
            ORDER BY from_date DESC
            LIMIT 1
        """, (query,))
        
        existing = cursor.fetchone()

        if existing:
            status = (existing.get("request_status") or "").strip().lower()

            # ✅ CASE 1: CLOSED → treat as NO ACTIVE LEAVE
            if status in ["closed", "leave closed"]:
                cursor.execute("""
                    SELECT name, army_number, `rank`, trade, company, section
                    FROM personnel
                    WHERE army_number LIKE %s
                    LIMIT 1
                """, (f"%{query}%",))
                
                results = cursor.fetchall()
                return jsonify(results)

            # ✅ CASE 2: ACTIVE LEAVE → normalize status
            if status.startswith("pending"):
                existing["request_status"] = "Pending"
            elif status.startswith("approved"):
                existing["request_status"] = "Approved"
            elif status.startswith("rejected"):
                existing["request_status"] = "Rejected"
            else:
                # fallback (kept as original if unknown)
                existing["request_status"] = existing.get("request_status")

            return jsonify({
                "exists": True,
                "existing_leave": existing
            })

        # ✅ CASE 3: NO LEAVE FOUND → return personnel
        cursor.execute("""
            SELECT name, army_number, `rank`, trade, company, section
            FROM personnel
            WHERE army_number LIKE %s
            LIMIT 1
        """, (f"%{query}%",))
        
        results = cursor.fetchall()
        return jsonify(results)

    except Exception as e:
        print("Error in search_personnel:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()






from datetime import datetime

@leave_bp.route("/submit_leave", methods=["POST"])
def submit_leave_request():
    data = request.get_json()
    print("Received data:", data)

    army_number = data.get("person_id")
    leave_type_str = data.get("leave_type")
    combined_leaves = data.get("combined_leaves", [])
    actual_leave_days = data.get("actual_leave_days")
    total_days = data.get("total_days")
    prefix_days = data.get("prefix_days", 0)
    suffix_days = data.get("suffix_days", 0)
    prefix_date = data.get("prefix_date")
    suffix_date = data.get("suffix_date")
    from_date = data.get("from_date")
    to_date = data.get("to_date")
    reason = data.get("reason")
    name = data.get("name")

    # NEW: Transport and Address data
    transport_data = data.get("transport", {})
    address_data = data.get("address_while_on_leave", {})

    if not all([army_number, leave_type_str, from_date, to_date, reason]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Personnel & Approval Logic (UNCHANGED)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT company, `rank`, section FROM personnel WHERE army_number = %s", (army_number,))
        personnel = cursor.fetchone()

        if not personnel:
            return jsonify({"status": "error", "message": "Personnel not found"}), 404

        company_name = personnel['company'].lower()
        rank = personnel['rank']
        section = personnel['section']

        if rank in ['Subedar', 'Naib Subedar', 'Subedar Major']:
            request_sent_to = 'Subedar Major'
            request_status = 'Pending at Subedar Major'
        else:
            request_sent_to = f'NCO {section}'
            request_status = f'Pending at NCO {section}'

    except Exception as e:
        return jsonify({"status": "error", "message": "Database error", "error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    # Insert main record + new tables (with rollback protection)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # ==================== EXISTING MAIN INSERT (UNCHANGED) ====================
        cursor.execute("""
            INSERT INTO leave_status_info
            (army_number, `rank`, name, company, leave_type, leave_days, from_date, to_date,
             prefix_date, suffix_date, prefix_days, suffix_days, request_sent_to, request_status,
             remarks, leave_reason, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """, (
            army_number, rank, name, company_name, leave_type_str,
            int(actual_leave_days or total_days), from_date, to_date,
            prefix_date, suffix_date, int(prefix_days or 0), int(suffix_days or 0),
            request_sent_to, request_status,
            f"{leave_type_str} for {total_days} day(s) (Prefix: {prefix_days}, Suffix: {suffix_days})",
            reason
        ))

        main_leave_id = cursor.lastrowid
        conn.commit()

        # ==================== EXISTING MULTI LEAVE TABLE (UNCHANGED) ====================
        for leave in combined_leaves:
            lt = leave.get("leave_type")
            fdate = leave.get("from_date")
            tdate = leave.get("to_date")
            if lt and fdate and tdate:
                try:
                    from_dt = datetime.strptime(fdate, "%Y-%m-%d")
                    to_dt = datetime.strptime(tdate, "%Y-%m-%d")
                    days_this_type = (to_dt - from_dt).days + 1
                except:
                    days_this_type = int(actual_leave_days or total_days)

                cursor.execute("""
                    INSERT INTO multi_leave_table 
                    (leave_request_id, army_number, leave_type, leave_days, from_date, to_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (main_leave_id, army_number, lt, days_this_type, fdate, tdate))

        conn.commit()

        # ==================== NEW: INSERT TRANSPORT ====================
        onward = transport_data.get("onward", {})
        return_journey = transport_data.get("return", {})

        cursor.execute("""
            INSERT INTO leave_transport 
            (leave_request_id, 
             onward_mode, onward_air_type, onward_train_type,
             return_mode, return_air_type, return_train_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            main_leave_id,
            onward.get("mode", ""),
            onward.get("air_type", ""),
            onward.get("train_type", ""),
            return_journey.get("mode", ""),
            return_journey.get("air_type", ""),
            return_journey.get("train_type", "")
        ))

        transport_id = cursor.lastrowid
        conn.commit()

        # ==================== NEW: INSERT JOURNEY LEGS ====================
        # Onward legs
        onward_legs = onward.get("legs", [])
        for i, leg in enumerate(onward_legs, 1):
            cursor.execute("""
                INSERT INTO leave_journey_legs 
                (transport_id, journey_type, leg_order, from_station, to_station)
                VALUES (%s, 'onward', %s, %s, %s)
            """, (transport_id, i, leg.get("from", ""), leg.get("to", "")))

        # Return legs
        return_legs = return_journey.get("legs", [])
        for i, leg in enumerate(return_legs, 1):
            cursor.execute("""
                INSERT INTO leave_journey_legs 
                (transport_id, journey_type, leg_order, from_station, to_station)
                VALUES (%s, 'return', %s, %s, %s)
            """, (transport_id, i, leg.get("from", ""), leg.get("to", "")))

        conn.commit()

        # ==================== NEW: INSERT ADDRESS WHILE ON LEAVE ====================
        cursor.execute("""
            INSERT INTO leave_address 
            (leave_request_id, same_as_permanent, address_line1, address_line2, 
             city, state, pincode, mobile, alternate_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            main_leave_id,
            address_data.get("same_as_permanent", True),
            address_data.get("address_line1", ""),
            address_data.get("address_line2", ""),
            address_data.get("city", ""),
            address_data.get("state", ""),
            address_data.get("pincode", ""),
            address_data.get("mobile", ""),
            address_data.get("alternate_contact", "")
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": f"Leave request ({leave_type_str}) for {total_days} day(s) submitted successfully!",
            "leave_request_id": main_leave_id
        })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print("Error:", str(e))
        return jsonify({"status": "error", "message": "Failed to submit leave", "error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


    # # Insert leave request - use actual_leave_days for leave_days field
    # try:
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("""
    #         INSERT INTO leave_status_info
    #         (army_number, `rank`, name, company, leave_type, leave_days, from_date, to_date, prefix_date, suffix_date, prefix_days, suffix_days, request_sent_to, request_status, recommend_date, rejected_date, remarks, leave_reason, created_at, updated_at)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, %s, %s, NOW(), NOW())
    #     """, (
    #         army_number,
    #         rank,
    #         name,
    #         company_name,
    #         leave_type,
    #         int(actual_leave_days),
    #         from_date,
    #         to_date,
    #         prefix_date,
    #         suffix_date,
    #         int(prefix_days),
    #         int(suffix_days),
    #         request_sent_to,
    #         request_status,
    #         f"{leave_type} for {total_days} day(s) (Actual: {actual_leave_days} days, Prefix: {prefix_days}, Suffix: {suffix_days})",
    #         reason
    #     ))
    #     conn.commit()
    #     return jsonify({'status':'success',"message": f"Leave request for {total_days} day(s) sent successfully!"})
    # except Exception as e:
    #     conn.rollback()
    #     return jsonify({"message": "Failed to apply leave", "error": str(e)}), 500
    # finally:
    #     cursor.close()
    #     conn.close()


# FOR SENDING THE LEAVE REQUEST TO HIGHER LEVEL
@leave_bp.route("/update_leave_status", methods=["POST"])
def update_leave_status():
    data = request.get_json()
    leave_id = data.get("id")
    status = data.get("status")

    if status not in ['Approved', 'Rejected']:
        return jsonify({"status": "error", "message": "Invalid status"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if status == 'Approved':
            cursor.execute("""
                UPDATE leave_status_info
                SET request_status = %s, updated_at = NOW()
                WHERE id = %s
            """, (status, leave_id))
        else:
            cursor.execute("""
                UPDATE leave_status_info
                SET request_status = %s, rejected_date = NOW()
                WHERE id = %s
            """, (status, leave_id))

        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@leave_bp.route("/get_leave_requests", methods=["GET"])
def get_leave_requests():
    print('in this route')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user = require_login()
    current_user_role = user['role']
    current_user_company = user['company']

    print("Current Role:", current_user_role)

    request_status = f'Pending at {current_user_role}'
    print("Request Status:", request_status)

    try:
        # =========================
        # CASE 1: NORMAL ROLES
        # =========================
        if current_user_role != '2IC' and current_user_role != 'CO' and current_user_role != 'Subedar Major':

            query = '''
                SELECT 
                    l.id,
                    l.name,
                    l.army_number,
                    p.rank,
                    l.company,
                    l.leave_type,
                    l.leave_days,
                    l.request_status,
                    l.remarks,
                    l.created_at
                FROM leave_status_info l
                LEFT JOIN personnel p 
                    ON l.army_number = p.army_number
                WHERE l.request_sent_to = %s 
                AND l.request_status = %s
                AND l.company = %s
                ORDER BY l.created_at DESC
            '''

            cursor.execute(query, (
                current_user_role,
                request_status,
                current_user_company
            ))
        elif current_user_role == 'Subedar Major':
            print("in this route of Subedar Major CHECKED")
            query = '''
                SELECT 
                    l.id,
                    l.name,
                    l.army_number,
                    p.rank,
                    l.company,
                    l.leave_type,
                    l.leave_days,
                    l.request_status,
                    l.remarks,
                    l.created_at
                FROM leave_status_info l
                LEFT JOIN personnel p 
                    ON l.army_number = p.army_number
                WHERE l.request_sent_to = %s 
                AND l.request_status = %s
                ORDER BY l.created_at DESC
            '''

            cursor.execute(query, (
                current_user_role,
                request_status,
                
            ))


        # =========================
        # CASE 2: CO ROLE
        # ========================

        
        elif current_user_role == '2IC' or current_user_role == 'CO':

            query = '''
                SELECT 
                    l.id,
                    l.name,
                    l.army_number,
                    l.company,
                    p.rank,
                    l.leave_type,
                    l.leave_days,
                    l.request_status,
                    l.remarks,
                    l.created_at
                FROM leave_status_info l
                LEFT JOIN personnel p 
                    ON l.army_number = p.army_number
                WHERE l.request_sent_to = %s 
                AND l.request_status = %s
                ORDER BY l.created_at DESC
            '''

            cursor.execute(query, (
                current_user_role,
                request_status
            ))

        rows = cursor.fetchall()

        print("Fetched Rows:", rows)

        return jsonify({
            "status": "success",
            "data": rows
        })

    except Exception as e:
        print("Error fetching leave requests:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


@leave_bp.route("/get_leave_request/<int:leave_id>", methods=["GET"])
def get_leave_request(leave_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch main leave request
        cursor.execute("""
            SELECT 
                id,
                army_number,
                `rank`,
                name,
                company,
                leave_type,
                leave_days,
                from_date,
                to_date,
                prefix_date,
                suffix_date,
                prefix_days,
                suffix_days,
                leave_reason,
                request_status,
                reject_reason
            FROM leave_status_info
            WHERE id = %s
        """, (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            return jsonify({
                "success": False,
                "message": "Leave request not found"
            }), 404

        # Fetch name and rank from personnel table
        cursor.execute("SELECT name, `rank` FROM personnel WHERE army_number = %s", 
                      (leave['army_number'],))
        name_result = cursor.fetchone()
        
        if name_result:
            leave['name'] = name_result['name']
            leave['rank'] = name_result['rank']

        # Handle Combined Leave - Check if leave_type has '+'
        if '+' in leave.get('leave_type', ''):
            # Fetch individual leave details from multi_leave_table
            cursor.execute("""
                SELECT 
                    leave_type,
                    leave_days,
                    from_date,
                    to_date
                FROM multi_leave_table 
                WHERE leave_request_id = %s
                ORDER BY id ASC
            """, (leave_id,))
            
            multi_details = cursor.fetchall()

            if multi_details:
                # Format leave_type as "AL(15) + PL(10)"
                formatted = []
                for d in multi_details:
                    formatted.append(f"{d['leave_type']}({d['leave_days']})")
                
                leave['leave_type'] = " + ".join(formatted)

                # Add full details for frontend (optional but very useful)
                leave['leave_details'] = []
                for d in multi_details:
                    leave['leave_details'].append({
                        "leave_type": d['leave_type'],
                        "leave_days": d['leave_days'],
                        "from_date": d['from_date'].strftime('%d-%b-%Y') if d['from_date'] else None,
                        "to_date": d['to_date'].strftime('%d-%b-%Y') if d['to_date'] else None
                    })

        # Convert all date fields to dd-MMM-YYYY format
        if leave.get('from_date'):
            leave['from_date'] = leave['from_date'].strftime('%d-%b-%Y')

        if leave.get('to_date'):
            leave['to_date'] = leave['to_date'].strftime('%d-%b-%Y')

        if leave.get('prefix_date'):
            leave['prefix_date'] = leave['prefix_date'].strftime('%d-%b-%Y')

        if leave.get('suffix_date'):
            leave['suffix_date'] = leave['suffix_date'].strftime('%d-%b-%Y')

        # Set leave_request_type based on user role
        user = require_login()
        if user['role'] == 'OC':
            leave['leave_request_type'] = 'OR'
        elif user['role'] == 'CO':
            leave['leave_request_type'] = 'OFFICER'

        print("THIS IS LEAVE RETURNED", leave)

        return jsonify({
            "success": True,
            "data": leave
        })

    except Exception as e:
        print("Error in get_leave_request:", str(e))
        return jsonify({
            "success": False,
            "message": "Server error",
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@leave_bp.route("/recommend_leave", methods=["POST"])
def recommend_leave():
    data = request.get_json()
    print(data)

    leave_id = data.get("leave_id")
    if not leave_id:
        return jsonify({"message": "Leave ID missing"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        send_request_to = ''
        request_status = ''

        user = require_login()
        current_user_role = user['role']

        # ================= ROLE FLOW =================
        if current_user_role.startswith("NCO "):
            send_request_to = current_user_role.replace("NCO ", "JCO ", 1)
            request_status = f"Pending at {send_request_to}"

        elif current_user_role.startswith("JCO "):
            send_request_to = 'S/JCO'
            request_status = f"Pending at {send_request_to}"

        elif current_user_role.startswith("S/JCO"):
            send_request_to = 'OC'
            request_status = f"Pending at {send_request_to}"

        elif current_user_role == 'Subedar Major':
            send_request_to = 'OC'
            request_status = 'Pending at OC'

        # ================= FINAL APPROVAL LOGIC =================
        if current_user_role == 'OC':
            cursor.execute("""
                SELECT `rank` FROM personnel 
                WHERE army_number = (SELECT army_number FROM leave_status_info WHERE id = %s)
            """, (leave_id,))
            rank_result = cursor.fetchone()
            rank = rank_result['rank'] if rank_result else ''

            if rank not in ['Subedar', 'Naib Subedar', 'Subedar Major']:
                send_request_to = 'Approved'
                request_status = 'Approved'
            else:
                send_request_to = '2IC'
                request_status = 'Pending at 2IC'

        elif current_user_role == '2IC':
            send_request_to = 'CO'
            request_status = 'Pending at CO'

        elif current_user_role == 'CO':
            send_request_to = 'Approved'
            request_status = 'Approved'

        # ================= FETCH LEAVE =================
        cursor.execute("""
            SELECT id, army_number, name, leave_type, leave_days,
                   from_date, to_date, leave_reason
            FROM leave_status_info
            WHERE id = %s
        """, (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            conn.rollback()
            return jsonify({"message": "Leave request not found"}), 404

        # ================= UPDATE onleave_status WHEN APPROVED =================
        # if request_status == 'Approved':
        #     cursor.execute("""
        #         UPDATE personnel 
        #         SET onleave_status = 1 
        #         WHERE army_number = %s
        #     """, (leave['army_number'],))

        # ================= UPDATE leave_details TABLE (Single + Combined) =================
        if request_status == 'Approved':
            year = str(datetime.now().year)
            army_number = leave['army_number']

            al = cl = aal = pl = 0
            remarks_text = None

            leave_type_str = (leave['leave_type'] or '').strip().upper()

            if '+' in leave_type_str:
                # Combined Leave - Split using multi_leave_table
                cursor.execute("""
                    SELECT leave_type, leave_days 
                    FROM multi_leave_table 
                    WHERE leave_request_id = %s
                """, (leave_id,))
                multi_leaves = cursor.fetchall()

                for item in multi_leaves:
                    lt = (item['leave_type'] or '').upper()
                    days = int(item['leave_days'] or 0)

                    if lt == 'AL':
                        al += days
                    elif lt == 'CL':
                        cl += days
                    elif lt == 'AAL':
                        aal += days
                    elif lt == 'PL':
                        pl += days
                    else:
                        if remarks_text:
                            remarks_text += f"; {lt}({days})"
                        else:
                            remarks_text = f"{lt}({days})"
            else:
                # Single Leave
                lt = leave_type_str
                days = int(leave['leave_days'] or 0)

                if lt == 'AL':
                    al = days
                elif lt == 'CL':
                    cl = days
                elif lt == 'AAL':
                    aal = days
                elif lt == 'PL':
                    pl = days
                else:
                    remarks_text = f"{lt}: {days} days"

            # Update or Insert into leave_details
            cursor.execute("""
                SELECT AL, CL, AAL, PL FROM leave_details
                WHERE army_number = %s AND year = %s
                FOR UPDATE
            """, (army_number, year))

            existing = cursor.fetchone()

            if existing:
                new_al = (existing['AL'] or 0) + al
                new_cl = (existing['CL'] or 0) + cl
                new_aal = (existing['AAL'] or 0) + aal
                new_pl = (existing['PL'] or 0) + pl

                cursor.execute("""
                    UPDATE leave_details
                    SET AL = %s, CL = %s, AAL = %s, PL = %s,
                        remarks = CONCAT(IFNULL(remarks, ''), %s)
                    WHERE army_number = %s AND year = %s
                """, (
                    new_al, new_cl, new_aal, new_pl,
                    f"; {remarks_text}" if remarks_text else "",
                    army_number, year
                ))
            else:
                cursor.execute("""
                    INSERT INTO leave_details
                    (army_number, year, AL, CL, AAL, PL, remarks, leave_start_date, leave_end_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    army_number, year, al, cl, aal, pl,
                    remarks_text,
                    leave['from_date'],
                    leave['to_date']
                ))

        # ================= INSERT HISTORY =================
        cursor.execute("""
            INSERT INTO leave_history (
                leave_request_id, army_number, name, leave_type,
                from_date, to_date, total_days, recommended_by, 
                remarks, status
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            leave["id"], leave["army_number"], leave["name"], 
            leave["leave_type"], leave["from_date"], leave["to_date"],
            leave["leave_days"], current_user_role, 
            leave["leave_reason"], request_status
        ))

        # ================= UPDATE MAIN TABLE =================
        cursor.execute("""
            UPDATE leave_status_info
            SET request_sent_to = %s,
                request_status = %s,
                recommend_date = NOW(),
                rejected_date = NULL,
                updated_at = NOW()
            WHERE id = %s
        """, (send_request_to, request_status, leave_id))

        conn.commit()

        return jsonify({"message": "Leave recommended successfully"}), 200

    except Exception as e:
        conn.rollback()
        print("ERROR in recommend_leave:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()




@leave_bp.route("/get_recommended_requests")
def get_recommended_requests():
    print("in this recommended route")

    user = require_login()
    recommended_by = user['role']
    user_company = user['company']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = '''
    SELECT
        lh.id,
        lh.leave_request_id,
        lh.army_number,
        lsi.rank,
        lsi.name,
        lsi.company,
        lh.leave_type,
        lsi.leave_days,
        lsi.from_date,
        lsi.to_date,
        lh.status,
        lh.recommended_at
    FROM leave_history lh
    JOIN leave_status_info lsi
        ON lh.leave_request_id = lsi.id
    WHERE lh.recommended_by = %s
'''

    # UNIT 2IC → sees ALL companies
    if recommended_by == '2IC' or recommended_by == 'Subedar Major' or recommended_by == 'CO':
        query += ' ORDER BY lh.recommended_at DESC'
        cursor.execute(query, (recommended_by,))

    # Company-level users → restricted by company
    else:
        query += ' AND lsi.company = %s ORDER BY lh.recommended_at DESC'
        cursor.execute(query, (recommended_by, user_company))

    data = cursor.fetchall()
    print(data,"this is data")

    
    cursor.close()
    conn.close()

    return jsonify({"data": data})


@leave_bp.route("/get_leave_history/<int:id>")
def get_leave_history(id):
    user = require_login()
    recommended_by = user['role']
    print(recommended_by)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                lh.id,
                lh.leave_request_id,
                lsi.name,
                lh.army_number,
                lsi.leave_type,
                lsi.leave_days,
                lsi.prefix_date,
                lsi.suffix_date,
                lsi.from_date,
                lsi.to_date,
                lsi.leave_reason,
                lsi.request_status,
                lh.remarks,
                lh.recommended_at
            FROM leave_history lh
            JOIN leave_status_info lsi
                ON lh.leave_request_id = lsi.id
            WHERE lh.id = %s
              AND lh.recommended_by = %s
        """, (id, recommended_by))

        data = cursor.fetchone()
        print(data, "from history")

        if not data:
            return jsonify({"message": "Record not found"}), 404

        # ================================================
        # HANDLE COMBINED LEAVE - If leave_type has '+'
        # ================================================
        if data.get('leave_type') and '+' in data['leave_type']:
            # Fetch individual leave details from multi_leave_table
            cursor.execute("""
                SELECT 
                    leave_type,
                    leave_days,
                    from_date,
                    to_date
                FROM multi_leave_table 
                WHERE leave_request_id = %s
                ORDER BY id ASC
            """, (data['leave_request_id'],))
            
            multi_details = cursor.fetchall()

            if multi_details:
                # Format leave_type nicely: AL(15) + PL(10)
                formatted = []
                for d in multi_details:
                    formatted.append(f"{d['leave_type']}({d['leave_days']})")
                
                data['leave_type'] = " + ".join(formatted)

                # Add detailed breakdown (very useful for frontend)
                data['leave_details'] = []
                for d in multi_details:
                    leave_item = {
                        "leave_type": d['leave_type'],
                        "leave_days": d['leave_days'],
                        "from_date": d['from_date'].strftime('%Y-%m-%d') if d.get('from_date') else None,
                        "to_date": d['to_date'].strftime('%Y-%m-%d') if d.get('to_date') else None
                    }
                    data['leave_details'].append(leave_item)

        # ================================================
        # DATE FORMATTING
        # ================================================
        if data.get('from_date'):
            data['from_date'] = data['from_date'].strftime('%Y-%m-%d')
        
        if data.get('to_date'):
            data['to_date'] = data['to_date'].strftime('%Y-%m-%d')

        if data.get('prefix_date'):
            data['prefix_date'] = data['prefix_date'].strftime('%Y-%m-%d')
        
        if data.get('suffix_date'):
            data['suffix_date'] = data['suffix_date'].strftime('%Y-%m-%d')

        if data.get('recommended_at'):
            data['recommended_at'] = data['recommended_at'].strftime('%Y-%m-%d %H:%M:%S')

        # ================================================
        # GET RANK AND COMPANY
        # ================================================
        cursor.execute("""
            SELECT `rank`, company 
            FROM personnel 
            WHERE army_number = %s
        """, (data['army_number'],))
        
        result_rank = cursor.fetchone()
        if result_rank:
            data['rank'] = result_rank['rank']
            data['company'] = result_rank['company']

        # ================================================
        # SET LEAVE REQUEST TYPE
        # ================================================
        user_data = {}
        rank = data.get('rank', '')

        if recommended_by == 'OC':
            if rank not in ['Subedar', 'Naib Subedar', 'Subedar Major']:
                user_data['leave_request_type'] = 'OR'
            else:
                user_data['leave_request_type'] = 'OFFICER'
        else:
            user_data['leave_request_type'] = 'OR'

        return jsonify({
            "data": data,
            "user_data": user_data
        })

    except Exception as e:
        print("Error in get_leave_history:", str(e))
        return jsonify({
            "message": "Server error",
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




@leave_bp.route("/reject_leave", methods=["POST"])
def reject_leave():
    data = request.get_json()

    leave_id = data.get("leave_id")
    reason = data.get("reason")
    
    if not leave_id or not reason:
        return jsonify({
            "message": "Leave ID and rejection reason required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user = require_login()
    current_role = user["role"]
    rejected_by = user.get("username", "SYSTEM")

    status_text = f"Rejected at {current_role}"
    now = datetime.now()

    try:
        # 🔹 START TRANSACTION
        conn.start_transaction()

        # 1️⃣ Fetch leave request details (LOCK ROW)
        cursor.execute("""
            SELECT
                id,
                army_number,
                       name,
                leave_type,
                from_date,
                to_date,
                leave_days,
                company
            FROM leave_status_info
            WHERE id = %s
            FOR UPDATE
        """, (leave_id,))

        leave = cursor.fetchone()

        if not leave:
            conn.rollback()
            return jsonify({
                "message": "Leave request not found"
            }), 404

        # 2️⃣ UPDATE leave_status_info
        cursor.execute("""
            UPDATE leave_status_info
            SET
                request_status = %s,
                reject_reason = %s,
                rejected_date = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            status_text,
            reason,
            now,
            now,
            leave_id
        ))

        # 3️⃣ INSERT INTO leave_history (ONLY INSERT)
        cursor.execute("""
            INSERT INTO leave_history (
                leave_request_id,
                army_number,
                name,
                leave_type,
                from_date,
                to_date,
                total_days,
                recommended_by,
                status,
                remarks,
                recommended_at,
                reject_reason,
                company
            )
            VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """, (
            leave["id"],
            leave["army_number"],
            leave['name'],
            leave["leave_type"],
            leave["from_date"],
            leave["to_date"],
            leave["leave_days"],
            rejected_by,          # who rejected
            status_text,
            "Leave rejected",
            now,
            reason,
            leave['company']
        ))

        # 🔹 COMMIT TRANSACTION
        conn.commit()

        return jsonify({
            "message": "Leave rejected successfully"
        }), 200

    except Exception as e:
        conn.rollback()
        print("REJECT ERROR:", e)
        return jsonify({
            "message": "Internal server error"
        }), 500

    finally:
        cursor.close()
        conn.close()


@leave_bp.route("/get_rejected_requests", methods=["GET"])
def get_rejected_requests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()

    company = user['company']
    role = user['role']
    army_number = user['army_number']
    print(army_number,"this is users army number")
    cursor.execute('''
select section from personnel where army_number = %s
''',(army_number,))
    result = cursor.fetchone()
    print("result",result)
    if result:
        section_result = result['section']
        print(section_result,"this is USERS SECTION")
    elif role not in ['2IC','OC','CO','Subedar Major'] and result == None:
        return jsonify({
            "error": 'User not found in personnel table'
        }), 400
    print(role)
    query = """
    SELECT
        l.id,
        l.army_number,
        p.`rank`,
        p.company,
        l.name,
        l.leave_type,
        l.leave_days,
        l.reject_reason,
        l.request_status
    FROM leave_status_info l
    LEFT JOIN personnel p 
        ON l.army_number = p.army_number
    WHERE l.request_status LIKE %s
    """

    try:
        status_pattern = "%Rejected at%"

        # 2IC → can see all companies
        if role in ['OC','2IC','CO','Subedar Major']:
            query += " ORDER BY l.updated_at DESC"
            print("in this query")
            cursor.execute(query, (status_pattern,))

        # Other roles → restricted to their own company
        else:
            query += " AND p.company = %s AND p.section = %s ORDER BY l.updated_at DESC"
            cursor.execute(query, (status_pattern, company,section_result))
        
        data = cursor.fetchall()
        print('data',data)
        return jsonify({
            "data": data
        }), 200

    except Exception as e:
        print("FETCH REJECTED ERROR:", e)
        return jsonify({
            "data": []
        }), 500

    finally:
        cursor.close()
        conn.close()






@leave_bp.route("/undo_rejected_leave", methods=["POST"])
def undo_reject_leave():
    data = request.get_json()
    leave_id = data.get("leave_id")
    print("this is leave id",leave_id)
    if not leave_id:
        return jsonify({"message": "Leave ID missing"}), 400

    user = require_login()
    current_user_role = user['role']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    

    try:
        # 1️⃣ Ensure leave exists & is rejected
        cursor.execute("""
            SELECT id
            FROM leave_status_info
            WHERE id = %s AND request_status like '%Rejected at%'
        """, (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            return jsonify({"message": "Rejected leave not found"}), 404

        # 2️⃣ Build role-based pending status
        send_request_to = current_user_role
        request_status = f"Pending at {current_user_role}"

        # 3️⃣ Undo rejection
        cursor.execute("""
            UPDATE leave_status_info
            SET
                request_sent_to = %s,
                request_status = %s,
                rejected_date = NULL,
                reject_reason = NULL,
                updated_at = NOW()
            WHERE id = %s
        """, (send_request_to, request_status, leave_id))

        conn.commit()

        return jsonify({"message": "Leave moved back to pending"}), 200

    except Exception as e:
        conn.rollback()
        print("UNDO ERROR:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()







@leave_bp.route("/rejected_leaves", methods=["GET"])
def co_rejected_leaves():
    print("in this routed route")
    user = require_login()  # get current logged-in user
    if user['role'] != 'CO':
        return jsonify({"message": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch leaves that were rejected
        cursor.execute("""
            SELECT 
                p.rank,
                lsi.id,
               lsi.army_number,
                p.name,
                lsi.leave_type,
                lsi.leave_days,
                lsi.reject_reason,
                lsi.request_status,
                lsi.updated_at
                    
            FROM leave_status_info as lsi left join personnel as p  on lsi.army_number =   p.army_number
            WHERE lsi.request_status = 'Rejected at OC' OR lsi.request_status = 'Rejected at 2iC'  
            ORDER BY lsi.updated_at DESC
        """)
        leaves = cursor.fetchall()
        print(leaves)
        return jsonify({"data": leaves}), 200

    except Exception as e:
        print("Error fetching CO rejected leaves:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()


# @leave_bp.route("/15CESR_leave_certificate/<army_number>")
@leave_bp.route("/download_certificate/<army_number>")
def download_leave_certificate(army_number):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("in this download route")
        # Fetch main leave data with ALL related information
        cursor.execute("""
            SELECT
                l.id as leave_id,
                l.leave_type,
                l.leave_days,
                l.from_date,
                l.to_date,
                l.prefix_date,
                l.suffix_date,
                l.prefix_days,
                l.suffix_days,
                l.created_at as applied_on,
                l.updated_at as issue_date,
                l.leave_reason,
                l.remarks,
                l.request_status,
                p.name,
                p.army_number,
                p.rank,
                p.company,
                p.section,
                p.trade,
                p.home_house_no,
                p.home_village,
                p.home_phone,
                p.home_to,
                p.home_po,
                p.home_ps,
                p.home_teh,
                p.home_nrs,
                p.home_nmh,
                p.home_district,
                p.home_state,
                m.number AS mobile_number,
                -- Transport information
                lt.transport_id as transport_id,
                lt.onward_mode,
                lt.onward_air_type,
                lt.onward_train_type,
                lt.return_mode,
                lt.return_air_type,
                lt.return_train_type,
                -- Address information
                la.same_as_permanent,
                la.address_line1,
                la.address_line2,
                la.city,
                la.state,
                la.pincode,
                la.mobile as leave_mobile,
                la.alternate_contact
            FROM leave_status_info l
            JOIN personnel p ON p.army_number = l.army_number
            LEFT JOIN mobile_phones m ON m.army_number = l.army_number
            LEFT JOIN leave_transport lt ON lt.leave_request_id = l.id
            LEFT JOIN leave_address la ON la.leave_request_id = l.id
            WHERE l.army_number = %s
              AND l.request_status = 'Approved'
            ORDER BY l.created_at DESC
            LIMIT 1
        """, (army_number,))
        
        data = cursor.fetchone()
        if not data:
            return "No approved leave certificate found for this user.", 404
        
        # ====================== HANDLE COMBINED LEAVE ======================
        leave_type_display = data['leave_type']
        leave_details_list = []
        
        if data['leave_type'] and '+' in data['leave_type']:
            cursor.execute("""
                SELECT leave_type, leave_days, from_date, to_date
                FROM multi_leave_table
                WHERE leave_request_id = %s
                ORDER BY id ASC
            """, (data['leave_id'],))
            multi_leaves = cursor.fetchall()
            
            if multi_leaves:
                formatted_parts = []
                for item in multi_leaves:
                    lt = item['leave_type']
                    days = item['leave_days']
                    formatted_parts.append(f"{lt}({days})")
                    
                    leave_details_list.append({
                        "type": lt,
                        "days": days,
                        "from_date": item['from_date'].strftime('%d-%m-%Y') if item['from_date'] else None,
                        "to_date": item['to_date'].strftime('%d-%m-%Y') if item['to_date'] else None
                    })
                leave_type_display = " + ".join(formatted_parts)
        
        # ====================== FETCH JOURNEY LEGS ======================
        onward_legs = []
        return_legs = []
        
        if data.get('transport_id'):
            cursor.execute("""
                SELECT journey_type, leg_order, from_station, to_station
                FROM leave_journey_legs
                WHERE transport_id = %s
                ORDER BY journey_type, leg_order
            """, (data['transport_id'],))
            
            legs = cursor.fetchall()
            for leg in legs:
                if leg['journey_type'] == 'onward':
                    onward_legs.append({
                        "order": leg['leg_order'],
                        "from": leg['from_station'],
                        "to": leg['to_station']
                    })
                else:
                    return_legs.append({
                        "order": leg['leg_order'],
                        "from": leg['from_station'],
                        "to": leg['to_station']
                    })
        
        # ====================== HANDLE ADDRESS (with permanent address fallback) ======================
        address_during_leave = {}
        
        if data.get('same_as_permanent') == 1 or data.get('same_as_permanent') ==True:
        # if True:
            # Build address from personnel table
            address_parts = []
            print("fixed in the database")
            if data.get('home_house_no'):
                address_parts.append(data['home_house_no'])
            if data.get('home_village'):
                address_parts.append(data['home_village'])
            if data.get('home_to'):
                address_parts.append(data['home_to'])
            if data.get('home_po'):
                address_parts.append(f"PO: {data['home_po']}")
            if data.get('home_ps'):
                address_parts.append(f"PS: {data['home_ps']}")
            if data.get('home_teh'):
                address_parts.append(f"Teh: {data['home_teh']}")
            if data.get('home_district'):
                address_parts.append(f"Dist: {data['home_district']}")
            if data.get('home_state'):
                address_parts.append(data['home_state'])
            if data.get('home_nrs'):
                address_parts.append(f"NRS: {data['home_nrs']}")
            if data.get('home_nmh'):
                address_parts.append(f"NMH: {data['home_nmh']}")
            
            address_during_leave = {
                "full_address": ", ".join(filter(None, address_parts)),
                "is_permanent": True,
                "address_line1": data.get('home_house_no', ''),
                "address_line2": data.get('home_village', ''),
                "city": data.get('home_teh', ''),
                "state": data.get('home_state', ''),
                "pincode": '',  # Not available in personnel table
                "mobile": data.get('leave_mobile') or data.get('mobile_number', 'N/A'),
                "alternate_contact": data.get('alternate_contact', 'N/A')
            }
        else:
            # Use the address provided during leave application
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            address_parts = []
            if data.get('address_line1'):
                address_parts.append(data['address_line1'])
            if data.get('address_line2'):
                address_parts.append(data['address_line2'])
            if data.get('city'):
                address_parts.append(data['city'])
            if data.get('state'):
                address_parts.append(data['state'])
            if data.get('pincode'):
                address_parts.append(f"PIN: {data['pincode']}")
            
            address_during_leave = {
                "full_address": ", ".join(filter(None, address_parts)) or "Address not provided",
                "is_permanent": False,
                "address_line1": data.get('address_line1', ''),
                "address_line2": data.get('address_line2', ''),
                "city": data.get('city', ''),
                "state": data.get('state', ''),
                "pincode": data.get('pincode', ''),
                "mobile": data.get('leave_mobile') or data.get('mobile_number', 'N/A'),
                "alternate_contact": data.get('alternate_contact', 'N/A')
            }
        
        # ====================== FORMAT TRANSPORT INFORMATION ======================
        transport_info = {
            "onward": {
                "mode": data.get('onward_mode', 'Not Specified'),
                "type": None,
                "legs": onward_legs,
                "full_route": " → ".join([f"{leg['from']} to {leg['to']}" for leg in onward_legs]) if onward_legs else "Not specified"
            },
            "return": {
                "mode": data.get('return_mode', 'Not Specified'),
                "type": None,
                "legs": return_legs,
                "full_route": " → ".join([f"{leg['from']} to {leg['to']}" for leg in return_legs]) if return_legs else "Not specified"
            }
        }
        
        # Add specific type details based on mode
        if data.get('onward_mode') == 'Air' and data.get('onward_air_type'):
            transport_info["onward"]["type"] = data['onward_air_type']
        elif data.get('onward_mode') == 'Train' and data.get('onward_train_type'):
            transport_info["onward"]["type"] = data['onward_train_type']
        
        if data.get('return_mode') == 'Air' and data.get('return_air_type'):
            transport_info["return"]["type"] = data['return_air_type']
        elif data.get('return_mode') == 'Train' and data.get('return_train_type'):
            transport_info["return"]["type"] = data['return_train_type']
        
        # ====================== PREPARE CERTIFICATE DATA ======================
        current_year = datetime.now().year
        cert_no = f"LEAVE/{current_year}/{data['leave_id']}"
        
        applicant = {
            "name": data['name'],
            "rank": data['rank'],
            "army_number": data['army_number'],
            "company_name": data['company'],
            "section_name": data['section'] if data['section'] else "HQ",
            "trade": data.get('trade', 'N/A'),
            "contact": data['mobile_number'] if data['mobile_number'] else 'N/A'
        }
        
        leave_info = {
            "certificate_number": cert_no,
            "leave_type": leave_type_display,
            "start_date": data['from_date'],
            "end_date": data['to_date'],
            "total_days": data['leave_days'],
            "issue_date": data['issue_date'] if data['issue_date'] else datetime.now(),
            "applied_on": data['applied_on'],
            "prefix_details": f"{data['prefix_days']} day(s) on {data['prefix_date'].strftime('%d-%m-%Y') if data['prefix_date'] else 'NIL'}",
            "suffix_details": f"{data['suffix_days']} day(s) on {data['suffix_date'].strftime('%d-%m-%Y') if data['suffix_date'] else 'NIL'}",
            "leave_reason": data.get('leave_reason', 'Not specified'),
            "remarks": data.get('remarks', 'N/A'),
            "address_during_leave": address_during_leave,
            "transport": transport_info,
            "reporting_date": (data['suffix_date'] if data['suffix_date'] else data['to_date']).strftime('%d-%m-%Y') if (data['suffix_date'] or data['to_date']) else 'Not specified',
            "leave_details": leave_details_list,
            "request_status": data['request_status']
        }
        
        print(f"Certificate generated for {army_number} with ID: {data['leave_id']}")
        print(leave_info)
        
        # Render template
        html = render_template("certificate.html", applicant=applicant, leave=leave_info)
        
        # Generate PDF
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
        
        if pisa_status.err:
            return "Error generating PDF", 500
        
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"Leave_Certificate_{army_number}_{data['leave_id']}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating certificate: {e}")
        import traceback
        traceback.print_exc()
        return str(e), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()





@leave_bp.route("/get_leave_for_co/<int:leave_id>", methods=["GET"])
def get_leave(leave_id):
    user = require_login()
    if user['role'] != 'CO':
        return jsonify({"message": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, army_number,`rank`, name, leave_type, leave_days, from_date, to_date,
                   prefix_date, suffix_date, prefix_days, suffix_days,
                   leave_reason, reject_reason, request_status
            FROM leave_status_info
            WHERE id = %s
        """, (leave_id,))
        leave = cursor.fetchone()
        if not leave:
            return jsonify({"message": "Leave not found"}), 404

        return jsonify({"data": leave}), 200

    except Exception as e:
        print("Error fetching leave details:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()
@leave_bp.route("/delete_leave/<army_number>", methods=["DELETE"])
def delete_leave(army_number):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete from history first (safer if FK exists)
    cursor.execute(
        "DELETE FROM leave_history WHERE army_number = %s",
        (army_number,)
    )

    cursor.execute(
        "DELETE FROM leave_status_info WHERE army_number = %s",
        (army_number,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

@leave_bp.route('/leave_history/<army_number>')
def full_leave_history(army_number):
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # returns dicts, not tuples
    cursor.execute("SELECT * FROM leave_details WHERE army_number = %s", (army_number,))
    rows   = cursor.fetchall()             # actually fetches the rows
    cursor.close()
    conn.close()
    return jsonify(rows)






@leave_bp.route("/leave-type-stats", methods=["GET"])
def get_leave_type_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    current_company = user['company']

    try:
        query = """
            SELECT leave_type
            FROM leave_status_info
            WHERE request_status = 'Approved' AND company = %s
              AND CURDATE() BETWEEN from_date AND to_date
        """
        cursor.execute(query,(current_company,))
        rows = cursor.fetchall()

        stats = {}

        for row in rows:
            leave_type = row.get("leave_type")

            if not leave_type:
                continue

            leave_type = leave_type.strip().upper()

            # ✅ DO NOT SPLIT — treat as unique type
            if leave_type not in stats:
                stats[leave_type] = 0

            stats[leave_type] += 1

        return jsonify(stats)

    except Exception as e:
        print("Error in leave-type-stats:", e)
        return jsonify({"error": "Failed to fetch stats"}), 500

    finally:
        cursor.close()
        conn.close()


@leave_bp.route("/expiring-soon", methods=["GET"])
def get_expiring_leaves():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    current_company = user['company']
    try:
        query = """
           SELECT 
    lsi.army_number,
    lsi.name,
    p.`rank`,
    DATE(lsi.to_date) AS leave_end_date
FROM leave_status_info lsi
JOIN personnel p
    ON lsi.army_number = p.army_number
WHERE lsi.request_status = 'Approved'
    AND p.company = %s
  AND lsi.to_date IS NOT NULL

  -- ✅ ensure leave is still active today
  AND CURDATE() BETWEEN lsi.from_date AND lsi.to_date

  -- ✅ expiring within next 10 days
  

ORDER BY lsi.to_date ASC;
        """

        cursor.execute(query,(current_company,))
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "army_number": row["army_number"],
                "name": row["name"],
                "rank": row["rank"],
                "leave_end_date": row["leave_end_date"].strftime("%Y-%m-%d")
            })

        return jsonify(result)

    except Exception as e:
        print("Error in expiring-soon:", e)
        return jsonify({"error": "Failed to fetch expiring leaves"}), 500

    finally:
        cursor.close()
        conn.close()




def serialize_dates(rows):
    for r in rows:
        for key, value in r.items():
            if isinstance(value, (datetime, date)):
                r[key] = value.strftime('%d-%m-%Y')  # ✅ only date, no time
    return rows


@leave_bp.route('/api/leaves', methods=['GET'])
def get_leaves():
    try:
        user = require_login()

        if not user or not isinstance(user, dict):
            return jsonify({"error": "Unauthorized"}), 401

        current_company = user['company']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Approved
        cursor.execute("""
            SELECT *
            FROM leave_status_info
            WHERE request_status = 'Approved' AND company = %s
            ORDER BY created_at DESC
        """, (current_company,))
        approved = cursor.fetchall()

        # Pending
        cursor.execute("""
            SELECT *
            FROM leave_status_info
            WHERE request_status LIKE '%Pending%' AND company = %s
            ORDER BY created_at DESC
        """, (current_company,))
        pending = cursor.fetchall()

        cursor.close()
        conn.close()

        # ✅ FIX HERE
        approved = serialize_dates(approved)
        pending  = serialize_dates(pending)

        return jsonify({
            "approved": approved,
            "pending": pending
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Something went wrong"}), 500

