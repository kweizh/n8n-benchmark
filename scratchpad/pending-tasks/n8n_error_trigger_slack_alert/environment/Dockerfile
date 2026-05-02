FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/workspace && chmod 0755 /home/user/workspace && \
    mkdir -p /logs/artifacts && echo "local-trial-123" > /logs/artifacts/trial_id

LABEL Author="any-task-builder"
LABEL Description="n8n task environment with Node.js v24 and n8n installed globally."

# Container contents:
#   - always required libs: curl wget ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 and n8n installed globally
#   - /home/user/workspace: base directory for the project
#   - /logs/artifacts/trial_id: mock trial ID file

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
