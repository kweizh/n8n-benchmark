# n8n Switch Node Routing

## Background
You have n8n installed globally. Create an n8n workflow that routes incoming webhook data using a Switch node based on a specific field, and returns a custom response.

## Requirements
1. Start n8n using `n8n start` (runs on port 5678) and open the UI in your browser.
2. Create a new workflow with a **Webhook** node listening on `POST /webhook/route-items`.
3. The Webhook node must be configured to respond using a "Respond to Webhook" node.
4. Connect the Webhook node to a **Switch** node. The Switch node should evaluate the `status` field from the webhook body (e.g., `{{ $json.body.status }}`).
5. The Switch node should have 4 outputs based on the `status` value:
   - If `status` equals `active`, route to an **Edit Fields (Set)** node that sets `category = "A"`.
   - If `status` equals `pending`, route to an **Edit Fields (Set)** node that sets `category = "B"`.
   - If `status` equals `inactive`, route to an **Edit Fields (Set)** node that sets `category = "C"`.
   - For any other value (fallback), route to an **Edit Fields (Set)** node that sets `category = "Unknown"`.
6. All Edit Fields (Set) nodes must connect to a single **Respond to Webhook** node.
7. The **Respond to Webhook** node should return the JSON from the Set node (which includes the `category` field).
8. Save and **Activate** the workflow.
9. Finally, export the workflow to `/home/user/workflow.json` using the command:
   `n8n export:workflow --all --output=/home/user/workflow.json`

## Constraints
- Project path: /home/user
- Exported file: /home/user/workflow.json
- The Switch node must use the exact strings: "active", "pending", "inactive".
- The Edit Fields (Set) nodes must set the `category` string exactly as specified ("A", "B", "C", "Unknown").