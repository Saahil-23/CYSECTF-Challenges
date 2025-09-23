FROM alpine:latest

# Install dependencies
RUN apk add --no-cache python3 bash

# Create challenge user for security
RUN adduser -D -s /bin/bash ctfuser

# Create challenge directory
RUN mkdir /challenge && chown ctfuser:ctfuser /challenge

WORKDIR /challenge
COPY --chown=ctfuser:ctfuser . .

# Switch to non-root user
USER ctfuser

# Make script executable
RUN chmod +x server.py

# Run in background mode
CMD ["python3", "server.py"]