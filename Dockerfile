# --- STAGE 1 : Build Frontend ---
FROM node:18 AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build     # Génère /app/dist

# --- STAGE 2 : Backend avec Python ---
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend code
COPY backend/ ./backend

# Create static folder and copy frontend build
RUN mkdir -p ./backend/static
COPY --from=frontend /app/dist ./backend/static

# Expose port and start FastAPI with Uvicorn
EXPOSE 8000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
