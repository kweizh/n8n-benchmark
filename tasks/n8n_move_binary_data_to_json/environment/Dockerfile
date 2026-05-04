FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="n8n workflow task for extracting binary data to JSON."

RUN mkdir -p /home/user/workspace && \
    cd /home/user/workspace && \
    echo "Hello, n8n world!" > input.txt && \
    cat > workflow.json <<'EOF'
{
  "id": "my-test-workflow-123",
  "name": "Extract Text Workflow",
  "nodes": [
    {
      "parameters": {},
      "id": "manual-trigger",
      "name": "When clicking 'Test workflow'",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [180, 240]
    },
    {
      "parameters": {
        "operation": "read",
        "fileSelector": "/home/user/workspace/input.txt",
        "options": {}
      },
      "id": "read-file",
      "name": "Read File",
      "type": "n8n-nodes-base.readWriteFile",
      "typeVersion": 1,
      "position": [400, 240]
    }
  ],
  "connections": {
    "When clicking 'Test workflow'": {
      "main": [
        [
          {
            "node": "Read File",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
EOF

# Container contents:
#   - Node.js v24 and n8n installed globally.
#   - /home/user/workspace  — n8n project directory
#   - input.txt containing the test string
#   - workflow.json with the initial nodes

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
