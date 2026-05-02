import os
import shutil
import json

PROJECT_DIR = "/home/user"

def test_workflow_file_exists():
    workflow_path = os.path.join(PROJECT_DIR, "workflow.json")
    assert os.path.isfile(workflow_path), f"Workflow file {workflow_path} does not exist."

def test_initial_workflow_nodes():
    workflow_path = os.path.join(PROJECT_DIR, "workflow.json")
    with open(workflow_path) as f:
        workflow = json.load(f)
    
    nodes = workflow.get("nodes", [])
    assert len(nodes) == 2, "Expected exactly 2 nodes in the initial workflow."
    
    types = [node.get("type") for node in nodes]
    assert "n8n-nodes-base.manualTrigger" in types, "Manual Trigger node missing."
    assert "n8n-nodes-base.set" in types, "Edit Fields (Set) node missing."