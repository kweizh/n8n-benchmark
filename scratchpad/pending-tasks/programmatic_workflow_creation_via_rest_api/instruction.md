The n8n REST API enables programmatic management and deployment of workflows across different self-hosted environments.

You need to write a `curl` command that programmatically creates a new n8n workflow using the n8n REST API in a standard terminal environment.

**Constraints:**
- You MUST target the `POST /api/v1/workflows` endpoint.
- You MUST authenticate the request by including the `X-N8N-API-KEY` header.
- You MUST provide a valid JSON body payload containing at minimum a `name` string and an empty `nodes` array for the new workflow.