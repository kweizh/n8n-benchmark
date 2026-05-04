FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="n8n environment with an initial workflow.json containing a Manual Trigger and an Edit Fields node."

RUN cd /home/user && \
    cat >workflow.json <<'EOF'
{
  "nodes": [
    {
      "parameters": {},
      "id": "e2f6b8a1-1c2d-4e3f-9a8b-7c6d5e4f3a2b",
      "name": "When clicking 'Execute Workflow'",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [ 250, 300 ]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "12345678-1234-1234-1234-123456789012",
              "name": "inputString",
              "value": "n8n_is_awesome",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "id": "f3e7c9b2-2d3e-5f4a-0b9c-8d7e6f5a4b3c",
      "name": "Edit Fields",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [ 450, 300 ]
    }
  ],
  "connections": {
    "When clicking 'Execute Workflow'": {
      "main": [
        [
          {
            "node": "Edit Fields",
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
#   - /home/user/workflow.json with the initial workflow setup.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]