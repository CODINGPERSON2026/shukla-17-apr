from imports import *
from middleware import require_login
import datetime

personnel_info = Blueprint('personal', __name__, url_prefix='/personnel_information')

# Dashboard route
@personnel_info.route('/')
def dashboard():
    user = require_login()
    print(user)
    if not user:
        return redirect(url_for('admin_login'))
    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
   
    cursor = connection.cursor(dictionary=True)
   
    try:
        # Get recent personnel (last 5)
        cursor.execute("""
            SELECT name, army_number, `rank`, date_of_enrollment
            FROM personnel
            ORDER BY id DESC
            LIMIT 5
        """)
        recent_personnel = cursor.fetchall()
        print('telli hereerajsdfjdklfj ')
        return render_template('/personnel_info/dashboard.html',
                       
                             recent_personnel=recent_personnel,
                             active_tab='dashboard')
   
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        connection.close()

def insert_sports_data(cursor, personnel_id, army_number, data):
    """Insert sports data into personnel_sports table"""
   
    sports_list = data.get('sports', [])
    for sport in sports_list:
        cursor.execute("""
            INSERT INTO personnel_sports (personnel_id, army_number, sport_type, sport_name)
            VALUES (%s, %s, %s, %s)
        """, (
            personnel_id,
            army_number,
            sport,
            sport
        ))
   
    other_sports = data.get('otherSports', '')
    if other_sports:
        additional_sports = [sport.strip() for sport in other_sports.split(',') if sport.strip()]
        for sport in additional_sports:
            cursor.execute("""
                INSERT INTO personnel_sports (personnel_id, army_number, sport_type, sport_name)
                VALUES (%s, %s, %s, %s)
            """, (
                personnel_id,
                army_number,
                'Other',
                sport
            ))

def insert_dynamic_data(cursor, personnel_id, army_number, data):
    """Insert dynamic data into related tables"""
    
    # Insert courses
    for idx, course in enumerate(data.get('courses', []), 1):
        if any(course.values()):
            cursor.execute("""
                INSERT INTO courses (personnel_id, army_number, sr_no, course, from_date, to_date, institute, grading, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                course.get('course', ''),
                course.get('courseFrom', None),
                course.get('courseTo', None),
                course.get('courseInstitute', ''),
                course.get('courseGrading', ''),
                course.get('courseRemarks', '')
            ))
    
    # Insert units
    for idx, unit in enumerate(data.get('units', []), 1):
        if any(unit.values()):
            cursor.execute("""
                INSERT INTO units_served (personnel_id, army_number, sr_no, unit, from_date, to_date, duty_performed)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                unit.get('unit', ''),
                unit.get('unitFrom', None),
                unit.get('unitTo', None),
                unit.get('unitDuty', '')
            ))
    
    # Insert loans
    for idx, loan in enumerate(data.get('loans', []), 1):
        if any(loan.values()):
            cursor.execute("""
                INSERT INTO loans (personnel_id, army_number, sr_no, loan_type, total_amount, bank_details, emi_per_month, pending, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                loan.get('loanType', ''),
                float(loan.get('loanAmount', 0)) if loan.get('loanAmount') else None,
                loan.get('loanBank', ''),
                float(loan.get('loanEMI', 0)) if loan.get('loanEMI') else None,
                float(loan.get('loanPending', 0)) if loan.get('loanPending') else None,
                loan.get('loanRemarks', '')
            ))
    
    # Insert punishments
    for idx, punishment in enumerate(data.get('punishments', []), 1):
        if any(punishment.values()):
            cursor.execute("""
                INSERT INTO punishments (personnel_id, army_number, sr_no, punishment_date, punishment, aa_sec, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                punishment.get('punishmentDate', None),
                punishment.get('punishment', ''),
                punishment.get('punishmentAASec', ''),
                punishment.get('punishmentRemarks', '')
            ))
    
    # Insert detailed courses
    for idx, detailed in enumerate(data.get('detailedCourses', []), 1):
        if any(detailed.values()):
            cursor.execute("""
                INSERT INTO detailed_courses (personnel_id, army_number, sr_no, course_name, from_date, to_date, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                detailed.get('detailedCourseName', ''),
                detailed.get('detailedCourseFrom', None),
                detailed.get('detailedCourseTo', None),
                detailed.get('detailedCourseRemarks', '')
            ))
    
    # Insert leaves
    for idx, leave in enumerate(data.get('leaves', []), 1):
        if any(leave.values()):
            cursor.execute("""
                INSERT INTO leave_details (personnel_id, army_number, sr_no, year, al_days, cl_days, aal_days, total_days, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                leave.get('leaveYear', ''),
                int(leave.get('leaveAL', 0)) if leave.get('leaveAL') else None,
                int(leave.get('leaveCL', 0)) if leave.get('leaveCL') else None,
                int(leave.get('leaveAAL', 0)) if leave.get('leaveAAL') else None,
                int(leave.get('leaveTotal', 0)) if leave.get('leaveTotal') else None,
                leave.get('leaveRemarks', '')
            ))
    
    # Insert family members
    for idx, family in enumerate(data.get('family', []), 1):
        if any(family.values()):
            cursor.execute("""
                INSERT INTO family_members (personnel_id, army_number, relation, name, date_of_birth, uid_no, part_ii_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number,
                family.get('familyRelation', ''),
                family.get('familyName', ''),
                family.get('familyDOB', None),
                family.get('familyUID', ''),
                family.get('familyPartII', '')
            ))
    
    # Insert children
    for idx, child in enumerate(data.get('children', []), 1):
        if any(child.values()):
            cursor.execute("""
                INSERT INTO children (personnel_id, army_number, sr_no, name, date_of_birth, class, part_ii_order, uid_no)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                child.get('childName', ''),
                child.get('childDOB', None),
                child.get('childClass', ''),
                child.get('childPartII', ''),
                child.get('childUID', '')
            ))
    
    # Insert mobiles
    for idx, mobile in enumerate(data.get('mobiles', []), 1):
        if any(mobile.values()):
            cursor.execute("""
                INSERT INTO mobile_phones (personnel_id, army_number, sr_no, type, number, service_provider, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                mobile.get('mobileType', ''),
                mobile.get('mobileNumber', ''),
                mobile.get('mobileProvider', ''),
                mobile.get('mobileRemarks', '')
            ))
    
    # Insert discord cases
    for idx, discord in enumerate(data.get('discordCases', []), 1):
        if any(discord.values()):
            cursor.execute("""
                INSERT INTO marital_discord_cases (personnel_id, army_number, sr_no, case_no, amount_to_pay, sanction_letter_no)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                discord.get('discordCaseNo', ''),
                float(discord.get('discordAmount', 0)) if discord.get('discordAmount') else None,
                discord.get('discordSanction', '')
            ))
    
    # Insert sports data
    insert_sports_data(cursor, personnel_id, army_number, data)

def delete_related_records(cursor, personnel_id, army_number):
    """Delete all related records for a personnel before updating/deleting"""
    tables = [
        'courses', 'units_served', 'loans', 'punishments',
        'detailed_courses', 'leave_details', 'family_members',
        'children', 'mobile_phones', 'marital_discord_cases',
        'personnel_sports'
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table} WHERE personnel_id = %s", (personnel_id,))
    cursor.execute("DELETE FROM weight_info WHERE army_number = %s", (army_number,))
@personnel_info.route('/get_total_personnel_count_and_courses')
def total_army_personnel__and_courses():
    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # TOTAL PERSONNEL
        if company == "Admin" or company == 'Center':
            cursor.execute("SELECT COUNT(*) as total FROM personnel")
        else:
            cursor.execute(
                "SELECT COUNT(*) as total FROM personnel WHERE company = %s",
                (company,)
            )

        total_personnel = cursor.fetchone()['total']


        # TOTAL COURSES
        if company == "Admin" or company == 'Center':
            cursor.execute("SELECT COUNT(*) as count FROM courses")
        else:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM courses c
                JOIN personnel p ON c.personnel_id = p.id
                WHERE p.company = %s
            """, (company,))

        total_courses = cursor.fetchone()['count']

        return jsonify({
            "total_army_personnel": total_personnel,
            "total_courses": total_courses
        }), 200

    except Exception as e:
        print('Server error', str(e))
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# View Data route - Lists personnel with med_cat = 'Yes'
@personnel_info.route('/personnel')
def view_personnel():

    user = require_login()
    company = user['company']

    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
   
    cursor = connection.cursor(dictionary=True)
   
    try:

        # TOTAL MEDICAL CASES
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM personnel
                WHERE med_cat = 'Yes'
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM personnel
                WHERE med_cat = 'Yes'
                AND company = %s
            """, (company,))

        total_medical = cursor.fetchone()['total']


        # COMPANY DISTRIBUTION
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT company, COUNT(*) as count
                FROM personnel
                WHERE med_cat = 'Yes'
                GROUP BY company
                ORDER BY company
            """)
        else:
            cursor.execute("""
                SELECT company, COUNT(*) as count
                FROM personnel
                WHERE med_cat = 'Yes'
                AND company = %s
                GROUP BY company
                ORDER BY company
            """, (company,))

        company_distribution = cursor.fetchall()


        # MEDICAL PERSONNEL LIST
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT id, name, army_number, date_of_birth, `rank`,
                       trade, date_of_enrollment, med_cat, company
                FROM personnel
                WHERE med_cat = 'Yes'
                ORDER BY company, id DESC
            """)
        else:
            cursor.execute("""
                SELECT id, name, army_number, date_of_birth, `rank`,
                       trade, date_of_enrollment, med_cat, company
                FROM personnel
                WHERE med_cat = 'Yes'
                AND company = %s
                ORDER BY company, id DESC
            """, (company,))

        medical_personnel = cursor.fetchall()

        print(f'this is total medical category {total_medical}')

        return render_template(
            '/personnel_info/personnel.html',
            total_medical=total_medical,
            medical_personnel=medical_personnel,
            company_distribution=company_distribution,
            active_tab='view-data'
        )

    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500

    finally:
        cursor.close()
        connection.close()  
@personnel_info.route('/get_medical_category_count', methods=['GET'])
def get_total_medical_category_count():

    user = require_login()
    company = user['company']

    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor(dictionary=True)

        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT COUNT(*) AS total_count
                FROM personnel
                WHERE med_cat = %s
            """, ('Yes',))
        else:
            cursor.execute("""
                SELECT COUNT(*) AS total_count
                FROM personnel
                WHERE med_cat = %s
                AND company = %s
            """, ('Yes', company))

        result = cursor.fetchone()
        total_count = result['total_count'] if result else 0

        print("this is total medical count", total_count)

        return jsonify({'total_medical_category_count': total_count}), 200

    except Exception as e:
        print("Error fetching total medical category count:", e)
        return jsonify({'error': 'Internal Server Error'}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@personnel_info.route('/rank_based_bar_graph_')
def rank_graph():
    print("in this rank based bar graph")

    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get rank distribution
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT `rank`, COUNT(*) as count
                FROM personnel
                GROUP BY `rank`
                ORDER BY count DESC
                LIMIT 10
            """)
        else:
            cursor.execute("""
                SELECT `rank`, COUNT(*) as count
                FROM personnel
                WHERE company = %s
                GROUP BY `rank`
                ORDER BY count DESC
                LIMIT 10
            """, (company,))

        rank_distribution = cursor.fetchall()
        print(rank_distribution)

        return jsonify({'rank_distribution': rank_distribution}), 200

    except Exception as e:
        print('Internal server error', str(e))
        return jsonify({'message': "internal server error"}), 500

    finally:
        cursor.close()
        connection.close()

@personnel_info.route('/age_bar_graph')
def age_graph():
    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # TOTAL PERSONNEL
        if company == "Admin" or company == 'Center':
            cursor.execute("SELECT COUNT(*) as total FROM personnel")
        else:
            cursor.execute(
                "SELECT COUNT(*) as total FROM personnel WHERE company = %s",
                (company,)
            )

        total_personnel = cursor.fetchone()['total']

        # AGE DISTRIBUTION
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT
                    CASE
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 18 AND 24 THEN '18-24'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 25 AND 30 THEN '25-30'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 31 AND 35 THEN '31-35'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 36 AND 40 THEN '36-40'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 40 AND 50 THEN '40-50'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 50 AND 60 THEN '50-60'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) > 60 THEN '60+'
                        ELSE 'Unknown'
                    END as age_range,
                    COUNT(*) as count
                FROM personnel
                WHERE date_of_birth IS NOT NULL
                GROUP BY age_range
                ORDER BY age_range
            """)
        else:
            cursor.execute("""
                SELECT
                    CASE
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 18 AND 24 THEN '18-24'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 25 AND 30 THEN '25-30'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 31 AND 35 THEN '31-35'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 36 AND 40 THEN '36-40'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 40 AND 50 THEN '40-50'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 50 AND 60 THEN '50-60'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) > 60 THEN '60+'
                        ELSE 'Unknown'
                    END as age_range,
                    COUNT(*) as count
                FROM personnel
                WHERE date_of_birth IS NOT NULL AND company = %s
                GROUP BY age_range
                ORDER BY age_range
            """, (company,))

        age_data = cursor.fetchall()

        age_distribution = []
        for row in age_data:
            percentage = round((row['count'] / total_personnel * 100), 1) if total_personnel > 0 else 0
            age_distribution.append({
                'range': row['age_range'],
                'count': row['count'],
                'percentage': percentage
            })

        print(age_distribution)

        return jsonify({'age_distribution': age_distribution}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# API endpoint to get medical personnel details
@personnel_info.route('/api/medical-personnel')
def api_medical_personnel():

    user = require_login()
    company = user['company']

    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
   
    cursor = connection.cursor(dictionary=True)
   
    try:

        # TOTAL MEDICAL CASES
        if company == "Admin" or company == 'Center':
            cursor.execute("SELECT COUNT(*) as total FROM personnel WHERE med_cat = 'Yes'")
        else:
            cursor.execute(
                "SELECT COUNT(*) as total FROM personnel WHERE med_cat = 'Yes' AND company = %s",
                (company,)
            )

        total_medical = cursor.fetchone()['total']


        # COMPANY DISTRIBUTION
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT company, COUNT(*) as count
                FROM personnel
                WHERE med_cat = 'Yes'
                GROUP BY company
                ORDER BY company
            """)
        else:
            cursor.execute("""
                SELECT company, COUNT(*) as count
                FROM personnel
                WHERE med_cat = 'Yes'
                AND company = %s
                GROUP BY company
                ORDER BY company
            """, (company,))

        company_distribution = cursor.fetchall()


        # MEDICAL PERSONNEL LIST
        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT id, name, army_number, `rank`, trade, date_of_enrollment, med_cat, company
                FROM personnel
                WHERE med_cat = 'Yes'
                ORDER BY id DESC
            """)
        else:
            cursor.execute("""
                SELECT id, name, army_number, `rank`, trade, date_of_enrollment, med_cat, company
                FROM personnel
                WHERE med_cat = 'Yes'
                AND company = %s
                ORDER BY id DESC
            """, (company,))

        medical_personnel = cursor.fetchall()
       
        # Convert date objects to strings
        for person in medical_personnel:
            if person['date_of_enrollment']:
                person['date_of_enrollment'] = person['date_of_enrollment'].strftime('%Y-%m-%d')
       
        return jsonify({
            'success': True,
            'total_medical': total_medical,
            'company_distribution': company_distribution,
            'medical_personnel': medical_personnel
        })
   
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        connection.close()
# Personnel Details route
@personnel_info.route('/personnel/<int:personnel_id>')
def personnel_details(personnel_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
   
    cursor = connection.cursor(dictionary=True)
   
    try:
        # Get main personnel details
        cursor.execute("""
            SELECT * FROM personnel WHERE id = %s
        """, (personnel_id,))
        personnel = cursor.fetchone()
       
        if not personnel:
            return "Personnel not found", 404
       
        # Fetch related data
        cursor.execute("""
            SELECT * FROM courses WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        courses = cursor.fetchall()
       
        cursor.execute("""
            SELECT * FROM family_members WHERE personnel_id = %s
        """, (personnel_id,))
        family = cursor.fetchall()
       
        cursor.execute("""
            SELECT * FROM children WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        children = cursor.fetchall()
       
        return render_template('personnel_details.html',
                             personnel=personnel,
                             courses=courses,
                             family=family,
                             children=children,
                             active_tab='view-data')
   
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        connection.close()

# Add personnel page route
@personnel_info.route('/add-personnel')
def add_personnel_page():
   
    return render_template('/personnel_info/index.html', active_tab='add-personnel')

# API endpoint for creating personnel
@personnel_info.route('/api/personnel', methods=['POST'])
def create_personnel():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    cursor = connection.cursor()
    
    try:
        data = request.get_json()
        army_number = data.get('armyNumber', '')
        print("armynumber is ",army_number)
        print("Received data:", data)
        cursor.execute("SELECT id FROM personnel WHERE army_number = %s", (army_number,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Army number already exists'}), 409
        
        
       
        def get_value(key, default=None):
            value = data.get(key, default)
            return None if value == '' else value
       
        def get_date(key):
            value = data.get(key)
            return value if value and value != '' else None
       
        def get_float(key):
            value = data.get(key)
            try:
                return float(value) if value and value != '' else None
            except (ValueError, TypeError):
                return None
       
        def get_int(key):
            value = data.get(key)
            try:
                return int(value) if value and value != '' else None
            except (ValueError, TypeError):
                return None

        # Insert into personnel table (unchanged)
        personnel_query = """
        INSERT INTO personnel (
            name, army_number, `rank`, trade, date_of_enrollment, date_of_birth, date_of_tos, date_of_tors,
            blood_group, religion, food_preference, drinker, company, civ_qualifications, decoration_awards,
            lacking_qualifications, willing_promotions, i_card_no, i_card_date, i_card_issued_by,
            bpet_grading, ppt_grading, bpet_date, clothing_card, pan_card_no, pan_part_ii,
            aadhar_card_no, aadhar_part_ii, joint_account_no, joint_account_bank, joint_account_ifsc,
            home_house_no, home_village, home_phone, home_to, home_po, home_ps, home_teh,
            home_nrs, home_nmh, home_district, home_state, border_area, distance_from_ib,
            height, weight, chest, identification_marks, court_cases, loan, total_leaves_encashed,
            participation_activities, present_family_location, prior_station, prior_station_date,
            worked_it, worked_unit_tenure, med_cat, last_recat_bd_date, last_recat_bd_at,
            next_recat_due, medical_problem, restrictions, computer_knowledge, it_literature,
            kin_name, kin_relation, kin_marriage_date, kin_account_no, kin_bank, kin_ifsc,
            kin_part_ii, vehicle_reg_no, vehicle_model, vehicle_purchase_date, vehicle_agif,
            driving_license_no, license_issue_date, license_expiry_date, disability_child,
            marital_discord, counselling, folder_prepared_on, folder_checked_by, bring_family,
            domestic_issues, other_requests, family_medical_issues, quality_points, strengths,
            weaknesses, detailed_course,batch,section
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s
        )
        """
       
        personnel_values = (
            get_value('name'),
            get_value('armyNumber'),
            get_value('rank'),
            get_value('trade'),
            get_date('dateOfEnrollment'),
            get_date('dateOfBirth'),
            get_date('dateOfTOS'),
            get_date('dateOfTORS'),
            get_value('bloodGroup'),
            get_value('religion'),
            get_value('foodPreference'),
            get_value('drinker'),
            get_value('company'),
            get_value('civQualifications'),
            get_value('decorationAwards'),
            get_value('lackingQualifications'),
            get_value('willingPromotions'),
            get_value('iCardNo'),
            get_date('iCardDate'),
            get_value('iCardIssuedBy'),
            get_value('bpetGrading'),
            get_value('pptGrading'),
            get_date('bpetDate'),
            get_value('clothingCard'),
            get_value('panCardNo'),
            get_value('panPartII'),
            get_value('aadharCardNo'),
            get_value('aadharPartII'),
            get_value('jointAccountNo'),
            get_value('jointAccountBank'),
            get_value('jointAccountIFSC'),
            get_value('homeHouseNo'),
            get_value('homeVillage'),
            get_value('homePhone'),
            get_value('homeTO'),
            get_value('homePO'),
            get_value('homePS'),
            get_value('homeTeh'),
            get_value('homeNRS'),
            get_value('homeNMH'),
            get_value('homeDistrict'),
            get_value('homeState'),
            get_value('borderArea'),
            get_float('distanceFromIB'),
            get_float('height'),
            get_float('weight'),
            get_float('chest'),
            get_value('identificationMarks'),
            get_value('courtCases'),
            get_value('loan'),
            get_int('totalLeavesEncashed'),
            get_value('participationActivities'),
            get_value('presentFamilyLocation'),
            get_value('priorStation'),
            get_date('priorStationDate'),
            get_value('workedIT'),
            get_value('workedUnitTenure'),
            get_value('medCat'),
            get_date('lastRecatBDDate'),
            get_value('lastRecatBDAt'),
            get_date('nextRecatDue'),
            get_value('medicalProblem'),
            get_value('restrictions'),  # Note: This is saved in personnel, but weight_info has its own restrictions field
            get_value('computerKnowledge'),
            get_value('itLiterature'),
            get_value('kinName'),
            get_value('kinRelation'),
            get_date('kinMarriageDate'),
            get_value('kinAccountNo'),
            get_value('kinBank'),
            get_value('kinIFSC'),
            get_value('kinPartII'),
            get_value('vehicleRegNo'),
            get_value('vehicleModel'),
            get_date('vehiclePurchaseDate'),
            get_value('vehicleAGIF'),
            get_value('drivingLicenseNo'),
            get_date('licenseIssueDate'),
            get_date('licenseExpiryDate'),
            get_value('disabilityChild'),
            get_value('maritalDiscord'),
            get_value('counselling'),
            get_date('folderPreparedOn'),
            get_value('folderCheckedBy'),
            get_value('bringFamily'),
            get_value('domesticIssues'),
            get_value('otherRequests'),
            get_value('familyMedicalIssues'),
            get_value('qualityPoints'),
            get_value('strengths'),
            get_value('weaknesses'),
            get_value('detailedCourse'),
            get_value('batch'),
            get_value('section')
        )

        cursor.execute(personnel_query, personnel_values)
        personnel_id = cursor.lastrowid
        army_number = data.get('armyNumber', '')

        insert_dynamic_data(cursor, personnel_id, army_number, data)

        # NEW/UPDATED: Insert into weight_info with section status (shape/category), permanent/temporary (if category), and restrictions
        # Skip if core fields missing
        if not army_number or not get_value('name'):
            print("Skipping weight_info insert: Missing core fields")
        else:
            date_of_birth_str = get_date('dateOfBirth')
            age = None
            if date_of_birth_str:
                dob = datetime.datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
                today = datetime.date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            status_type = get_value('physicalStatus', 'shape')  # 'shape' or 'category'
            category_type = get_value('categoryType') if status_type == 'category' else None  # 'permanent' or 'temporary' if category
            restrictions = get_value('physicalRestrictions')  # Always save

            weight_query = """
            INSERT INTO weight_info (name, army_number, age, `rank`, height, actual_weight, company, status_type, category_type, restrictions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            weight_values = (
                get_value('name'),
                army_number,
                age,
                get_value('rank'),
                get_float('height'),
                get_float('weight'),
                get_value('company'),
                status_type,
                category_type,
                restrictions
            )
            cursor.execute(weight_query, weight_values)

        connection.commit()
        return jsonify({'success': True, 'personnel_id': personnel_id}), 201
    except Error as e:
        connection.rollback()
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        print(f"General error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
   
@personnel_info.route('/sports_distribution_chart')
def sports_distribution_chart():
    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT
                    sport_name,
                    COUNT(*) as count
                FROM personnel_sports
                GROUP BY sport_name
                ORDER BY count DESC
            """)
        else:
            cursor.execute("""
                SELECT
                    ps.sport_name,
                    COUNT(*) as count
                FROM personnel_sports ps
                JOIN personnel p ON ps.personnel_id = p.id
                WHERE p.company = %s
                GROUP BY ps.sport_name
                ORDER BY count DESC
            """, (company,))

        result = cursor.fetchall()

        sports_distribution = []
        for row in result:
            sports_distribution.append({
                'sport': row['sport_name'],
                'count': row['count']
            })

        return jsonify({'sports_distribution': sports_distribution}), 200

    except Exception as e:
        print(f"Error in sports distribution chart: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()
@personnel_info.route('/api/test', methods=['GET'])
def test_connection():
    connection = get_db_connection()
    if connection:
        connection.close()
        return jsonify({'success': True, 'message': 'Database connected'})
    return jsonify({'success': False, 'message': 'Connection failed'})

# API endpoint to get all personnel data
@personnel_info.route('/api/all-personnel')
def api_all_personnel():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
   
    cursor = connection.cursor(dictionary=True)
   
    try:
        # Get list of all personnel
        cursor.execute("""
            SELECT id, name, army_number, `rank`, trade, date_of_enrollment, med_cat, company
            FROM personnel
            ORDER BY company, name
        """)
        all_personnel = cursor.fetchall()
       
        # Convert date objects to strings for JSON serialization
        for person in all_personnel:
            if person['date_of_enrollment']:
                person['date_of_enrollment'] = person['date_of_enrollment'].strftime('%Y-%m-%d')
            # Ensure med_cat has a value
            if person['med_cat'] is None:
                person['med_cat'] = 'No'
       
        return jsonify({
            'success': True,
            'personnel': all_personnel
        })
   
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@personnel_info.route('/state_wise')
def religion_chart():
    print('in this route')

    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT home_state, COUNT(home_state) AS home_state_count
                FROM personnel
                GROUP BY home_state
            """)
        else:
            cursor.execute("""
                SELECT home_state, COUNT(home_state) AS home_state_count
                FROM personnel
                WHERE company = %s
                GROUP BY home_state
            """, (company,))

        result = cursor.fetchall()

        print(result)
        return jsonify({'data': result}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# Add these new routes to your personnel_info.py

@personnel_info.route('/years_in_service_chart')
def years_in_service_chart():
    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT
                    CASE
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 0 AND 5 THEN '0-5 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 5 AND 15 THEN '5-15 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 15 AND 25 THEN '15-25 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 25 AND 35 THEN '25-35 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 35 AND 45 THEN '35-45 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 45 AND 50 THEN '45-50 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 50 AND 64 THEN '50-64 Years'
                        ELSE 'Unknown'
                    END as service_range,
                    COUNT(*) as count
                FROM personnel
                WHERE date_of_enrollment IS NOT NULL
                GROUP BY service_range
                ORDER BY
                    CASE service_range
                        WHEN '0-5 Years' THEN 1
                        WHEN '5-15 Years' THEN 2
                        WHEN '15-25 Years' THEN 3
                        WHEN '25-35 Years' THEN 4
                        WHEN '35-45 Years' THEN 5
                        WHEN '45-50 Years' THEN 6
                        WHEN '50-64 Years' THEN 7
                        ELSE 8
                    END
            """)
        else:
            cursor.execute("""
                SELECT
                    CASE
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 0 AND 5 THEN '0-5 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 5 AND 15 THEN '5-15 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 15 AND 25 THEN '15-25 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 25 AND 35 THEN '25-35 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 35 AND 45 THEN '35-45 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 45 AND 50 THEN '45-50 Years'
                        WHEN TIMESTAMPDIFF(YEAR, date_of_enrollment, CURDATE()) BETWEEN 50 AND 64 THEN '50-64 Years'
                        ELSE 'Unknown'
                    END as service_range,
                    COUNT(*) as count
                FROM personnel
                WHERE date_of_enrollment IS NOT NULL
                AND company = %s
                GROUP BY service_range
                ORDER BY
                    CASE service_range
                        WHEN '0-5 Years' THEN 1
                        WHEN '5-15 Years' THEN 2
                        WHEN '15-25 Years' THEN 3
                        WHEN '25-35 Years' THEN 4
                        WHEN '35-45 Years' THEN 5
                        WHEN '45-50 Years' THEN 6
                        WHEN '50-64 Years' THEN 7
                        ELSE 8
                    END
            """, (company,))

        result = cursor.fetchall()

        service_distribution = []
        for row in result:
            service_distribution.append({
                'range': row['service_range'],
                'count': row['count']
            })

        return jsonify({'service_distribution': service_distribution}), 200

    except Exception as e:
        print(f"Error in years in service chart: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()
@personnel_info.route('/loan_amounts_chart')
def loan_amounts_chart():
    user = require_login()
    company = user['company']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        if company == "Admin" or company == 'Center':
            cursor.execute("""
                SELECT
                    CASE
                        WHEN total_amount BETWEEN 0 AND 500000 THEN '0-5 Lakhs'
                        WHEN total_amount BETWEEN 500001 AND 1000000 THEN '5-10 Lakhs'
                        WHEN total_amount BETWEEN 1000001 AND 1500000 THEN '10-15 Lakhs'
                        WHEN total_amount BETWEEN 1500001 AND 2000000 THEN '15-20 Lakhs'
                        WHEN total_amount > 2000000 THEN '>20 Lakhs'
                        ELSE 'Unknown'
                    END as loan_range,
                    COUNT(*) as count
                FROM loans
                WHERE total_amount IS NOT NULL
                GROUP BY loan_range
                ORDER BY
                    CASE loan_range
                        WHEN '0-5 Lakhs' THEN 1
                        WHEN '5-10 Lakhs' THEN 2
                        WHEN '10-15 Lakhs' THEN 3
                        WHEN '15-20 Lakhs' THEN 4
                        WHEN '>20 Lakhs' THEN 5
                        ELSE 6
                    END
            """)
        else:
            cursor.execute("""
                SELECT
                    CASE
                        WHEN l.total_amount BETWEEN 0 AND 500000 THEN '0-5 Lakhs'
                        WHEN l.total_amount BETWEEN 500001 AND 1000000 THEN '5-10 Lakhs'
                        WHEN l.total_amount BETWEEN 1000001 AND 1500000 THEN '10-15 Lakhs'
                        WHEN l.total_amount BETWEEN 1500001 AND 2000000 THEN '15-20 Lakhs'
                        WHEN l.total_amount > 2000000 THEN '>20 Lakhs'
                        ELSE 'Unknown'
                    END as loan_range,
                    COUNT(*) as count
                FROM loans l
                JOIN personnel p ON l.personnel_id = p.id
                WHERE l.total_amount IS NOT NULL
                AND p.company = %s
                GROUP BY loan_range
                ORDER BY
                    CASE loan_range
                        WHEN '0-5 Lakhs' THEN 1
                        WHEN '5-10 Lakhs' THEN 2
                        WHEN '10-15 Lakhs' THEN 3
                        WHEN '15-20 Lakhs' THEN 4
                        WHEN '>20 Lakhs' THEN 5
                        ELSE 6
                    END
            """, (company,))

        result = cursor.fetchall()

        loan_distribution = []
        for row in result:
            loan_distribution.append({
                'range': row['loan_range'],
                'count': row['count']
            })

        return jsonify({'loan_distribution': loan_distribution}), 200

    except Exception as e:
        print(f"Error in loan amounts chart: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()       
# Add these routes to your personnel_info.py file
@personnel_info.route('/update-personnel')
def update_personnel_page():
    """Render the update personnel page"""
    return render_template('/personnel_info/update.html', active_tab='update-personnel')

@personnel_info.route('/api/personnel/search/<army_number>', methods=['GET'])
def search_personnel(army_number):
    """Search for personnel by army number and return all details"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
   
    cursor = connection.cursor(dictionary=True)
   
    try:
        # Get personnel basic information
        cursor.execute("""
            SELECT * FROM personnel WHERE army_number = %s
        """, (army_number,))
        personnel = cursor.fetchone()
       
        if not personnel:
            return jsonify({'success': False, 'message': 'Personnel not found'}), 404
       
        personnel_id = personnel['id']
       
        # Convert dates to string format for JSON
        date_fields = ['date_of_birth', 'date_of_enrollment', 'date_of_tos', 'date_of_tors',
                      'i_card_date', 'bpet_date', 'kin_marriage_date', 'vehicle_purchase_date',
                      'license_issue_date', 'license_expiry_date', 'folder_prepared_on',
                      'prior_station_date', 'last_recat_bd_date', 'next_recat_due']
       
        for field in date_fields:
            if field in personnel and personnel[field]:
                personnel[field] = personnel[field].strftime('%Y-%m-%d')
       
        # Get courses
        cursor.execute("""
            SELECT * FROM courses WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        courses = cursor.fetchall()
       
        for course in courses:
            if course.get('from_date'):
                course['from_date'] = course['from_date'].strftime('%Y-%m-%d')
            if course.get('to_date'):
                course['to_date'] = course['to_date'].strftime('%Y-%m-%d')
       
        # Get units served
        cursor.execute("""
            SELECT * FROM units_served WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        units = cursor.fetchall()
       
        for unit in units:
            if unit.get('from_date'):
                unit['from_date'] = unit['from_date'].strftime('%Y-%m-%d')
            if unit.get('to_date'):
                unit['to_date'] = unit['to_date'].strftime('%Y-%m-%d')
       
        # Get loans
        cursor.execute("""
            SELECT * FROM loans WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        loans = cursor.fetchall()
       
        # Get punishments
        cursor.execute("""
            SELECT * FROM punishments WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        punishments = cursor.fetchall()
       
        for punishment in punishments:
            if punishment.get('punishment_date'):
                punishment['punishment_date'] = punishment['punishment_date'].strftime('%Y-%m-%d')
       
        # Get detailed courses
        cursor.execute("""
            SELECT * FROM detailed_courses WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        detailed_courses = cursor.fetchall()
       
        for course in detailed_courses:
            if course.get('from_date'):
                course['from_date'] = course['from_date'].strftime('%Y-%m-%d')
            if course.get('to_date'):
                course['to_date'] = course['to_date'].strftime('%Y-%m-%d')
       
        # Get leave details
        cursor.execute("""
            SELECT * FROM leave_details WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        leaves = cursor.fetchall()
       
        # Get family members
        cursor.execute("""
            SELECT * FROM family_members WHERE personnel_id = %s
        """, (personnel_id,))
        family = cursor.fetchall()
       
        for member in family:
            if member.get('date_of_birth'):
                member['date_of_birth'] = member['date_of_birth'].strftime('%Y-%m-%d')
       
        # Get children
        cursor.execute("""
            SELECT * FROM children WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        children = cursor.fetchall()
       
        for child in children:
            if child.get('date_of_birth'):
                child['date_of_birth'] = child['date_of_birth'].strftime('%Y-%m-%d')
       
        # Get mobile phones
        cursor.execute("""
            SELECT * FROM mobile_phones WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        mobiles = cursor.fetchall()
       
        # Get marital discord cases
        cursor.execute("""
            SELECT * FROM marital_discord_cases WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        discord_cases = cursor.fetchall()
        
        # Get sports data - return as list of sport names
        cursor.execute("""
            SELECT sport_name FROM personnel_sports WHERE personnel_id = %s
        """, (personnel_id,))
        sports_data = cursor.fetchall()
        sports = [sport['sport_name'] for sport in sports_data]
        
        # Get weight_info data for status fields
        cursor.execute("""
            SELECT status_type, category_type, restrictions FROM weight_info WHERE army_number = %s LIMIT 1
        """, (army_number,))
        weight_info = cursor.fetchone()
        
        # Add weight_info fields to personnel object
        if weight_info:
            personnel['physical_status'] = weight_info.get('status_type')
            personnel['category_type'] = weight_info.get('category_type')
            personnel['physical_restrictions'] = weight_info.get('restrictions')
       
        return jsonify({
            'success': True,
            'data': {
                'personnel': personnel,
                'courses': courses,
                'units': units,
                'loans': loans,
                'punishments': punishments,
                'detailed_courses': detailed_courses,
                'leaves': leaves,
                'family': family,
                'children': children,
                'mobiles': mobiles,
                'discord_cases': discord_cases,
                'sports': sports  # Now returns ['Football', 'Basketball', 'Cricket']
            }
        }), 200
   
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@personnel_info.route('/api/personnel/update/<army_number>', methods=['PUT'])
def update_personnel(army_number):
    """Update personnel information"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    cursor = connection.cursor()
    try:
        data = request.get_json()
        print("Received update data:", json.dumps(data, indent=2))
       
        # First, get the personnel ID
        cursor.execute("SELECT id FROM personnel WHERE army_number = %s", (army_number,))
        result = cursor.fetchone()
       
        if not result:
            return jsonify({'success': False, 'message': 'Personnel not found'}), 404
       
        personnel_id = result[0]
       
        # Helper functions (same as create)
        def get_value(key, default=None):
            value = data.get(key, default)
            return None if value == '' else value
       
        def get_date(key):
            value = data.get(key)
            return value if value and value != '' else None
       
        def get_float(key):
            value = data.get(key)
            try:
                return float(value) if value and value != '' else None
            except (ValueError, TypeError):
                return None
       
        def get_int(key):
            value = data.get(key)
            try:
                return int(value) if value and value != '' else None
            except (ValueError, TypeError):
                return None

        # Update personnel main table - INCLUDING batch and section
        personnel_query = """
        UPDATE personnel SET
            name = %s, `rank` = %s, trade = %s, date_of_enrollment = %s, date_of_birth = %s,
            date_of_tos = %s, date_of_tors = %s, blood_group = %s, religion = %s,
            food_preference = %s, drinker = %s, company = %s, civ_qualifications = %s,
            decoration_awards = %s, lacking_qualifications = %s, willing_promotions = %s,
            i_card_no = %s, i_card_date = %s, i_card_issued_by = %s, bpet_grading = %s,
            ppt_grading = %s, bpet_date = %s, clothing_card = %s, pan_card_no = %s,
            pan_part_ii = %s, aadhar_card_no = %s, aadhar_part_ii = %s, joint_account_no = %s,
            joint_account_bank = %s, joint_account_ifsc = %s, home_house_no = %s,
            home_village = %s, home_phone = %s, home_to = %s, home_po = %s, home_ps = %s,
            home_teh = %s, home_nrs = %s, home_nmh = %s, home_district = %s, home_state = %s,
            border_area = %s, distance_from_ib = %s, height = %s, weight = %s, chest = %s,
            identification_marks = %s, court_cases = %s, loan = %s, total_leaves_encashed = %s,
            participation_activities = %s, present_family_location = %s, prior_station = %s,
            prior_station_date = %s, worked_it = %s, worked_unit_tenure = %s, med_cat = %s,
            last_recat_bd_date = %s, last_recat_bd_at = %s, next_recat_due = %s,
            medical_problem = %s, restrictions = %s, computer_knowledge = %s, it_literature = %s,
            kin_name = %s, kin_relation = %s, kin_marriage_date = %s, kin_account_no = %s,
            kin_bank = %s, kin_ifsc = %s, kin_part_ii = %s, vehicle_reg_no = %s,
            vehicle_model = %s, vehicle_purchase_date = %s, vehicle_agif = %s,
            driving_license_no = %s, license_issue_date = %s, license_expiry_date = %s,
            disability_child = %s, marital_discord = %s, counselling = %s,
            folder_prepared_on = %s, folder_checked_by = %s, bring_family = %s,
            domestic_issues = %s, other_requests = %s, family_medical_issues = %s,
            quality_points = %s, strengths = %s, weaknesses = %s, detailed_course = %s,
            batch = %s, section = %s
        WHERE army_number = %s
        """
       
        personnel_values = (
            get_value('name'),
            get_value('rank'),
            get_value('trade'),
            get_date('dateOfEnrollment'),
            get_date('dateOfBirth'),
            get_date('dateOfTOS'),
            get_date('dateOfTORS'),
            get_value('bloodGroup'),
            get_value('religion'),
            get_value('foodPreference'),
            get_value('drinker'),
            get_value('company'),
            get_value('civQualifications'),
            get_value('decorationAwards'),
            get_value('lackingQualifications'),
            get_value('willingPromotions'),
            get_value('iCardNo'),
            get_date('iCardDate'),
            get_value('iCardIssuedBy'),
            get_value('bpetGrading'),
            get_value('pptGrading'),
            get_date('bpetDate'),
            get_value('clothingCard'),
            get_value('panCardNo'),
            get_value('panPartII'),
            get_value('aadharCardNo'),
            get_value('aadharPartII'),
            get_value('jointAccountNo'),
            get_value('jointAccountBank'),
            get_value('jointAccountIFSC'),
            get_value('homeHouseNo'),
            get_value('homeVillage'),
            get_value('homePhone'),
            get_value('homeTO'),
            get_value('homePO'),
            get_value('homePS'),
            get_value('homeTeh'),
            get_value('homeNRS'),
            get_value('homeNMH'),
            get_value('homeDistrict'),
            get_value('homeState'),
            get_value('borderArea'),
            get_float('distanceFromIB'),
            get_float('height'),
            get_float('weight'),
            get_float('chest'),
            get_value('identificationMarks'),
            get_value('courtCases'),
            get_value('loan'),
            get_int('totalLeavesEncashed'),
            get_value('participationActivities'),
            get_value('presentFamilyLocation'),
            get_value('priorStation'),
            get_date('priorStationDate'),
            get_value('workedIT'),
            get_value('workedUnitTenure'),
            get_value('medCat'),
            get_date('lastRecatBDDate'),
            get_value('lastRecatBDAt'),
            get_date('nextRecatDue'),
            get_value('medicalProblem'),
            get_value('restrictions'),
            get_value('computerKnowledge'),
            get_value('itLiterature'),
            get_value('kinName'),
            get_value('kinRelation'),
            get_date('kinMarriageDate'),
            get_value('kinAccountNo'),
            get_value('kinBank'),
            get_value('kinIFSC'),
            get_value('kinPartII'),
            get_value('vehicleRegNo'),
            get_value('vehicleModel'),
            get_date('vehiclePurchaseDate'),
            get_value('vehicleAGIF'),
            get_value('drivingLicenseNo'),
            get_date('licenseIssueDate'),
            get_date('licenseExpiryDate'),
            get_value('disabilityChild'),
            get_value('maritalDiscord'),
            get_value('counselling'),
            get_date('folderPreparedOn'),
            get_value('folderCheckedBy'),
            get_value('bringFamily'),
            get_value('domesticIssues'),
            get_value('otherRequests'),
            get_value('familyMedicalIssues'),
            get_value('qualityPoints'),
            get_value('strengths'),
            get_value('weaknesses'),
            get_value('detailedCourse'),
            get_value('batch'),
            get_value('section'),
            army_number
        )
        
        print("Executing personnel update query...")
        cursor.execute(personnel_query, personnel_values)
        print(f"Personnel table updated. Rows affected: {cursor.rowcount}")

        # Delete old related records
        print("Deleting old related records...")
        delete_related_records(cursor, personnel_id, army_number)

        # CRITICAL: Re-insert all dynamic data
        print("Inserting dynamic data...")
        insert_dynamic_data(cursor, personnel_id, army_number, data)

        # Re-insert into weight_info
        if army_number and get_value('name'):
            print("Updating weight_info...")
            date_of_birth_str = get_date('dateOfBirth')
            age = None
            if date_of_birth_str:
                dob = datetime.datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
                today = datetime.date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            status_type = get_value('physicalStatus', 'shape')
            category_type = get_value('categoryType') if status_type == 'category' else None
            restrictions = get_value('physicalRestrictions')  # Changed from 'restrictions'

            weight_query = """
            INSERT INTO weight_info (name, army_number, age, `rank`, height, actual_weight, company, status_type, category_type, restrictions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            weight_values = (
                get_value('name'),
                army_number,
                age,
                get_value('rank'),
                get_float('height'),
                get_float('weight'),
                get_value('company'),
                status_type,
                category_type,
                restrictions
            )
            cursor.execute(weight_query, weight_values)
            print(f"Weight info updated. Rows affected: {cursor.rowcount}")

        connection.commit()
        print("Transaction committed successfully!")
        return jsonify({'success': True, 'personnel_id': personnel_id, 'message': 'Personnel updated successfully'}), 200
        
    except Error as e:
        connection.rollback()
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        print(f"General error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@personnel_info.route('/delete-personnel')
def delete_personnel_page():
    """Render the delete personnel page"""
    return render_template('/personnel_info/delete.html', active_tab='delete-personnel')

@personnel_info.route('/api/personnel/delete/<army_number>', methods=['DELETE'])
def delete_personnel(army_number):
    """Delete personnel and all related records"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    cursor = connection.cursor()
    try:
        # First, get the personnel ID
        cursor.execute("SELECT id FROM personnel WHERE army_number = %s", (army_number,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'success': False, 'message': 'Personnel not found'}), 404
        
        personnel_id = result[0]
        
        # Delete related records
        delete_related_records(cursor, personnel_id, army_number)
        
        # Finally delete from personnel table
        cursor.execute("DELETE FROM personnel WHERE id = %s", (personnel_id,))
        
        connection.commit()
        return jsonify({'success': True, 'message': 'Personnel deleted successfully'}), 200
    except Error as e:
        connection.rollback()
        print(f"Database error during deletion: {e}")
        return jsonify({'success': False, 'message': f"Database error: {str(e)}"}), 500
    except Exception as e:
        connection.rollback()
        print(f"General error during deletion: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
@personnel_info.route('/api/personnel')
def get_personnel():
    search = request.args.get('search', '')
    filter_company = request.args.get('company','')
    user = require_login()
    if not user:
        return jsonify({"count": 0, "data": []}), 401

    user_company = user['company']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query with parentheses around OR conditions
    query = """
        SELECT army_number, `rank`, name, home_state , company
        FROM personnel
        WHERE (army_number LIKE %s OR `rank` LIKE %s OR name LIKE %s)
    """
    params = [f"%{search}%", f"%{search}%", f"%{search}%"]
    print(user['company'])
    # Apply company filter only if user is not Admin
    if user_company != "Admin" and user_company !='Center':
        query += " AND company = %s"
        params.append(user_company)
    else:
        #admin can filter manually
        if filter_company:
            query += "AND company = %s"
            params.append(filter_company)
        

    query += " ORDER BY name"

    cursor.execute(query, params)
    data = cursor.fetchall()

    return jsonify({
        "count": len(data),
        "data": data
    })

@personnel_info.route('/api/personnel/delete-row/<table_name>/<int:row_id>', methods=['DELETE'])
def delete_table_row(table_name, row_id):
    """
    Delete a single row from any of the dynamic sub-tables.
    Allowed table names and their primary key columns:
        courses               -> id
        units_served          -> id
        loans                 -> id
        punishments           -> id
        detailed_courses      -> id
        leave_details         -> id
        family_members        -> id
        children              -> id
        mobile_phones         -> id
        marital_discord_cases -> id
        personnel_sports      -> id
    """
 
    ALLOWED_TABLES = {
        'courses',
        'units_served',
        'loans',
        'punishments',
        'detailed_courses',
        'leave_details',
        'family_members',
        'children',
        'mobile_phones',
        'marital_discord_cases',
        'personnel_sports',
    }
 
    if table_name not in ALLOWED_TABLES:
        return jsonify({'success': False, 'message': f'Invalid table: {table_name}'}), 400
 
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
 
    cursor = connection.cursor()
    try:
        # Verify the row exists before deleting
        cursor.execute(f"SELECT id FROM `{table_name}` WHERE id = %s", (row_id,))
        if not cursor.fetchone():
            return jsonify({'success': False, 'message': 'Row not found'}), 404
 
        cursor.execute(f"DELETE FROM `{table_name}` WHERE id = %s", (row_id,))
        connection.commit()
 
        return jsonify({'success': True, 'message': 'Row deleted successfully'}), 200
 
    except Error as e:
        connection.rollback()
        print(f"Database error deleting row from {table_name}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        print(f"General error deleting row from {table_name}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()