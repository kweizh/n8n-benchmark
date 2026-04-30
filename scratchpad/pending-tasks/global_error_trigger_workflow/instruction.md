Robust n8n deployments require global error monitoring to catch execution failures across all workflows and alert developers.

You need to create a minimal n8n workflow JSON that uses an Error Trigger to catch workflow failures and formats the failed execution ID and error message into a structured JSON payload in the n8n visual editor environment.

**Constraints:**
- The trigger node MUST be an official n8n Error Trigger (`n8n-nodes-base.errorTrigger`).
- You MUST extract the `execution.id` and `error.message` from the error trigger's output using valid n8n expressions.
- The output MUST be a valid n8n workflow JSON definition.