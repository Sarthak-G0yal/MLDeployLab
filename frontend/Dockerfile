FROM python:3.11-slim

WORKDIR /frontend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV BACKEND_API_URL=http://localhost:8000

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address=0.0.0.0"]