FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/node && chmod 0755 /home/node

LABEL Author="any-task-builder"
LABEL Description="n8n Execute Command Node task environment."

RUN cat > /home/node/script.sh <<'EOF'
#!/bin/bash
echo '{"id": 42, "status": "completed"}'
EOF
RUN chmod +x /home/node/script.sh

# Set environment variable to avoid n8n telemetry prompt and configure n8n
ENV N8N_DIAGNOSTICS_ENABLED=false
ENV N8N_PERSONALIZATION_ZERO_TRUST_MODE=true
ENV N8N_USER_FOLDER=/home/node

# Container contents:
#   - Node.js v24 and n8n installed globally
#   - /home/node/script.sh - shell script that outputs JSON

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
