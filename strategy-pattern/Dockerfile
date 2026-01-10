# Multi-stage Dockerfile for Strategy Pattern Demo
FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend
COPY frontend/ ./frontend/

# Expose ports for backend and frontend
EXPOSE 8000 8080

# Create a startup script
RUN echo '#!/bin/bash\n\
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend && python3 -m http.server 8080\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
