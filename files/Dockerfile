FROM python:3.11-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files (exclude venv if present)
COPY . .

EXPOSE 5000

# Use unbuffered stdout for logs
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
