import os
import json
import pytest

PROJECT_DIR = "/home/user"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow_final.json")

def test_workflow_final_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Final workflow file {WORKFLOW_FILE} does not exist."

def test_crypto_node_configured_correctly():
    with open(WORKFLOW_FILE) as f:
        try:
            workflow = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {WORKFLOW_FILE} is not valid JSON.")
            
    nodes = workflow.get("nodes", [])
    
    crypto_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.crypto"]
    assert len(crypto_nodes) == 1, f"Expected exactly 1 Crypto node, found {len(crypto_nodes)}"
    
    crypto_node = crypto_nodes[0]
    params = crypto_node.get("parameters", {})
    
    assert params.get("action", "hash") == "hash", f"Crypto node action should be 'hash', got '{params.get('action')}'"
    assert params.get("type", "MD5") == "MD5", f"Crypto node type should be 'MD5', got '{params.get('type')}'"
    assert params.get("value") == "={{ $json.inputString }}" or params.get("value") == "={{$json.inputString}}", \
        f"Crypto node value should be '={{{{ $json.inputString }}}}', got '{params.get('value')}'"
    assert params.get("dataPropertyName") == "md5_hash", f"Crypto node dataPropertyName should be 'md5_hash', got '{params.get('dataPropertyName')}'"
    assert params.get("encoding", "hex") == "hex", f"Crypto node encoding should be 'hex', got '{params.get('encoding')}'"

def test_connections_updated_correctly():
    with open(WORKFLOW_FILE) as f:
        workflow = json.load(f)
        
    connections = workflow.get("connections", {})
    nodes = workflow.get("nodes", [])
    
    crypto_node_name = None
    set_node_name = None
    
    for n in nodes:
        if n.get("type") == "n8n-nodes-base.crypto":
            crypto_node_name = n.get("name")
        elif n.get("type") == "n8n-nodes-base.set":
            set_node_name = n.get("name")
            
    assert crypto_node_name is not None, "Crypto node not found in nodes list."
    assert set_node_name is not None, "Set node not found in nodes list."
    
    set_connections = connections.get(set_node_name, {}).get("main", [])
    assert len(set_connections) > 0, f"No outgoing connections found for Set node '{set_node_name}'"
    
    connected_to_crypto = False
    for connection_group in set_connections:
        for connection in connection_group:
            if connection.get("node") == crypto_node_name:
                connected_to_crypto = True
                break
                
    assert connected_to_crypto, f"Set node '{set_node_name}' is not connected to Crypto node '{crypto_node_name}'"