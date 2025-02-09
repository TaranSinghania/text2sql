import logging
from config import Config
from google import genai

class GeminiSQLGenerator:
    """
    Uses the Gemini API (via Google's Generative AI Python client) to convert natural
    language queries into SQL. This version includes schema details in the prompt.
    """
    def __init__(self, schema_manager, api_key: str, model: str = None):
        self.schema_manager = schema_manager
        # Initialize the Gemini client with the API key.
        self.client = genai.Client(api_key=api_key)
        # Use the provided model identifier or default to "gemini-2.0-flash"
        if model is None:
            model = "gemini-2.0-flash"
        self.model = model
        logging.info("Initialized Gemini API client with model: %s", self.model)

    def generate_sql(self, natural_language_query: str, context=None) -> str:
        prompt = self.create_prompt(natural_language_query)
        logging.info("Generated prompt for Gemini API: %s", prompt)
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            raw_sql = response.text
            logging.info("Raw Gemini API output: %s", raw_sql)
            sql_query = self.clean_response(raw_sql)
            logging.info("Cleaned SQL: %s", sql_query)
            return sql_query
        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error("Error calling Gemini API: %s", e)
            return error_msg

    def create_prompt(self, natural_language_query: str) -> str:
        """
        Constructs a prompt that includes the database schema (table names and columns)
        and instructs Gemini to convert the provided natural language query into SQL.
        """
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
            f"{schema_prompt}\n\n"
            f"Convert the following natural language query into SQL for sqllite3:\n"
            f"{natural_language_query}\n"
            f"SQL:"
        )
        print("Prompt: ", prompt)
        return prompt

    def clean_response(self, response_text: str) -> str:
        """
        Cleans the response text by removing newlines, extra spaces, and any leading text that
        starts with "sql " (case-insensitive) or markdown formatting (e.g. "```sql").
        """
        cleaned = response_text.strip().replace("\n", " ")
        # If the response starts with markdown formatting or "sql ", remove that prefix.
        if cleaned.lower().startswith("```"):
            cleaned = cleaned[3:].strip()
            if cleaned.lower().startswith("sqlite"):
                cleaned = cleaned[len("sqlite"):].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
        elif cleaned.lower().startswith("sqlite "):
            cleaned = cleaned[len("sqlite "):].strip()
            
        cleaned = cleaned.strip().replace("\n", " ")
        # If the response starts with markdown formatting or "sql ", remove that prefix.
        if cleaned.lower().startswith("```"):
            cleaned = cleaned[3:].strip()
            if cleaned.lower().startswith("sql"):
                cleaned = cleaned[len("sql"):].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
        elif cleaned.lower().startswith("sql "):
            cleaned = cleaned[len("sql "):].strip()
        return cleaned
