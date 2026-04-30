An n8n workflow receives incoming JSON payloads via a Webhook node, but currently returns empty responses causing client timeouts.

You need to write an n8n workflow JSON definition that triggers on a webhook, adds a `received_at` timestamp to the incoming payload using n8n's Luxon expression syntax, and responds synchronously with the modified data in the n8n visual editor environment. 

**Constraints:**
- The Webhook node's "Response Mode" MUST be explicitly configured to return data from the Last Node (e.g., "Last Node" or "When Last Node Finishes").
- The timestamp MUST be generated using the `{{ $now }}` expression.
- The output MUST be a valid n8n workflow JSON array.