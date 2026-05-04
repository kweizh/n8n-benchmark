import os
import json

def test_workflow_json_exists_and_valid():
    workflow_path = "/home/user/myproject/workflow.json"
    assert os.path.isfile(workflow_path), f"Workflow file {workflow_path} does not exist"
    
    with open(workflow_path, 'r') as f:
        try:
            workflow = json.load(f)
        except json.JSONDecodeError:
            assert False, "workflow.json is not valid JSON"
            
    assert "nodes" in workflow, "workflow.json does not contain a 'nodes' array"
    assert isinstance(workflow["nodes"], list), "'nodes' is not an array"
    
    nodes = workflow["nodes"]
    
    # Check Read/Write Files from Disk
    read_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.readWriteFile"]
    assert len(read_nodes) > 0, "No Read/Write Files from Disk node found"
    read_node = read_nodes[0]
    params = read_node.get("parameters", {})
    # It might be in fileSelector
    assert "data.csv" in str(params), "Read/Write node does not seem to reference data.csv"
    
    # Check Extract From File
    extract_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.extractFromFile"]
    assert len(extract_nodes) > 0, "No Extract From File node found"
    
    # Check Split In Batches
    split_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.splitInBatches"]
    assert len(split_nodes) > 0, "No Split In Batches node found"
    split_node = split_nodes[0]
    split_params = split_node.get("parameters", {})
    assert str(split_params.get("batchSize", "")) == "10", "Split In Batches node does not have batchSize set to 10"

    # Connections could be checked, but this is enough for intermediate complexity
    assert "connections" in workflow, "workflow.json does not contain a 'connections' object"
