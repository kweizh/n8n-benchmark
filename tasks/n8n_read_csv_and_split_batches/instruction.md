# Read CSV and Split into Batches

## Background
Create an n8n workflow that reads a local CSV file, parses the data, and splits it into batches of 10 items. This is a common pattern for processing large datasets without overloading memory or API rate limits.

## Requirements
- Create an n8n workflow JSON file at `/home/user/myproject/workflow.json`.
- The workflow must include a `Read/Write Files from Disk` node to read the file `/home/user/myproject/data.csv`.
- The workflow must include an `Extract From File` node to parse the CSV binary data into JSON items.
- The workflow must include a `Split In Batches` (or `Loop Over Items`) node to split the parsed items into batches of 10.
- The nodes must be properly connected in sequence.

## Implementation Guide
1. Create a valid n8n workflow JSON structure (an object with a `nodes` array and `connections` object).
2. Add a `Manual Trigger` node (type `n8n-nodes-base.manualTrigger`) to start the workflow.
3. Add a `Read/Write Files from Disk` node (type `n8n-nodes-base.readWriteFile`) with the operation set to read `/home/user/myproject/data.csv`.
4. Add an `Extract From File` node (type `n8n-nodes-base.extractFromFile`) configured to extract from CSV.
5. Add a `Split In Batches` node (type `n8n-nodes-base.splitInBatches`) with `batchSize` set to 10.
6. Ensure the `connections` object links the nodes in the correct order: Manual Trigger -> Read/Write Files from Disk -> Extract From File -> Split In Batches.

## Constraints
- Project path: `/home/user/myproject`
- The output must be a valid n8n workflow JSON file named `workflow.json`.
- Do not run the workflow, just create the JSON definition.

## Integrations
- None