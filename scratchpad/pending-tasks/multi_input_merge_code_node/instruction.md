Workflows often need to combine data from multiple API requests, but developers struggle with data persistence across different node branches.

You need to write a JavaScript Code node script that takes data from two different input connections (Input 0: Users, Input 1: Orders) and merges them into a single array of items based on a matching `user_id` in the n8n Code node environment.

**Constraints:**
- You MUST access data from both input streams using `$input.all(0)` and `$input.all(1)`.
- Do NOT use the built-in n8n Merge node; the joining logic must be handled entirely within the custom JavaScript code.
- The final returned output MUST strictly follow the n8n data model (`[{json: {...}}]`).