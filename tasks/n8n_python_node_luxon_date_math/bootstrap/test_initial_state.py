import os
import shutil
import json
import pytest

PROJECT_DIR = "/home/user"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."

def test_workflow_contains_calculate_days_node():
    with open(WORKFLOW_FILE) as f:
        workflow = json.load(f)
    
    nodes = workflow.get("nodes", [])
    calculate_days_node = next((n for n in nodes if n.get("name") == "Calculate Days"), None)
    
    assert calculate_days_node is not None, "Workflow does not contain a 'Calculate Days' node."
    assert calculate_days_node.get("type") == "n8n-nodes-base.code", "The 'Calculate Days' node is not a code node."
    
    parameters = calculate_days_node.get("parameters", {})
    assert parameters.get("language") == "python", "The 'Calculate Days' node is not configured to use Python."
