from imports import *
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
agniveer_bp = Blueprint("agniveer_bp", __name__, url_prefix="/agni")

@agniveer_bp.route('/get_batches', methods=['GET'])
def get_batches():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True ,buffered=True)
        cursor.execute("SELECT DISTINCT batch FROM personnel WHERE batch IS NOT NULL ORDER BY batch ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([row['batch'] for row in rows])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@agniveer_bp.route('/api/assistant-test', methods=['POST'])
def save_assistant_test():
    try:
        data = request.json
        batchSelected = data.get('batch')

        if not batchSelected:
            return jsonify({'success': False, 'error': 'Batch is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True,buffered=True)

        # 🔹 Check if batch already exists in assistant_test
        cursor.execute("SELECT id FROM assistant_test WHERE batch = %s", (batchSelected,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Assistant test already initialized for this batch'}), 400
        # 🔹 Get DOE and TOS
        # 🔹 Get DOE and TOS
        cursor.execute(
            "SELECT date_of_enrollment, date_of_tos FROM personnel WHERE batch = %s LIMIT 1",
            (batchSelected,)
        )
        result = cursor.fetchone()






        if not result:
            return jsonify({'success': False, 'error': 'Batch not found'}), 404

        DOE = result['date_of_enrollment']
        TOS = result['date_of_tos']

        # 🔹 Auto calculations
        asst_test1 = DOE + relativedelta(months=12)
        asst_test2 = DOE + relativedelta(months=18)
        asst_test3 = DOE + relativedelta(months=30)
        asst_test4 = DOE + relativedelta(months=42)

        TOE = DOE + relativedelta(years=4)
        END_OF_TENURE = TOS + relativedelta(months=20)
        from_date = DOE + relativedelta(months=42)
        to_date   = DOE + relativedelta(months=45)
        screening_board = f"{from_date.strftime('%m/%y')} to {to_date.strftime('%m/%y')}"




        # 🔹 Insert
        sql = """
        INSERT INTO assistant_test
        (batch, asst_test1, asst_test2, asst_test3, asst_test4,
         test1_status, test2_status, test3_status, test4_status,
         DOE, TOE, TOS, END_OF_TENURE)
        VALUES (%s,%s,%s,%s,%s,0,0,0,0,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            batchSelected,
            asst_test1,
            asst_test2,
            asst_test3,
            asst_test4,
            DOE,
            TOE,
            TOS,
            END_OF_TENURE
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Assistant test dates auto-generated successfully'
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500









@agniveer_bp.route('/get_all_agniveers', methods=['GET'])
def get_all_agniveers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = """
    SELECT 
        a.*,
        
        a.remarks,

        IFNULL(p.strength, 0) AS strength
    FROM assistant_test a
    LEFT JOIN (
        SELECT batch, COUNT(*) AS strength
        FROM personnel
        GROUP BY batch
    ) p ON p.batch = a.batch
   
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert dates to string format and compute dynamic fields
    for row in rows:
        for key, value in row.items():
            if hasattr(value, "strftime"):
                row[key] = value.strftime('%Y-%m-%d')

        # 🔹 Compute "Assmt completed on / or such wef" dynamically
        # For 4 sub-columns (1st Yr, 2nd Yr, 3rd Yr, 4th Yr)
        row["assmt_wef_1st"] = row.get("emergency_test1")
        row["assmt_wef_2nd"] = row.get("emergency_test2")
        row["assmt_wef_3rd"] = row.get("emergency_test3")
        row["assmt_wef_4th"] = row.get("emergency_test4")

        # 🔹 Fill Screening Board if blank
        if not row.get("screening_board"):
            DOE = row.get("DOE")
            if DOE:
                # If DOE is already a string from the strftime loop above
                DOE_date = datetime.strptime(DOE, "%Y-%m-%d")
                from_date = DOE_date + relativedelta(months=42)
                to_date   = DOE_date + relativedelta(months=45)
                row["screening_board"] = f"{from_date.strftime('%m/%y')} to {to_date.strftime('%m/%y')}"

    cursor.close()
    conn.close()
    return jsonify(rows)

@agniveer_bp.route('/delete-assistant-data', methods=['POST'])
def delete_assistant_data():
    """
    Delete emergency test data and/or remarks for a specific batch
    """
    try:
        data = request.json
        batch = data.get('batch')
        test_no = data.get('test_no')  # 1, 2, 3, or 4
        del_type = data.get('del_type')  # emergency_date, emergency_type, both, remarks, all
        
        if not batch or not test_no or not del_type:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Build column names based on test number
        emergency_date_col = f'emergency_test{test_no}'
        emergency_type_col = f'emergency_test{test_no}_type'
        
        # Prepare UPDATE query based on deletion type
        if del_type == 'emergency_date':
            query = f"""
                UPDATE assistant_test 
                SET {emergency_date_col} = NULL 
                WHERE batch = %s
            """
        elif del_type == 'emergency_type':
            query = f"""
                UPDATE assistant_test 
                SET {emergency_type_col} = NULL 
                WHERE batch = %s
            """
        elif del_type == 'both':
            query = f"""
                UPDATE assistant_test 
                SET {emergency_date_col} = NULL, 
                    {emergency_type_col} = NULL 
                WHERE batch = %s
            """
        elif del_type == 'remarks':
            query = """
                UPDATE assistant_test 
                SET remarks = NULL 
                WHERE batch = %s
            """
        elif del_type == 'all':
            query = f"""
                UPDATE assistant_test 
                SET {emergency_date_col} = NULL, 
                    {emergency_type_col} = NULL,
                    remarks = NULL 
                WHERE batch = %s
            """
        else:
            return jsonify({'success': False, 'error': 'Invalid deletion type'}), 400
        
        # Execute the query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (batch,))
        conn.commit()
        cursor.close()
        
        return jsonify({
            'success': True, 
            'message': f'Successfully deleted {del_type} for batch {batch}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



    




@agniveer_bp.route("/update-assistant", methods=["POST"])
def update_assistant():
    data = request.get_json()

    batch = data.get("batch")
    test_no = data.get("test_no")
    status = data.get("status")
    emergency_type = data.get("emergency_type")
    new_date = data.get("new_date")
    remarks = data.get("remarks")

    if not batch or not test_no or status not in (0, 1):
        return jsonify({"success": False, "error": "Invalid input"}), 400

    if not remarks or remarks.strip() == "":
        remarks = "No Remarks"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        column_name = f"test{test_no}_status"
        test_label = f"TEST-{test_no}"

        sql_status = f"""
           UPDATE assistant_test
SET {column_name} = %s,
    remarks = CASE
        WHEN remarks IS NULL
             OR remarks = 'No Remarks'
             OR TRIM(remarks) = ''
        THEN CONCAT(%s, ' : ', %s)
        ELSE CONCAT(remarks, ' | ', %s, ' : ', %s)
    END
WHERE batch = %s

        """

        cursor.execute(
            sql_status,
            (status, test_label, remarks, test_label, remarks, batch)
        )

        if emergency_type in ("prepone", "postpone") and new_date:
            date_column = f"emergency_test{test_no}"
            type_column = f"emergency_test{test_no}_type"

            sql_emergency = f"""
                UPDATE assistant_test
                SET {date_column} = %s,
                    {type_column} = %s
                WHERE batch = %s
            """
            cursor.execute(sql_emergency, (new_date, emergency_type, batch))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("Error updating assistant:", e)
        return jsonify({"success": False, "error": "Server error"}), 500

@agniveer_bp.route('/api/upcomming_test_alarms', methods=['GET'])
def upcoming_test_alarms():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Get all assistant test records
        query = """
        SELECT 
            batch, 
            asst_test1, asst_test2, asst_test3, asst_test4,
            test1_status, test2_status, test3_status, test4_status,
            emergency_test1, emergency_test2, emergency_test3, emergency_test4
        FROM assistant_test
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        upcoming_tests = []
        today = date.today()
        # Look ahead 30 days for alarms
        alarm_window = today + timedelta(days=30)
        
        for row in rows:
            # Check each of the 4 tests
            for i in range(1, 5):
                status_key = f"test{i}_status"
                # If test is already completed (status 1), skip it
                if row.get(status_key) == 1:
                    continue
                
                # Use emergency date if available, otherwise original scheduled date
                sched_date = row.get(f"emergency_test{i}") or row.get(f"asst_test{i}")
                
                if sched_date:
                    # If sched_date is a string, convert to date object
                    if isinstance(sched_date, str):
                        try:
                            sched_date = datetime.strptime(sched_date, '%Y-%m-%d').date()
                        except ValueError:
                            continue
                    
                    # If it's within our window (today to 30 days from now)
                    if today <= sched_date <= alarm_window:
                        upcoming_tests.append({
                            "batch": row['batch'],
                            "test_no": i,
                            "test_name": f"Assistant Test {i}",
                            "test_date": sched_date.strftime('%Y-%m-%d'),
                            "days_left": (sched_date - today).days
                        })
        
        cursor.close()
        conn.close()
        
        return jsonify({"rows": upcoming_tests})
        
    except Exception as e:
        print("Error fetching upcoming alarms:", e)
        return jsonify({"success": False, "error": str(e)}), 500
