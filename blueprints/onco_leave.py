from imports import *
from db_config import get_db_connection

onco_leave_bp = Blueprint('onco_leave', __name__, url_prefix='/onco')


def require_onco():
    """Return the current user dict if role is ONCO, else return None."""
    user = require_login()
    if not user or user.get('role') != 'ONCO':
        return None
    return user

@onco_leave_bp.route('/manage_leave', methods=['GET'])
def manage_leave():
    user = require_onco()
    if not user:
        return "403 Forbidden – Only ONCO role can access this page.", 403
    return render_template('manage_leave.html')

@onco_leave_bp.route('/api/on_leave_persons', methods=['GET'])
def on_leave_persons():
    user = require_onco()
    if not user:
        return jsonify({'status': 'error', 'message': 'Unauthorized. ONCO role required.'}), 403

    company = user.get('company')
    if not company:
        return jsonify({'status': 'error', 'message': 'Company not found in session.'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.army_number,
                p.name,
                p.rank,
                p.company,
                l.leave_type,
                l.from_date,
                l.to_date,
                l.leave_days,
                l.id AS leave_id
            FROM personnel p
            JOIN leave_status_info l ON p.army_number = l.army_number
            WHERE p.onleave_status = 1
              AND p.company = %s
              AND l.request_status = 'Approved'
            ORDER BY l.from_date DESC
        """, (company,))

        rows = cursor.fetchall()

        for row in rows:
            if row.get('from_date'):
                row['from_date'] = str(row['from_date'])
            if row.get('to_date'):
                row['to_date'] = str(row['to_date'])

        return jsonify({'status': 'success', 'data': rows})

    except Exception as e:
        print("Error fetching on-leave persons:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@onco_leave_bp.route('/remove_leave', methods=['POST'])
def remove_leave():
    user = require_onco()
    if not user:
        return jsonify({'status': 'error', 'message': 'Unauthorized. ONCO role required.'}), 403

    data = request.get_json()
    army_number = data.get('army_number')

    if not army_number:
        return jsonify({'status': 'error', 'message': 'Army number is required.'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE personnel
            SET onleave_status = 0
            WHERE army_number = %s
        """, (army_number,))
        cursor.execute("""
        Update leave_status_info
                    set request_status  = 'Leave Closed' where army_number = %s""",(army_number,)) 
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': 'Personnel not found.'}), 404

        return jsonify({'status': 'success', 'message': f'Personnel {army_number} removed from leave successfully.'})

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error removing leave:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@onco_leave_bp.route('/extend_leave', methods=['POST'])
def extend_leave():
    user = require_onco()
    if not user:
        return jsonify({'status': 'error', 'message': 'Unauthorized. ONCO role required.'}), 403

    data = request.get_json()
    army_number      = data.get('army_number')
    new_to_date_str  = data.get('new_to_date')
    leave_type       = data.get('leave_type')

    # ── Validate inputs ───────────────────────────────────────────
    if not army_number or not new_to_date_str:
        return jsonify({'status': 'error', 'message': 'army_number and new_to_date are required.'}), 400

    VALID_LEAVE_TYPES = {'AL', 'CL', 'AAL', 'PL'}
    if not leave_type or leave_type not in VALID_LEAVE_TYPES:
        return jsonify({'status': 'error', 'message': 'A valid leave_type (AL/CL/AAL/PL) is required.'}), 400

    conn   = None
    cursor = None
    try:
        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ── 1. Fetch current approved leave record ────────────────
        cursor.execute("""
            SELECT id, from_date, to_date, request_status
            FROM leave_status_info
            WHERE army_number = %s
              AND request_status = 'Approved'
            ORDER BY from_date DESC
            LIMIT 1
        """, (army_number,))
        leave = cursor.fetchone()

        if not leave:
            return jsonify({'status': 'error', 'message': 'No approved leave record found for this personnel.'}), 404

        from_date   = leave['from_date']
        old_to_date = leave['to_date']
        new_to_date = datetime.strptime(new_to_date_str, '%Y-%m-%d').date()

        if new_to_date <= from_date:
            return jsonify({'status': 'error', 'message': 'New to_date must be after from_date.'}), 400

        if new_to_date <= old_to_date:
            return jsonify({'status': 'error', 'message': 'New to_date must be after the current end date.'}), 400

        # ── 2. Calculate days ─────────────────────────────────────
        total_leave_days = (new_to_date - from_date).days + 1
        extended_days    = (new_to_date - old_to_date).days

        # ── 3. Update leave_status_info ───────────────────────────
        cursor.execute("""
            UPDATE leave_status_info
            SET to_date    = %s,
                leave_days = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (new_to_date_str, total_leave_days, leave['id']))

        # ── 4. Update leave_details ───────────────────────────────
        current_year = str(new_to_date.year)

        cursor.execute(f"""
            UPDATE leave_details
            SET `{leave_type}`  = COALESCE(`{leave_type}`, 0) + %s,
                leave_end_date  = %s
            WHERE army_number = %s
              AND year = %s
        """, (extended_days, new_to_date_str, army_number, current_year))

        # If no row exists for this year, insert one
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO leave_details
                    (army_number, year, AL, CL, AAL, PL, leave_end_date, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Created on leave extension')
            """, (
                army_number,
                current_year,
                extended_days if leave_type == 'AL'  else 0,
                extended_days if leave_type == 'CL'  else 0,
                extended_days if leave_type == 'AAL' else 0,
                extended_days if leave_type == 'PL'  else 0,
                new_to_date_str,
            ))

        conn.commit()

        return jsonify({
            'status':        'success',
            'message':       f'Leave extended by {extended_days} day(s) under {leave_type}. Total duration: {total_leave_days} days.',
            'new_to_date':   new_to_date_str,
            'leave_days':    total_leave_days,
            'extended_days': extended_days,
            'leave_type':    leave_type,
        })

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error extending leave:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn:   conn.close()