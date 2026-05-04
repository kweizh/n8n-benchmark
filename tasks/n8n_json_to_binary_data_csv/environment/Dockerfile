FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install n8n -g && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user
RUN mkdir -p /home/node && chmod 0755 /home/node

LABEL Author="any-task-builder"
LABEL Description="n8n environment for JSON to CSV conversion task"

# Container contents:
#   - n8n installed globally via npm
#   - /home/user - base user directory
#   - /home/node - n8n workspace directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
