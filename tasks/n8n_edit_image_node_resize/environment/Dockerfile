FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash graphicsmagick && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/node && chmod 0755 /home/node

LABEL Author="any-task-builder"
LABEL Description="n8n environment with GraphicsMagick for Edit Image node testing"

# Create a 200x200 test image using GraphicsMagick
RUN gm convert -size 200x200 xc:red /home/node/input.png

ENV N8N_USER_FOLDER=/home/node
ENV WEBHOOK_URL=http://localhost:5678/

# Container contents:
#   - Node.js 20 and n8n installed globally.
#   - GraphicsMagick installed for Edit Image node.
#   - /home/node/input.png - 200x200 test image.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
