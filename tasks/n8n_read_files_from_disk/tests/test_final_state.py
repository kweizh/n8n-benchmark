import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user"
WORKFLOW_FILE = "/home/user/workflow.json"
DATA_DIR = "/home/user/data"

def test_workflow_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file not found at {WORKFLOW_FILE}"

def test_workflow_execution():
    """Priority 1: Use n8n CLI to verify the workflow logic."""
    # Execute the workflow
    env = os.environ.copy()
    env["N8N_USER_FOLDER"] = "/home/user/.n8n"
    
    execute_result = subprocess.run(
        ["n8n", "execute", f"--file={WORKFLOW_FILE}"],
        capture_output=True, text=True, cwd=PROJECT_DIR, env=env
    )
    assert execute_result.returncode == 0, f"'n8n execute' failed: {execute_result.stderr}\n{execute_result.stdout}"

    output = execute_result.stdout
    assert "report.csv" in output, f"Expected 'report.csv' in the output, got: {output}"
    assert "summary.txt" in output, f"Expected 'summary.txt' in the output, got: {output}"
    assert "logo.png" in output, f"Expected 'logo.png' in the output, got: {output}"
