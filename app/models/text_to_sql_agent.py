import logging
import re
import sqlite3
from .nlp_processor import NLProcessor
from .conversation_context import ConversationContext
from .schema_manager import SchemaManager
from .sql_generator import GeminiSQLGenerator
from .feedback_module import FeedbackModule
from app.contex_store import get_context, set_context
from config import Config
from .database import SQLiteDatabase
from .sql_executor import SQLExecutor

class TextToSQLAgent:
    """
    Orchestrates the text-to-SQL conversion process, including conversation management
    and query refinement using the Gemini API.
    In conversion-only mode, the SQL is not executed; instead, a simulated result is returned.
    Before returning a conversion, the agent validates the generated SQL query with Gemini.
    """
    def __init__(self, schema_info: dict, db_file: str, user_id: str,
                 read_only: bool = True, use_dynamic_schema: bool = False, use_gemini: bool = True, 
                 execute_sql: bool = None):
        logging.info("Initializing TextToSQLAgent for user_id: %s", user_id)
        self.nlp = NLProcessor()
        self.conversation_context = ConversationContext()
        if use_dynamic_schema:
            logging.info("Using dynamic schema introspection.")
            self.schema_manager = SchemaManager(db_file=db_file, use_dynamic_schema=True)
        else:
            logging.info("Using static schema information.")
            self.schema_manager = SchemaManager(schema_info)
        logging.info("Using Gemini API for text-to-SQL conversion.")
        self.sql_generator = GeminiSQLGenerator(
            self.schema_manager,
            api_key=Config.GEMINI_API_KEY,
            model=Config.GEMINI_MODEL
        )
        self.execute_sql = execute_sql if execute_sql is not None else Config.EXECUTE_SQL
        if self.execute_sql:
            self.db_layer = SQLiteDatabase(db_file, read_only=read_only)
            self.executor = SQLExecutor(self.db_layer, self.sql_generator)
        else:
            self.executor = None
        self.feedback_module = FeedbackModule(self.schema_manager, self.sql_generator)
        self.user_id = user_id
        logging.info("TextToSQLAgent initialized successfully.")

    def simulate_result(self, sql_query: str) -> dict:
        """
        Simulates a query result based on the generated SQL.
        This function parses the SELECT clause to determine the columns.
        If '*' is used, returns all columns from the table schema;
        otherwise, returns dummy rows for the selected columns.
        """
        match = re.search(r'select\s+(.*?)\s+from\s+(\w+)', sql_query, re.IGNORECASE)
        if match:
            columns_text = match.group(1).strip()
            table_name = match.group(2).strip().lower()
            logging.info("Parsed SELECT columns: %s, table: %s", columns_text, table_name)
            schema = self.schema_manager.get_schema()
            table_schema = schema.get(table_name, {})
            all_columns = table_schema.get("columns", [])
            if columns_text == "*" or columns_text == "*,":  # Wildcard selection
                columns = all_columns
            else:
                columns = [col.strip() for col in columns_text.split(",")]
            # For simulation, return dummy rows.
            dummy_rows = []
            for i in range(2):
                row = []
                for col in columns:
                    if "id" in col.lower():
                        row.append(i + 1)
                    else:
                        row.append(f"dummy_{col}_{i+1}")
                dummy_rows.append(row)
            simulated_result = {"columns": columns, "rows": dummy_rows}
            logging.info("Simulated result: %s", simulated_result)
            return simulated_result
        else:
            logging.info("Could not parse SELECT clause. Returning empty result.")
            return {"columns": [], "rows": []}

    def validate_query(self, sql_query: str) -> dict:
        """
        Validates the generated SQL query using the Gemini API.
        The prompt includes the database schema and the SQL query.
        If the query is valid, Gemini should return "yes".
        Otherwise, Gemini returns a brief explanation and a prompt to help the user.
        """
        schema = self.schema_manager.get_schema()
        schema_lines = ["Database Schema:"]
        for table, info in schema.items():
            columns = info.get("columns", [])
            schema_lines.append(f"Table '{table}': {', '.join(columns)}")
        schema_prompt = "\n".join(schema_lines)
        prompt = (
            f"{schema_prompt}\n\n"
            f"Given the SQL query:\n{sql_query}\n\n"
            f"Is this query valid according to the above schema? "
            f"If valid, reply only with 'yes'. If invalid, provide a brief explanation and a prompt to help the user fix it."
        )
        logging.info("Validation prompt: %s", prompt)
        try:
            response = self.sql_generator.client.models.generate_content(
                model=self.sql_generator.model,
                contents=prompt
            )
            validation_text = response.text.strip()
            logging.info("Validation response: %s", validation_text)
            return {"validation": validation_text}
        except Exception as e:
            error_msg = f"Validation error: {e}"
            logging.error(error_msg)
            return {"validation": error_msg}

    def process_query(self, user_input: str) -> dict:
        logging.info("Processing query for user_id: %s", self.user_id)
        self.conversation_context.history = get_context(self.user_id)
        if self.conversation_context.history:
            logging.info("Loaded existing conversation context for user_id: %s", self.user_id)
        else:
            logging.info("No existing conversation context found for user_id: %s", self.user_id)
        parsed_query = self.nlp.parse(user_input)
        normalized_query = self.nlp.normalize_terms(parsed_query, self.schema_manager)
        logging.info("Normalized query: %s", normalized_query)
        sql_query = self.sql_generator.generate_sql(normalized_query, context=self.conversation_context.get_context())
        if sql_query.startswith("Error:"):
            logging.error("Gemini API returned an error: %s", sql_query)
            return {"sql": sql_query, "result": None, "schema": [], "error": sql_query}
        
        # Validate the generated SQL query.
        validation = self.validate_query(sql_query)
        if validation.get("validation", "").strip().lower() != "yes":
            # Return an error response with the validation message.
            logging.error("Validation failed: %s", validation.get("validation"))
            return {"sql": sql_query, "result": None, "schema": [], "error": validation.get("validation")}
        
        # In conversion-only mode, simulate the result; otherwise, execute the query.
        if not Config.EXECUTE_SQL or self.executor is None:
            result = self.simulate_result(sql_query)
        else:
            try:
                result = self.executor.execute(sql_query)
            except Exception as e:
                logging.error("Error executing SQL query: %s", e)
                return {"sql": sql_query, "result": None, "schema": [], "error": str(e)}
        self.conversation_context.add_turn(user_input, sql_query)
        set_context(self.user_id, self.conversation_context.get_context())
        schema_for_result = result.get("columns", []) if isinstance(result, dict) else []
        logging.info("Query processed for user_id: %s", self.user_id)
        return {"sql": sql_query, "result": result, "schema": schema_for_result}

    def refine_query(self, feedback: str) -> dict:
        logging.info("Refining query for user_id: %s with feedback: %s", self.user_id, feedback)
        self.conversation_context.history = get_context(self.user_id)
        if self.conversation_context.history:
            last_turn = self.conversation_context.history[-1]
            current_sql = last_turn.get("system")
            refined_sql = self.feedback_module.refine_query(current_sql, feedback, context=self.conversation_context.get_context())
            # Validate the refined SQL query.
            validation = self.validate_query(refined_sql)
            if validation.get("validation", "").strip().lower() != "yes":
                logging.error("Validation failed for refinement: %s", validation.get("validation"))
                return {"sql": refined_sql, "result": None, "schema": [], "error": validation.get("validation")}
            if not Config.EXECUTE_SQL or self.executor is None:
                result = self.simulate_result(refined_sql)
            else:
                try:
                    result = self.executor.execute(refined_sql)
                except Exception as e:
                    logging.error("Error executing SQL query: %s", e)
                    return {"sql": refined_sql, "result": None, "schema": [], "error": str(e)}
            self.conversation_context.add_turn(feedback, refined_sql)
            set_context(self.user_id, self.conversation_context.get_context())
            schema_for_result = result.get("columns", []) if isinstance(result, dict) else []
            logging.info("Query refinement complete for user_id: %s", self.user_id)
            return {"sql": refined_sql, "result": result, "schema": schema_for_result}
        else:
            logging.error("No previous query to refine for user_id: %s", self.user_id)
            return {"sql": None, "result": None, "schema": [], "error": "No previous query to refine."}
