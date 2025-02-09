# app/models/nlp_processor.py

import re
import logging

class NLProcessor:
    """
    Minimal NLP processor that trims input and normalizes schema terms.
    """
    def parse(self, text: str) -> str:
        parsed = text.strip()
        logging.debug("Parsed text: %s", parsed)
        return parsed

    def normalize_terms(self, text: str, schema_manager) -> str:
        logging.info("Normalizing terms for text: %s", text)
        schema = schema_manager.get_schema()
        for table in schema.keys():
            plural = table + "s"
            pattern = re.compile(r"\b" + re.escape(plural) + r"\b", re.IGNORECASE)
            if pattern.search(text):
                corrected = schema_manager.correct_term(plural, list(schema.keys()))
                text = pattern.sub(corrected, text)
                logging.info("Normalized '%s' to '%s'", plural, corrected)
        return text
