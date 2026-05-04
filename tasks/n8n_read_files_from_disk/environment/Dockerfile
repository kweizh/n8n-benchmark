FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

# Set n8n to allow external modules if needed, and to avoid asking for telemetry
ENV N8N_DIAGNOSTICS_ENABLED=false \
    N8N_PERSONALIZATION_ZERO_TRUST_MODE=true

LABEL Author="any-task-builder"
LABEL Description="n8n environment installed globally via npm with test data."

RUN mkdir -p /home/user/data && \
    echo "id,value\n1,100\n2,200" > /home/user/data/report.csv && \
    echo "This is a summary." > /home/user/data/summary.txt && \
    echo "fake png data" > /home/user/data/logo.png

# Container contents:
#   - Node.js v20
#   - n8n installed globally
#   - /home/user project path
#   - /home/user/data with test files

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]