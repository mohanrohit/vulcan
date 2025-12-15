FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run as non-root user for security
RUN useradd --create-home apiuser && chown -R apiuser:apiuser /app

USER apiuser

EXPOSE 5000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "main:app"]
