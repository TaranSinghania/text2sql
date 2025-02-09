# app/models/conversation_context.py

import logging

class ConversationContext:
    """
    Manages conversation history for a user session.
    Each turn is stored as a dictionary with keys 'user' and 'system'.
    """
    def __init__(self):
        self.history = []
        logging.info("Initialized new conversation context.")

    def add_turn(self, user_input: str, system_output: str):
        self.history.append({"user": user_input, "system": system_output})
        logging.info("Added conversation turn. User: %s | System: %s", user_input, system_output)

    def get_context(self):
        return self.history
