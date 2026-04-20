from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    Blueprint,
    redirect,
    url_for,
    flash,
    make_response,
    send_file,
    Request,
    current_app
)

from datetime import datetime, date, timedelta

from xhtml2pdf import pisa
from io import BytesIO
from middleware import require_login

import mysql.connector
from mysql.connector import Error
import mysql

from db_config import get_db_connection
import re
import json
import os
import pandas as pd
from datetime import datetime
from decimal import Decimal

from middleware import require_login, jwt, JWT_ALGO, JWT_SECRET

from blueprints.personal_information import personnel_info
from blueprints.weight_ms import weight_ms
from blueprints.apply_leave import leave_bp
from blueprints.dashboard import dashboard_bp
from blueprints.task_manager import task_bp
from blueprints.account_management import accounts_bp
from blueprints.weight_ms import compute_authorization
from blueprints.loan import loan_bp
from blueprints.roll_call import roll_call_bp
from blueprints.add_user import add_user_bp
from blueprints.update_interview_status import inteview_bp
from blueprints.oncourses import oncourses_bp
from apscheduler.schedulers.background import BackgroundScheduler
from blueprints.dues_in_out import dues_bp
from blueprints.agniveer_asst import agniveer_bp
from blueprints.chat import chat_bp
from blueprints.project import projects_bp

from blueprints.ollama import ollama_bot_bp
from blueprints.onco_leave import onco_leave_bp
from blueprints.sensitive_persons import sensitive_bp
