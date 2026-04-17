"""
HRMS Chatbot - Natural language interface to HRMS database.
Answers any question about personnel, leave, weight, loans, tasks, etc.
Uses db_config.py for database connection.
"""
from chatbot.routes import chatbot_bp

__all__ = ["chatbot_bp"]
