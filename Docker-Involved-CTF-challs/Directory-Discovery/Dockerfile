FROM alpine:latest

# Install Python and Flask using Alpine packages
RUN apk add --no-cache python3 py3-flask

# Create non-root user
RUN adduser -D -s /bin/sh ctfuser

WORKDIR /app

# Copy application files
COPY --chown=ctfuser:ctfuser app.py .

USER ctfuser

EXPOSE 9676

CMD ["python3", "app.py"]