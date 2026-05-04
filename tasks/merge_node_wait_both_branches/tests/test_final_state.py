import os
import subprocess
import json

def test_workflow_exists():
    assert os.path.exists("/home/user/workspace/workflow.json"), "workflow.json does not exist"

def test_workflow_execution():
    # Import the workflow
    import_result = subprocess.run(
        ["n8n", "import:workflow", "--input=/home/user/workspace/workflow.json"],
        capture_output=True,
        text=True
    )
    assert import_result.returncode == 0, f"Failed to import workflow: {import_result.stderr}\n{import_result.stdout}"
    
    # Execute the workflow
    execute_result = subprocess.run(
        ["n8n", "execute", "--id=test-workflow", "--rawOutput"],
        capture_output=True,
        text=True
    )
    assert execute_result.returncode == 0, f"Failed to execute workflow: {execute_result.stderr}\n{execute_result.stdout}"
    
    # Parse the output
    try:
        output_data = json.loads(execute_result.stdout)
    except json.JSONDecodeError:
        assert False, f"Failed to parse n8n execute output as JSON: {execute_result.stdout}"
    
    # The output of n8n execute --rawOutput should be an array of items
    assert isinstance(output_data, list), f"Expected output to be a list, got {type(output_data)}"
    assert len(output_data) > 0, "Expected output to contain at least one item"
    
    # We want to verify that the output data is exactly {"branch": "A"}
    # The item structure in n8n is typically {"json": {"branch": "A"}, "pairedItem": ...}
    # But --rawOutput might just return the raw JSON or the full structure.
    # Let's check if the branch key is present in the output.
    
    found_branch_a = False
    for item in output_data:
        # Check if it's the raw data or wrapped in 'json'
        data_to_check = item.get("json", item)
        if data_to_check.get("branch") == "A":
            found_branch_a = True
            break
            
    assert found_branch_a, f"Expected output to contain 'branch': 'A'. Got: {output_data}"
