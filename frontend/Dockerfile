FROM python:3.10-slim

WORKDIR /frontend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./frontend ./frontend

ENV BACKEND_API_URL=http://backend:8000

EXPOSE 8501

CMD ["streamlit", "run", "./frontend/main.py", "--server.port", "8501", "--server.address=0.0.0.0"]
