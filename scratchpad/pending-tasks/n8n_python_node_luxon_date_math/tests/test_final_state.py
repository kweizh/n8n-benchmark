import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")

def test_workflow_execution():
    """Priority 1: Use n8n CLI to verify the workflow execution and output."""
    result = subprocess.run(
        ["n8n", "execute", "--file=" + WORKFLOW_FILE],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    assert result.returncode == 0, f"n8n execute failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    
    # n8n execute might output some logs before the actual JSON result.
    # We try to extract the JSON part. The final output is usually an array of objects or a single object.
    stdout = result.stdout.strip()
    
    output_data = None
    
    # Try to parse the whole stdout first
    try:
        output_data = json.loads(stdout)
    except json.JSONDecodeError:
        # If it fails, try to find the first '[' or '{' and parse from there
        for i, char in enumerate(stdout):
            if char in ('[', '{'):
                try:
                    output_data = json.loads(stdout[i:])
                    break
                except json.JSONDecodeError:
                    continue
                    
    if output_data is None:
        pytest.fail(f"Could not parse JSON output from n8n execute. Output was:\n{stdout}")
    
    # output_data should be a list of items, or a single item
    if isinstance(output_data, dict):
        output_data = [output_data]
        
    assert len(output_data) > 0, "No output data returned from the workflow."
    
    # The output from a code node should be a list of items with 'json' key
    first_item = output_data[0]
    
    if "json" in first_item:
        item_data = first_item["json"]
    else:
        item_data = first_item
        
    assert "days_difference" in item_data, f"The output does not contain 'days_difference'. Got: {item_data}"
    
    days_diff = item_data["days_difference"]
    assert days_diff == 9, f"Expected days_difference to be 9, but got {days_diff}"
