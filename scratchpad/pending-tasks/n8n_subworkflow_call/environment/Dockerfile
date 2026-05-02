FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n@1.82.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/n8n_project && chmod 0755 /home/user/n8n_project

ENV N8N_USER_FOLDER=/home/user/.n8n

LABEL Author="any-task-builder"
LABEL Description="n8n environment installed globally via npm for testing workflow creation."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
