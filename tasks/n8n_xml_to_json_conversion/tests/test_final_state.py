import os
import subprocess
import json
import pytest

WORKFLOW_FILE = "/home/user/workflow.json"

def test_workflow_file_exists():
    """Priority 3: Ensure the workflow file was created."""
    assert os.path.exists(WORKFLOW_FILE), f"Workflow file not found at {WORKFLOW_FILE}"

def test_workflow_execution():
    """Priority 1: Execute the workflow using n8n CLI and check the output."""
    result = subprocess.run(
        ["n8n", "execute", "--file", WORKFLOW_FILE],
        capture_output=True,
        text=True,
        cwd="/home/user"
    )
    
    assert result.returncode == 0, f"n8n execute failed with error:\n{result.stderr}\nOutput:\n{result.stdout}"
    
    # Check that the output contains the expected JSON structure
    # Since n8n execution output can be verbose, we check if the expected JSON string or keys are present
    output = result.stdout
    assert "Alice" in output, f"Expected 'Alice' in the workflow output, but got: {output}"
    assert "id" in output and "1" in output, f"Expected 'id': '1' in the workflow output, but got: {output}"
    assert "root" in output, f"Expected 'root' in the workflow output, but got: {output}"
    assert "user" in output, f"Expected 'user' in the workflow output, but got: {output}"