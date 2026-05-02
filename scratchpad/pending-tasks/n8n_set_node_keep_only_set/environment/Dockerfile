FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/workspace && chmod 0755 /home/user/workspace

LABEL Author="any-task-builder"
LABEL Description="n8n workflow environment for testing the Set node Keep Only Set functionality."

# Container contents:
#   - Node.js v20 and n8n installed globally.
#   - /home/user/workspace - empty directory for the workflow file.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
