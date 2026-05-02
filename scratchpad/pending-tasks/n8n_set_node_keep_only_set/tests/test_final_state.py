import os
import json
import pytest

WORKFLOW_FILE = "/home/user/workspace/workflow.json"

def get_workflow_json():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."
    with open(WORKFLOW_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Workflow file is not valid JSON: {e}")

def test_workflow_file_exists_and_valid():
    get_workflow_json()

def test_workflow_contains_trigger_node():
    workflow = get_workflow_json()
    nodes = workflow.get("nodes", [])
    trigger_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.manualTrigger"]
    assert len(trigger_nodes) > 0, "No Manual Trigger node found in the workflow."

def test_workflow_contains_code_node():
    workflow = get_workflow_json()
    nodes = workflow.get("nodes", [])
    code_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.code"]
    assert len(code_nodes) > 0, "No Code node found in the workflow."
    
    # Check if any code node contains the mock data
    mock_data_found = False
    for node in code_nodes:
        params_str = json.dumps(node.get("parameters", {}))
        if "user_id" in params_str and "name" in params_str and "email" in params_str and "password_hash" in params_str:
            mock_data_found = True
            break
            
    assert mock_data_found, "Code node does not appear to output the required mock data."

def test_workflow_contains_set_node_with_keep_only_set():
    workflow = get_workflow_json()
    nodes = workflow.get("nodes", [])
    set_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.set"]
    assert len(set_nodes) > 0, "No Set node found in the workflow."
    
    # Check if keepOnlySet is true
    keep_only_set_found = False
    for node in set_nodes:
        params = node.get("parameters", {})
        options = params.get("options", {})
        
        # keepOnlySet could be at parameters.keepOnlySet or parameters.options.keepOnlySet
        if params.get("keepOnlySet") is True or options.get("keepOnlySet") is True:
            keep_only_set_found = True
            break
            
    assert keep_only_set_found, "Set node does not have keepOnlySet enabled."

def test_set_node_keeps_required_fields():
    workflow = get_workflow_json()
    nodes = workflow.get("nodes", [])
    set_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.set"]
    
    required_fields = {"user_id", "name", "email"}
    fields_found = set()
    
    for node in set_nodes:
        params = node.get("parameters", {})
        # Depending on n8n version, values might be under 'values.string' or 'assignments.assignments'
        # We will just do a string dump of the node to check if the fields are mentioned
        node_str = json.dumps(node)
        for field in required_fields:
            if field in node_str:
                fields_found.add(field)
                
    missing_fields = required_fields - fields_found
    assert not missing_fields, f"Set node is missing configuration for fields: {missing_fields}"

def test_workflow_connections():
    workflow = get_workflow_json()
    connections = workflow.get("connections", {})
    
    # In n8n, connections are a dict where keys are node names.
    # We just need to verify that connections exist and link nodes.
    assert len(connections) > 0, "Workflow has no connections between nodes."
    
    nodes = workflow.get("nodes", [])
    trigger_name = next((n.get("name") for n in nodes if n.get("type") == "n8n-nodes-base.manualTrigger"), None)
    code_name = next((n.get("name") for n in nodes if n.get("type") == "n8n-nodes-base.code"), None)
    set_name = next((n.get("name") for n in nodes if n.get("type") == "n8n-nodes-base.set"), None)
    
    # Check that Trigger connects to Code, and Code connects to Set
    # connections format: { "Start": { "main": [ [ { "node": "Code", "type": "main", "index": 0 } ] ] } }
    
    # We'll just check if the names appear in the connections dict
    conn_str = json.dumps(connections)
    if trigger_name and code_name:
        assert code_name in conn_str, f"Code node '{code_name}' is not connected."
    if set_name:
        assert set_name in conn_str, f"Set node '{set_name}' is not connected."
