# Multi-stage build for minimal image size
FROM python:3.12-alpine3.19 AS builder

# Build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev

WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# Runtime stage
FROM python:3.12-alpine3.19

LABEL maintainer="llms-os@example.com" \
      version="2.0.0" \
      description="Enhanced LLMs_OS with monitoring"

# Install runtime dependencies
RUN apk add --no-cache libffi openssl curl && \
    adduser -D -u 1000 appuser

WORKDIR /app

# Copy wheels and install
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=appuser:appuser ./src/ /app/
RUN pip install --no-cache-dir -e /app

# Security: Run as non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import LLMs_OS; print('healthy')" || exit 1

ENTRYPOINT ["llms-os"]
CMD ["--help"]
