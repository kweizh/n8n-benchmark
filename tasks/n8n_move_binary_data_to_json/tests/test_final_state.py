import os
import json
import pytest
import subprocess

PROJECT_DIR = "/home/user/workspace"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_workflow_execution():
    """Priority 1: Use n8n CLI to execute the workflow."""
    # We need to set N8N_USER_FOLDER to a writable directory in case it tries to write to ~/.n8n
    env = os.environ.copy()
    env["N8N_USER_FOLDER"] = "/home/user/.n8n"
    
    # First import the workflow
    import_result = subprocess.run(
        ["n8n", "import:workflow", "--input", WORKFLOW_FILE],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=env
    )
    assert import_result.returncode == 0, f"'n8n import:workflow' failed: {import_result.stderr}\nStdout: {import_result.stdout}"
    
    # Then execute it
    result = subprocess.run(
        ["n8n", "execute", "--id=my-test-workflow-123"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=env
    )
    assert result.returncode == 0, f"'n8n execute' failed with error: {result.stderr}\nStdout: {result.stdout}"

def test_output_file_exists():
    """Priority 3: Check if the output file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"Expected output file at {OUTPUT_FILE} but it does not exist. The workflow should write the result to this file."

def test_output_file_contents():
    """Priority 3: Check if the output file contains the extracted text."""
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()
    
    # Try to parse it as JSON. Sometimes n8n writes array of items, sometimes just the object.
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Output file {OUTPUT_FILE} is not valid JSON. Content: {content[:100]}...")

    # Convert data to string to easily check if "Hello, n8n world!" is present in the JSON payload
    data_str = json.dumps(data)
    assert "Hello, n8n world!" in data_str, f"Expected 'Hello, n8n world!' in the output JSON, but got: {data_str[:200]}..."
    assert "extractedText" in data_str, f"Expected property 'extractedText' in the output JSON, but got: {data_str[:200]}..."
