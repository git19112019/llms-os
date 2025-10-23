FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    Flask==3.0.0 \
    Flask-CORS==4.0.0 \
    requests==2.31.0 \
    redis==5.0.1 \
    prometheus-client==0.19.0

COPY app.py .

EXPOSE 8000

# Health endpoint
HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-u", "app.py"]
