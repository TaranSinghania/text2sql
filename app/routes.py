import logging
from flask import Blueprint, request, jsonify, render_template
from app.models.text_to_sql_agent import TextToSQLAgent
from config import Config

bp = Blueprint('routes', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_id = data.get("user_id")
    user_query = data.get("query")
    if not user_id or not user_query:
        logging.error("Missing user_id or query parameter in /query request.")
        return jsonify({"error": "Missing user_id or query parameter"}), 400
    logging.info("Received /query request from user_id=%s", user_id)
    # Optionally override read_only and execute_sql from payload.
    execute_sql = data.get("execute_sql")
    read_only = data.get("read_only", Config.READ_ONLY)
    agent = TextToSQLAgent(
        schema_info=Config.STATIC_SCHEMA_INFO,
        db_file=Config.DB_FILE,
        user_id=user_id,
        read_only=read_only,
        use_dynamic_schema=Config.USE_DYNAMIC_SCHEMA,
        use_gemini=True,
        execute_sql=execute_sql
    )
    response_data = agent.process_query(user_query)
    logging.info("Processed query for user_id=%s. Generated SQL: %s", user_id, response_data["sql"])
    return jsonify(response_data), 200

@bp.route('/refine', methods=['POST'])
def refine():
    data = request.get_json()
    user_id = data.get("user_id")
    feedback = data.get("feedback")
    if not user_id or not feedback:
        logging.error("Missing user_id or feedback parameter in /refine request.")
        return jsonify({"error": "Missing user_id or feedback parameter"}), 400
    logging.info("Received /refine request from user_id=%s with feedback: %s", user_id, feedback)
    execute_sql = data.get("execute_sql")
    read_only = data.get("read_only", Config.READ_ONLY)
    agent = TextToSQLAgent(
        schema_info=Config.STATIC_SCHEMA_INFO,
        db_file=Config.DB_FILE,
        user_id=user_id,
        read_only=read_only,
        use_dynamic_schema=Config.USE_DYNAMIC_SCHEMA,
        use_gemini=True,
        execute_sql=execute_sql
    )
    response_data = agent.refine_query(feedback)
    if response_data.get("sql") is None:
        logging.error("No previous query found to refine for user_id=%s", user_id)
        return jsonify({"error": "No previous query to refine"}), 400
    logging.info("Refined SQL for user_id=%s: %s", user_id, response_data["sql"])
    return jsonify(response_data), 200
