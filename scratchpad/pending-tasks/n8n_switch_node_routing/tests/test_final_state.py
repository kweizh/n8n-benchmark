import os
import json
import pytest

WORKFLOW_FILE = "/home/user/workflow.json"

def get_workflows():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."
    with open(WORKFLOW_FILE, "r") as f:
        try:
            data = json.load(f)
            if isinstance(data, dict):
                return [data]
            elif isinstance(data, list):
                return data
            else:
                pytest.fail("Workflow JSON must be an object or an array of objects.")
        except json.JSONDecodeError:
            pytest.fail("Workflow file is not valid JSON.")

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."

def test_webhook_node_exists():
    workflows = get_workflows()
    found = False
    for wf in workflows:
        for node in wf.get("nodes", []):
            if node.get("type") == "n8n-nodes-base.webhook":
                params = node.get("parameters", {})
                path = params.get("path", "")
                if "route-items" in path:
                    found = True
                    break
    assert found, "Expected a Webhook node with path 'route-items'."

def test_switch_node_exists():
    workflows = get_workflows()
    found = False
    for wf in workflows:
        for node in wf.get("nodes", []):
            if node.get("type") == "n8n-nodes-base.switch":
                params = node.get("parameters", {})
                # Check if the switch node has rules for active, pending, inactive
                rules_str = json.dumps(params.get("rules", {}))
                if "active" in rules_str and "pending" in rules_str and "inactive" in rules_str:
                    found = True
                    break
    assert found, "Expected a Switch node with rules for 'active', 'pending', and 'inactive'."

def test_set_nodes_exist():
    workflows = get_workflows()
    categories = set()
    for wf in workflows:
        for node in wf.get("nodes", []):
            if node.get("type") in ["n8n-nodes-base.set", "n8n-nodes-base.editFields"]:
                params = node.get("parameters", {})
                params_str = json.dumps(params)
                if '"category"' in params_str or "'category'" in params_str:
                    if '"A"' in params_str or "'A'" in params_str: categories.add("A")
                    if '"B"' in params_str or "'B'" in params_str: categories.add("B")
                    if '"C"' in params_str or "'C'" in params_str: categories.add("C")
                    if '"Unknown"' in params_str or "'Unknown'" in params_str: categories.add("Unknown")
    
    assert "A" in categories, "Expected a Set node that sets category to 'A'."
    assert "B" in categories, "Expected a Set node that sets category to 'B'."
    assert "C" in categories, "Expected a Set node that sets category to 'C'."
    assert "Unknown" in categories, "Expected a Set node that sets category to 'Unknown'."

def test_respond_to_webhook_node_exists():
    workflows = get_workflows()
    found = False
    for wf in workflows:
        for node in wf.get("nodes", []):
            if node.get("type") == "n8n-nodes-base.respondToWebhook":
                found = True
                break
    assert found, "Expected a 'Respond to Webhook' node."
