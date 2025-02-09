import logging
from config import Config

class FeedbackModule:
    """
    Uses the Gemini API (via the provided SQL generator) to refine an existing SQL query based on user feedback.
    """
    def __init__(self, schema_manager, sql_generator):
        self.schema_manager = schema_manager
        self.sql_generator = sql_generator
        logging.info("FeedbackModule initialized using Gemini for refinement.")

    def refine_query(self, current_sql: str, feedback: str, context=None) -> str:
        # Construct a prompt that includes the current SQL and the feedback.
        if Config.EXECUTE_SQL:
            schema = self.schema_manager.get_schema()
            schema_lines = ["Database Schema:"]
            for table, info in schema.items():
                columns = info.get("columns", [])
                schema_lines.append(f"Table '{table}': {', '.join(columns)}")
            schema_prompt = "\n".join(schema_lines)
        else:
            schema_prompt = ""
        prompt = (
            "Never include explaination, just give me the result. The current SQL query is:\n"
            f"{current_sql}\n\n"
            "and the schema is:\n"
            f"{schema_prompt}\n\n"
            "Based on the following feedback, refine the SQL query for sqllite3:\n"
            f"Feedback: {feedback}\n\n"
            "Refined SQL:"
        )
        # Optionally add any additional context (e.g., conversation history).
        # if context:
        #     prompt = "Context:\n" + "\n".join(context) + "\n\n" + prompt
        logging.info("Generated refinement prompt: %s", prompt)
        try:
            # Use the pre-initialized Gemini client from the SQL generator.
            response = self.sql_generator.client.models.generate_content(
                model=self.sql_generator.model,
                contents=prompt
            )
            raw_refined = response.text
            logging.info("Raw Gemini refinement output: %s", raw_refined)
            refined_sql = self.sql_generator.clean_response(raw_refined)
            logging.info("Cleaned refined SQL: %s", refined_sql)
            return refined_sql
        except Exception as e:
            error_msg = f"Error during refinement: {e}"
            logging.error(error_msg)
            return error_msg


