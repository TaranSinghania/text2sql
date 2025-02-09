# run.py
import logging
from app import create_app

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Starting the Flask application in DEBUG mode...")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
