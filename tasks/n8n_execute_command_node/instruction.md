# n8n Execute Command Node

## Background
In n8n, the Execute Command node allows you to run shell commands on the host machine. Often, these commands output JSON strings that need to be parsed into proper n8n items for subsequent nodes to process.

## Requirements
- Create an n8n workflow that uses an Execute Command node to run a pre-existing shell script.
- The script is located at `/home/node/script.sh` and outputs a JSON string to standard output.
- After the Execute Command node, add a Code node that parses the `stdout` from the previous node and returns it as a valid n8n item (an array of objects with a `json` key).
- Save the workflow as a JSON file to `/home/node/workflow.json`.

## Implementation Guide
1. The Execute Command node should have its `command` parameter set to `/home/node/script.sh`.
2. The Code node should take the `stdout` from the Execute Command node's output, parse it using `JSON.parse()`, and return it in the format `[{ json: parsedData }]`.
3. The workflow JSON should contain the `nodes` and `connections` arrays defining this flow.

## Constraints
- Project path: `/home/node`
- The script `/home/node/script.sh` already exists and is executable.
- The workflow file must be saved to `/home/node/workflow.json`.

## Integrations
- None