import os
import subprocess
import shutil

WORKFLOW_FILE = "/home/node/workflow.json"
OUTPUT_IMAGE = "/home/node/output.png"

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."

def test_workflow_execution_and_output():
    assert os.path.isfile(WORKFLOW_FILE), "Workflow file must exist to execute."
    shutil.copy(WORKFLOW_FILE, "/tmp/workflow.json")
    
    if os.path.exists(OUTPUT_IMAGE):
        os.remove(OUTPUT_IMAGE)
        
    result = subprocess.run(
        ["n8n", "execute", "--file", "/tmp/workflow.json"],
        capture_output=True, text=True, cwd="/home/node"
    )
    
    assert result.returncode == 0, f"Workflow execution failed: {result.stderr}\n{result.stdout}"
    assert os.path.isfile(OUTPUT_IMAGE), f"Output image {OUTPUT_IMAGE} was not created by the workflow."

    # Check dimensions
    result = subprocess.run(
        ["gm", "identify", "-format", "%w %h", OUTPUT_IMAGE],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to identify output image: {result.stderr}"
    
    dimensions = result.stdout.strip().split()
    assert len(dimensions) == 2, f"Unexpected output from gm identify: {result.stdout}"
    
    width, height = int(dimensions[0]), int(dimensions[1])
    assert width <= 100 and height <= 100, f"Image dimensions {width}x{height} exceed maximum 100x100."
    assert width > 0 and height > 0, "Image dimensions are invalid (<= 0)."
