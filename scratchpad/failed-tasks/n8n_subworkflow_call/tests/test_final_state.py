import os
import subprocess
import json
import pytest

def test_workflows_exported():
    # Export workflows
    result = subprocess.run(["n8n", "export:workflow", "--all", "--output=/tmp/workflows.json"], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to export workflows: {result.stderr}"
    assert os.path.exists("/tmp/workflows.json"), "Workflows export file not found."

def test_subworkflow_exists():
    with open("/tmp/workflows.json", "r") as f:
        data = json.load(f)
        
    workflows = data.get("workflows", [])
    if not workflows and isinstance(data, list):
        workflows = data
        
    subworkflow = next((w for w in workflows if w.get("name") == "Subworkflow - Process Data"), None)
    assert subworkflow is not None, "Subworkflow - Process Data not found."
    
    node_types = [n.get("type") for n in subworkflow.get("nodes", [])]
    assert "n8n-nodes-base.executeWorkflowTrigger" in node_types, "Subworkflow is missing executeWorkflowTrigger node."
    assert "n8n-nodes-base.set" in node_types, "Subworkflow is missing set node."

def test_parent_workflow_exists():
    with open("/tmp/workflows.json", "r") as f:
        data = json.load(f)
        
    workflows = data.get("workflows", [])
    if not workflows and isinstance(data, list):
        workflows = data
        
    parent_workflow = next((w for w in workflows if w.get("name") == "Parent Workflow"), None)
    assert parent_workflow is not None, "Parent Workflow not found."
    
    node_types = [n.get("type") for n in parent_workflow.get("nodes", [])]
    assert "n8n-nodes-base.manualTrigger" in node_types, "Parent Workflow is missing manualTrigger node."
    assert "n8n-nodes-base.executeWorkflow" in node_types, "Parent Workflow is missing executeWorkflow node."
    
    # Check if executeWorkflow node references the subworkflow ID
    subworkflow = next((w for w in workflows if w.get("name") == "Subworkflow - Process Data"), None)
    subworkflow_id = subworkflow.get("id")
    
    execute_node = next((n for n in parent_workflow.get("nodes", []) if n.get("type") == "n8n-nodes-base.executeWorkflow"), None)
    assert execute_node is not None
    
    workflow_id_param = execute_node.get("parameters", {}).get("workflowId")
    assert workflow_id_param == subworkflow_id, f"Execute Workflow node does not reference the correct Subworkflow ID. Expected {subworkflow_id}, got {workflow_id_param}"
