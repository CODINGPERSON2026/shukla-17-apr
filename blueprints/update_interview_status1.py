from imports import *


inteview_bp = Blueprint('inteview_bp',__name__,url_prefix='/inteview_update')


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
