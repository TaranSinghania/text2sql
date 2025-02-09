# text2sql

A production-inspired text-to-SQL conversion application that leverages the Gemini API to convert natural language queries into SQL. The application supports multi-turn conversations, query refinement, and safeguards against destructive operations using read-only mode. Conversation context is stored in Redis, and conversion logs are stored in a SQLite database.

## Improvements and WIP

- Completely integrate redis
- Dockerize the application
- Use locally hosted models instead of Gemini
- Clean up and dynamic DB initialization (migrations, etc.)
## Requirements

- Python 3.9 or later  
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional, but recommended)  
- Redis (for conversation context; can be run locally or via Docker)  
- SQLite (bundled with Python)
- Gemini API Key (free - https://ai.google.dev/gemini-api/docs/api-key)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/text-to-sql-chat.git
   cd text-to-sql-chat```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate```
  
3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt```

4. **Configure the Application**

   ```Replace your gemini key in config.py```

5. **Run Redis**

   ```bash
   docker run -d -p 6379:6379 --name redis redis:6
   ```

6. **Initialise DB**

   ```bash
   sqlite3 example.db < init_db.sql  
   ```

7. **Run the Application**

   ```bash
   python run.py
   ```

## Running the tests

1. **Initialise test db**

   ```bash
   sqlite3 example.db < tests/test_db.sql  
   ```

2. **Run the test suite**

   ```bash
   pytest --maxfail=1 --disable-warnings -q
