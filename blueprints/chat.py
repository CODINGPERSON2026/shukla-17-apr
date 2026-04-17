from imports import *

chat_bp = Blueprint('chat_bp', __name__, url_prefix='/chat')


@chat_bp.route("/users")
def chat_users():
    q = request.args.get("q", "")
    user = require_login()
    current_user_id = user['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if q:
        cursor.execute("""
            SELECT 
                u.id, 
                u.username,
                COUNT(m.id) as unread_count
            FROM users u
            LEFT JOIN messages m ON m.sender_id = u.id 
                AND m.receiver_id = %s 
                AND m.status = 'sent'
            WHERE u.username LIKE %s AND u.id != %s
            GROUP BY u.id, u.username
            ORDER BY unread_count DESC, u.username
        """, (current_user_id, f"%{q}%", current_user_id))
    else:
        cursor.execute("""
            SELECT 
                u.id, 
                u.username,
                COUNT(m.id) as unread_count
            FROM users u
            LEFT JOIN messages m ON m.sender_id = u.id 
                AND m.receiver_id = %s 
                AND m.status = 'sent'
            WHERE u.id != %s
            GROUP BY u.id, u.username
            ORDER BY unread_count DESC, u.username
        """, (current_user_id, current_user_id))

    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


@chat_bp.route("/me", methods=["GET"])
def get_current_user():
    user = require_login()
    user_id = user['user_id']
    if not user_id:
        return jsonify({"id": None}), 401
    return jsonify({"id": user_id})


@chat_bp.route("/messages/<int:receiver_id>")
def chat_messages(receiver_id):
    user = require_login()
    sender_id = user['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, sender_id, receiver_id, message, file_type, file_path, created_at, status
        FROM messages
        WHERE 
          (sender_id = %s AND receiver_id = %s)
          OR
          (sender_id = %s AND receiver_id = %s)
        ORDER BY created_at
    """, (sender_id, receiver_id, receiver_id, sender_id))

    messages = cursor.fetchall()

    # Mark messages as read
    cursor.execute("""
        UPDATE messages
        SET status = 'read'
        WHERE receiver_id = %s 
          AND sender_id = %s 
          AND status = 'sent'
    """, (sender_id, receiver_id))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(messages)


@chat_bp.route("/messages", methods=["POST"])
def send_message():
    user = require_login()
    sender_id = user['user_id']

    data = request.get_json()
    receiver_id = data.get("receiver_id")
    message = data.get("message", "").strip()

    if not receiver_id or not message:
        return jsonify({"error": "Missing receiver_id or message"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message, created_at, status)
        VALUES (%s, %s, %s, NOW(), 'sent')
    """, (sender_id, receiver_id, message))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})


@chat_bp.route("/messages/upload", methods=["POST"])
def send_file_message():
    user = require_login()
    sender_id = user['user_id']

    receiver_id = request.form.get("receiver_id")
    caption = request.form.get("message", "").strip()
    file = request.files.get("file")

    if not receiver_id or not file:
        return jsonify({"error": "Missing receiver_id or file"}), 400

    allowed_image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
    original_filename = file.filename or "upload"
    ext = os.path.splitext(original_filename)[1].lower()
    file_type = 'image' if ext in allowed_image_exts else 'file'

    import uuid
    safe_name = f"{uuid.uuid4().hex}{ext}"
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'static', 'uploads', 'chat')
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, safe_name)
    file.save(save_path)

    file_path = f"/static/uploads/chat/{safe_name}"
    message_text = caption if caption else (
        "📷 Photo" if file_type == 'image' else f"📎 {original_filename}"
    )

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message, file_type, file_path, created_at, status)
        VALUES (%s, %s, %s, %s, %s, NOW(), 'sent')
    """, (sender_id, receiver_id, message_text, file_type, file_path))
    conn.commit()
    new_id = cursor.lastrowid

    cursor.execute("""
        SELECT id, sender_id, receiver_id, message, file_type, file_path, created_at, status
        FROM messages WHERE id = %s
    """, (new_id,))
    new_msg = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": new_msg})


@chat_bp.route("/unread-count", methods=["GET"])
def get_unread_count():
    user = require_login()
    user_id = user['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT COUNT(*) as unread_count
        FROM messages
        WHERE receiver_id = %s AND status = 'sent'
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"unread_count": result['unread_count']})


@chat_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_details(user_id):
    user = require_login()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT username, email, role, company, army_number
        FROM users 
        WHERE id = %s
    """, (user_id,))
    target_user = cursor.fetchone()
    cursor.close()
    conn.close()

    if target_user:
        return jsonify(target_user)
    return jsonify({"error": "User not found"}), 404


@chat_bp.route("/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    user = require_login()
    user_id = user['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT sender_id, receiver_id FROM messages WHERE id = %s", (message_id,))
    msg = cursor.fetchone()

    if not msg:
        cursor.close()
        conn.close()
        return jsonify({"error": "Message not found"}), 404

    if msg['sender_id'] != user_id and msg['receiver_id'] != user_id:
        cursor.close()
        conn.close()
        return jsonify({"error": "Unauthorized"}), 403

    cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})


@chat_bp.route("/messages/forward", methods=["POST"])
def forward_message():
    user = require_login()
    sender_id = user['user_id']

    data = request.get_json()
    receiver_ids = data.get("receiver_ids", [])
    message_id = data.get("message_id")

    if not receiver_ids or not message_id:
        return jsonify({"error": "Missing parameters"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the original message row and forward it as-is
    cursor.execute(
        "SELECT message, file_type, file_path FROM messages WHERE id = %s",
        (message_id,)
    )
    msg = cursor.fetchone()

    if not msg:
        cursor.close()
        conn.close()
        return jsonify({"error": "Message not found"}), 404

    for rec_id in receiver_ids:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, message, file_type, file_path, created_at, status)
            VALUES (%s, %s, %s, %s, %s, NOW(), 'sent')
        """, (sender_id, rec_id, msg['message'], msg['file_type'], msg['file_path']))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})