FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash unzip && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="n8n environment with multiple files to be compressed into a ZIP archive."

RUN echo "Content of file 1" > /home/user/file1.txt && \
    echo "Content of file 2" > /home/user/file2.txt && \
    mkdir -p /home/user/output && \
    chmod -R 0777 /home/user

ENV N8N_USER_FOLDER=/home/user/.n8n

# Container contents:
#   - n8n installed globally via npm
#   - /home/user/file1.txt and /home/user/file2.txt
#   - /home/user/output directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
