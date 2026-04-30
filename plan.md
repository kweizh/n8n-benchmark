# Evaluation Dataset Research: n8n (n8n.io)
This research document provides technical details, API usage, and common developer challenges for n8n, a powerful low-code workflow automation platform. It is designed to assist in creating high-quality evaluation datasets and benchmark tasks for AI coding agents.
---
### 1. Library Overview
*   **Description**: n8n is a "fair-code" licensed workflow automation tool that allows users to connect various applications, APIs, and databases. It uses a node-based visual editor and supports custom logic via JavaScript and Python.
*   **Ecosystem Role**: It serves as the "glue" in modern tech stacks, competing with Zapier and Make but offering superior self-hosting capabilities, data privacy, and extensibility through code.
*   **Project Setup**:
    *   **Local (npm)**: 
        ```bash
        npm install n8n -g
        n8n start
        ```
    *   **Docker (Recommended)**:
        ```bash
        docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
        ```
    *   **Development**: Clone the repo, `npm install`, `npm run build`, `npm start`.
---
### 2. Core Primitives & APIs
#### A. Data Model (The "Item")
All data in n8n flows as an **array of objects**. Each object must contain a `json` key (for data) and optionally a `binary` key (for files).
```json
[
  {
    "json": {
      "id": 123,
      "name": "Pochi"
    },
    "binary": {
      "data": { "data": "...", "mimeType": "image/png", "fileName": "photo.png" }
    }
  }
]
```
#### B. Expressions
Expressions use `{{ ... }}` syntax and are JavaScript-based. They are used to dynamically set node parameters.
*   **Accessing previous node data**: `{{ $node["HTTP Request"].json.id }}` or `{{ $json.id }}` (for current item).
*   **Date handling (Luxon)**: `{{ $now.plus({ days: 1 }).toISODate() }}`.
*   [Expressions Documentation](https://docs.n8n.io/code/expressions/)
#### C. Code Node (JavaScript & Python)
Used for complex transformations.
*   **JavaScript**:
    ```javascript
    const items = $input.all(); // Get all input items
    for (let item of items) {
      item.json.processed = true;
    }
    return items; // MUST return an array of objects with 'json' key
    ```
*   **Python**:
    ```python
    items = _input.all()
    for item in items:
        item["json"]["processed"] = True
    return items
    ```
*   **Constraint**: Python requires bracket notation `item["json"]["key"]` (no dot notation).
*   [Code Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
#### D. n8n REST API
Used to programmatically manage workflows and credentials.
*   **Auth**: `X-N8N-API-KEY` header.
*   **Endpoints**:
    *   `GET /api/v1/workflows`: List workflows.
    *   `POST /api/v1/workflows`: Create a workflow from JSON.
    *   `GET /api/v1/credentials`: List credentials.
*   [API Reference](https://docs.n8n.io/api/api-reference/)
---
### 3. Real-World Use Cases & Templates
*   **SaaS Integration**: Syncing Shopify orders to a Google Sheet and sending a Slack notification.
*   **AI Agents**: Using the "AI Agent" node to process webhooks and call external tools (e.g., searching a vector store).
*   **Error Handling**: A global "Error Trigger" workflow that logs failures to a database and alerts the dev team.
*   **Data Transformation**: Flattening complex nested JSON from an API (e.g., Stripe) into a flat structure for a CRM.
*   [Official Template Library](https://n8n.io/workflows/)
---
### 4. Developer Friction Points
1.  **Data Persistence ("Include Other Input Fields")**: In nodes like "Set" or "HTTP Request", users often forget to check "Include Other Input Fields", causing data from previous nodes to be dropped. [Discussion](https://community.n8n.io/t/passing-data-from-previous-nodes/2544).
2.  **Code Node Return Format**: Beginners often return a raw object `return { id: 1 };` instead of the required `return [{ json: { id: 1 } }];`. [Common Issue](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/common-issues/).
3.  **Webhook Response Modes**: Failing to set the Webhook node's "Response Mode" to "Last Node" or "When Last Node Finishes", leading to empty responses or timeouts.
4.  **Binary Data Handling**: Confusion when moving data between `json` and `binary` keys (requires the "Move Binary Data" node).
---
### 5. Evaluation Ideas
*   **Simple**: Create a workflow that triggers on a webhook, adds a timestamp to the incoming JSON using an expression, and returns the modified data.
*   **Intermediate**: Implement a "Merge" logic that takes data from two different API nodes (e.g., Users and Orders) and joins them by a common `user_id`.
*   **Intermediate**: Write a Python Code node that filters an array of items based on a complex date condition (e.g., "older than 30 days").
*   **Advanced**: Build a robust error-handling flow that uses an Error Trigger to catch failures in a multi-step HTTP process and retries the request once before failing.
*   **Advanced**: Programmatically create a new workflow and associated credentials using the n8n REST API.
*   **Complex**: Construct a multi-branch workflow that processes binary image data, uploads it to S3, and updates a database record with the URL.
---
### 6. Sources
1. [Official n8n Documentation](https://docs.n8n.io/) - Primary reference for all features.
2. [n8n llms.txt](https://docs.n8n.io/llms.txt) - Condensed documentation for LLM context.
3. [n8n Community Forum](https://community.n8n.io/) - Source for common developer friction points and "how-to" questions.
4. [n8n GitHub Repository](https://github.com/n8n-io/n8n) - Source for issue tracking and codebase structure.
5. [n8n REST API Reference](https://docs.n8n.io/api/api-reference/) - Technical details for programmatic management.