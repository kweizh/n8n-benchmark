# Database Cleanup with n8n

## Background
You need to automate the cleanup of old logs in a PostgreSQL database using an n8n workflow. The workflow should run on a daily schedule and delete records older than 30 days.

## Requirements
1. Start the necessary services (PostgreSQL and n8n) by running `/home/user/n8n-task/start.sh`.
2. Create an n8n workflow named `Database Cleanup Workflow`.
3. The workflow must contain a Schedule Trigger node (`n8n-nodes-base.scheduleTrigger`) configured to run daily at 3:00 AM (using the cron expression `0 3 * * *`).
4. The workflow must contain a Postgres node (`n8n-nodes-base.postgres`) connected to the Schedule Trigger.
5. The Postgres node must use the `executeQuery` operation to execute the following SQL query: `DELETE FROM logs WHERE created_at < NOW() - INTERVAL '30 days';`.
6. The Postgres node must be configured to use a credential named `postgres_creds` connecting to `localhost:5432` with database `n8n_db`, user `n8n_user`, and password `n8n_pass`.
7. Save and activate the workflow. Since you are running headless, you can use the n8n CLI (`n8n import:workflow`, `n8n import:credentials`) or the n8n REST API to create and activate the workflow.

## Constraints
- Project path: `/home/user/n8n-task`
- Start command: `/home/user/n8n-task/start.sh`
- The n8n instance runs on port 5678.

## Integrations
- None