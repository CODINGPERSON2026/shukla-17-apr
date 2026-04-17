from imports import *


inteview_bp = Blueprint('inteview_bp',__name__,url_prefix='/interview_update')


@inteview_bp.route('/pending_interview_list')
def get_pending_kunba_interviews():
    user = require_login()
    user_company = user['company'].strip()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('select home_state from personnel where army_number = %s',(user['army_number'],))
    result = cursor.fetchone()
    
    if not result:
        cursor.close()
        return jsonify([])

    home_state = result['home_state']

    print(f"JCO Pending Interview Debug: User={user['username']}, Role={user['role']}, Company='{user_company}', Home State='{home_state}'")

    print(f"DEBUG JCO Filter: Start. UserCompany='{user_company}', HomeState='{home_state}'")

    # STRICT FILTERING TEST - Case-insensitive and trimmed
    cursor.execute("""
      SELECT id, army_number, `rank`, name, home_state, company
      FROM personnel
      WHERE interview_status = 0
        AND LOWER(TRIM(home_state)) = LOWER(TRIM(%s))
        AND LOWER(TRIM(company)) = LOWER(TRIM(%s))
        AND `rank` NOT IN ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major');
    """,(home_state, user_company))
    data = cursor.fetchall()
    
    cursor.close()
    return jsonify(data)


@inteview_bp.route('/update_interview_status', methods=['POST'])
def complete_kunba_interview():
    data = request.json
    personnel_id = data['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personnel
        SET interview_status = 1
        WHERE id = %s
    """, (personnel_id,))
    conn.commit()
    cursor.close()

    return jsonify({"success": True})




@inteview_bp.route('/completed_interview_list', methods=['GET'])
def completed_interview_list():
    
    user = require_login()
    user_company = user['company'].strip()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Get User's Home State
        cursor.execute('SELECT home_state FROM personnel WHERE army_number = %s', (user['army_number'],))
        result = cursor.fetchone()
        
        if not result:
            return jsonify([])

        home_state = result['home_state']

        # 2. Filter Completed Interviews by State, Company, and Non-JCO Rank
        query = """
            SELECT
                id,
                army_number,
                `rank`,
                name,
                home_state,
                updated_at AS completed_on
            FROM personnel
            WHERE interview_status = 1
              AND LOWER(TRIM(home_state)) = LOWER(TRIM(%s))
              AND LOWER(TRIM(company)) = LOWER(TRIM(%s))
              AND `rank` NOT IN ('Naib Subedar', 'Subedar', 'Sub Maj', 'Subedar Major')
            ORDER BY updated_at DESC
        """
        cursor.execute(query, (home_state, user_company))
        rows = cursor.fetchall()

        return jsonify(rows)

    except Exception as e:
        print("Completed Interview List Error:", e)
        return jsonify([])

    finally:
        if cursor:
            cursor.close()
            conn.close()



@inteview_bp.route('/jco-availabilty')
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

        # 1️⃣ Pending interviews (unchanged)
        cursor.execute(f"""
            SELECT name, army_number, home_state, company, `rank`
            FROM personnel
            WHERE interview_status = 0
              AND `rank` NOT IN ({rank_placeholders})
            ORDER BY home_state, name
        """, (*excluded_ranks,))

        pending_data = cursor.fetchall()

        # 2️⃣ Collect unique home_states (unchanged)
        home_states = list({
            row['home_state']
            for row in pending_data
            if row['home_state']
        })

        jco_map = {}          # key = (home_state, company)
        assigned_jco_map = {} # assigned (Pending) JCOs (unchanged)

        if home_states:
            placeholders = ",".join(["%s"] * len(home_states))

            # 3️⃣ Live eligible JCOs — now fetching company too
            cursor.execute(f"""
                SELECT name, home_state, `rank`, company
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
                jco_company = jco['company']
                key = (state, jco_company)          # ← keyed by both
                if key not in jco_map:
                    jco_map[key] = jco['name']       # most senior per state+company

            # 4️⃣ Assigned JCOs (Pending) — unchanged
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

        # 5️⃣ Attach JCO with fallback logic — company-aware lookup
        for row in pending_data:
            state = row['home_state']
            soldier_company = row['company']
            key = (state, soldier_company)           # ← match soldier's company

            if key in jco_map:
                row['jco_name'] = jco_map[key]
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


@inteview_bp.route('/get-available-jcos')
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


@inteview_bp.route('/assign_jco', methods=['POST'])
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




#  <div class="theme-tile" data-theme="dark">
#                 <i class="fas fa-check-circle active-check"></i>
#                 <div class="theme-swatch" style="background: linear-gradient(135deg, #0f172a, #1e293b);">
#                   <i class="fas fa-moon" style="color:#cbd5f5"></i>
#                 </div>
#                 <span class="theme-tile-name">Dark</span>
#               </div>






# @media (min-width: 1600px) {
#   .stats-grid {
#     grid-template-columns: repeat(8, 1fr);
#   }
# }

# /* Large laptops */
# @media (max-width: 1400px) {
#   .stats-grid {
#     grid-template-columns: repeat(6, 1fr);
#   }
# }

# /* Normal laptops */
# @media (max-width: 1200px) {
#   .stats-grid {
#     grid-template-columns: repeat(5, 1fr);
#   }
# }

# /* Tablets */
# @media (max-width: 992px) {
#   .stats-grid {
#     grid-template-columns: repeat(4, 1fr);
#   }
# }

# /* Mobile */
# @media (max-width: 576px) {
#   .stats-grid {
#     grid-template-columns: repeat(2, 1fr);
#   }
# }