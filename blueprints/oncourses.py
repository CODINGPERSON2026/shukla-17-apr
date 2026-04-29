from imports import *

oncourses_bp = Blueprint('oncourses_bp', __name__, url_prefix='/oncourses')

@oncourses_bp.route('/add_on_course', methods=['POST'])
def add_on_course():
    data = request.get_json()

    army_number = data.get('army_number')
    course_name = data.get('course_name')
    institute_name = data.get('institute_name')
    course_starting_date = data.get('course_starting_date')
    course_end_date = data.get('course_end_date')
    course_status =  data.get('course_status')
    if not all([army_number, course_name, institute_name, course_starting_date, course_end_date]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            INSERT INTO candidate_on_courses (
                army_number,
                course_starting_date,
                course_end_date,
                course_name,
                institute_name,
                course_status
            ) VALUES (%s, %s, %s, %s, %s,%s)
        """
        cursor.execute(query, (
            army_number,
            course_starting_date,
            course_end_date,
            course_name,
            institute_name,
            course_status
        ))
        conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Error adding on course: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@oncourses_bp.route('/manage_course')
def manage_course():
    token = request.cookies.get('token')
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    
    return render_template('manage_course.html',
                           role=payload['role'],
                           current_user_name=payload['username'],
                           today=date.today().isoformat())

@oncourses_bp.route('/get_courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT
                coc.id,
                coc.army_number,
                p.name,
                p.rank,
                p.company,
                coc.course_name,
                coc.institute_name,
                coc.course_starting_date,
                coc.course_end_date
            FROM candidate_on_courses coc
            LEFT JOIN personnel p ON coc.army_number = p.army_number
            WHERE coc.status = 'Active'
            ORDER BY coc.course_starting_date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        courses = []
        for row in rows:
            courses.append({
                "id": row[0],
                "army_number": row[1],
                "name": row[2] or "Unknown",
                "rank": row[3] or "—",
                "company": row[4] or "—",
                "course_name": row[5] or "—",
                "institute_name": row[6] or "—",
                "course_starting_date": str(row[7]) if row[7] else "—",
                "course_end_date": str(row[8]) if row[8] else "—"
            })

        return jsonify({"status": "success", "data": courses}), 200

    except Exception as e:
        print(f"Error fetching courses: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@oncourses_bp.route('/remove_from_course/<int:course_id>', methods=['DELETE'])
def remove_from_course(course_id):
    """
    Removes a candidate from course by deleting the record in candidate_on_courses.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM candidate_on_courses WHERE id = %s", (course_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Record not found"}), 404

        return jsonify({"status": "success", "message": "Removed from course"}), 200

    except Exception as e:
        conn.rollback()
        print(f"Error removing from course: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()




@oncourses_bp.route('/get_reserved_courses', methods=['GET'])
def get_reserved_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT
                coc.id,
                coc.army_number,
                p.name,
                p.`rank`,
                p.company,
                coc.course_name,
                coc.institute_name,
                coc.course_starting_date,
                coc.course_end_date,
                coc.course_status
            FROM candidate_on_courses coc
            LEFT JOIN personnel p ON coc.army_number = p.army_number
            WHERE coc.course_status IN ('Reserved', 'Confirmed')
              AND coc.status IN ('Active', 'Upcoming')          -- Added as per your request
            ORDER BY coc.course_name ASC, 
                     coc.course_starting_date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        from collections import defaultdict

        courses = defaultdict(lambda: {
            "course_name": "",
            "institute_name": "",
            "course_starting_date": "",
            "course_end_date": "",
            "reserved_count": 0,
            "confirmed_count": 0,
            "candidates": []
        })

        for row in rows:
            key = row['course_name']
            
            # Initialize course details only once
            if not courses[key]['course_name']:
                courses[key].update({
                    "course_name": row['course_name'] or "Unknown Course",
                    "institute_name": row['institute_name'] or "—",
                    "course_starting_date": str(row['course_starting_date']) if row['course_starting_date'] else "—",
                    "course_end_date": str(row['course_end_date']) if row['course_end_date'] else "—",
                })

            courses[key]['candidates'].append({
                "id": row['id'],
                "army_number": row['army_number'],
                "name": row['name'] or "Unknown",
                "rank": row['rank'] or "—",
                "company": row['company'] or "—",
                "course_status": row['course_status']
            })

            if row['course_status'] == 'Reserved':
                courses[key]['reserved_count'] += 1
            else:
                courses[key]['confirmed_count'] += 1

        return jsonify({
            "status": "success", 
            "data": list(courses.values())
        }), 200

    except Exception as e:
        print(f"Error fetching reserved courses: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@oncourses_bp.route('/validate_army_number', methods=['GET'])
def validate_army_number():
    army_number = request.args.get('army_number')
    if not army_number:
        return jsonify({"status": "error", "message": "Army number required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT name, `rank`
            FROM personnel 
            WHERE army_number = %s
        """, (army_number,))
        
        personnel = cursor.fetchone()
        
        if personnel:
            return jsonify({
                "status": "success",
                "exists": True,
                "name": personnel['name'],
                "rank": personnel['rank']
            }), 200
        else:
            return jsonify({
                "status": "success",
                "exists": False
            }), 200
    except Exception as e:
        print(f"Error validating army number: {e}")
        return jsonify({"status": "error", "message": "Database error"}), 500
    finally:
        cursor.close()
        conn.close()


@oncourses_bp.route('/get_upcoming_courses', methods=['GET'])
def get_upcoming_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT
                coc.id,
                coc.army_number,
                p.name,
                p.`rank`,
                p.company,
                coc.course_name,
                coc.institute_name,
                coc.course_starting_date,
                coc.course_end_date,
                coc.course_status
            FROM candidate_on_courses coc
            LEFT JOIN personnel p ON coc.army_number = p.army_number
            WHERE coc.status = 'Upcoming'
            ORDER BY coc.course_name ASC, coc.course_starting_date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        from collections import defaultdict
        courses = defaultdict(lambda: {
            "course_name": "",
            "institute_name": "",
            "course_starting_date": "",
            "course_end_date": "",
            "reserved_count": 0,
            "confirmed_count": 0,
            "candidates": []
        })

        for row in rows:
            key = row['course_name']
            if not courses[key]['course_name']:
                courses[key].update({
                    "course_name": row['course_name'] or "Unknown Course",
                    "institute_name": row['institute_name'] or "—",
                    "course_starting_date": str(row['course_starting_date']) if row['course_starting_date'] else "—",
                    "course_end_date": str(row['course_end_date']) if row['course_end_date'] else "—",
                })

            courses[key]['candidates'].append({
                "id": row['id'],
                "army_number": row['army_number'],
                "name": row['name'] or "Unknown",
                "rank": row['rank'] or "—",
                "company": row['company'] or "—",
                "course_status": row['course_status']
            })

            if row['course_status'] == 'Reserved':
                courses[key]['reserved_count'] += 1
            elif row['course_status'] == 'Confirmed':
                courses[key]['confirmed_count'] += 1

        return jsonify({"status": "success", "data": list(courses.values())}), 200

    except Exception as e:
        print(f"Error fetching upcoming courses: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@oncourses_bp.route('/confirm_course/<int:course_id>', methods=['PATCH'])
def confirm_course(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE candidate_on_courses SET course_status = 'Confirmed' WHERE id = %s AND course_status = 'Reserved'",
            (course_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Record not found or already confirmed"}), 404
        return jsonify({"status": "success", "message": "Course confirmed"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Error confirming course: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()