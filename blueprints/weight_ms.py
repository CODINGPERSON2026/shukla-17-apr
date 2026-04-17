from imports import *

weight_ms = Blueprint('weight', __name__, url_prefix='/weight_system')

# --- Helper functions ---
def round_to_nearest_even(n):
    """
    Rounds a number to the nearest even integer.
    """
    rounded = round(n)
    if rounded % 2 != 0:
        if n > rounded:
            rounded += 1
        else:
            rounded -= 1
    return rounded

def get_ideal_weight(age, height_cm, cursor):
    cursor.execute("SELECT age_range, ideal_weight_kg FROM ideal_weights WHERE height_cm = %s", (height_cm,))
    rows = cursor.fetchall()
    for row in rows:
        age_range = row['age_range']
        ideal_weight = row['ideal_weight_kg']
        try:
            lower_age, upper_age = map(int, age_range.split('-'))
            if lower_age <= age <= upper_age:
                return float(ideal_weight)
        except:
            continue
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(age,height_cm)
    return None

def compute_authorization(company=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if company and company != "All":
        cursor.execute("SELECT army_number, name,`rank`,company, age, height, actual_weight,status_type FROM weight_info WHERE company = %s", (company,))
    else:
        cursor.execute("SELECT army_number, name,`rank`, company, age, height, actual_weight,status_type FROM weight_info")
    
    soldiers = cursor.fetchall()
    
    results = []

    for s in soldiers:
        age = s['age']
        height_cm = round_to_nearest_even(s['height'])
        actual_weight = s['actual_weight']
        name = s['name']
        company = s['company']
        army_number = s['army_number']
        rank = s['rank']
        status_type = s['status_type']

        ideal_weight = get_ideal_weight(age, height_cm, cursor)

        if ideal_weight is None:
            print("in this checkout @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            status = "No ideal weight found"
            lower = upper = None
            weight_deviation_percent = None
            weight_deviation_kg = None
        else:
            lower = round(ideal_weight * 0.9, 2)
            upper = round(ideal_weight * 1.1, 2)

            if lower <= actual_weight <= upper:
                status = "Fit"
                weight_deviation_kg = 0
                weight_deviation_percent = 0
            else:
                status = "UnFit"
                if actual_weight < lower:
                    deviation = lower - actual_weight
                    weight_deviation_kg = round(deviation, 1)
                    weight_deviation_percent = round((deviation / lower) * 100, 1)
                else:  # actual_weight > upper
                    
                    deviation = actual_weight - upper
                    weight_deviation_kg = round(deviation, 1)
                    weight_deviation_percent = round((deviation / upper) * 100, 1)
                
        results.append({
            'army_number': army_number,
            "name": name,
            'rank':rank,
            "company": company,
            "age": age,
            "height_cm": height_cm,
            "actual_weight": actual_weight,
            "ideal_weight": ideal_weight,
            "lower_limit": lower,
            "upper_limit": upper,
            "status": status,
            "weight_deviation_percent": weight_deviation_percent,
            "weight_deviation_kg": weight_deviation_kg,
            "status_type" : status_type
        })

    cursor.close()
    connection.close()
    return results
    print("hjhjhjhj")
# --- Validation functions ---
def validate_alpha(value, field_name):
    """Validate that value contains only letters and spaces"""
    if not re.match(r'^[a-zA-Z\s]+$', value):
        return f"{field_name} can only contain letters and spaces"
    return None

def validate_alpha_numeric(value, field_name):
    """Validate that value contains only letters and numbers"""
    if not re.match(r'^[a-zA-Z0-9]+$', value):
        return f"{field_name} can only contain letters and numbers"
    return None

def validate_numeric(value, field_name):
    """Validate that value is a valid number"""
    try:
        float(value)
        return None
    except ValueError:
        return f"{field_name} must be a valid number"

def validate_integer(value, field_name, min_val=None, max_val=None):
    """Validate that value is a valid integer within range"""
    print('this is triggered !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    try:
        int_val = int(value)
        if min_val is not None and int_val < min_val:
            return f"{field_name} must be at least {min_val}"
        if max_val is not None and int_val > max_val:
            return f"{field_name} must be at most {max_val}"
        return None
    except ValueError:
        return f"{field_name} must be a whole number"

 

@weight_ms.route('/api/add-user', methods=['POST'])
def add_user():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract fields
        name = data.get('name', '').strip()
        army_number = data.get('army_number', '').strip()
        age = data.get('age')
        rank = data.get('rank')
        height_cm = data.get('height_cm')
        actual_weight = data.get('actual_weight')
        company = data.get('company', '').strip()
        status_type = data.get('status_type', 'shape').strip()
        category_type = data.get('category_type')  # Can be None
        restrictions = data.get('restrictions')   # Can be None

        # Validate required fields
        required_fields = {
            'name': name,
            'army_number': army_number,
            'age': age,
            'rank': rank,
            'height_cm': height_cm,
            'actual_weight': actual_weight,
            'company': company,
            'status_type': status_type
        }
        
        for field, value in required_fields.items():
            if not value and value != 0:
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400

        # Validate field formats
        validation_errors = []
        
        # Name validation (only letters and spaces)
        name_error = validate_alpha(name, 'Name')
        if name_error:
            validation_errors.append(name_error)
        
        # Army number validation (alphanumeric)
        army_number_error = validate_alpha_numeric(army_number, 'Army number')
        if army_number_error:
            validation_errors.append(army_number_error)
        
        # Age validation (integer between 18 and 60)
        age_error = validate_integer(age, 'Age', 18, 60)
        if age_error:
            validation_errors.append(age_error)
        
        # Height validation (integer between 100 and 250, convert to float for DB)
        height_error = validate_integer(height_cm, 'Height', 100, 250)
        if height_error:
            validation_errors.append(height_error)
        
        # Weight validation (numeric between 30 and 200)
        weight_error = validate_numeric(str(actual_weight), 'Weight')
        if weight_error:
            validation_errors.append(weight_error)
        else:
            weight_val = float(actual_weight)
            if weight_val < 30 or weight_val > 200:
                validation_errors.append('Weight must be between 30kg and 200kg')

        # Validate status_type
        if status_type not in ['shape', 'category']:
            validation_errors.append('Status type must be either "shape" or "category"')

        # Validate category_type and restrictions if status_type is 'category'
        if status_type == 'category':
            if category_type not in ['permanent', 'temporary']:
                validation_errors.append('Category type must be either "permanent" or "temporary"')
            if restrictions is None or not restrictions.strip():
                validation_errors.append('Restrictions are required when status type is "category"')

        if validation_errors:
            return jsonify({'error': '; '.join(validation_errors)}), 400

        # Convert to proper types
        age = int(age)
        height_cm = float(height_cm)
        actual_weight = float(actual_weight)

        # Check if army_number already exists
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT army_number FROM weight_info WHERE army_number = %s", (army_number,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Army number already exists'}), 400

        # Calculate ideal weight using your existing function
        rounded_height = round_to_nearest_even(height_cm)
        ideal_weight = get_ideal_weight(age, rounded_height, cursor)

        if ideal_weight is None:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Could not determine ideal weight for the given age and height'}), 400

        # Calculate limits and status
        lower_limit = round(ideal_weight * 0.9, 2)
        upper_limit = round(ideal_weight * 1.1, 2)

        if lower_limit <= actual_weight <= upper_limit:
            status = "Fit"
            weight_deviation_kg = 0
            weight_deviation_percent = 0
        else:
            status = "UnFit"
            if actual_weight < lower_limit:
                deviation = lower_limit - actual_weight
                weight_deviation_kg = round(deviation, 1)
                weight_deviation_percent = round((deviation / lower_limit) * 100, 1)
            else:
                deviation = actual_weight - upper_limit
                weight_deviation_kg = round(deviation, 1)
                weight_deviation_percent = round((deviation / upper_limit) * 100, 1)

        # Prepare and log the INSERT query
        query = "INSERT INTO weight_info (`name`, `army_number`, `age`, `rank`, `height`, `actual_weight`, `company`, `status_type`, `category_type`, `restrictions`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        
        # Execute with parameterized values
        cursor.execute(query, (name, army_number, age, rank, height_cm, actual_weight, company, status_type, category_type, restrictions))

        connection.commit()
        
        # Get the inserted user's ID
        user_id = cursor.lastrowid
        
        cursor.close()
        connection.close()

        # Return success response
        return jsonify({
            'message': 'User added successfully',
            'user': {
                'id': user_id,
                'name': name,
                'army_number': army_number,
                'age': age,
                'rank': rank,
                'height_cm': height_cm,
                'actual_weight': actual_weight,
                'company': company,
                'status_type': status_type,
                'category_type': category_type,
                'restrictions': restrictions,
                'ideal_weight': ideal_weight,
                'lower_limit': lower_limit,
                'upper_limit': upper_limit,
                'status': status,
                'weight_deviation_kg': weight_deviation_kg,
                'weight_deviation_percent': weight_deviation_percent
            }
        }), 201

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return jsonify({'error': 'Database error occurred'}), 500

@weight_ms.route('/api/summary')
def api_summary():
    auto_save_monthly_unfit()
    company = request.args.get('company', 'All')
    data = compute_authorization(company)
    total = len(data)
    unFit = sum(1 for d in data if d['status'] == "UnFit")
    Fit = sum(1 for d in data if d['status'] == "Fit")
    return jsonify({
        "total": total, 
        "unFit": unFit, 
        "Fit": Fit,
        "company": company
    })

@weight_ms.route('/api/unauthorized')
def api_unFit():
    company = request.args.get('company', 'All')
    data = compute_authorization(company)
    unFit = [d for d in data if d['status'] == "UnFit"]
    return jsonify({"count": len(unFit), "rows": unFit})

@weight_ms.route('/api/authorized')
def api_Fit():
    company = request.args.get('company', 'All')
    data = compute_authorization(company)
    Fit = [d for d in data if d['status'] == "Fit"]
    return jsonify({"count": len(Fit), "rows": Fit})

@weight_ms.route('/api/companies')
def api_companies():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT company FROM weight_info ORDER BY company")
    companies = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    connection.close()
    return jsonify({"companies": companies})

@weight_ms.route('/')
def dashboard():
    user = require_login()
    
    if not user:
        return redirect(url_for('admin_login'))
    return render_template('weight_system/home.html')

@weight_ms.route('/api/status-summary')
def api_status_summary():
    company = request.args.get('company', 'All')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        if company and company != "All":
            cursor.execute("""
                SELECT 
                    status_type,
                    COUNT(*) as count
                FROM weight_info 
                WHERE company = %s
                GROUP BY status_type
            """, (company,))
        else:
            cursor.execute("""
                SELECT 
                    status_type,
                    COUNT(*) as count
                FROM weight_info 
                GROUP BY status_type
            """)
        
        status_counts = cursor.fetchall()
        
        # Initialize counts
        safe_count = 0
        category_count = 0
        
        # Extract counts from query results
        for row in status_counts:
            if row['status_type'] == 'shape':
                safe_count = row['count']
            elif row['status_type'] == 'category':
                category_count = row['count']
        
        return jsonify({
            "safe_count": safe_count,
            "category_count": category_count,
            "company": company
        })
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        cursor.close()
        connection.close()

@weight_ms.route('/api/status-data')
def api_status_data():
    status_type = request.args.get('status_type')
    company = request.args.get('company', 'All')
    #"incoming status status",status_type)
    
    if not status_type:
        return jsonify({'error': 'status_type parameter is required'}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        if company and company != "All":
            cursor.execute("""
                SELECT 
                    army_number, name, company,`rank`, age, height as height_cm, 
                    actual_weight, status_type, category_type, restrictions
                FROM weight_info 
                WHERE status_type = %s AND company = %s
                ORDER BY name
            """, (status_type, company))
        else:
            cursor.execute("""
                SELECT 
                    army_number, name, company,`rank`, age, height as height_cm, 
                    actual_weight, status_type, category_type, restrictions
                FROM weight_info 
                WHERE status_type = %s
                ORDER BY name
            """, (status_type,))
        
        users = cursor.fetchall()
        print(len(users))
        
        # Calculate fitness status for each user
        results = []
        for user in users:
            age = user['age']
            height_cm = round_to_nearest_even(user['height_cm'])
            actual_weight = user['actual_weight']
            
            ideal_weight = get_ideal_weight(age, height_cm, cursor)
            
            if ideal_weight is None:
                status = "No ideal weight found"
                lower = upper = None
                weight_deviation_percent = None
                weight_deviation_kg = None
            else:
                lower = round(ideal_weight * 0.9, 2)
                upper = round(ideal_weight * 1.1, 2)

                if lower <= actual_weight <= upper:
                    status = "Fit"
                    weight_deviation_kg = 0
                    weight_deviation_percent = 0
                else:
                    status = "UnFit"
                    if actual_weight < lower:
                        deviation = lower - actual_weight
                        weight_deviation_kg = round(deviation, 1)
                        weight_deviation_percent = round((deviation / lower) * 100, 1)
                    else:
                        deviation = actual_weight - upper
                        weight_deviation_kg = round(deviation, 1)
                        weight_deviation_percent = round((deviation / upper) * 100, 1)

            results.append({
                'army_number': user['army_number'],
                "name": user['name'],
                "company": user['company'],
                'rank':user['rank'],
                "age": user['age'],
                "height_cm": user['height_cm'],
                "actual_weight": user['actual_weight'],
                "status_type": user['status_type'],
                "category_type": user['category_type'],
                "restrictions": user['restrictions'],
                "ideal_weight": ideal_weight,
                "lower_limit": lower,
                "upper_limit": upper,
                "status": status,
                "weight_deviation_percent": weight_deviation_percent,
                "weight_deviation_kg": weight_deviation_kg
            })
        #results,"these are resutls")
        return jsonify({
            "count": len(results),
            "rows": results,
            "status_type": status_type,
            "company": company
        })
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        cursor.close()
        connection.close()
@weight_ms.route('/api/bar-graph-data')
def api_bar_graph_data():
    company = request.args.get('company', 'All')
    fit_unfit_filter = request.args.get('fitUnfitFilter', 'Fit')
    safe_category_filter = request.args.get('safeCategoryFilter', 'shape')

    print("\n================ API /bar-graph-data =================")
    print("Company:", company)
    print("Fit / Unfit Filter:", fit_unfit_filter)
    print("Safe / Category Filter:", safe_category_filter)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    JCO_RANKS = ("Naib Subedar", "Subedar", "Subedar Major")

    try:
        # ============================================================
        # 1. Fit / Unfit counts
        # ============================================================
        data = compute_authorization(company)
        print("Total authorization records:", len(data))

        fit_count = sum(1 for d in data if d['status'] == "Fit")
        unfit_count = sum(1 for d in data if d['status'] == "UnFit")

        print("Fit count:", fit_count)
        print("UnFit count:", unfit_count)

        # ============================================================
        # 2. JCO / OR counts for selected Fit / UnFit
        # ============================================================
        jco_status_count = sum(
            1 for d in data
            if d['status'] == fit_unfit_filter
            and d['rank'] in JCO_RANKS
        )

        or_status_count = sum(
            1 for d in data
            if d['status'] == fit_unfit_filter
            and d['rank'] not in JCO_RANKS
        )

        print("JCO", fit_unfit_filter, "count:", jco_status_count)
        print("OR", fit_unfit_filter, "count:", or_status_count)

        # ============================================================
        # 3. Total Safe & Category counts
        # ============================================================
        if company != "All":
            cursor.execute("""
                SELECT COUNT(*) AS count
                FROM weight_info
                WHERE company = %s AND status_type = 'shape'
            """, (company,))
        else:
            cursor.execute("""
                SELECT COUNT(*) AS count
                FROM weight_info
                WHERE status_type = 'shape'
            """)

        total_safe_count = cursor.fetchone()['count'] or 0
        print("Total SAFE count:", total_safe_count)

        if company != "All":
            cursor.execute("""
                SELECT COUNT(*) AS count
                FROM weight_info
                WHERE company = %s AND status_type = 'category'
            """, (company,))
        else:
            cursor.execute("""
                SELECT COUNT(*) AS count
                FROM weight_info
                WHERE status_type = 'category'
            """)

        total_category_count = cursor.fetchone()['count'] or 0
        print("Total CATEGORY count:", total_category_count)

        # ============================================================
        # 4. JCO vs OR → Safe / Category
        # ============================================================
        if safe_category_filter == 'shape':
            print("MODE: SHAPE (JCO vs OR)")

            if company != "All":
                cursor.execute("""
                    SELECT `rank`, COUNT(*) AS cnt
                    FROM weight_info
                    WHERE company = %s AND status_type = 'shape'
                    GROUP BY `rank`
                """, (company,))
            else:
                cursor.execute("""
                    SELECT `rank`, COUNT(*) AS cnt
                    FROM weight_info
                    WHERE status_type = 'shape'
                    GROUP BY `rank`
                """)

            rows = cursor.fetchall()
            print("Shape rows:", rows)

            jco_val = sum(
                r['cnt'] for r in rows
                if (r['rank'] or '').strip().lower()
                in [x.lower() for x in JCO_RANKS]
            )

            or_val = sum(
                r['cnt'] for r in rows
                if (r['rank'] or '').strip().lower()
                not in [x.lower() for x in JCO_RANKS]
            )

            print("JCO Safe:", jco_val)
            print("OR Safe:", or_val)

            jcoSafeOrCategory = {
                "labels": ["JCO Shape I", "OR Shape I"],
                "data": [jco_val, or_val]
            }

        else:
            print("MODE: CATEGORY (Temporary / Permanent)")

            query = """
                SELECT `rank`,
                       COALESCE(LOWER(TRIM(category_type)), 'unknown') AS cat_type,
                       COUNT(*) AS cnt
                FROM weight_info
                WHERE status_type = 'category'
            """
            params = []

            if company != "All":
                query += " AND company = %s"
                params.append(company)

            query += " GROUP BY `rank`, category_type"

            print("Executing CATEGORY query:", query)
            print("Params:", params)

            cursor.execute(query, params)
            results = cursor.fetchall()

            print("Category rows:", results)

            jco_temp = jco_perm = or_temp = or_perm = 0

            for row in results:
                rank = row['rank']
                cat_type = row['cat_type']
                cnt = row['cnt']

                is_jco = rank in JCO_RANKS

                print(f"Row → Rank:{rank}, Type:{cat_type}, Count:{cnt}, Is JCO:{is_jco}")

                if cat_type in ('temporary', 'temp'):
                    if is_jco:
                        jco_temp += cnt
                    else:
                        or_temp += cnt

                elif cat_type in ('permanent', 'perm'):
                    if is_jco:
                        jco_perm += cnt
                    else:
                        or_perm += cnt

            print("FINAL COUNTS →",
                  "JCO Temp:", jco_temp,
                  "JCO Perm:", jco_perm,
                  "OR Temp:", or_temp,
                  "OR Perm:", or_perm)

            jcoSafeOrCategory = {
                "labels": [
                    "JCO Temporary", "JCO Permanent",
                    "OR Temporary", "OR Permanent"
                ],
                "data": [jco_temp, jco_perm, or_temp, or_perm]
            }

        print("FINAL jcoSafeOrCategory:", jcoSafeOrCategory)

        # ============================================================
        # RESPONSE
        # ============================================================
        return jsonify({
            "fitUnfit": {
                "labels": ["Fit", "Unfit"],
                "data": [fit_count, unfit_count]
            },
            "safeCategory": {
                "labels": ["Shape 1", "Category"],
                "data": [total_safe_count, total_category_count]
            },
            "jcoOrFit": {
                "labels": [f"JCO {fit_unfit_filter}", f"OR {fit_unfit_filter}"],
                "data": [jco_status_count, or_status_count]
            },
            "jcoSafeOrCategory": jcoSafeOrCategory
        })

    except mysql.connector.Error as err:
        print("❌ DB Error:", err)
        return jsonify({'error': 'Database error occurred'}), 500

    finally:
        cursor.close()
        connection.close()


@weight_ms.route('/api/unfit-graph')
def unfit_graph():
    company = request.args.get('company', 'ALL')

    cursor = get_db_connection().cursor(dictionary=True)
    cursor.execute("""
        SELECT month, unfit_count
        FROM monthly_medical_status
        WHERE year = YEAR(CURDATE())
          AND unit = %s
        ORDER BY month
    """, (company,))

    return jsonify(cursor.fetchall())

COMPANIES = [
    "All",
    "1 Company",
    "2 Company",
    "3 Company",
    "HQ company"
]

def auto_save_monthly_unfit():
    now = datetime.now()
    year = now.year
    month = now.month
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    for company in COMPANIES:
        # Check if already saved
        cursor.execute("""
            SELECT id FROM monthly_medical_status
            WHERE year=%s AND month=%s AND unit=%s
        """, (year, month, company))

        if cursor.fetchone():
            continue

        # Compute official count
        data = compute_authorization(company)
        unFit = sum(1 for d in data if d['status'] == "UnFit")
        print("THIS IS UNFIT COUNT",unFit)

        cursor.execute("""
            INSERT INTO monthly_medical_status (year, month, unit, unfit_count)
            VALUES (%s, %s, %s, %s)
        """, (year, month, company, unFit))

def _to_json_serializable(val):
    """Convert DB values (e.g. Decimal) to JSON-serializable Python types."""
    if val is None:
        return None
    if hasattr(val, '__float__') and not isinstance(val, bool):
        try:
            return float(val)
        except (TypeError, ValueError):
            pass
    if hasattr(val, '__int__') and not isinstance(val, bool):
        try:
            return int(val)
        except (TypeError, ValueError):
            pass
    if isinstance(val, (str, bool)):
        return val
    return str(val)


@weight_ms.route('/api/person-details/<army_number>')
def api_person_details(army_number):
    """Get detailed information about a specific person for View button / API."""
    request.args.get('status_class', '')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT 
                army_number, name, company, `rank`, age, height as height_cm, 
                actual_weight, status_type, category_type, restrictions
            FROM weight_info 
            WHERE army_number = %s
        """, (army_number,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Person not found'}), 404
        
        age = _to_json_serializable(user['age']) or 0
        height_raw = user['height_cm']
        height_cm = round_to_nearest_even(height_raw) if height_raw is not None else None
        actual_weight = _to_json_serializable(user['actual_weight'])
        if actual_weight is not None:
            actual_weight = float(actual_weight)
        
        ideal_weight = get_ideal_weight(age, height_cm, cursor) if height_cm else None
        if ideal_weight is not None:
            ideal_weight = float(ideal_weight)
        
        if ideal_weight is None:
            status = "No ideal weight found"
            lower = upper = None
            weight_deviation_percent = None
            weight_deviation_kg = None
        else:
            lower = round(ideal_weight * 0.9, 2)
            upper = round(ideal_weight * 1.1, 2)
            if lower <= actual_weight <= upper:
                status = "Fit"
                weight_deviation_kg = 0
                weight_deviation_percent = 0
            else:
                status = "UnFit"
                if actual_weight < lower:
                    deviation = lower - actual_weight
                    weight_deviation_kg = round(deviation, 1)
                    weight_deviation_percent = round((deviation / lower) * 100, 1)
                else:
                    deviation = actual_weight - upper
                    weight_deviation_kg = round(deviation, 1)
                    weight_deviation_percent = round((deviation / upper) * 100, 1)
        
        result = {
            'army_number': str(user['army_number']) if user['army_number'] is not None else '',
            'name': str(user['name']) if user['name'] is not None else '',
            'company': str(user['company']) if user['company'] is not None else '',
            'rank': str(user['rank']) if user['rank'] is not None else '',
            'age': _to_json_serializable(user['age']),
            'height_cm': _to_json_serializable(user['height_cm']),
            'actual_weight': actual_weight,
            'status_type': str(user['status_type']) if user['status_type'] is not None else '',
            'category_type': str(user['category_type']) if user['category_type'] is not None else None,
            'restrictions': str(user['restrictions']) if user['restrictions'] is not None else None,
            'ideal_weight': ideal_weight,
            'lower_limit': lower,
            'upper_limit': upper,
            'status': status,
            'weight_deviation_percent': weight_deviation_percent,
            'weight_deviation_kg': weight_deviation_kg
        }
        
        return jsonify(result)
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        cursor.close()
        connection.close()

    