
from imports import *
import re

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

# Question Categories and Mappings
QUESTION_CATEGORIES = {
    "personnel": {
        "patterns": [
            r"how many personnel",
            r"total (soldiers|troops|personnel)",
            r"strength of",
            r"manpower",
            r"count of personnel"
        ],
        "questions": [
            "How many total personnel are there?",
            "How many personnel in each company?",
            "How many officers are there?",
            "How many JCOs are there?",
            "How many ORs are there?",
            "How many Agniveers are there?",
            "How many personnel by rank?",
            "How many personnel in detachment?",
            "How many personnel on leave?",
            "How many personnel on posting?"
        ]
    },
    "leave": {
        "patterns": [
            r"leave",
            r"on leave",
            r"pending leave",
            r"approved leave",
            r"rejected leave"
        ],
        "questions": [
            "How many leave requests are pending?",
            "How many leaves approved this month?",
            "How many leaves rejected?",
            "Who is on leave today?",
            "What types of leaves are most common?",
            "How many casual leaves approved?",
            "How many annual leaves pending?",
            "Which company has most leaves?",
            "Show leave statistics by month",
            "Who has been on leave longest?"
        ]
    },
    "interview": {
        "patterns": [
            r"interview",
            r"kunba",
            r"welfare interview"
        ],
        "questions": [
            "How many interviews pending?",
            "Interview completion percentage?",
            "Which JCO is assigned most interviews?",
            "Pending interviews by state?",
            "Interview status by company?",
            "How many interviews completed this month?",
            "Which personnel need urgent interviews?",
            "Interview statistics by rank?",
            "List personnel never interviewed",
            "Average time between interviews?"
        ]
    },
    "loans": {
        "patterns": [
            r"loan",
            r"borrowed",
            r"debt",
            r"emi"
        ],
        "questions": [
            "How many active loans?",
            "Total loan amount outstanding?",
            "Loans by type?",
            "Who has highest loan amount?",
            "Average EMI per person?",
            "Loans by company?",
            "Personnel with multiple loans?",
            "Loans nearing completion?",
            "Monthly EMI collection total?",
            "Loan default risks?"
        ]
    },
    "medical": {
        "patterns": [
            r"medical",
            r"unfit",
            r"medical category",
            r"restriction",
            r"disability"
        ],
        "questions": [
            "How many personnel medically unfit?",
            "Medical categories distribution?",
            "Personnel with restrictions?",
            "Last medical categorization dates?",
            "Upcoming recat due dates?",
            "Medical problems by type?",
            "Blood group distribution?",
            "Height and weight averages?",
            "Disability cases?",
            "Medical issues requiring counseling?"
        ]
    },
    "training": {
        "patterns": [
            r"course",
            r"training",
            r"qualification",
            r"on course"
        ],
        "questions": [
            "How many on courses currently?",
            "Course completion statistics?",
            "Pending course enrollments?",
            "Course distribution by institute?",
            "Courses ending this month?",
            "Personnel qualifications summary?",
            "Lacking qualifications list?",
            "Agniveer test schedules?",
            "Upcoming assistant tests?",
            "Course success rates?"
        ]
    },
    "deployment": {
        "patterns": [
            r"detachment",
            r"deployment",
            r"td",
            r"attachment",
            r"posting"
        ],
        "questions": [
            "How many on detachment?",
            "Detachment duration statistics?",
            "TD/Attachment count?",
            "Personnel on posting?",
            "Longest detachment durations?",
            "Detachment locations list?",
            "Overdue detachment returns?",
            "Company-wise deployment?",
            "Detachment vs unit strength?",
            "Recent postings list?"
        ]
    },
    "family": {
        "patterns": [
            r"family",
            r"kin",
            r"dependent",
            r"married",
            r"children"
        ],
        "questions": [
            "Married personnel count?",
            "Family location statistics?",
            "Disability in family cases?",
            "Domestic issues reported?",
            "Family medical problems?",
            "Marital discord cases?",
            "NOK details verification?",
            "Family brought to station?",
            "Counseling cases?",
            "Vehicle ownership statistics?"
        ]
    },
    "administrative": {
        "patterns": [
            r"document",
            r"i-card",
            r"pan",
            r"aadhar",
            r"bank account"
        ],
        "questions": [
            "I-Card expiry upcoming?",
            "Missing PAN card details?",
            "Incomplete Aadhar records?",
            "Bank account verification status?",
            "Clothing card distribution?",
            "BPET/PPT grading distribution?",
            "Identity card renewals due?",
            "Joint account setup completion?",
            "Document verification pending?",
            "Administrative compliance rate?"
        ]
    },
    "performance": {
        "patterns": [
            r"grading",
            r"bpet",
            r"ppt",
            r"performance",
            r"quality"
        ],
        "questions": [
            "BPET grading distribution?",
            "PPT grading averages?",
            "Recent BPET dates?",
            "Performance by company?",
            "Outstanding performers?",
            "Below average performers?",
            "Quality points summary?",
            "Strengths and weaknesses?",
            "Promotion willingness data?",
            "Performance trends over time?"
        ]
    }
}

# Database Query Functions
def execute_query(query_type, params=None):
    """Execute database queries based on question type"""
    from app import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if query_type == "total_personnel":
            cursor.execute("SELECT COUNT(*) as count FROM personnel")
            result = cursor.fetchone()
            return f"Total personnel: {result['count']}"
            
        elif query_type == "personnel_by_company":
            cursor.execute("""
                SELECT company, COUNT(*) as count 
                FROM personnel 
                GROUP BY company 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Personnel by company:\n"
            for row in results:
                response += f"• {row['company']}: {row['count']}\n"
            return response
            
        elif query_type == "officers_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE `rank` IN ('Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 
                                'Colonel', 'Brigadier', 'Major General', 
                                'Lieutenant General', 'General', 'OC')
            """)
            result = cursor.fetchone()
            return f"Total Officers: {result['count']}"
            
        elif query_type == "jco_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE `rank` IN ('Subedar', 'Naib Subedar', 'Subedar Major', 'JCO')
            """)
            result = cursor.fetchone()
            return f"Total JCOs: {result['count']}"
            
        elif query_type == "or_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE `rank` NOT IN ('Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 
                                    'Colonel', 'Brigadier', 'Major General', 
                                    'Lieutenant General', 'General', 'OC',
                                    'Subedar', 'Naib Subedar', 'Subedar Major', 'JCO')
            """)
            result = cursor.fetchone()
            return f"Total ORs (Other Ranks): {result['count']}"
            
        elif query_type == "agniveer_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE `rank` = 'Agniveer'
            """)
            result = cursor.fetchone()
            return f"Total Agniveers: {result['count']}"
            
        elif query_type == "personnel_by_rank":
            cursor.execute("""
                SELECT `rank`, COUNT(*) as count 
                FROM personnel 
                GROUP BY `rank` 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Personnel by rank:\n"
            for row in results:
                response += f"• {row['rank']}: {row['count']}\n"
            return response
            
        elif query_type == "detachment_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE detachment_status = 1
            """)
            result = cursor.fetchone()
            return f"Personnel on detachment: {result['count']}"
            
        elif query_type == "on_leave_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE onleave_status = 1
            """)
            result = cursor.fetchone()
            return f"Personnel currently on leave: {result['count']}"
            
        elif query_type == "on_posting_count":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE posting_status = 1
            """)
            result = cursor.fetchone()
            return f"Personnel on posting: {result['count']}"
            
        # LEAVE QUERIES
        elif query_type == "pending_leave_requests":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM leave_status_info 
                WHERE request_status LIKE 'Pending%'
            """)
            result = cursor.fetchone()
            return f"Pending leave requests: {result['count']}"
            
        elif query_type == "approved_leaves_month":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM leave_status_info 
                WHERE request_status = 'Approved'
                AND MONTH(recommend_date) = MONTH(CURDATE())
                AND YEAR(recommend_date) = YEAR(CURDATE())
            """)
            result = cursor.fetchone()
            return f"Leaves approved this month: {result['count']}"
            
        elif query_type == "rejected_leaves":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM leave_status_info 
                WHERE request_status = 'Rejected'
            """)
            result = cursor.fetchone()
            return f"Rejected leave requests: {result['count']}"
            
        elif query_type == "on_leave_today":
            cursor.execute("""
                SELECT l.name, l.army_number, l.leave_type, l.from_date, l.to_date, l.company
                FROM leave_status_info l
                WHERE l.request_status = 'Approved'
                AND CURDATE() BETWEEN l.from_date AND l.to_date
                ORDER BY l.company, l.name
            """)
            results = cursor.fetchall()
            if not results:
                return "No personnel on leave today."
            response = "Personnel on leave today:\n"
            for row in results:
                response += f"• {row['name']} ({row['army_number']}) - {row['company']}\n"
                response += f"  Type: {row['leave_type']}, Duration: {row['from_date']} to {row['to_date']}\n"
            return response
            
        elif query_type == "leave_types_distribution":
            cursor.execute("""
                SELECT leave_type, COUNT(*) as count 
                FROM leave_status_info 
                WHERE request_status = 'Approved'
                GROUP BY leave_type 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Leave types distribution:\n"
            for row in results:
                response += f"• {row['leave_type']}: {row['count']}\n"
            return response
            
        elif query_type == "casual_leaves_approved":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM leave_status_info 
                WHERE leave_type = 'Casual Leave' 
                AND request_status = 'Approved'
            """)
            result = cursor.fetchone()
            return f"Approved casual leaves: {result['count']}"
            
        elif query_type == "annual_leaves_pending":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM leave_status_info 
                WHERE leave_type = 'Annual Leave' 
                AND request_status LIKE 'Pending%'
            """)
            result = cursor.fetchone()
            return f"Pending annual leaves: {result['count']}"
            
        elif query_type == "leaves_by_company":
            cursor.execute("""
                SELECT company, COUNT(*) as count 
                FROM leave_status_info 
                WHERE request_status = 'Approved'
                GROUP BY company 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Approved leaves by company:\n"
            for row in results:
                response += f"• {row['company']}: {row['count']}\n"
            return response
            
        # INTERVIEW QUERIES
        elif query_type == "pending_interviews":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE interview_status = 0
                AND `rank` NOT IN ('Subedar', 'Naib Subedar', 'Subedar Major', 
                                   'Lieutenant', 'Captain', 'Major')
            """)
            result = cursor.fetchone()
            return f"Pending interviews: {result['count']}"
            
        elif query_type == "interview_percentage":
            cursor.execute("""
                SELECT 
                    SUM(interview_status = 1) as completed,
                    COUNT(*) as total
                FROM personnel
                WHERE `rank` NOT IN ('Subedar', 'Naib Subedar', 'Subedar Major', 
                                     'Lieutenant', 'Captain', 'Major')
            """)
            result = cursor.fetchone()
            if result['total'] > 0:
                percentage = (result['completed'] / result['total']) * 100
                return f"Interview completion: {percentage:.1f}% ({result['completed']}/{result['total']})"
            return "No interview data available"
            
        elif query_type == "interviews_by_state":
            cursor.execute("""
                SELECT home_state, 
                       COUNT(*) as total,
                       SUM(interview_status = 0) as pending
                FROM personnel 
                WHERE home_state IS NOT NULL
                GROUP BY home_state 
                ORDER BY pending DESC
                LIMIT 10
            """)
            results = cursor.fetchall()
            response = "Pending interviews by state (Top 10):\n"
            for row in results:
                response += f"• {row['home_state']}: {row['pending']} pending out of {row['total']}\n"
            return response
            
        elif query_type == "interviews_by_company":
            cursor.execute("""
                SELECT company, 
                       COUNT(*) as total,
                       SUM(interview_status = 0) as pending,
                       SUM(interview_status = 1) as completed
                FROM personnel 
                GROUP BY company 
                ORDER BY company
            """)
            results = cursor.fetchall()
            response = "Interview status by company:\n"
            for row in results:
                response += f"• {row['company']}: {row['completed']} completed, {row['pending']} pending\n"
            return response
            
        # LOAN QUERIES
        elif query_type == "active_loans":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM loans
            """)
            result = cursor.fetchone()
            return f"Active loans: {result['count']}"
            
        elif query_type == "total_loan_amount":
            cursor.execute("""
                SELECT SUM(total_amount) as total 
                FROM loans
            """)
            result = cursor.fetchone()
            total = result['total'] if result['total'] else 0
            return f"Total outstanding loan amount: ₹{total:,.2f}"
            
        elif query_type == "loans_by_type":
            cursor.execute("""
                SELECT loan_type, COUNT(*) as count, SUM(total_amount) as total 
                FROM loans 
                GROUP BY loan_type 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Loans by type:\n"
            for row in results:
                response += f"• {row['loan_type']}: {row['count']} loans, ₹{row['total']:,.2f}\n"
            return response
            
        elif query_type == "highest_loan":
            cursor.execute("""
                SELECT l.army_number, p.name, p.rank, l.loan_type, l.total_amount
                FROM loans l
                JOIN personnel p ON l.army_number = p.army_number
                ORDER BY l.total_amount DESC
                LIMIT 5
            """)
            results = cursor.fetchall()
            response = "Top 5 highest loans:\n"
            for row in results:
                response += f"• {row['name']} ({row['army_number']}) - {row['rank']}\n"
                response += f"  Type: {row['loan_type']}, Amount: ₹{row['total_amount']:,.2f}\n"
            return response
            
        elif query_type == "average_emi":
            cursor.execute("""
                SELECT AVG(emi_per_month) as avg_emi 
                FROM loans
            """)
            result = cursor.fetchone()
            avg = result['avg_emi'] if result['avg_emi'] else 0
            return f"Average EMI per person: ₹{avg:,.2f}"
            
        # MEDICAL QUERIES
        elif query_type == "medically_unfit":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM troop_medical_status 
                WHERE status_type = 'unfit'
            """)
            result = cursor.fetchone()
            return f"Medically unfit personnel: {result['count']}"
            
        elif query_type == "medical_categories":
            cursor.execute("""
                SELECT med_cat, COUNT(*) as count 
                FROM personnel 
                WHERE med_cat IS NOT NULL 
                GROUP BY med_cat 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Medical categories distribution:\n"
            for row in results:
                response += f"• {row['med_cat']}: {row['count']}\n"
            return response
            
        elif query_type == "restrictions":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE restrictions IS NOT NULL 
                AND restrictions != ''
            """)
            result = cursor.fetchone()
            return f"Personnel with medical restrictions: {result['count']}"
            
        elif query_type == "blood_group_distribution":
            cursor.execute("""
                SELECT blood_group, COUNT(*) as count 
                FROM personnel 
                WHERE blood_group IS NOT NULL 
                GROUP BY blood_group 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Blood group distribution:\n"
            for row in results:
                response += f"• {row['blood_group']}: {row['count']}\n"
            return response
            
        # TRAINING/COURSE QUERIES
        elif query_type == "on_courses":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM candidate_on_courses
            """)
            result = cursor.fetchone()
            return f"Personnel currently on courses: {result['count']}"
            
        elif query_type == "courses_by_institute":
            cursor.execute("""
                SELECT institute_name, COUNT(*) as count 
                FROM candidate_on_courses 
                GROUP BY institute_name 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Courses by institute:\n"
            for row in results:
                response += f"• {row['institute_name']}: {row['count']}\n"
            return response
            
        elif query_type == "upcoming_tests":
            cursor.execute("""
                SELECT batch, asst_test1, asst_test2, asst_test3, asst_test4
                FROM assistant_test
                WHERE test1_status = 0 OR test2_status = 0 
                   OR test3_status = 0 OR test4_status = 0
            """)
            results = cursor.fetchall()
            response = "Upcoming Agniveer tests:\n"
            for row in results:
                response += f"• Batch {row['batch']}:\n"
                if row['asst_test1']:
                    response += f"  Test 1: {row['asst_test1']}\n"
                if row['asst_test2']:
                    response += f"  Test 2: {row['asst_test2']}\n"
                if row['asst_test3']:
                    response += f"  Test 3: {row['asst_test3']}\n"
                if row['asst_test4']:
                    response += f"  Test 4: {row['asst_test4']}\n"
            return response if results else "No upcoming tests scheduled"
            
        # DEPLOYMENT QUERIES
        elif query_type == "td_attachment":
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM personnel 
                WHERE td_status = 1
            """)
            result = cursor.fetchone()
            return f"Personnel on TD/Attachment: {result['count']}"
            
        elif query_type == "detachment_locations":
            cursor.execute("""
                SELECT d.det_name, COUNT(*) as count
                FROM assigned_det ad
                JOIN dets d ON ad.det_id = d.det_id
                WHERE ad.det_status = 1
                GROUP BY d.det_name
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "Detachment locations:\n"
            for row in results:
                response += f"• {row['det_name']}: {row['count']} personnel\n"
            return response
            
        elif query_type == "overdue_detachment":
            cursor.execute("""
                SELECT p.name, p.army_number, d.det_name, ad.assigned_on,
                       DATEDIFF(NOW(), ad.assigned_on) as days
                FROM assigned_det ad
                JOIN personnel p ON ad.army_number = p.army_number
                JOIN dets d ON ad.det_id = d.det_id
                WHERE ad.det_status = 1
                AND DATEDIFF(NOW(), ad.assigned_on) > 90
                ORDER BY days DESC
                LIMIT 10
            """)
            results = cursor.fetchall()
            if not results:
                return "No overdue detachments (>90 days)"
            response = "Overdue detachments (>90 days):\n"
            for row in results:
                response += f"• {row['name']} ({row['army_number']})\n"
                response += f"  Location: {row['det_name']}, Duration: {row['days']} days\n"
            return response
            
        # ADMINISTRATIVE QUERIES
        elif query_type == "icard_expiry":
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM personnel
                WHERE i_card_date < DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                AND i_card_date IS NOT NULL
            """)
            result = cursor.fetchone()
            return f"I-Cards expiring in next 30 days: {result['count']}"
            
        elif query_type == "missing_pan":
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM personnel
                WHERE pan_card_no IS NULL OR pan_card_no = ''
            """)
            result = cursor.fetchone()
            return f"Personnel without PAN card details: {result['count']}"
            
        elif query_type == "missing_aadhar":
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM personnel
                WHERE aadhar_card_no IS NULL OR aadhar_card_no = ''
            """)
            result = cursor.fetchone()
            return f"Personnel without Aadhar details: {result['count']}"
            
        # PERFORMANCE QUERIES
        elif query_type == "bpet_grading":
            cursor.execute("""
                SELECT bpet_grading, COUNT(*) as count
                FROM personnel
                WHERE bpet_grading IS NOT NULL
                GROUP BY bpet_grading
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "BPET grading distribution:\n"
            for row in results:
                response += f"• {row['bpet_grading']}: {row['count']}\n"
            return response
            
        elif query_type == "ppt_grading":
            cursor.execute("""
                SELECT ppt_grading, COUNT(*) as count
                FROM personnel
                WHERE ppt_grading IS NOT NULL
                GROUP BY ppt_grading
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            response = "PPT grading distribution:\n"
            for row in results:
                response += f"• {row['ppt_grading']}: {row['count']}\n"
            return response
            
        else:
            return "Query type not implemented yet."
            
    except Exception as e:
        return f"Error executing query: {str(e)}"
    finally:
        cursor.close()
        conn.close()


def match_question(user_input):
    """Match user input to predefined questions"""
    user_input_lower = user_input.lower()
    
    # Direct question matching
    query_map = {
        # Personnel queries
        "how many total personnel": "total_personnel",
        "total personnel": "total_personnel",
        "personnel count": "total_personnel",
        "how many personnel in each company": "personnel_by_company",
        "company wise strength": "personnel_by_company",
        "how many officers": "officers_count",
        "officer count": "officers_count",
        "how many jcos": "jco_count",
        "jco count": "jco_count",
        "how many ors": "or_count",
        "or count": "or_count",
        "how many agniveers": "agniveer_count",
        "agniveer count": "agniveer_count",
        "personnel by rank": "personnel_by_rank",
        "rank wise distribution": "personnel_by_rank",
        "how many on detachment": "detachment_count",
        "detachment count": "detachment_count",
        "how many on leave": "on_leave_count",
        "leave count": "on_leave_count",
        "how many on posting": "on_posting_count",
        "posting count": "on_posting_count",
        
        # Leave queries
        "pending leave requests": "pending_leave_requests",
        "how many pending leaves": "pending_leave_requests",
        "approved leaves this month": "approved_leaves_month",
        "monthly approved leaves": "approved_leaves_month",
        "rejected leaves": "rejected_leaves",
        "who is on leave today": "on_leave_today",
        "today's leave": "on_leave_today",
        "leave types": "leave_types_distribution",
        "casual leaves approved": "casual_leaves_approved",
        "annual leaves pending": "annual_leaves_pending",
        "leaves by company": "leaves_by_company",
        
        # Interview queries
        "pending interviews": "pending_interviews",
        "interview completion percentage": "interview_percentage",
        "interview percentage": "interview_percentage",
        "interviews by state": "interviews_by_state",
        "state wise interviews": "interviews_by_state",
        "interviews by company": "interviews_by_company",
        
        # Loan queries
        "active loans": "active_loans",
        "total loan amount": "total_loan_amount",
        "outstanding loans": "total_loan_amount",
        "loans by type": "loans_by_type",
        "highest loan": "highest_loan",
        "top loans": "highest_loan",
        "average emi": "average_emi",
        
        # Medical queries
        "medically unfit": "medically_unfit",
        "unfit personnel": "medically_unfit",
        "medical categories": "medical_categories",
        "medical restrictions": "restrictions",
        "personnel with restrictions": "restrictions",
        "blood group distribution": "blood_group_distribution",
        "blood groups": "blood_group_distribution",
        
        # Training queries
        "on courses": "on_courses",
        "current courses": "on_courses",
        "courses by institute": "courses_by_institute",
        "upcoming tests": "upcoming_tests",
        "agniveer tests": "upcoming_tests",
        
        # Deployment queries
        "td attachment": "td_attachment",
        "on td": "td_attachment",
        "detachment locations": "detachment_locations",
        "overdue detachment": "overdue_detachment",
        
        # Administrative queries
        "icard expiry": "icard_expiry",
        "expiring icards": "icard_expiry",
        "missing pan": "missing_pan",
        "no pan card": "missing_pan",
        "missing aadhar": "missing_aadhar",
        "no aadhar": "missing_aadhar",
        
        # Performance queries
        "bpet grading": "bpet_grading",
        "bpet distribution": "bpet_grading",
        "ppt grading": "ppt_grading",
        "ppt distribution": "ppt_grading"
    }
    
    # Check for exact or partial matches
    for key, value in query_map.items():
        if key in user_input_lower:
            return value
    
    return None


@chatbot_bp.route('/chat/message', methods=['POST'])
def chat_message():
    """Handle incoming chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Match question and execute query
        query_type = match_question(user_message)
        
        if query_type:
            response = execute_query(query_type)
        else:
            response = "I couldn't understand your question. Please try:\n\n"
            response += "• How many total personnel?\n"
            response += "• Pending leave requests?\n"
            response += "• Interview completion percentage?\n"
            response += "• Active loans?\n"
            response += "• Personnel on detachment?\n"
            response += "• Medical categories distribution?\n"
            response += "\nType 'help' to see all available questions."
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@chatbot_bp.route('/chat/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions"""
    suggestions = [
        "How many total personnel?",
        "Pending leave requests?",
        "Interview completion percentage?",
        "Active loans count?",
        "Who is on leave today?",
        "Medical categories distribution?",
        "Personnel on detachment?",
        "Upcoming Agniveer tests?",
        "BPET grading distribution?",
        "Overdue detachments?"
    ]
    
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })


@chatbot_bp.route('/chat/help', methods=['GET'])
def get_help():
    """Get all available questions categorized"""
    help_data = {
        'categories': []
    }
    
    for category, data in QUESTION_CATEGORIES.items():
        help_data['categories'].append({
            'name': category.title(),
            'questions': data['questions']
        })
    
    return jsonify({
        'success': True,
        'help': help_data
    })