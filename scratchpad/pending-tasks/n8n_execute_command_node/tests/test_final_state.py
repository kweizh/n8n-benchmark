import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/node"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."

def test_workflow_has_required_nodes():
    with open(WORKFLOW_FILE, "r") as f:
        try:
            workflow = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Workflow file is not valid JSON.")
    
    nodes = workflow.get("nodes", [])
    has_execute_command = False
    has_code_node = False
    for node in nodes:
        node_type = node.get("type", "")
        if "executeCommand" in node_type or "ExecuteCommand" in node_type or node_type == "n8n-nodes-base.executeCommand":
            has_execute_command = True
            command = node.get("parameters", {}).get("command", "")
            assert "script.sh" in command, f"Execute Command node does not run the required script. Command: {command}"
        if "code" in node_type or "Code" in node_type or node_type == "n8n-nodes-base.code":
            has_code_node = True
            
    assert has_execute_command, "Workflow is missing the Execute Command node."
    assert has_code_node, "Workflow is missing the Code node."

def test_workflow_execution():
    # Execute the workflow using n8n CLI
    result = subprocess.run(
        ["n8n", "execute", "--file", WORKFLOW_FILE],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    # The command should succeed
    assert result.returncode == 0, f"Workflow execution failed: {result.stderr}\n{result.stdout}"
    
    # The output should contain the parsed JSON data from the script
    assert '"id": 42' in result.stdout, f"Expected '\"id\": 42' in output, got: {result.stdout}"
    assert '"status": "completed"' in result.stdout, f"Expected '\"status\": \"completed\"' in output, got: {result.stdout}"
