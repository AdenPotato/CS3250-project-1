FROM python:3.12-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy templates and static files to where Flask expects them (relative to WORKDIR /app/src)
COPY templates/ ./src/templates/
COPY static/ ./src/static/

WORKDIR /app/src
ENV FLASK_APP=app
EXPOSE 5000

# Seed database and serve Flask app
CMD ["sh", "-c", "python init_db.py && flask run --host=0.0.0.0 --port=5000"]
