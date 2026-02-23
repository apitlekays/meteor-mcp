FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["python", "server.py"]
