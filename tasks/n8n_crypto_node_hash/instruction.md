# Hash String with Crypto Node in n8n

## Background
You have an existing n8n workflow at `/home/user/workflow.json`. It contains a Manual Trigger node and an Edit Fields (Set) node that outputs a field called `inputString` with the value `n8n_is_awesome`. Your task is to add a Crypto node to the workflow to generate an MD5 hash of this string.

## Requirements
- Add a Crypto node to the workflow.
- Connect the Edit Fields node to the Crypto node.
- Configure the Crypto node to generate an MD5 hash of the `inputString` field.
- The hash must be encoded as `HEX`.
- Write the resulting hash to a new property named `md5_hash`.
- Save the updated workflow to `/home/user/workflow_final.json`.

## Implementation Guide
1. Read the existing workflow from `/home/user/workflow.json`.
2. Add a new node of type `n8n-nodes-base.crypto`.
3. Configure its parameters: `action: "hash"`, `type: "MD5"`, `value: "={{ $json.inputString }}"`, `dataPropertyName: "md5_hash"`, `encoding: "hex"`.
4. Update the `connections` object so that the output of the Edit Fields node connects to the input of the new Crypto node.
5. Save the updated JSON to `/home/user/workflow_final.json`.

## Constraints
- Project path: /home/user
- Do not modify the existing nodes' parameters or IDs.
- Ensure the final file is valid JSON.