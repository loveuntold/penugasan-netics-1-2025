FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt
COPY . .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/deps /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]