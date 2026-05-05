# Database Cleanup Workflow Report

## Summary
The Database Cleanup Workflow has been successfully created and activated in n8n.

## Workflow Details
- **Name**: Database Cleanup Workflow
- **Trigger**: Schedule Trigger
  - **Schedule**: Daily at 3:00 AM (Cron: `0 3 * * *`)
- **Action**: Postgres Node
  - **Operation**: Execute Query
  - **SQL**: `DELETE FROM logs WHERE created_at < NOW() - INTERVAL '30 days';`
  - **Credentials**: `postgres_creds` (Localhost:5432, n8n_db)

## Status
- **Credentials**: Imported (ID: 1)
- **Workflow**: Imported and Activated (ID: 1)
- **Services**: PostgreSQL and n8n are running.
