from imports import *

task_bp = Blueprint('task',__name__,url_prefix='/task_manager')

@task_bp.route('/')
def home():
    return render_template('/task_manager/task.html')

@task_bp.route('/create-task', methods=['POST'])
def update_task():
    data = request.get_json()
    print(data,"this is data")
    task_name = data.get('task_name')
    description = data.get('description')
    priority = data.get('priority')
    assigned_to = data.get('assigned_to')
    due_date = data.get('due_date')
    user = require_login()
    admin = user['role']
    print(admin)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
    INSERT INTO tasks (task_name, description, priority, assigned_to, assigned_by, due_date)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

        cursor.execute(query, (
    task_name,
    description,
    priority,
    assigned_to,
    admin,
    due_date
))


        conn.commit()

        return jsonify({"status": "success", "message": "Task updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@task_bp.route("/view_task")
def view_task():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            t.id,
            t.task_name,
            t.task_status,
            t.assigned_to,
            p.name AS assigned_name
        FROM tasks t
        LEFT JOIN personnel p 
            ON t.assigned_to = p.army_number
        ORDER BY t.id DESC
    """)

    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(tasks)


@task_bp.route("/get_task/<int:id>")
def get_task_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    print(id,"this is id")
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()
    print(task)
    cursor.close()
    conn.close()

    return jsonify(task)

@task_bp.route('delete_task/<int:id>',methods = ['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = 'DELETE FROM tasks where id = %s'
        cursor.execute(query,(id,))
    except Exception as e:
        print('Exception',str(e))
    return jsonify({'message': f'{id} deleted'}),200



@task_bp.route('/get_task_update/<int:task_id>')
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    task = cursor.fetchone()
    print(task)
    cursor.close()
    conn.close()
    
    if task:
        # Format date as yyyy-mm-dd for input[type=date]
        task['due_date'] = task['due_date'].strftime('%Y-%m-%d') if task['due_date'] else ''
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404





# the below route is for updating the task
@task_bp.route('/update_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    try:
        data = request.form  
        print(data,"this is data from form")

        task_name = data.get("task_name")
        description = data.get("description")
        priority = data.get("priority")
        assigned_to = data.get("assigned_to")
        due_date = data.get("due_date")

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE tasks
            SET task_name=%s, description=%s, priority=%s,
                assigned_to=%s, due_date=%s
            WHERE id=%s
        """

        cursor.execute(query, (task_name, description, priority, assigned_to, due_date, task_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Task updated successfully"}), 200

    except Exception as e:
        print("Update Task Error:", e)
        return jsonify({"status": "error", "message": "Failed to update task"}), 500
    



@task_bp.route('/get_my_tasks')
def get_my_tasks():
    user =require_login()
    current_user = user['army_number']  # assume username is stored in session
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, task_name, description, priority, due_date, task_status, remarks, range_status
        FROM tasks
        WHERE assigned_to = %s
        ORDER BY due_date ASC
    """, (current_user,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'tasks': tasks})



@task_bp.route('/update_task', methods=['POST'])
def jco_update_task():
    try:
        data = request.get_json()
        task_id = data.get('id')
        field = data.get('field')
        value = data.get('value')

        if not task_id or not field:
            return jsonify({'error': 'Missing id or field'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()

        # Map field to column name (add more if needed)
        allowed_fields = {
            'task_status': 'task_status',
            'remarks': 'remarks',
            'range_status': 'range_status'
        }

        if field not in allowed_fields:
            return jsonify({'error': 'Invalid field'}), 400

        column = allowed_fields[field]

        # Handle range_status as integer
        if field == 'range_status':
            value = int(value)

        query = f"UPDATE tasks SET {column} = %s WHERE id = %s"
        cursor.execute(query, (value, task_id))
        
        cursor.close()

        return jsonify({'success': True, 'message': 'Task updated successfully'})

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500