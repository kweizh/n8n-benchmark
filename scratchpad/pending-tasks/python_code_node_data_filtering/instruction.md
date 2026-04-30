n8n supports Python in Code nodes, but it requires specific syntax to navigate the n8n internal data model, unlike standard Python dot notation.

You need to write a Python script for an n8n Code node that filters an array of items and removes any item where the field `is_archived` is `True` in the n8n Python execution environment.

**Constraints:**
- You MUST use `_input.all()` to fetch the incoming data.
- You MUST use bracket notation (e.g., `item["json"]["is_archived"]`) to access and evaluate data properties.
- Do NOT use standard object dot notation for the data access.