FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="n8n environment with a prepared workflow.json containing a Python code node."

RUN cat >/home/user/workflow.json <<'EOF'
{
  "name": "Date Math Workflow",
  "nodes": [
    {
      "parameters": {},
      "name": "Start",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "keepOnlySet": true,
        "values": {
          "string": [
            {"name": "startDate", "value": "2023-10-01"},
            {"name": "endDate", "value": "2023-10-10"}
          ]
        },
        "options": {}
      },
      "name": "Mock Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [460, 300]
    },
    {
      "parameters": {
        "language": "python",
        "pythonCode": "# Write your Python code here\n# It should calculate the difference in days between startDate and endDate\n# and store it in a new field called 'days_difference'\n\nitems = _input.all()\nreturn items\n"
      },
      "name": "Calculate Days",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [680, 300]
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [{"node": "Mock Data", "type": "main", "index": 0}]
      ]
    },
    "Mock Data": {
      "main": [
        [{"node": "Calculate Days", "type": "main", "index": 0}]
      ]
    }
  },
  "active": false,
  "settings": {},
  "versionId": "1"
}
EOF

# Container contents:
#   - always required libs: curl wget ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v20 and n8n installed globally
#   - /home/user/workflow.json - the target n8n workflow with a Python code node

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]