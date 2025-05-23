# Étape de build frontend
FROM node:18 AS frontend
WORKDIR /app
COPY frontend/ /app/
RUN npm install && npm run build

# Étape finale backend
FROM python:3.11 AS stage-1
WORKDIR /app
COPY backend/ /app/backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]

# ⛔ ICI ça plante
#COPY --from=frontend /app/dist /app/backend/static
