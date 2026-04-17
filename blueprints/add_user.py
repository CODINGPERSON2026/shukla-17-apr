from imports import *

add_user_bp = Blueprint("add_user_bp", __name__, url_prefix="/user_role")


@add_user_bp.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        user =require_login()
        current_user = user['army_number']  # assume username is stored in session
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        required = ["username", "email", "password", "role"]
        if not all(k in data for k in required):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({
                "success": False,
                "message": "Email already exists"
            }), 409

        user = User(
            username=data["username"],
            email=data["email"],
            password=(data["password"]),
            role=data["role"],
            company=data.get("company"),
            army_number=data.get("army_number")
        )

        return jsonify({
            "success": True,
            "message": "User added successfully"
        })

    except Exception as e:
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
