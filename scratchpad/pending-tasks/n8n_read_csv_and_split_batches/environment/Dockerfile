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

LABEL Author="any-task-builder"
LABEL Description="n8n task environment with n8n installed globally and a sample CSV data file in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >data.csv <<'EOF'
id,name,email
1,Alice,alice@example.com
2,Bob,bob@example.com
3,Charlie,charlie@example.com
4,David,david@example.com
5,Eve,eve@example.com
6,Frank,frank@example.com
7,Grace,grace@example.com
8,Heidi,heidi@example.com
9,Ivan,ivan@example.com
10,Judy,judy@example.com
11,Mallory,mallory@example.com
12,Niaj,niaj@example.com
13,Olivia,olivia@example.com
14,Peggy,peggy@example.com
15,Sybil,sybil@example.com
EOF

# Container contents:
#   - Node.js v20 and n8n installed globally.
#   - /home/user/myproject  — project directory
#   - /home/user/myproject/data.csv — sample CSV file

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
