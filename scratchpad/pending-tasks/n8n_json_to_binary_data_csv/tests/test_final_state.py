import os
import json
import pytest

WORKFLOW_FILE = "/home/node/workflow.json"

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file not found at {WORKFLOW_FILE}"

def test_workflow_is_valid_json():
    with open(WORKFLOW_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Workflow file is not valid JSON: {e}")
    assert isinstance(data, dict), "Workflow JSON should be an object"

def test_workflow_contains_required_nodes():
    with open(WORKFLOW_FILE, "r") as f:
        data = json.load(f)
    
    nodes = data.get("nodes", [])
    assert len(nodes) == 3, f"Expected exactly 3 nodes, found {len(nodes)}"
    
    node_types = [node.get("type", "").lower() for node in nodes]
    
    assert "n8n-nodes-base.manualtrigger" in node_types, "Missing Manual Trigger node"
    assert "n8n-nodes-base.code" in node_types, "Missing Code node"
    assert "n8n-nodes-base.converttofile" in node_types, "Missing Convert to File node"

def test_convert_node_configuration():
    with open(WORKFLOW_FILE, "r") as f:
        data = json.load(f)
        
    nodes = data.get("nodes", [])
    convert_node = next((n for n in nodes if n.get("type", "").lower() == "n8n-nodes-base.converttofile"), None)
    assert convert_node is not None, "Convert to File node not found"
    
    params = convert_node.get("parameters", {})
    # Check if operation is configured for CSV (usually 'toCsv' or 'toFile' depending on n8n version, but let's check fileName)
    options = params.get("options", {})
    file_name = options.get("fileName", "")
    assert file_name == "users.csv", f"Expected Convert node to output 'users.csv', got '{file_name}'"

def test_nodes_are_connected():
    with open(WORKFLOW_FILE, "r") as f:
        data = json.load(f)
        
    nodes = data.get("nodes", [])
    trigger_node = next((n for n in nodes if n.get("type", "").lower() == "n8n-nodes-base.manualtrigger"), None)
    code_node = next((n for n in nodes if n.get("type", "").lower() == "n8n-nodes-base.code"), None)
    convert_node = next((n for n in nodes if n.get("type", "").lower() == "n8n-nodes-base.converttofile"), None)
    
    trigger_name = trigger_node.get("name")
    code_name = code_node.get("name")
    convert_name = convert_node.get("name")
    
    connections = data.get("connections", {})
    
    # Check trigger -> code connection
    trigger_connections = connections.get(trigger_name, {}).get("main", [])
    assert len(trigger_connections) > 0, "Manual Trigger is not connected to anything"
    
    # The connection array is a list of arrays: main[0] contains the targets
    trigger_targets = [target.get("node") for target in trigger_connections[0]]
    assert code_name in trigger_targets, "Manual Trigger is not connected to Code node"
    
    # Check code -> convert connection
    code_connections = connections.get(code_name, {}).get("main", [])
    assert len(code_connections) > 0, "Code node is not connected to anything"
    code_targets = [target.get("node") for target in code_connections[0]]
    assert convert_name in code_targets, "Code node is not connected to Convert to File node"
