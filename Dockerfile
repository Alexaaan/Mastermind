# Stage frontend
FROM node:18 AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build     # génère /app/dist

# Stage backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/ ./backend

# Ajoute cette ligne pour créer le dossier
RUN mkdir -p ./backend/static

COPY --from=frontend /app/dist ./backend/static
EXPOSE 8000
CMD ["uvicorn","backend.app:app","--host","0.0.0.0","--port","8000"]
