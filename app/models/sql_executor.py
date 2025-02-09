import logging
from google import genai

class SQLExecutor:
    """
    Executes SQL queries via a provided database abstraction layer.
    First, it uses the Gemini API (through the provided GeminiSQLGenerator) to
    validate and clean up the SQL query. Then it executes the cleaned query.
    Returns a dictionary containing the cleaned SQL query and the execution result.
    """
    def __init__(self, db_layer, sql_generator):
        self.db_layer = db_layer
        self.sql_generator = sql_generator

    def execute(self, query: str) -> dict:
        logging.info("SQLExecutor received query for execution.")
        try:
            # Build a prompt to ask Gemini to validate and clean the SQL query.
            validation_prompt = (
                "Return only the SQL statement! Please validate and clean / fix the following SQL query and return only the cleaned SQL:\n" +
                query
            )
            logging.info("Validation prompt for SQLExecutor: %s", validation_prompt)
            # Call Gemini using the pre-initialized client from the gemini_generator.
            response = self.sql_generator.client.models.generate_content(
                model=self.sql_generator.model,
                contents=validation_prompt
            )
            
            # Clean the response.
            cleaned_query = self.sql_generator.clean_response(response.text)
            
            logging.info("SQLExecutor cleaned query: %s", cleaned_query)
            # Execute the cleaned query using the database layer.
            result = self.db_layer.execute_query(cleaned_query)
            logging.info("SQLExecutor executed cleaned query, result: %s", result)
            # Return both the cleaned query and the result.
            return result
        except Exception as e:
            logging.error("SQLExecutor encountered an error: %s", e)
            raise
