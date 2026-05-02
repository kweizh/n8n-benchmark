FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql postgresql-contrib sudo && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n pm2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="n8n environment with PostgreSQL for database cleanup task."

RUN mkdir -p /home/user/n8n-task && \
    cd /home/user/n8n-task && \
    cat > start.sh <<'EOF'
#!/bin/bash
service postgresql start
export N8N_ENCRYPTION_KEY="testkey"
export N8N_PORT=5678
# Start n8n in background
pm2 start n8n -- start
sleep 5
EOF

RUN chmod +x /home/user/n8n-task/start.sh

# Initialize PostgreSQL database and user as root using su - postgres
RUN service postgresql start && \
    su - postgres -c "psql --command \"CREATE USER n8n_user WITH SUPERUSER PASSWORD 'n8n_pass';\"" && \
    su - postgres -c "createdb -O n8n_user n8n_db" && \
    su - postgres -c "psql -d n8n_db -c \"CREATE TABLE logs (id SERIAL PRIMARY KEY, message TEXT, created_at TIMESTAMP DEFAULT NOW());\"" && \
    su - postgres -c "psql -d n8n_db -c \"INSERT INTO logs (message, created_at) VALUES ('Old log 1', NOW() - INTERVAL '40 days');\"" && \
    su - postgres -c "psql -d n8n_db -c \"INSERT INTO logs (message, created_at) VALUES ('Old log 2', NOW() - INTERVAL '35 days');\"" && \
    su - postgres -c "psql -d n8n_db -c \"INSERT INTO logs (message, created_at) VALUES ('Recent log 1', NOW() - INTERVAL '5 days');\""

# Container contents:
#   - Node.js v24 and n8n installed globally
#   - PostgreSQL installed and configured with n8n_db, n8n_user, and a logs table
#   - /home/user/n8n-task/start.sh to start services

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
