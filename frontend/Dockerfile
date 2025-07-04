FROM python:3.12.11-slim-bookworm

WORKDIR /frontend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV BACKEND_API_URL=http://localhost:8000

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address=0.0.0.0"]