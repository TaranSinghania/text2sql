# Dockerfile

FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies: sqlite3, curl, etc.
RUN apt-get update && apt-get install -y sqlite3 curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application.
COPY . /app/

# Copy and set execute permissions for the entrypoint script.
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

CMD ["/app/entrypoint.sh"]
