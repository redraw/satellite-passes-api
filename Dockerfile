FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
CMD gunicorn main:api -b 0.0.0.0:8000 --access-logfile - --error-logfile -
