from flask import Flask,redirect,request
import jwt
JWT_SECRET = "MY_SUPER_SECRET_KEY_123"      # change this later
JWT_ALGO = "HS256"
def require_login():
    """Check if user is logged in via JWT token"""
    token = request.cookies.get('token')
    
    if not token:
        return None  # Not logged in
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload  # Returns user dict with role, username, etc.
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    except Exception as e:
        print(f"JWT decode error: {e}")
        return None