from imports import *
from datetime import datetime

projects_bp = Blueprint('@projects_bp',__name__,url_prefix='/projects')



# ==================== PROJECT MANAGEMENT API ROUTES ====================
# Add these routes to your Flask application



# ==================== API ROUTE 1: GET ALL PROJECTS (ENHANCED) ====================
@projects_bp.route('/all_projects', methods=['GET'])
def api_get_all_projects():
    """
    Enhanced version - Get all projects with proper filtering
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    role = user['role']
    company = user['company']

    try:
        query = """
            SELECT 
                project_id, 
                head, 
                project_name, 
                current_stage, 
                project_cost, 
                project_items, 
                quantity, 
                project_description,
                company,
                created_on,
                deadline,
                status
            FROM projects
        """
        params = []

        # Apply filters based on role
        if company != "Admin" and role != 'PROJECT JCO' and role != 'PROJECT OFFICER':
            query += " WHERE company = %s"
            params.append(company)

        query += " ORDER BY project_id DESC"

        cursor.execute(query, params)
        projects = cursor.fetchall()

        # Format response for frontend
        formatted_projects = []
        for project in projects:
            formatted_projects.append({
                'id': project['project_id'],
                'title': project['project_name'],
                'description': project['project_description'] or 'No description available',
                'stage': project['current_stage'] or 'Planning',
                'owner': project['head'] or 'Unassigned',
                'cost': project['project_cost'],
                'items': project['project_items'],
                'quantity': project['quantity'],
                'company': project.get('company', ''),
                'start_date': project.get('created_date', datetime.now().strftime('%Y-%m-%d')),
                'deadline': project.get('deadline', ''),
                'status': project.get('status', 'Active'),
                'category': 'Engineering'  # You can add this field to DB if needed
            })

        return jsonify({
            'status': 'success',
            'projects': formatted_projects,
            'count': len(formatted_projects)
        })

    except Exception as e:
        print("Error fetching projects:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e),
            'projects': []
        }), 500
    finally:
        cursor.close()
        conn.close()


# ==================== API ROUTE 2: GET PROJECT BY ID ====================
@projects_bp.route('/get_project/<int:project_id>', methods=['GET'])
def api_get_project_by_id(project_id):
    """
    Get detailed information about a specific project
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()

    try:
        query = """
            SELECT 
                project_id, 
                head, 
                project_name, 
                current_stage, 
                project_cost, 
                project_items, 
                quantity, 
                project_description,
                company,
                created_on,
                deadline,
                status,
                updated_date,
                updated_by
            FROM projects
            WHERE project_id = %s
        """
        
        cursor.execute(query, (project_id,))
        project = cursor.fetchone()

        if not project:
            return jsonify({
                'status': 'error',
                'message': 'Project not found'
            }), 404

        return jsonify({
            'status': 'success',
            'project': {
                'id': project['project_id'],
                'title': project['project_name'],
                'description': project['project_description'],
                'stage': project['current_stage'],
                'owner': project['head'],
                'cost': project['project_cost'],
                'items': project['project_items'],
                'quantity': project['quantity'],
                'company': project.get('company', ''),
                'start_date': project.get('created_date', ''),
                'deadline': project.get('deadline', ''),
                'status': project.get('status', ''),
                'updated_date': project.get('updated_date', ''),
                'updated_by': project.get('updated_by', '')
            }
        })

    except Exception as e:
        print("Error fetching project:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()


# ==================== API ROUTE 3: UPDATE PROJECT STAGE ====================
@projects_bp.route('/update-stage', methods=['POST'])
def api_update_project_stage():
    """
    Update the current stage of a project
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        new_stage = data.get('new_stage')
        notes = data.get('notes', '')
        updated_by = data.get('updated_by', user['name'])

        if not project_id or not new_stage:
            return jsonify({
                'status': 'error',
                'message': 'Project ID and new stage are required'
            }), 400

        # Check if project exists
        cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
        project = cursor.fetchone()

        if not project:
            return jsonify({
                'status': 'error',
                'message': 'Project not found'
            }), 404

        # Update the project stage
        update_query = """
            UPDATE projects 
            SET current_stage = %s,
                updated_date = %s,
                updated_by = %s
            WHERE project_id = %s
        """
        
        cursor.execute(update_query, (
            new_stage,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            updated_by,
            project_id
        ))

        # Insert into project history/timeline table (if you have one)
        # If you don't have a project_history table, create one or skip this
        try:
            history_query = """
                INSERT INTO project_history 
                (project_id, stage, notes, updated_by, updated_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(history_query, (
                project_id,
                new_stage,
                notes,
                updated_by,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
        except:
            # If table doesn't exist, just skip
            pass

        conn.commit()

        return jsonify({
            'status': 'success',
            'message': 'Project stage updated successfully',
            'new_stage': new_stage
        })

    except Exception as e:
        conn.rollback()
        print("Error updating project stage:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()


# ==================== API ROUTE 4: GET PROJECT TIMELINE ====================
@projects_bp.route('/project_timeline/<int:project_id>/timeline', methods=['GET'])
def api_get_project_timeline(project_id):
    """
    Get the timeline/history of a project
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Check if project_history table exists
        # If not, return empty timeline
        try:
            query = """
                SELECT 
                    stage,
                    notes,
                    updated_by,
                    updated_date as date
                FROM project_history
                WHERE project_id = %s
                ORDER BY updated_date DESC
            """
            
            cursor.execute(query, (project_id,))
            timeline = cursor.fetchall()

            return jsonify({
                'status': 'success',
                'timeline': timeline,
                'count': len(timeline)
            })

        except:
            # If table doesn't exist, return the current project stage as timeline
            cursor.execute("""
                SELECT 
                    current_stage as stage,
                    updated_date as date,
                    updated_by
                FROM projects 
                WHERE project_id = %s
            """, (project_id,))
            
            current = cursor.fetchone()
            
            if current:
                timeline = [{
                    'stage': current['stage'],
                    'date': current['date'],
                    'updated_by': current.get('updated_by', 'System'),
                    'notes': ''
                }]
            else:
                timeline = []

            return jsonify({
                'status': 'success',
                'timeline': timeline,
                'count': len(timeline)
            })

    except Exception as e:
        print("Error fetching timeline:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timeline': []
        }), 500
    finally:
        cursor.close()
        conn.close()


# ==================== API ROUTE 5: GET PROJECT STATISTICS ====================
@projects_bp.route('/stats', methods=['GET'])
def api_get_project_stats():
    """
    Get overall project statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    role = user['role']
    company = user['company']

    try:
        # Base query for filtering
        where_clause = ""
        params = []

        if company != "Admin" and role != 'PROJECT JCO' and role != 'PROJECT OFFICER':
            where_clause = "WHERE company = %s"
            params.append(company)

        # Get total projects
        cursor.execute(f"SELECT COUNT(*) as total FROM projects {where_clause}", params)
        total = cursor.fetchone()['total']

        # Get projects by stage
        cursor.execute(f"""
            SELECT 
                current_stage,
                COUNT(*) as count
            FROM projects
            {where_clause}
            GROUP BY current_stage
        """, params)
        by_stage = cursor.fetchall()

        # Get total cost
        cursor.execute(f"""
            SELECT 
                SUM(CAST(project_cost AS DECIMAL(10,2))) as total_cost
            FROM projects
            {where_clause}
        """, params)
        cost_result = cursor.fetchone()
        total_cost = cost_result['total_cost'] if cost_result['total_cost'] else 0

        # Format stage stats
        stage_stats = {}
        for item in by_stage:
            stage_stats[item['current_stage']] = item['count']

        return jsonify({
            'status': 'success',
            'stats': {
                'total_projects': total,
                'total_cost': float(total_cost),
                'by_stage': stage_stats,
                'planning': stage_stats.get('Planning', 0),
                'in_progress': stage_stats.get('In Progress', 0),
                'testing': stage_stats.get('Testing', 0),
                'completed': stage_stats.get('Completed', 0),
                'on_hold': stage_stats.get('On Hold', 0)
            }
        })

    except Exception as e:
        print("Error fetching project stats:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()


# ==================== API ROUTE 6: SEARCH/FILTER PROJECTS ====================
@projects_bp.route('/search', methods=['GET'])
def api_search_projects():
    """
    Search and filter projects
    Query params: stage, search, company
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()

    try:
        # Get query parameters
        stage_filter = request.args.get('stage', '')
        search_term = request.args.get('search', '')
        company_filter = request.args.get('company', '')

        query = """
            SELECT 
                project_id, 
                head, 
                project_name, 
                current_stage, 
                project_cost, 
                project_items, 
                quantity, 
                project_description,
                company
            FROM projects
            WHERE 1=1
        """
        params = []

        # Apply filters
        if stage_filter:
            query += " AND current_stage = %s"
            params.append(stage_filter)

        if search_term:
            query += " AND (project_name LIKE %s OR project_description LIKE %s)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])

        if company_filter:
            query += " AND company = %s"
            params.append(company_filter)

        # Apply company restriction for non-admin users
        if user['company'] != "Admin" and user['role'] not in ['PROJECT JCO', 'PROJECT OFFICER']:
            query += " AND company = %s"
            params.append(user['company'])

        query += " ORDER BY project_id DESC"

        cursor.execute(query, params)
        projects = cursor.fetchall()

        # Format response
        formatted_projects = []
        for project in projects:
            formatted_projects.append({
                'id': project['project_id'],
                'title': project['project_name'],
                'description': project['project_description'],
                'stage': project['current_stage'],
                'owner': project['head'],
                'cost': project['project_cost'],
                'items': project['project_items'],
                'quantity': project['quantity'],
                'company': project.get('company', '')
            })

        return jsonify({
            'status': 'success',
            'projects': formatted_projects,
            'count': len(formatted_projects)
        })

    except Exception as e:
        print("Error searching projects:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e),
            'projects': []
        }), 500
    finally:
        cursor.close()
        conn.close()


# ==================== API ROUTE 7: DELETE PROJECT ====================
@projects_bp.route('/delete_projects/<int:project_id>/delete', methods=['DELETE'])
def api_delete_project(project_id):
    """
    Delete a project (only for authorized users)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()

    try:
        # Check authorization
        if user['role'] not in ['Admin', 'PROJECT JCO', 'PROJECT OFFICER']:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized to delete projects'
            }), 403

        # Check if project exists
        cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
        project = cursor.fetchone()

        if not project:
            return jsonify({
                'status': 'error',
                'message': 'Project not found'
            }), 404

        # Delete project
        cursor.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
        
        # Delete project history if exists
        try:
            cursor.execute("DELETE FROM project_history WHERE project_id = %s", (project_id,))
        except:
            pass

        conn.commit()

        return jsonify({
            'status': 'success',
            'message': 'Project deleted successfully'
        })

    except Exception as e:
        conn.rollback()
        print("Error deleting project:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()

@projects_bp.route('/stats/cost_by_head', methods=['GET'])
def cost_by_head():
    connection = get_db_connection()
    if not connection:
        return jsonify({
            "status": "error",
            "message": "Cannot connect to database"
        }), 500

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT 
            COALESCE(head, 'Unassigned') AS head,
            ROUND(SUM(project_cost), 2) AS total_cost,
            COUNT(*) AS count
        FROM projects
        GROUP BY head
        HAVING total_cost IS NOT NULL
        ORDER BY total_cost DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # Convert Decimal → float (JSON cannot handle Decimal directly)
        result_data = []
        for row in rows:
            result_data.append({
                "head": row["head"],
                "total_cost": float(row["total_cost"]),
                "count": int(row["count"])
            })

        return jsonify({
            "status": "success",
            "data": result_data
        })

    except Error as err:
        print(f"Query error: {err}")
        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:
        # Always clean up
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@projects_bp.route('/create', methods=['POST'])
def create_project():
    data = request.get_json()

    project_name = (data.get("project_name") or "").strip()
    head = (data.get("head") or "").strip()
    cost = data.get("project_cost")
    items = (data.get("project_items") or "").strip()
    quantity = data.get("quantity") or 0
    description = (data.get("project_description") or "").strip()

    # Server-side validation
    if not project_name or not head:
        return jsonify({"status": "error", "message": "Project name and head are required"})

    try:
        cost = float(cost)
        if cost < 0:
            raise ValueError
    except:
        return jsonify({"status": "error", "message": "Invalid cost value"})

    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError
    except:
        return jsonify({"status": "error", "message": "Invalid quantity value"})

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO projects 
            (project_name, head, project_cost, project_items, quantity, project_description, current_stage, created_on, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            project_name,
            head,
            cost,
            items,
            quantity,
            description,
            "PPP",
            datetime.now(),
            "Active"
        ))

        connection.commit()
        return jsonify({"status": "success"})

    except Exception as e:
        print("Project Create Error:", e)
        return jsonify({"status": "error", "message": "Database error"}), 500

    finally:
        cursor.close()
        connection.close()
